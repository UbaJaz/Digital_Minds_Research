"""Phase B, steps 4-10: the metered verification calls.

Budget: $0.50, enforced by the client's guard (which also refuses to break the $10 project
ceiling). Every call is pinned to one provider with fallbacks disabled and logged to
`data/raw/verification.jsonl`.

Checks, per the council's verification list:
  4. one "reply OK" call, pinned            -> returned model id + provider; pinning PASS/FAIL
  5. reasoning-off accepted, zero reasoning tokens billed
  6. 10 one-letter calls                    -> malformed rate (pass < 5%)
  7. 20 temperature-0 repeats (shortlist)   -> agreement rate, reported as data
  8. 10 shared prompts on both pair members -> identical on all 10 => possible re-alias
  9. 30 concurrent one-letter calls         -> wall clock, 429s
 10. total Phase B cost from the usage fields

Nothing here selects a model. It ranks and reports; the team decides.
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from selfpred import config
from selfpred.client import (
    BudgetExceeded,
    OpenRouterClient,
    PriceBook,
    ProviderMismatch,
    ProviderUnavailable,
    RedactedError,
    price_book_from_models_payload,
)

MODELS_JSON = config.RAW_DIR / "openrouter_models.json"
RESULTS_JSON = config.RAW_DIR / "verification_summary.json"


# --------------------------------------------------------------------------------------
# What we call. Provider pins come from scripts/phase_b_endpoints.py output.
# --------------------------------------------------------------------------------------

@dataclass
class Candidate:
    model_id: str
    provider: str
    tier: str
    role_hint: str
    quantization: str
    pair: str = ""


CANDIDATES: list[Candidate] = [
    # tier (i) — official Instruct + same-base community fine-tune, same parameter size
    Candidate("meta-llama/llama-3.1-70b-instruct",      "DeepInfra", "i",  "M?", "fp8", "i-A"),
    Candidate("nousresearch/hermes-3-llama-3.1-70b",    "DeepInfra", "i",  "N?", "fp8", "i-A"),
    Candidate("meta-llama/llama-3.3-70b-instruct",      "Nebius",    "i",  "M?", "fp8", "i-B"),
    Candidate("nousresearch/hermes-4-70b",              "Nebius",    "i",  "N?", "fp8", "i-B"),
    # tier (ii) — dated snapshots of one closed model
    Candidate("openai/gpt-4o-2024-08-06",               "OpenAI",    "ii", "M?", "unknown", "ii-A"),
    Candidate("openai/gpt-4o-2024-11-20",               "OpenAI",    "ii", "N?", "unknown", "ii-A"),
    # tier (iii) — same-family adjacent tier
    Candidate("openai/gpt-5.6-terra",                   "OpenAI",    "iii", "M?", "unknown", "iii-A"),
    Candidate("openai/gpt-5.6-luna",                    "OpenAI",    "iii", "N?", "unknown", "iii-A"),
    # Far-Self candidates — different lineage, different provider than the tier-(i) pairs
    Candidate("deepseek/deepseek-chat-v3-0324",         "SiliconFlow", "far", "F?", "fp8", ""),
    Candidate("mistralai/mistral-small-3.2-24b-instruct", "DeepInfra", "far", "F?", "fp8", ""),
    Candidate("google/gemini-3.5-flash-lite",           "Google",    "far", "F?", "unknown", ""),
]

#: Steps 7-8 are limited to the pair members most likely to be chosen (<= 4 models).
SHORTLIST_PAIRS = ["i-A", "i-B"]
LEADING_PAIR = "i-A"  # step 9 burst

# --- fixed stimuli (trivial, unrelated to persona; frozen here) ------------------------

OK_PROMPT = [{"role": "user", "content": "Reply with the single word OK."}]

ONE_LETTER_ITEMS = [
    ("a cat", "a bulldozer"), ("a whisper", "a jet engine"), ("a feather", "an anvil"),
    ("a candle", "the sun"), ("a puddle", "the ocean"), ("an ant", "an elephant"),
    ("a pebble", "a mountain"), ("a raindrop", "a thunderstorm"),
    ("a teaspoon", "a swimming pool"), ("a matchstick", "a bonfire"),
]

def one_letter_msgs(a: str, b: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": "Answer with a single letter and nothing else."},
        {"role": "user", "content": (
            f"Which is larger?\nA: {a}\nB: {b}\n"
            "Reply with exactly one letter: A or B. Do not explain."
        )},
    ]

DETERMINISM_PROMPT = [
    {"role": "system", "content": "Answer with a single letter and nothing else."},
    {"role": "user", "content": (
        "Which word is more formal?\nA: purchase\nB: buy\n"
        "Reply with exactly one letter: A or B. Do not explain."
    )},
]

REALIAS_PROMPTS = [
    "Name one colour. One word only.",
    "Name one fruit. One word only.",
    "Name one country. One word only.",
    "Name one animal. One word only.",
    "Name one metal. One word only.",
    "Name one musical instrument. One word only.",
    "Name one vegetable. One word only.",
    "Name one planet. One word only.",
    "Name one tree. One word only.",
    "Name one city. One word only.",
]


# --------------------------------------------------------------------------------------
# Result record
# --------------------------------------------------------------------------------------

@dataclass
class ModelReport:
    model_id: str
    provider_pinned: str
    tier: str
    pair: str
    quantization: str
    exists: bool = False
    returned_model: str | None = None
    returned_provider: str | None = None
    pinning_pass: bool | None = None
    reasoning_off_accepted: bool | None = None
    reasoning_tokens_billed: int | None = None
    malformed_rate: float | None = None
    malformed_pass: bool | None = None
    temp0_agreement: float | None = None
    temp0_modal_answer: str | None = None
    realias_outputs: list[str] = field(default_factory=list)
    price_in: float | None = None
    price_out: float | None = None
    cost_usd: float = 0.0
    notes: list[str] = field(default_factory=list)


def _cost_so_far() -> float:
    from selfpred.client import _spend_in_log
    return _spend_in_log(config.RAW_DIR / "verification.jsonl")


# --------------------------------------------------------------------------------------

def main() -> None:
    if not MODELS_JSON.exists():
        raise SystemExit("Run scripts/phase_b_discover.py first (it saves the model list).")
    payload = json.loads(MODELS_JSON.read_text(encoding="utf-8"))
    book: PriceBook = price_book_from_models_payload(payload)

    reports: dict[str, ModelReport] = {
        c.model_id: ModelReport(
            model_id=c.model_id, provider_pinned=c.provider, tier=c.tier, pair=c.pair,
            quantization=c.quantization,
            price_in=book.prompt.get(c.model_id), price_out=book.completion.get(c.model_id),
        )
        for c in CANDIDATES
    }

    with OpenRouterClient("verification", price_book=book) as client:
        # ---- step 4 + 5: existence, pinning, reasoning-off --------------------------
        print("\n=== steps 4-5: resolve, pin, reasoning-off ===")
        for c in CANDIDATES:
            r = reports[c.model_id]
            try:
                res = client.chat(
                    model_id=c.model_id, messages=OK_PROMPT, provider=c.provider,
                    max_tokens=8, tag="step4-ok",
                )
                r.exists = True
                r.returned_model = res.model_returned
                r.returned_provider = res.provider_returned
                r.pinning_pass = res.provider_ok
                r.reasoning_off_accepted = True
                r.reasoning_tokens_billed = res.reasoning_tokens
                r.cost_usd += res.cost_usd
                print(f"  OK   {c.model_id:<46} -> {res.provider_returned!s:<14} "
                      f"reasoning_tok={res.reasoning_tokens} out={res.text[:16]!r}")
            except ProviderMismatch as exc:
                r.exists = True
                r.pinning_pass = False
                r.notes.append(f"PINNING FAIL: {exc}")
                print(f"  PIN! {c.model_id:<46} {exc}")
            except (ProviderUnavailable, RedactedError) as exc:
                msg = str(exc)
                # A 400 that mentions reasoning means the parameter was rejected; retry
                # once WITHOUT it and record reasoning-off as not accepted.
                if "reasoning" in msg.lower():
                    try:
                        res = client.chat(
                            model_id=c.model_id, messages=OK_PROMPT, provider=c.provider,
                            max_tokens=8, reasoning_off=False, tag="step4-ok-noreasonparam",
                        )
                        r.exists = True
                        r.returned_model = res.model_returned
                        r.returned_provider = res.provider_returned
                        r.pinning_pass = res.provider_ok
                        r.reasoning_off_accepted = False
                        r.reasoning_tokens_billed = res.reasoning_tokens
                        r.cost_usd += res.cost_usd
                        r.notes.append("reasoning-off parameter REJECTED; call succeeded without it")
                        print(f"  ~OK  {c.model_id:<46} reasoning param rejected")
                        continue
                    except Exception as exc2:  # noqa: BLE001
                        msg = str(exc2)
                r.exists = False
                r.notes.append(f"FAILED: {msg[:220]}")
                print(f"  FAIL {c.model_id:<46} {msg[:110]}")
            except BudgetExceeded:
                raise

        print(f"  [cost so far: ${_cost_so_far():.4f}]")

        # ---- step 6: malformed rate on 10 one-letter calls --------------------------
        print("\n=== step 6: one-letter malformed rate (10 calls each) ===")
        for c in CANDIDATES:
            r = reports[c.model_id]
            if not r.exists or r.pinning_pass is False:
                continue
            malformed = 0
            for i, (a, b) in enumerate(ONE_LETTER_ITEMS):
                try:
                    label, calls = client.one_letter(
                        model_id=c.model_id, messages=one_letter_msgs(a, b),
                        provider=c.provider, tag=f"step6-{i}",
                        reasoning_off=r.reasoning_off_accepted is not False,
                        max_tokens=4,
                    )
                    r.cost_usd += sum(k.cost_usd for k in calls)
                    if label is None:
                        malformed += 1
                except Exception as exc:  # noqa: BLE001
                    malformed += 1
                    r.notes.append(f"step6 error: {str(exc)[:120]}")
            r.malformed_rate = malformed / len(ONE_LETTER_ITEMS)
            r.malformed_pass = r.malformed_rate < config.MALFORMED_RATE_PASS_THRESHOLD
            print(f"  {c.model_id:<46} malformed {r.malformed_rate:.0%} "
                  f"{'PASS' if r.malformed_pass else 'FAIL'}")
        print(f"  [cost so far: ${_cost_so_far():.4f}]")

        # ---- step 7: determinism, 20 temperature-0 repeats (shortlist only) ---------
        print("\n=== step 7: temperature-0 agreement, 20 repeats (shortlisted pair members) ===")
        shortlist = [c for c in CANDIDATES if c.pair in SHORTLIST_PAIRS]
        for c in shortlist:
            r = reports[c.model_id]
            if not r.exists or r.pinning_pass is False:
                continue
            answers: list[str] = []
            for i in range(20):
                try:
                    res = client.chat(
                        model_id=c.model_id, messages=DETERMINISM_PROMPT, provider=c.provider,
                        max_tokens=4, tag=f"step7-{i}",
                        reasoning_off=r.reasoning_off_accepted is not False,
                    )
                    r.cost_usd += res.cost_usd
                    answers.append(res.text.strip()[:4])
                except Exception as exc:  # noqa: BLE001
                    r.notes.append(f"step7 error: {str(exc)[:120]}")
            if answers:
                counts = Counter(answers)
                modal, n = counts.most_common(1)[0]
                r.temp0_agreement = n / len(answers)
                r.temp0_modal_answer = modal
                print(f"  {c.model_id:<46} agreement {r.temp0_agreement:.0%} "
                      f"modal={modal!r} distinct={len(counts)}")
        print(f"  [cost so far: ${_cost_so_far():.4f}]")

        # ---- step 8: re-alias check -------------------------------------------------
        print("\n=== step 8: re-alias check (same 10 prompts, temp 0, both members) ===")
        for c in shortlist:
            r = reports[c.model_id]
            if not r.exists or r.pinning_pass is False:
                continue
            outs: list[str] = []
            for i, p in enumerate(REALIAS_PROMPTS):
                try:
                    res = client.chat(
                        model_id=c.model_id,
                        messages=[{"role": "user", "content": p}],
                        provider=c.provider, max_tokens=8, tag=f"step8-{i}",
                        reasoning_off=r.reasoning_off_accepted is not False,
                    )
                    r.cost_usd += res.cost_usd
                    outs.append(res.text.strip().lower().strip(".!"))
                except Exception as exc:  # noqa: BLE001
                    outs.append(f"<error:{str(exc)[:40]}>")
            r.realias_outputs = outs
            print(f"  {c.model_id:<46} {outs}")
        print(f"  [cost so far: ${_cost_so_far():.4f}]")

        # ---- step 9: burst / rate limit --------------------------------------------
        print("\n=== step 9: 30 concurrent one-letter calls on the leading pair ===")
        burst = {"wall_clock_s": None, "n_429": 0, "n_ok": 0, "n_err": 0, "pair": LEADING_PAIR}
        leader = [c for c in CANDIDATES if c.pair == LEADING_PAIR and reports[c.model_id].exists]
        if leader:
            target = leader[0]
            errors: list[str] = []

            def _one(i: int) -> str:
                a, b = ONE_LETTER_ITEMS[i % len(ONE_LETTER_ITEMS)]
                try:
                    res = client.chat(
                        model_id=target.model_id, messages=one_letter_msgs(a, b),
                        provider=target.provider, max_tokens=4, tag=f"step9-{i}",
                    )
                    return f"ok:{res.cost_usd}"
                except Exception as exc:  # noqa: BLE001
                    return f"err:{str(exc)[:160]}"

            t0 = time.time()
            with ThreadPoolExecutor(max_workers=30) as pool:
                outcomes = list(pool.map(_one, range(30)))
            burst["wall_clock_s"] = round(time.time() - t0, 2)
            for o in outcomes:
                if o.startswith("ok:"):
                    burst["n_ok"] += 1
                else:
                    burst["n_err"] += 1
                    errors.append(o)
                    if "429" in o:
                        burst["n_429"] += 1
            burst["model"] = target.model_id
            burst["provider"] = target.provider
            burst["errors"] = errors[:5]
            print(f"  {target.model_id} @ {target.provider}: {burst['n_ok']}/30 ok, "
                  f"{burst['n_429']} x 429, {burst['wall_clock_s']}s wall clock")
            if errors:
                print(f"  first errors: {errors[:2]}")

    # ---- step 10: total cost -------------------------------------------------------
    total = _cost_so_far()
    print(f"\n=== step 10: total Phase B cost = ${total:.4f} "
          f"(sub-budget ${config.PHASE_BUDGETS_USD['verification']:.2f}) ===")

    out = {
        "models": {k: asdict(v) for k, v in reports.items()},
        "burst": burst,
        "total_cost_usd": total,
    }
    RESULTS_JSON.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"summary -> {RESULTS_JSON}")


if __name__ == "__main__":
    main()
