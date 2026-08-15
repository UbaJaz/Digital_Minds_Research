"""Diagnostic: why is VO-D's clustered CI so much tighter than the binomial?

If per-prompt accuracy is pinned near 0.5 (the predictor gives the same letter to both of a
prompt's two items, so exactly one is right whenever the two items share a slot ordering),
the between-prompt variance collapses and the cluster bootstrap reports a very tight
interval that is NOT evidence of precision about the underlying rate. Worth knowing before
that interval is quoted anywhere.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from selfpred import config                                  # noqa: E402
from selfpred.analysis.score import load_column, score_cell   # noqa: E402
from run_pipeline import candidate_pairs, load_prompts        # noqa: E402

pids = {p.prompt_id for p in load_prompts("prompts_pilot.json")}

for pair_id in ("VO-D", "VO-B"):
    pair = next(p for p in candidate_pairs() if p.pair_id == pair_id)
    for col in ("M", "N"):
        tag = f"_pilot_{pair.pair_id}"
        cd = load_column(col, run_tag=tag, labels_dir=config.LABELS_DIR, prompt_ids=pids)
        sc = score_cell(config.Cell(col, col), cd, run_tag=tag)
        per: dict[str, list[int]] = {}
        for iid, ok in sc.correct.items():
            per.setdefault(cd.prompt_of[iid], []).append(ok)
        means = np.array([np.mean(v) for v in per.values()])
        sizes = Counter(len(v) for v in per.values())
        acc = float(np.mean(list(sc.correct.values())))
        n = len(sc.correct)
        binom_half = 1.96 * np.sqrt(acc * (1 - acc) / n)
        # SE of the clustered mean, computed analytically for comparison
        clust_se = means.std(ddof=1) / np.sqrt(len(means))
        print(f"\n{pair_id} {col}: acc={acc:.3f} n={n} prompts={len(per)} sizes={dict(sizes)}")
        print(f"  per-prompt accuracy distribution: {dict(Counter(np.round(means,3)))}")
        print(f"  binomial 95% half-width  = {binom_half:.4f}")
        print(f"  clustered 95% half-width = {1.96*clust_se:.4f}  (between-prompt sd={means.std(ddof=1):.4f})")
