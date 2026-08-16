# 08 — Persona Pilot Results (Phase 1D)

**Band (02 row P9, fixed before the pilot):** per column, ≥ 80 items where possible, Self accuracy 60–80 % AND Baseline D (5-fold CV grouped by prompt, point estimate) ≤ 58 %. Screen ≤ 3 pairs at 40 items on M; winner at 80 items on M and N. Selection: in-band, then D closest to 50 %, then Self closest to 70 %.

## Screen (20 pilot prompts × 2 personas on M)
| Pair | usable | Self acc (M→M) | D acc | in band |
|---|---|---|---|---|
| VO-A | 40/40 | 0.600 | 0.675 | no |
| VO-B | 40/40 | 0.575 | 0.600 | no |
| VO-C | 40/40 | 0.600 | 0.650 | no |
| VO-D | 40/40 | 0.500 | 0.450 | no |

## Full pilot (40 pilot prompts × 2 personas)
| Pair | Column | usable | Self acc | D acc | in band |
|---|---|---|---|---|---|
| VO-D | M | 80/80 | 0.500 | 0.325 | no |
| VO-D | N | 67/80 | 0.478 | 0.597 | no |
| VO-B | M | 80/80 | 0.600 | 0.588 | no |
| VO-B | N | 80/80 | 0.675 | 0.662 | no |
| VO-C | M | 80/80 | 0.650 | 0.650 | no |
| VO-C | N | 78/80 | 0.744 | 0.756 | no |
| VO-A | M | 80/80 | 0.575 | 0.637 | no |
| VO-A | N | 77/80 | 0.610 | 0.766 | no |

## Gate outcome
**Level 3: no pair in band on M — temperature fallback would be next; NOT run in this session (see 02 Fallback).** Winner: `None`.

Spend so far: $0.2953. Raw: `data/generated/*_pilot_*`, log `data/raw/pilot.jsonl`. Pilot prompts are excluded from the main set.
