"""The single OpenRouter call site for the whole project.

Everything that touches the network goes through :class:`OpenRouterClient`. Nothing else
in the repo may make API calls. The client enforces, in this order:

1. **Budget guard.** The projected worst-case cost of a call is computed *before* the
   request is issued. If it would push the phase over its sub-budget, or the project over
   its ceiling, :class:`BudgetExceeded` is raised and no request is sent.
2. **Provider pinning.** Every call sends ``provider={"order": [pinned], "allow_fallbacks":
   False}``. If the response comes back from a different provider, that is a validity
   failure, not a warning: :class:`ProviderMismatch` is raised. If the pinned provider is
   unavailable, :class:`ProviderUnavailable` aborts the run so it can be resumed later —
   the client never silently switches provider or model.
3. **Reasoning off** and ``temperature=0`` by default for predictor-style calls.
4. **Append-only per-call logging** to ``data/raw/<phase>.jsonl``. This log is the
   reproducibility record and is also what makes spend resumable across processes.

Secrets: the API key is read via python-dotenv and never stored on the instance in a
form that gets printed. :func:`redact` scrubs it from every exception message and any
text this module emits. Do not add a ``print`` of a request header.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import httpx
from dotenv import load_dotenv

from . import config


# --------------------------------------------------------------------------------------
# Secret handling
# --------------------------------------------------------------------------------------

_KEY_CACHE: str | None = None


def load_api_key() -> str:
    """Load the OpenRouter key from .env. Never log or return this to a caller that prints."""
    global _KEY_CACHE
    if _KEY_CACHE:
        return _KEY_CACHE
    load_dotenv(config.REPO_ROOT / ".env")
    key = os.environ.get(config.OPENROUTER_KEY_ENV_VAR)
    if not key:
        raise RuntimeError(
            f"{config.OPENROUTER_KEY_ENV_VAR} is not set. Put it in .env at the repo root. "
            "Do not pass it on the command line."
        )
    _KEY_CACHE = key.strip()
    return _KEY_CACHE


def redact(text: str) -> str:
    """Remove the API key (and anything key-shaped) from a string before it is shown."""
    out = str(text)
    if _KEY_CACHE:
        out = out.replace(_KEY_CACHE, "<OPENROUTER_KEY:REDACTED>")
    # Belt and braces: scrub anything that looks like an OpenRouter/OpenAI-style key even
    # if it never passed through load_api_key().
    import re

    out = re.sub(r"sk-[A-Za-z0-9_\-]{8,}", "<KEY:REDACTED>", out)
    out = re.sub(r"(?i)(authorization\"?\s*[:=]\s*\"?)(bearer\s+)?\S+", r"\1<REDACTED>", out)
    return out


class RedactedError(RuntimeError):
    """Base error whose message is always scrubbed of secrets."""

    def __init__(self, message: str) -> None:
        super().__init__(redact(message))


class BudgetExceeded(RedactedError):
    """Raised BEFORE a call when its projected cost would breach a budget."""


class ProviderUnavailable(RedactedError):
    """The pinned provider could not serve the request. Abort and resume; never switch."""


class ProviderMismatch(RedactedError):
    """The response came from a provider other than the pinned one — a validity failure."""


class MissingPrice(RedactedError):
    """No verified price for a model, so the guard cannot project. Refuse rather than guess."""


# --------------------------------------------------------------------------------------
# Prices
# --------------------------------------------------------------------------------------


@dataclass
class PriceBook:
    """Verified per-token prices, in USD per million tokens, keyed by model id.

    Populated from OpenRouter's own model/endpoint listing during Phase B. The guard
    refuses to project a call for a model that is not in here — guessing a price would
    defeat the guard, which is the one thing standing between the sprint and the $10.
    """

    prompt: dict[str, float] = field(default_factory=dict)
    completion: dict[str, float] = field(default_factory=dict)

    def add(self, model_id: str, prompt_usd_per_mtok: float, completion_usd_per_mtok: float) -> None:
        self.prompt[model_id] = float(prompt_usd_per_mtok)
        self.completion[model_id] = float(completion_usd_per_mtok)

    def project(self, model_id: str, *, est_prompt_tokens: int, max_completion_tokens: int) -> float:
        if model_id not in self.prompt:
            raise MissingPrice(
                f"No verified price for {model_id!r}. Load prices from the OpenRouter "
                "model list before calling; the budget guard does not guess."
            )
        return (
            est_prompt_tokens * self.prompt[model_id]
            + max_completion_tokens * self.completion[model_id]
        ) / 1_000_000.0

    def actual(self, model_id: str, prompt_tokens: int, completion_tokens: int) -> float | None:
        if model_id not in self.prompt:
            return None
        return (
            prompt_tokens * self.prompt[model_id]
            + completion_tokens * self.completion[model_id]
        ) / 1_000_000.0


def estimate_tokens(text: str) -> int:
    """Deliberately conservative token estimate for the pre-call projection (~3 chars/token)."""
    return max(1, int(len(text) / 3) + 8)


# --------------------------------------------------------------------------------------
# Budget guard
# --------------------------------------------------------------------------------------


class BudgetGuard:
    """Projects cost before each call and refuses to break the budget.

    Spend is reconstructed by reading the append-only logs on construction, so a crashed
    and resumed run does not forget what it already spent.
    """

    def __init__(self, phase: str, *, phase_budget_usd: float | None = None) -> None:
        if phase not in config.PHASE_BUDGETS_USD and phase_budget_usd is None:
            raise BudgetExceeded(
                f"Unknown phase {phase!r} and no explicit sub-budget. Add it to "
                "config.PHASE_BUDGETS_USD rather than passing an ad-hoc number."
            )
        self.phase = phase
        self.phase_budget = (
            phase_budget_usd if phase_budget_usd is not None else config.PHASE_BUDGETS_USD[phase]
        )
        self.phase_spent = _spend_in_log(config.RAW_DIR / f"{phase}.jsonl")
        self.project_spent = _total_spend_all_phases()

    # -- queries ------------------------------------------------------------------
    @property
    def phase_remaining(self) -> float:
        return self.phase_budget - self.phase_spent

    @property
    def project_remaining(self) -> float:
        return config.PROJECT_CEILING_USD - self.project_spent

    # -- enforcement --------------------------------------------------------------
    def check(self, projected_usd: float) -> None:
        """Raise if this call must not be made. Called before every request."""
        if self.phase_spent + projected_usd > self.phase_budget + 1e-12:
            raise BudgetExceeded(
                f"Phase {self.phase!r} sub-budget would be exceeded: spent "
                f"${self.phase_spent:.4f} + projected ${projected_usd:.4f} > "
                f"${self.phase_budget:.2f}. No call was made."
            )
        if self.project_spent + projected_usd > config.PROJECT_CEILING_USD + 1e-12:
            raise BudgetExceeded(
                f"PROJECT CEILING would be exceeded: spent ${self.project_spent:.4f} + "
                f"projected ${projected_usd:.4f} > ${config.PROJECT_CEILING_USD:.2f}. "
                "No call was made."
            )

    def commit(self, actual_usd: float) -> None:
        self.phase_spent += actual_usd
        self.project_spent += actual_usd


def _spend_in_log(path: Path) -> float:
    if not path.exists():
        return 0.0
    total = 0.0
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                total += float(json.loads(line).get("cost_usd") or 0.0)
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
    return total


def _total_spend_all_phases() -> float:
    return sum(_spend_in_log(p) for p in config.RAW_DIR.glob("*.jsonl"))


# --------------------------------------------------------------------------------------
# Result
# --------------------------------------------------------------------------------------


@dataclass
class CallResult:
    text: str
    model_requested: str
    model_returned: str | None
    provider_pinned: str | None
    provider_returned: str | None
    prompt_tokens: int
    completion_tokens: int
    reasoning_tokens: int
    cost_usd: float
    cost_source: str          # "openrouter" | "pricebook" | "unknown"
    latency_s: float
    prompt_sha256: str
    finish_reason: str | None
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    @property
    def provider_ok(self) -> bool:
        if self.provider_pinned is None:
            return True
        if self.provider_returned is None:
            return False
        return _provider_key(self.provider_returned) == _provider_key(self.provider_pinned)


def _provider_key(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------------------


class OpenRouterClient:
    """OpenRouter wrapper with pinning, reasoning-off, budget guard and per-call logging."""

    def __init__(
        self,
        phase: str,
        *,
        price_book: PriceBook | None = None,
        phase_budget_usd: float | None = None,
        log_path: Path | None = None,
        timeout_s: float = config.REQUEST_TIMEOUT_S,
    ) -> None:
        self.phase = phase
        self.guard = BudgetGuard(phase, phase_budget_usd=phase_budget_usd)
        self.prices = price_book or PriceBook()
        self.log_path = log_path or (config.RAW_DIR / f"{phase}.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        # The guard and the append-only log are shared mutable state. Concurrent calls
        # (e.g. the Phase B burst test) must not be able to race past the budget check or
        # interleave half-written log lines.
        self._lock = threading.Lock()
        self._client = httpx.Client(
            base_url=config.OPENROUTER_BASE_URL,
            timeout=timeout_s,
            headers={
                "Authorization": f"Bearer {load_api_key()}",
                "Content-Type": "application/json",
                **config.OPENROUTER_HEADERS,
            },
        )

    # -- lifecycle ----------------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "OpenRouterClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- unmetered GETs -----------------------------------------------------------
    def get_models(self) -> dict[str, Any]:
        """GET /models. Listing is free; no budget check needed, and none is skipped for calls."""
        return self._get("/models")

    def get_endpoints(self, model_id: str) -> dict[str, Any]:
        """GET /models/{author}/{slug}/endpoints — providers, quantization, per-provider price."""
        return self._get(f"/models/{model_id}/endpoints")

    def _get(self, path: str) -> dict[str, Any]:
        try:
            resp = self._client.get(path)
        except httpx.HTTPError as exc:
            raise RedactedError(f"GET {path} failed: {exc}") from None
        if resp.status_code != 200:
            raise RedactedError(f"GET {path} -> HTTP {resp.status_code}: {resp.text[:400]}")
        return resp.json()

    # -- the metered call ---------------------------------------------------------
    def chat(
        self,
        *,
        model_id: str,
        messages: Sequence[dict[str, str]],
        provider: str | None = None,
        temperature: float = config.PREDICTOR_TEMPERATURE,
        max_tokens: int = config.MAX_PREDICTION_TOKENS,
        reasoning_off: bool = True,
        tag: str = "",
        extra_body: dict[str, Any] | None = None,
        allow_unpriced: bool = False,
    ) -> CallResult:
        """One chat completion, pinned and budgeted.

        ``provider`` is the pinned backend provider name. ``None`` means unpinned, which is
        acceptable only for exploratory verification calls — never for experimental data,
        where pinning is a validity condition.

        Retries inside this method never change ``model_id`` or ``provider``.
        """
        prompt_text = _flatten(messages)
        prompt_hash = sha256_of(prompt_text)
        est_in = estimate_tokens(prompt_text)

        # --- 1. budget guard, BEFORE the request ---------------------------------
        try:
            projected = self.prices.project(
                model_id, est_prompt_tokens=est_in, max_completion_tokens=max_tokens
            )
        except MissingPrice:
            if not allow_unpriced:
                raise
            projected = 0.0
        with self._lock:
            # Reserve the projected cost up front so N concurrent calls cannot each pass a
            # check against the same stale balance and collectively overshoot.
            self.guard.check(projected)
            self.guard.commit(projected)
        reserved = projected

        # --- 2. build the request ------------------------------------------------
        body: dict[str, Any] = {
            "model": model_id,
            "messages": list(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            # Ask OpenRouter to return its own authoritative cost in the usage block.
            "usage": {"include": True},
        }
        if provider is not None:
            body["provider"] = {"order": [provider], "allow_fallbacks": False}
        if reasoning_off:
            # OpenRouter's unified reasoning control. `enabled: False` is the portable
            # form; `effort: "none"`/`max_tokens: 0` are model-specific spellings that
            # Phase B records acceptance of per model.
            body["reasoning"] = {"enabled": False, "exclude": True}
        if extra_body:
            body.update(extra_body)

        # --- 3. issue, with transport-level retry that never re-routes ------------
        started = time.time()
        payload, status = self._post_with_retry("/chat/completions", body)
        latency = time.time() - started

        # --- 4. provider availability / mismatch ---------------------------------
        if status in (404, 502, 503) or (isinstance(payload, dict) and _looks_unavailable(payload)):
            self._release(reserved)
            raise ProviderUnavailable(
                f"Pinned provider {provider!r} could not serve {model_id!r} "
                f"(HTTP {status}). Aborting so the run can be resumed from its checkpoint. "
                "The client never switches provider — switching would break the "
                "same-weights precondition."
            )
        if status != 200:
            self._release(reserved)
            raise RedactedError(
                f"chat/completions -> HTTP {status} for {model_id!r}: {json.dumps(payload)[:400]}"
            )

        result = self._to_result(
            payload, model_id=model_id, provider=provider,
            prompt_hash=prompt_hash, latency=latency, max_tokens=max_tokens,
        )

        # --- 5. account and log, even on mismatch --------------------------------
        # Swap the up-front reservation for the actual billed cost.
        with self._lock:
            self.guard.commit(result.cost_usd - reserved)
            self._log(result, tag=tag, temperature=temperature, max_tokens=max_tokens,
                      reasoning_off=reasoning_off, provider_ok=result.provider_ok)

        if provider is not None and not result.provider_ok:
            raise ProviderMismatch(
                f"Pinned {provider!r} but response came from {result.provider_returned!r} "
                f"for {model_id!r}. Recorded as a pinning FAIL; the pair is not usable for "
                "experimental data until this resolves."
            )
        return result

    # -- one-letter helper --------------------------------------------------------
    def one_letter(
        self,
        *,
        model_id: str,
        messages: Sequence[dict[str, str]],
        allowed: Iterable[str] = ("A", "B"),
        provider: str | None = None,
        tag: str = "",
        **kw: Any,
    ) -> tuple[str | None, list[CallResult]]:
        """Constrained single-label call with the pre-declared one-retry-then-log policy.

        Returns ``(label_or_None, calls)``. A ``None`` label means the output was still
        malformed after the retry; the caller logs it and moves on. Whether a
        still-malformed item is excluded is a research rule that lives in `02`.
        """
        allowed_set = {a.upper() for a in allowed}
        calls: list[CallResult] = []
        for attempt in range(config.MALFORMED_RETRIES + 1):
            res = self.chat(
                model_id=model_id, messages=messages, provider=provider,
                tag=f"{tag}|attempt{attempt}", **kw,
            )
            calls.append(res)
            label = _parse_label(res.text, allowed_set)
            if label is not None:
                return label, calls
        return None, calls

    # -- internals ----------------------------------------------------------------
    def _release(self, amount: float) -> None:
        """Give back an up-front reservation when the call never produced billable usage."""
        if amount:
            with self._lock:
                self.guard.commit(-amount)

    def _post_with_retry(
        self, path: str, body: dict[str, Any], *, attempts: int = 7
    ) -> tuple[dict[str, Any], int]:
        """Transport retry only. The body — model id and provider pin — is never mutated.

        Backoff is exponential with jitter, because the realistic failure is a *shared*
        upstream overload: every worker in the pool gets 429 at the same instant, and a
        short flat retry just re-synchronises them into the same wall. Jitter spreads them
        out; the long tail (up to ~60 s) rides out a provider hiccup rather than aborting a
        run that is expensive to redo. Retrying never re-routes — switching provider or
        model to escape a 429 would break the same-weights precondition.
        """
        last: tuple[dict[str, Any], int] = ({}, 0)
        for i in range(attempts):
            try:
                resp = self._client.post(path, json=body)
            except httpx.HTTPError as exc:
                last = ({"error": redact(str(exc))}, 0)
                time.sleep(_backoff(i))
                continue
            try:
                payload = resp.json()
            except ValueError:
                payload = {"error": {"message": redact(resp.text[:400])}}
            if resp.status_code == 429 or 500 <= resp.status_code < 600:
                last = (payload, resp.status_code)
                time.sleep(_backoff(i))
                continue
            return payload, resp.status_code
        return last

    def _to_result(
        self,
        payload: dict[str, Any],
        *,
        model_id: str,
        provider: str | None,
        prompt_hash: str,
        latency: float,
        max_tokens: int,
    ) -> CallResult:
        choices = payload.get("choices") or [{}]
        message = (choices[0] or {}).get("message") or {}
        text = (message.get("content") or "").strip()
        usage = payload.get("usage") or {}
        p_tok = int(usage.get("prompt_tokens") or 0)
        c_tok = int(usage.get("completion_tokens") or 0)
        details = usage.get("completion_tokens_details") or {}
        r_tok = int(details.get("reasoning_tokens") or 0)

        cost = usage.get("cost")
        if cost is not None:
            cost_usd, source = float(cost), "openrouter"
        else:
            computed = self.prices.actual(model_id, p_tok, c_tok)
            cost_usd, source = (computed, "pricebook") if computed is not None else (0.0, "unknown")

        return CallResult(
            text=text,
            model_requested=model_id,
            model_returned=payload.get("model"),
            provider_pinned=provider,
            provider_returned=payload.get("provider"),
            prompt_tokens=p_tok,
            completion_tokens=c_tok,
            reasoning_tokens=r_tok,
            cost_usd=cost_usd,
            cost_source=source,
            latency_s=latency,
            prompt_sha256=prompt_hash,
            finish_reason=(choices[0] or {}).get("finish_reason"),
            raw=payload,
        )

    def _log(self, r: CallResult, **extra: Any) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "phase": self.phase,
            "tag": extra.pop("tag", ""),
            "model_requested": r.model_requested,
            "model_returned": r.model_returned,
            "provider_pinned": r.provider_pinned,
            "provider_returned": r.provider_returned,
            "provider_ok": extra.pop("provider_ok", None),
            "prompt_sha256": r.prompt_sha256,
            "prompt_tokens": r.prompt_tokens,
            "completion_tokens": r.completion_tokens,
            "reasoning_tokens": r.reasoning_tokens,
            "cost_usd": r.cost_usd,
            "cost_source": r.cost_source,
            "latency_s": round(r.latency_s, 3),
            "finish_reason": r.finish_reason,
            "output": r.text[:200],
            "params": extra,
        }
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------


def _backoff(attempt: int, *, base: float = 3.0, cap: float = 60.0) -> float:
    """Exponential backoff with full jitter, capped."""
    import random

    return random.uniform(0.0, min(cap, base * (2 ** attempt)))


def _flatten(messages: Sequence[dict[str, str]]) -> str:
    return "\n".join(f"{m.get('role','')}: {m.get('content','')}" for m in messages)


def _parse_label(text: str, allowed: set[str]) -> str | None:
    """Strict-ish single-label parse: the reply must be one allowed letter, alone."""
    stripped = text.strip().strip(".;:!\"'` \n\t*")
    if stripped.upper() in allowed:
        return stripped.upper()
    return None


def _looks_unavailable(payload: dict[str, Any]) -> bool:
    err = payload.get("error")
    if not isinstance(err, dict):
        return False
    msg = str(err.get("message", "")).lower()
    return any(s in msg for s in ("no allowed providers", "no endpoints", "not available", "no providers"))


def price_book_from_models_payload(payload: dict[str, Any]) -> PriceBook:
    """Build a :class:`PriceBook` from the /models response (prices are per-token strings)."""
    book = PriceBook()
    for m in payload.get("data", []):
        pricing = m.get("pricing") or {}
        try:
            p_in = float(pricing.get("prompt", "nan")) * 1_000_000
            p_out = float(pricing.get("completion", "nan")) * 1_000_000
        except (TypeError, ValueError):
            continue
        if p_in != p_in or p_out != p_out:  # NaN check
            continue
        book.add(m["id"], p_in, p_out)
    return book
