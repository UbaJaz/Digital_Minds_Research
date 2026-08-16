# 07 — Calibration Probe Results (Phase 1C)

**Rule (02 row P8):** 50 frozen paraphrase-preference items; Agreement(X, Target); accept Near > Far if the point estimate A_near > A_far; CI reported.

| Quantity | Value | 95 % bootstrap CI |
|---|---|---|
| Items with all three answers | 47 | — |
| A_near (Hermes-3 vs Llama-3.1) | 0.660 | [0.532, 0.787] |
| A_far (mistralai/mistral-small-3.2-24b-instruct vs Llama-3.1) | 0.638 | [0.489, 0.766] |
| Δ = A_near − A_far | +0.021 | [-0.064, +0.106] |
| Target's share of "A" answers (position bias) | 0.38 | — |
| Malformed (target/near/far) | {'target': 1, 'near': 2, 'far': 0} | — |

**Outcome:** Near > Far on the point estimate — similarity ordering accepted; ASSUMPTION 9 (Far not distilled from Target) not contradicted.
No Far swap needed.

Spend so far: $0.0377. Raw: `data/generated/calibration/`, log `data/raw/calibration.jsonl`.
