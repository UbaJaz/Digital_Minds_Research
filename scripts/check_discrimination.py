"""Does the predictor DISCRIMINATE between the two responses generated from one prompt?

Both personas are generated from every source prompt, so each prompt yields exactly two
items with opposite ground truth. A predictor with any signal should assign them to
*different* personas. One that assigns both to the same persona has no discrimination at
all, and scores exactly 50 % on that prompt by construction.

This separates "at chance because it is guessing" from "at chance because it cannot tell
the two apart" — different claims, and only the data can say which.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from selfpred import config                       # noqa: E402
from run_pipeline import load_prompts             # noqa: E402

pids = {p.prompt_id for p in load_prompts("prompts_pilot.json")}
out = {}

for pair_id in ("VO-A", "VO-B", "VO-C", "VO-D"):
    for col in ("M", "N"):
        path = config.GENERATED_DIR / f"predictions_{col}_to_{col}_pilot_{pair_id}.jsonl"
        if not path.exists():
            continue
        rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        rows = [r for r in rows if r["source_prompt_id"] in pids and r.get("chosen_letter")]
        by: dict[str, list[str]] = {}
        for r in rows:
            pred = r["option_a_persona"] if r["chosen_letter"] == "A" else r["option_b_persona"]
            by.setdefault(r["source_prompt_id"], []).append(pred)
        pairs = {k: v for k, v in by.items() if len(v) == 2}
        same = sum(1 for v in pairs.values() if v[0] == v[1])
        n = len(pairs)
        if not n:
            continue
        key = f"{pair_id}-{col}"
        out[key] = {"n_prompts_with_both": n, "same_persona_for_both": same,
                    "same_rate": same / n, "discriminated": n - same}
        print(f"{key:>8}: assigned BOTH responses to the same persona in "
              f"{same}/{n} prompts ({same/n:.0%})  -> discriminated in {n-same}")

(ROOT / "data/results/discrimination.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("\n-> data/results/discrimination.json")
