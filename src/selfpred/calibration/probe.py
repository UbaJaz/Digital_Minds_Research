"""Phase 1C — similarity calibration probe (02 row P8, locked 2026-08-15).

50 forced-choice items: two paraphrases of one sentence, "Which reads better?". Frozen once
(A/B order randomised with ``config.CALIBRATION_SEED``); every predictor sees the identical
items at temperature 0. Agreement(X, Target) = share of items where X's letter equals
Target's letter. Δ = A_near − A_far, paired bootstrap over items.

Pre-declared rule (row P8): the Near > Far ordering is accepted if the **point estimate**
A_near > A_far; the CI is reported. If not, Far is swapped for ``config.FAR_SWAP`` and the
probe re-run before the main experiment.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Sequence

import numpy as np

from .. import config
from ..checkpoint import Checkpoint
from ..client import OpenRouterClient, PriceBook

STIM_DIR = config.REPO_ROOT / "data" / "stimuli" / "calibration"
SOURCE_PATH = STIM_DIR / "items_source.json"
FROZEN_PATH = STIM_DIR / "items.json"
OUT_DIR = config.GENERATED_DIR / "calibration"


@dataclass(frozen=True)
class CalItem:
    item_id: str
    text_a: str
    text_b: str
    flipped: bool   # True if canonical (x, y) was shown as (B, A)


def freeze_items() -> list[CalItem]:
    """Randomise A/B order once and write items.json with a content hash. Idempotent."""
    if FROZEN_PATH.exists():
        data = json.loads(FROZEN_PATH.read_text(encoding="utf-8"))
        return [CalItem(**it) for it in data["items"]]
    src = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    rng = random.Random(config.CALIBRATION_SEED)
    items: list[CalItem] = []
    for i, (x, y) in enumerate(src["items"]):
        flipped = rng.random() < 0.5
        a, b = (y, x) if flipped else (x, y)
        items.append(CalItem(item_id=f"cal-{i+1:03d}", text_a=a, text_b=b, flipped=flipped))
    payload = {"question": src["question"], "seed": config.CALIBRATION_SEED, "items": [asdict(it) for it in items]}
    FROZEN_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    h = hashlib.sha256(FROZEN_PATH.read_bytes()).hexdigest()
    (STIM_DIR / "FREEZE.md").write_text(
        f"# Calibration items freeze\n\nFrozen before any model saw them. `items.json` sha256 `{h}`; "
        f"seed {config.CALIBRATION_SEED}; {len(items)} items.\n", encoding="utf-8")
    return items


def question_text() -> str:
    return json.loads(FROZEN_PATH.read_text(encoding="utf-8"))["question"]


def run_predictor(
    *, role: str, items: Sequence[CalItem], price_book: PriceBook, phase: str = "calibration",
    spec: config.ModelSpec | None = None, run_tag: str = "",
) -> dict[str, str | None]:
    """Run one predictor over the frozen items, resumably. Returns item_id -> letter/None."""
    spec = spec or config.model(role)
    q = question_text()
    out_path = OUT_DIR / f"calibration_{role}{run_tag}.jsonl"
    ckpt = Checkpoint(run_id=f"calibration_{role}{run_tag}")
    todo = set(ckpt.pending([it.item_id for it in items]))
    if todo:
        with OpenRouterClient(phase, price_book=price_book) as client:
            for it in items:
                if it.item_id not in todo:
                    continue
                messages = [
                    {"role": "system", "content": "Answer with a single letter and nothing else."},
                    {"role": "user", "content": q.format(a=it.text_a, b=it.text_b)},
                ]
                letter, calls = client.one_letter(
                    model_id=spec.model_id, messages=messages, provider=spec.provider,
                    tag=f"cal|{role}|{it.item_id}",
                )
                rec = {"item_id": it.item_id, "role": role, "letter": letter,
                       "model_returned": calls[-1].model_returned, "provider_returned": calls[-1].provider_returned}
                out_path.parent.mkdir(parents=True, exist_ok=True)
                with out_path.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec) + "\n")
                ckpt.mark(it.item_id, {"letter": letter})
    answers: dict[str, str | None] = {}
    for line in out_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            answers[r["item_id"]] = r["letter"]
    return answers


@dataclass
class CalibrationResult:
    n_items: int
    a_near: float
    a_far: float
    delta: float
    delta_ci: tuple[float, float]
    a_near_ci: tuple[float, float]
    a_far_ci: tuple[float, float]
    near_gt_far_point: bool
    n_malformed: dict[str, int]
    target_a_share: float   # position bias check on the target


def analyze(target: dict[str, str | None], near: dict[str, str | None], far: dict[str, str | None],
            *, n_boot: int = 10_000, seed: int = config.BOOTSTRAP_SEED) -> CalibrationResult:
    ids = sorted(i for i in target if target[i] and near.get(i) and far.get(i))
    t = np.asarray([target[i] for i in ids]); n_ = np.asarray([near[i] for i in ids]); f = np.asarray([far[i] for i in ids])
    agree_n = (n_ == t).astype(float); agree_f = (f == t).astype(float)
    rng = np.random.default_rng(seed)
    bn, bf, bd = np.empty(n_boot), np.empty(n_boot), np.empty(n_boot)
    for k in range(n_boot):
        idx = rng.integers(0, len(ids), size=len(ids))
        bn[k] = agree_n[idx].mean(); bf[k] = agree_f[idx].mean(); bd[k] = bn[k] - bf[k]
    q = lambda arr: (float(np.quantile(arr, 0.025)), float(np.quantile(arr, 0.975)))
    return CalibrationResult(
        n_items=len(ids), a_near=float(agree_n.mean()), a_far=float(agree_f.mean()),
        delta=float(agree_n.mean() - agree_f.mean()), delta_ci=q(bd), a_near_ci=q(bn), a_far_ci=q(bf),
        near_gt_far_point=bool(agree_n.mean() > agree_f.mean()),
        n_malformed={"target": sum(1 for v in target.values() if v is None),
                     "near": sum(1 for v in near.values() if v is None),
                     "far": sum(1 for v in far.values() if v is None)},
        target_a_share=float((t == "A").mean()),
    )
