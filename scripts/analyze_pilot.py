"""Pilot-as-result analysis. No API calls — reads only what Phase D already bought.

The four persona pairs span a wide range of surface leakage by construction (VO-A/B/C on the
original scaffold, VO-D on a style-equalising one). That turns the failed pilot into a
measurement: does self-prediction accuracy track the surface-feature baseline across designs?

Outputs data/results/pilot_analysis.json.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from selfpred import config                                   # noqa: E402
from selfpred.analysis.score import load_column, score_cell    # noqa: E402
from selfpred.analysis.stats import BootstrapCI                # noqa: E402
from selfpred.baseline import fit_baseline_cv                  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from run_pipeline import candidate_pairs, load_prompts         # noqa: E402


def clustered_ci(correct: dict[str, int], prompt_of: dict[str, str],
                 n_boot: int = 10_000, seed: int = config.BOOTSTRAP_SEED) -> BootstrapCI:
    """Accuracy CI resampling SOURCE PROMPTS, not texts (both personas share a prompt)."""
    ids = sorted(correct)
    vals = np.asarray([correct[i] for i in ids], float)
    by: dict[str, list[int]] = {}
    for pos, i in enumerate(ids):
        by.setdefault(prompt_of[i], []).append(pos)
    prompts = sorted(by)
    rng = np.random.default_rng(seed)
    boot = np.empty(n_boot)
    for k in range(n_boot):
        pick = rng.integers(0, len(prompts), len(prompts))
        idx = [p for i in pick for p in by[prompts[i]]]
        boot[k] = vals[idx].mean()
    return BootstrapCI(float(vals.mean()), *np.quantile(boot, [0.025, 0.975]), n_boot=n_boot)


def main() -> None:
    all_prompts = load_prompts("prompts_pilot.json")
    pids = {p.prompt_id for p in all_prompts}
    rows = []
    for pair in candidate_pairs():
        for col in ("M", "N"):
            tag = f"_pilot_{pair.pair_id}"
            try:
                cd = load_column(col, run_tag=tag, labels_dir=config.LABELS_DIR, prompt_ids=pids)
                if not cd.texts:
                    continue
                sc = score_cell(config.Cell(col, col), cd, run_tag=tag)
                if not sc.correct:
                    continue
            except FileNotFoundError:
                continue
            ci = clustered_ci(sc.correct, cd.prompt_of)
            usable = sorted(cd.usable)
            d = fit_baseline_cv(
                target_column=col, item_ids=usable,
                texts=[cd.texts[i] for i in usable],
                labels=[int(cd.labels[i].persona_key == pair.key_b) for i in usable],
                groups=[cd.prompt_of[i] for i in usable],
            )
            rows.append({
                "pair": pair.pair_id, "column": col, "scaffold":
                    "style-equalised" if pair.scaffold else "original",
                "n_scored": len(sc.correct), "n_usable": len(cd.usable),
                "self": ci.point, "self_lo": ci.lo, "self_hi": ci.hi,
                "d": d.accuracy,
                "self_beats_chance": bool(ci.lo > 0.5),
                "mean_words": float(np.mean([len(cd.texts[i].split()) for i in usable])),
                # Position-bias diagnostic. A predictor that always answers the same letter
                # scores ~50% with almost no between-prompt variance, which would masquerade
                # as a tight "at chance" interval. a_share near 0 or 1 means degenerate.
                "a_share": float(sc.a_share),
                "n_malformed": int(sc.n_malformed),
            })
            print(f"{pair.pair_id} {col} ({rows[-1]['scaffold']:>15}): "
                  f"Self {ci.point:.3f} [{ci.lo:.3f},{ci.hi:.3f}]  D {d.accuracy:.3f}  "
                  f"n={len(sc.correct)}  words={rows[-1]['mean_words']:.0f}  "
                  f"A-share={sc.a_share:.2f}")

    self_v = np.array([r["self"] for r in rows])
    d_v = np.array([r["d"] for r in rows])
    r_pearson = float(np.corrcoef(self_v, d_v)[0, 1])
    # Slope of Self on D across designs.
    slope, intercept = np.polyfit(d_v, self_v, 1)
    print(f"\nAcross {len(rows)} column-results: corr(Self, D) = {r_pearson:+.3f}; "
          f"Self ≈ {slope:.2f}·D + {intercept:.2f}")
    print(f"D ≥ Self in {int(sum(d_v >= self_v))}/{len(rows)} column-results")

    out = {"rows": rows, "corr_self_d": r_pearson, "slope": float(slope),
           "intercept": float(intercept), "n_results": len(rows),
           "d_ge_self": int(sum(d_v >= self_v))}
    (config.RESULTS_DIR if hasattr(config, "RESULTS_DIR") else ROOT / "data/results").mkdir(
        parents=True, exist_ok=True)
    (ROOT / "data/results/pilot_analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-> data/results/pilot_analysis.json")


if __name__ == "__main__":
    main()
