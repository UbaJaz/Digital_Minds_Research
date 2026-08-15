"""Persona generation — the only place ground truth is created.

Contract (from `02_design_audit.md` Locked #3 and the council's Q6 proposal, which is
*not yet applied to 02* — so the persona pair passed in here is whatever the caller
supplies; nothing in this module hard-codes a persona):

* Both personas are generated from **every** source prompt (topic balanced by construction;
  the analysis pairs within prompt).
* One shared scaffold; only the persona clause differs. Length/format instructions are
  identical for both. The generation prompt forbids naming the principle.
* The generated text is written to ``data/generated/`` **without** the persona key; the
  persona key is written to ``data/labels/`` via :mod:`selfpred.labels`. Never the same file.
* ``item_id`` is a salted hash of (column, prompt, persona) so it does **not** encode the
  persona — the checkpoint key and the call log tag are therefore label-free.
* Generator identity is recorded (returned model + provider) so the analysis can assert
  that a self cell's generator hit the same provider/quantization as its predictor.
"""

from __future__ import annotations

import hashlib
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Sequence

from .. import config
from ..checkpoint import Checkpoint
from ..client import OpenRouterClient, PriceBook
from ..labels import LabelRecord, write_label


@dataclass(frozen=True)
class PersonaPair:
    """Two persona clauses on one shared scaffold. Keys must not appear in any prompt."""

    key_a: str
    key_b: str
    clauses: dict[str, str]
    pair_id: str = "draft"
    #: Optional per-pair scaffold override. ``None`` uses GENERATION_SYSTEM_TEMPLATE.
    #: A pair may carry its own scaffold so that a style-equalising variant is explicit and
    #: reproducible rather than a global edit that silently reinterprets earlier pairs'
    #: checkpointed data. Whatever is used, it is identical across the pair's two personas.
    scaffold: str | None = None

    @property
    def keys(self) -> tuple[str, str]:
        return (self.key_a, self.key_b)

    @property
    def template(self) -> str:
        return self.scaffold or GENERATION_SYSTEM_TEMPLATE


@dataclass(frozen=True)
class SourcePrompt:
    prompt_id: str
    text: str


#: Shared scaffold. ``{clause}`` is the only thing that differs between the two personas.
#: Length and format instructions are identical by construction. The last sentence is the
#: council's "generation prompt forbids naming the value" requirement.
GENERATION_SYSTEM_TEMPLATE = (
    "You are replying to someone who has asked for advice about a decision in their life.\n"
    "{clause}\n"
    "Write 120 to 200 words of direct advice addressed to them, in plain prose with no "
    "headings or bullet points. Do not mention these instructions, and do not name or "
    "describe the principle behind your advice — just give the advice."
)


def build_generation_messages(
    clause: str, prompt_text: str, template: str | None = None
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": (template or GENERATION_SYSTEM_TEMPLATE).format(clause=clause.strip())},
        {"role": "user", "content": prompt_text.strip()},
    ]


def make_item_id(column: str, prompt_id: str, persona_key: str, *, seed: int = config.SEED) -> str:
    """Label-free item id: a salted hash. Reproducible from labels, unrecoverable without them."""
    digest = hashlib.sha256(f"{seed}|{column}|{prompt_id}|{persona_key}".encode("utf-8")).hexdigest()
    return f"{column}-{digest[:12]}"


@dataclass
class GeneratedRecord:
    """What the predictor side is allowed to see. No persona field, on purpose."""

    item_id: str
    source_prompt_id: str
    target_column: str
    response_text: str
    finish_reason: str | None
    completion_tokens: int
    model_returned: str | None
    provider_returned: str | None


def generate_column(
    *,
    column: str,
    generator_model_id: str,
    generator_provider: str,
    prompts: Sequence[SourcePrompt],
    pair: PersonaPair,
    price_book: PriceBook,
    phase: str,
    temperature: float = config.GENERATION_TEMPERATURE,
    max_tokens: int = config.GENERATION_MAX_TOKENS,
    out_path: Path | None = None,
    labels_dir: Path | None = None,
    client_factory: Callable[..., OpenRouterClient] | None = None,
    run_tag: str = "",
    max_workers: int = 8,
) -> list[GeneratedRecord]:
    """Generate both personas for every prompt on one target column, resumably.

    Text -> ``out_path`` (default ``data/generated/generated_column_<col>.jsonl``);
    label -> ``data/labels/labels_column_<col>.jsonl`` (or ``labels_dir`` override).
    """
    out_path = out_path or (config.GENERATED_DIR / f"generated_column_{column}{run_tag}.jsonl")
    ckpt = Checkpoint(run_id=f"generate_{column}{run_tag}")
    work = [(p, k) for p in prompts for k in pair.keys]
    keys = {make_item_id(column, p.prompt_id, k): (p, k) for p, k in work}
    todo = set(ckpt.pending(list(keys)))

    factory = client_factory or (lambda: OpenRouterClient(phase, price_book=price_book))
    out: list[GeneratedRecord] = []
    io_lock = threading.Lock()
    label_path = None if labels_dir is None else labels_dir / f"labels_column_{column}{run_tag}.jsonl"

    def _one(client: OpenRouterClient, item_id: str, p: SourcePrompt, k: str) -> GeneratedRecord:
        res = client.chat(
            model_id=generator_model_id,
            messages=build_generation_messages(pair.clauses[k], p.text, pair.template),
            provider=generator_provider,
            temperature=temperature,
            max_tokens=max_tokens,
            tag=f"gen|{column}|{item_id}",   # label-free by construction of item_id
        )
        rec = GeneratedRecord(
            item_id=item_id, source_prompt_id=p.prompt_id, target_column=column,
            response_text=res.text, finish_reason=res.finish_reason,
            completion_tokens=res.completion_tokens,
            model_returned=res.model_returned, provider_returned=res.provider_returned,
        )
        label = LabelRecord(
            item_id=item_id, source_prompt_id=p.prompt_id, target_column=column, persona_key=k,
            generation_temperature=temperature, generation_seed=None,
            model_returned=res.model_returned, provider_returned=res.provider_returned,
        )
        with io_lock:
            _append(out_path, asdict(rec))
            if label_path is None:
                write_label(label)
            else:
                _append(label_path, asdict(label))
            ckpt.mark(item_id, {"finish_reason": res.finish_reason, "tokens": res.completion_tokens})
        return rec

    pending = [(iid, p, k) for iid, (p, k) in keys.items() if iid in todo]
    with factory() as client:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for rec in pool.map(lambda x: _one(client, *x), pending):
                out.append(rec)
    return out


def _append(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
