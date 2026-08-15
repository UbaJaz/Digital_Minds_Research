"""Run one prediction cell.

A *cell* is a (predictor role, target column) pair: M->M, N->M, F->M, M->N, N->N, F->N.
The runner is fully parameterised by that pair, so every cell in the crossed design is
expressible from `config.py` without a code change — and so is the M-row-only design.
Which cells are actually run is a research decision recorded in `02_design_audit.md`;
`config.ACTIVE_CELLS` is `None` until that decision exists, and this runner refuses to
start without it.

No API calls are made by importing this module. Phase C+ only.
"""

from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Sequence

from .. import config
from ..checkpoint import Checkpoint
from ..client import OpenRouterClient, PriceBook
from .prompts import build_predictor_prompt


@dataclass
class PredictionRecord:
    """One predictor's answer on one item. Contains no ground-truth label.

    Scoring joins these against `data/labels/` afterwards, in `analysis/`, which is the
    only place the two ever meet.
    """

    item_id: str
    source_prompt_id: str      # bootstrap resamples by THIS, not by text
    cell: str                  # e.g. "N->M"
    predictor_role: str
    target_column: str
    chosen_letter: str | None  # None == malformed after the one retry
    option_a_persona: str
    option_b_persona: str
    flipped: bool
    model_returned: str | None
    provider_returned: str | None
    malformed: bool


@dataclass
class GeneratedItem:
    """An item produced by the generation phase, as seen by the predictor side.

    Note the absence of a persona/label field: the predictor side is not given one.
    """

    item_id: str
    source_prompt_id: str
    target_column: str
    response_text: str


def run_cell(
    *,
    cell: config.Cell,
    items: Sequence[GeneratedItem],
    persona_keys: tuple[str, str],
    persona_clauses: dict[str, str],
    price_book: PriceBook,
    phase: str = "prediction",
    out_path: Path | None = None,
    client_factory: Callable[..., OpenRouterClient] | None = None,
    predictor_spec: config.ModelSpec | None = None,
    run_tag: str = "",
    max_workers: int = 8,
) -> list[PredictionRecord]:
    """Run every item of one cell, resumably.

    Aborts (budget guard, pinned provider unavailable) propagate: the checkpoint holds the
    completed items, so a rerun continues rather than re-calling. The client never switches
    provider or model to work around an abort.
    """
    # ``predictor_spec`` lets a smoke test supply the model explicitly without filling
    # config.MODELS (which is transcribed only after 02 records the decision).
    spec = predictor_spec or config.model(cell.predictor)
    out_path = out_path or (config.GENERATED_DIR / f"predictions_{cell.name.replace('->', '_to_')}{run_tag}.jsonl")
    ckpt = Checkpoint(run_id=f"predict_{cell.name}{run_tag}")
    todo = set(ckpt.pending([i.item_id for i in items]))

    factory = client_factory or (lambda: OpenRouterClient(phase, price_book=price_book))
    records: list[PredictionRecord] = []

    for item in items:
        if item.target_column != cell.target:
            raise ValueError(
                f"Item {item.item_id} is from column {item.target_column!r} but cell "
                f"{cell.name} predicts column {cell.target!r}."
            )
    pending_items = [i for i in items if i.item_id in todo]
    io_lock = threading.Lock()

    def _one(client: OpenRouterClient, item: GeneratedItem) -> PredictionRecord:
        prompt = build_predictor_prompt(
            item_id=item.item_id,
            response_text=item.response_text,
            persona_keys=persona_keys,
            persona_clauses=persona_clauses,
        )
        letter, calls = client.one_letter(
            model_id=spec.model_id,
            messages=prompt.messages,
            provider=spec.provider,
            tag=f"{cell.name}|{item.item_id}",
        )
        last = calls[-1]
        rec = PredictionRecord(
            item_id=item.item_id,
            source_prompt_id=item.source_prompt_id,
            cell=cell.name,
            predictor_role=cell.predictor,
            target_column=cell.target,
            chosen_letter=letter,
            option_a_persona=prompt.option_a_persona,
            option_b_persona=prompt.option_b_persona,
            flipped=prompt.flipped,
            model_returned=last.model_returned,
            provider_returned=last.provider_returned,
            malformed=letter is None,
        )
        with io_lock:
            _append(out_path, asdict(rec))
            ckpt.mark(item.item_id, {"letter": letter})
        return rec

    with factory() as client:
        # The client is lock-safe (budget reservation + log are serialised); a modest pool
        # keeps wall-clock down without stressing the pinned provider.
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for rec in pool.map(lambda it: _one(client, it), pending_items):
                records.append(rec)
    return records


def _append(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
