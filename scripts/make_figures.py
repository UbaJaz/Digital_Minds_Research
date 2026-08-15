"""Figures for the report.

Figure 1 — the pilot: self-prediction accuracy against the surface-feature baseline across
           eight column-results. If self-prediction were reading something the surface
           classifier cannot, points would sit well above the diagonal.
Figure 2 — the leakage manipulation (02 amendment A4): the self-advantage (M->M minus N->M)
           on leaky stimuli versus style-equalised stimuli, with prompt-clustered CIs.

No API calls. Reads data/results/*.json written by the pipeline and analyze_pilot.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data/results"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
    "figure.dpi": 200, "savefig.bbox": "tight", "axes.grid": True,
    "grid.alpha": 0.25, "axes.spines.top": False, "axes.spines.right": False,
})

BLUE, ORANGE, GREY = "#2c6fb5", "#d1642a", "#666666"


def figure1() -> None:
    p = RES / "pilot_analysis.json"
    if not p.exists():
        print("skip fig1: no pilot_analysis.json"); return
    rows = json.loads(p.read_text(encoding="utf-8"))["rows"]
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    ax.plot([0.25, 0.85], [0.25, 0.85], ls="--", c=GREY, lw=1,
            label="self = surface baseline")
    ax.axhline(0.5, c=GREY, lw=0.8, alpha=0.5)
    ax.axvline(0.5, c=GREY, lw=0.8, alpha=0.5)
    for r in rows:
        clean = r["scaffold"] != "original"
        ax.errorbar(r["d"], r["self"],
                    yerr=[[r["self"] - r["self_lo"]], [r["self_hi"] - r["self"]]],
                    fmt="o", ms=9, capsize=3, lw=1.2,
                    color=ORANGE if clean else BLUE,
                    label=("style-equalised (VO-D)" if clean else "original scaffold")
                    if r["pair"] in ("VO-A", "VO-D") and r["column"] == "M" else None)
        ax.annotate(f"{r['pair']}-{r['column']}", (r["d"], r["self"]),
                    textcoords="offset points", xytext=(8, -3), fontsize=8, color=GREY)
    ax.set_xlabel("Surface-feature baseline D (accuracy)")
    ax.set_ylabel("Self-prediction accuracy (M→M / N→N)")
    ax.set_title("Self-prediction tracks the surface baseline")
    ax.set_xlim(0.25, 0.85); ax.set_ylim(0.4, 0.88)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    fig.savefig(FIG / "fig1_self_vs_surface.png")
    print("-> figures/fig1_self_vs_surface.png")


def figure2() -> None:
    p = RES / "main_two_set.json"
    if not p.exists():
        print("skip fig2: no main_two_set.json yet"); return
    d = json.loads(p.read_text(encoding="utf-8"))
    order = [("VO-C", "leaky stimuli\n(surface cue present)", BLUE),
             ("VO-D", "style-equalised stimuli\n(surface cue removed)", ORANGE)]
    have = [(k, lab, c) for k, lab, c in order if k in d["pairs"]]
    if not have:
        print("skip fig2: no pairs"); return

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))

    # -- left: the self-advantage in each stimulus set ---------------------------------
    ax = axes[0]
    for i, (k, lab, c) in enumerate(have):
        s = d["pairs"][k]["self_vs_near"]
        ax.errorbar(i, s["point"], yerr=[[s["point"] - s["lo"]], [s["hi"] - s["point"]]],
                    fmt="o", ms=11, capsize=5, lw=2, color=c)
    ax.axhline(0, c=GREY, lw=1)
    ax.set_xticks(range(len(have)))
    ax.set_xticklabels([lab for _, lab, _ in have], fontsize=9)
    ax.set_xlim(-0.5, len(have) - 0.5)
    ax.set_ylabel("Self-advantage:  acc(M→M) − acc(N→M)")
    # Title states what the data show, not what was predicted: the self-advantage is
    # negative where style leaks and exactly zero once it is removed.
    ax.set_title("No self-advantage in either condition")

    # -- right: all six cells per set ---------------------------------------------------
    ax = axes[1]
    cells = ["M->M", "N->M", "F->M", "M->N", "N->N", "F->N"]
    w = 0.38
    for j, (k, lab, c) in enumerate(have):
        cd = d["pairs"][k]["cells"]
        xs = [i + (j - 0.5) * w for i in range(len(cells))]
        ys = [cd[cn]["acc"] for cn in cells]
        err = [[cd[cn]["acc"] - cd[cn]["lo"] for cn in cells],
               [cd[cn]["hi"] - cd[cn]["acc"] for cn in cells]]
        ax.errorbar(xs, ys, yerr=err, fmt="o", ms=7, capsize=3, lw=1.2, color=c,
                    label=k + (" (leaky)" if k == "VO-C" else " (clean)"))
        # Surface baseline D, per generator column — the reference every LLM is measured
        # against. On the leaky set it sits ABOVE every language model.
        bd = d["pairs"][k]["baseline_d"]
        for col, span in (("M", (0, 2)), ("N", (3, 5))):
            x0 = span[0] + (j - 0.5) * w - 0.18
            x1 = span[1] + (j - 0.5) * w + 0.18
            ax.plot([x0, x1], [bd[col]] * 2, ls=":", lw=2, color=c,
                    label=f"{k}: surface baseline D" if col == "M" else None)
    ax.axhline(0.5, c=GREY, ls="--", lw=1, label="chance")
    ax.set_xticks(range(len(cells)))
    ax.set_xticklabels([c.replace("->", "→") for c in cells])
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Cell  (predictor → generator column)")
    ax.set_title("All six cells, both stimulus sets")
    ax.legend(fontsize=9, frameon=False)
    fig.savefig(FIG / "fig2_leakage_manipulation.png")
    print("-> figures/fig2_leakage_manipulation.png")


if __name__ == "__main__":
    figure1()
    figure2()
