"""Bias-corrected analysis of the self-prediction probe (02 amendment A8).

Raw accuracy on a counterbalanced forced choice is not interpretable on its own: a model
with a strong position preference scores near chance whatever it knows. Splitting by which
slot the model's OWN text occupied turns the same data into a signal-detection problem:

    hit rate      = P(say A | own text is A)
    false alarm   = P(say A | own text is B)
    discrimination = hit - false alarm      (0 if the model answers by position alone)
    balanced accuracy = (P(correct | own in A) + P(correct | own in B)) / 2

Discrimination is what "can the model predict its own output" means; raw accuracy is not.
No API calls.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from selfpred.predict.prompts import option_order_for  # noqa: E402

out: dict = {}
for role, name in (("M", "meta-llama/llama-3.1-70b-instruct"),
                   ("N", "nousresearch/hermes-3-llama-3.1-70b")):
    path = ROOT / f"data/checkpoints/selfpred_{role}_VO-C.jsonl"
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = [r for r in rows if r["result"].get("correct") is not None]

    own_a = [r for r in rows if not option_order_for("selfpred|" + r["key"])]
    own_b = [r for r in rows if option_order_for("selfpred|" + r["key"])]
    p_correct_a = sum(r["result"]["correct"] for r in own_a) / len(own_a)
    p_correct_b = sum(r["result"]["correct"] for r in own_b) / len(own_b)

    # P(say A | own is A) is just accuracy on own-in-A; P(say A | own is B) is the error
    # rate on own-in-B, because saying A there is wrong.
    hit, fa = p_correct_a, 1.0 - p_correct_b
    a_share = sum(bool(r["result"]["chose_a"]) for r in rows) / len(rows)

    out[role] = {
        "model": name, "n": len(rows),
        "raw_accuracy": sum(r["result"]["correct"] for r in rows) / len(rows),
        "a_share": a_share,
        "degenerate_by_prereg_rule": bool(a_share >= 0.9 or a_share <= 0.1),
        "p_correct_own_in_A": p_correct_a, "n_own_in_A": len(own_a),
        "p_correct_own_in_B": p_correct_b, "n_own_in_B": len(own_b),
        "hit_rate": hit, "false_alarm_rate": fa,
        "discrimination": hit - fa,
        "balanced_accuracy": (p_correct_a + p_correct_b) / 2,
    }
    d = out[role]
    print(f"{role} ({name})")
    print(f"   raw accuracy      {d['raw_accuracy']:.3f}   A-share {a_share:.2f}"
          f"{'   [DEGENERATE by pre-registered rule]' if d['degenerate_by_prereg_rule'] else ''}")
    print(f"   own text in A     {p_correct_a:.3f} (n={len(own_a)})")
    print(f"   own text in B     {p_correct_b:.3f} (n={len(own_b)})")
    print(f"   discrimination    {hit - fa:+.3f}   balanced accuracy {(p_correct_a+p_correct_b)/2:.3f}")

base = json.loads((ROOT / "data/results/selfrec.json").read_text(encoding="utf-8"))
out["surface_baseline_authorship"] = base["surface_baseline_authorship"]
print(f"\nsurface baseline on the same authorship discrimination: "
      f"{base['surface_baseline_authorship']:.3f}")
(ROOT / "data/results/selfpred_corrected.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("-> data/results/selfpred_corrected.json")
