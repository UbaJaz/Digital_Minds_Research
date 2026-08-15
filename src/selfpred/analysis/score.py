"""The only place predictions and ground-truth labels are joined.

Inputs are the label-free prediction JSONL written by ``predict.run_cell`` and the label
JSONL written by ``personas.generate`` (via ``selfpred.labels``). Outputs are the per-item
correctness maps the bootstrap functions consume, plus the validity checks 02 requires:

* self cells: generator provider/quantization == predictor provider (Locked #5);
* position-bias check per predictor (Locked #3);
* label-blind exclusions applied to generations *before* the join (row P11).
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

from .. import config
from ..labels import LabelRecord, load_labels
from ..personas.quality import assess


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


@dataclass
class ColumnData:
    """Everything about one target column: generated texts, labels, quality verdicts."""

    column: str
    texts: dict[str, str]                 # item_id -> response text
    prompt_of: dict[str, str]             # item_id -> source prompt id
    labels: dict[str, LabelRecord]        # item_id -> label
    usable: set[str]                      # item ids passing the label-blind rules
    quality_reasons: Counter = field(default_factory=Counter)
    generator_provider: str | None = None
    generator_model: str | None = None


def load_column(
    column: str,
    *,
    run_tag: str = "",
    labels_dir: Path | None = None,
    prompt_ids: set[str] | None = None,
) -> ColumnData:
    """Load one generated column.

    ``prompt_ids`` restricts the load to items from those source prompts. Without it a
    resumed run reads every item the checkpoint has accumulated, which silently changes
    what a "40-item screen" means between a fresh run and a resume — the numbers stop
    being reproducible. Callers that mean a specific subset must say so.
    """
    gen_path = config.GENERATED_DIR / f"generated_column_{column}{run_tag}.jsonl"
    rows = _read_jsonl(gen_path)
    if prompt_ids is not None:
        rows = [r for r in rows if r["source_prompt_id"] in prompt_ids]
    if labels_dir is None:
        labels = load_labels(column) if not run_tag else {
            r["item_id"]: LabelRecord(**r) for r in _read_jsonl(config.LABELS_DIR / f"labels_column_{column}{run_tag}.jsonl")
        }
    else:
        labels = {r["item_id"]: LabelRecord(**r) for r in _read_jsonl(labels_dir / f"labels_column_{column}{run_tag}.jsonl")}
    texts, prompt_of, usable, reasons = {}, {}, set(), Counter()
    providers, models = Counter(), Counter()
    for r in rows:
        texts[r["item_id"]] = r["response_text"]
        prompt_of[r["item_id"]] = r["source_prompt_id"]
        v = assess(r["response_text"], r.get("finish_reason"))
        if v.usable:
            usable.add(r["item_id"])
        reasons.update(v.reasons)
        providers[r.get("provider_returned")] += 1
        models[r.get("model_returned")] += 1
    return ColumnData(
        column=column, texts=texts, prompt_of=prompt_of, labels=labels, usable=usable,
        quality_reasons=reasons,
        generator_provider=providers.most_common(1)[0][0] if providers else None,
        generator_model=models.most_common(1)[0][0] if models else None,
    )


@dataclass
class CellScore:
    cell: str
    correct: dict[str, int]          # item_id -> 0/1 (usable, non-malformed items only)
    n_predicted: int
    n_malformed: int
    n_excluded_quality: int
    a_share: float                   # share of "A" answers — position-bias check
    flipped_acc: float | None        # accuracy on flipped items
    unflipped_acc: float | None      # accuracy on unflipped items
    predictor_provider: str | None
    predictor_model: str | None
    provider_ok_for_self: bool | None   # only meaningful for self cells


def score_cell(cell: config.Cell, col: ColumnData, *, run_tag: str = "") -> CellScore:
    path = config.GENERATED_DIR / f"predictions_{cell.name.replace('->', '_to_')}{run_tag}.jsonl"
    preds = _read_jsonl(path)
    correct: dict[str, int] = {}
    n_mal = n_excl = 0
    a_count = 0
    flip_c, flip_n, unflip_c, unflip_n = 0, 0, 0, 0
    providers, models = Counter(), Counter()
    for p in preds:
        iid = p["item_id"]
        providers[p.get("provider_returned")] += 1
        models[p.get("model_returned")] += 1
        if iid not in col.usable:
            n_excl += 1
            continue
        if p["malformed"] or p["chosen_letter"] is None:
            n_mal += 1
            continue
        lab = col.labels[iid].persona_key
        truth_letter = "A" if p["option_a_persona"] == lab else "B"
        ok = int(p["chosen_letter"] == truth_letter)
        correct[iid] = ok
        a_count += p["chosen_letter"] == "A"
        if p["flipped"]:
            flip_c += ok; flip_n += 1
        else:
            unflip_c += ok; unflip_n += 1
    pred_provider = providers.most_common(1)[0][0] if providers else None
    self_ok = None
    if cell.is_self_cell:
        self_ok = (pred_provider is not None and pred_provider == col.generator_provider
                   and models.most_common(1)[0][0] == col.generator_model)
    return CellScore(
        cell=cell.name, correct=correct, n_predicted=len(preds), n_malformed=n_mal,
        n_excluded_quality=n_excl, a_share=(a_count / len(correct)) if correct else float("nan"),
        flipped_acc=(flip_c / flip_n) if flip_n else None,
        unflipped_acc=(unflip_c / unflip_n) if unflip_n else None,
        predictor_provider=pred_provider, predictor_model=models.most_common(1)[0][0] if models else None,
        provider_ok_for_self=self_ok,
    )


def accuracy_ci(correct: Mapping[str, int], prompt_of: Mapping[str, str], *, n_boot: int = 10_000,
                seed: int = config.BOOTSTRAP_SEED) -> tuple[float, float, float]:
    """Cell accuracy with a prompt-clustered bootstrap CI."""
    import numpy as np
    ids = sorted(correct)
    if not ids:
        return float("nan"), float("nan"), float("nan")
    by_prompt: dict[str, list[int]] = {}
    for pos, i in enumerate(ids):
        by_prompt.setdefault(prompt_of[i], []).append(pos)
    prompts = sorted(by_prompt)
    vals = np.asarray([correct[i] for i in ids], dtype=float)
    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot)
    for k in range(n_boot):
        pick = rng.integers(0, len(prompts), size=len(prompts))
        idx = [p for j in pick for p in by_prompt[prompts[j]]]
        boots[k] = vals[idx].mean()
    return float(vals.mean()), float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))
