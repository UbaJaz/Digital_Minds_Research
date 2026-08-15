# 06 — Hermes-3 Enactment Smoke Test (council ASSUMPTION 8)

**Status:** pre-registered criteria written **before** any call (this section). Results are appended below by the run script and must not alter this section.

## What this is and is not

- **Is:** a feasibility check of whether both members of the tier-(i) pair (`meta-llama/llama-3.1-70b-instruct`, `nousresearch/hermes-3-llama-3.1-70b`, both DeepInfra fp8) can (a) enact a persona clause on a dilemma prompt with usable output, and (b) return a clean one-letter answer on the *real* predictor prompt at real input length. This is `05_status_and_plan.md` §4.1 / §6.
- **Is not:** the Phase D pilot, and not evidence about the feasibility band. **Self / Near accuracies are sealed** — the run script writes predictions and labels to separate files and computes no accuracy. Nobody reads a Self number before the band is written into `02`.
- Uses **draft** stimuli (`data/stimuli/smoke/`, hashes in `FREEZE.md`) that are excluded from the main stimulus set. The persona pair is the council's Q6 *example*, not a locked decision.
- Generation temperature: `config.GENERATION_TEMPERATURE = 1.0` (the current code default; the value is an open decision — see 05 §1.3). 1.0 is the harder condition for usability, so a pass here is conservative.

## Pre-declared criteria (council Q2/Q6: "> 90 % usable")

**Generation (per model, 20 outputs = 10 prompts × 2 personas):**
A generation is **unusable** if any of:
1. empty, or fewer than 60 words;
2. a refusal / deflection (regex on "I can't", "I cannot", "I'm not able", "as an AI", "I am not able", "consult a professional" as the *whole* answer);
3. echoes the instruction: contains "instruction", "persona", "as instructed", "the principle", "I was told";
4. wrong format: markdown headings or bullet lists (`^#`, `^- `, `^\* `, `^\d+\.` at line start).

Soft flags (recorded, reviewed by eye, do **not** fail an item by themselves): contains "autonomy", "welfare", "wellbeing", "well-being"; `finish_reason == "length"` (truncated at 320 tokens but otherwise complete prose).

**Pass:** usable rate ≥ 90 % (≥ 18/20) **per model**. Llama is expected to pass; Hermes is the question.

**Prediction (per predictor, 40 items = both columns):** malformed rate (no A/B parsed after one retry) < 5 % on the actual `PREDICTOR_TEMPLATE`. **Pass:** ≥ 38/40 clean letters per predictor.

**Consequence table (fixed now):**
- Hermes passes both → tier-(i) pair viable for the crossed design; proceed to 02 sign-off Q1 with the crossed design available.
- Hermes fails generation, passes prediction → the N *column* is not buildable; ladder level 2 (M-row) with the tier-(i) pair as predictors is the live design; record and go to sign-off #13.
- Hermes fails prediction → tier-(i) pair not viable as specified; fallback pair is tier-(ii) GPT-4o snapshots (re-alias check owed) — sign-off.

**Budget:** phase `smoke`, sub-budget $0.08; expected ≈ $0.02. Log: `data/raw/smoke.jsonl`.

---

## Results (appended by scripts/smoke_hermes_enactment.py)

### Stage 1 — generation usability (pre-declared rules in the section above)

| Column / generator | n | usable | rate | hard-fail reasons | soft flags | finish=length | mean words | PASS (>=90%) |
|---|---|---|---|---|---|---|---|---|
| M / `meta-llama/llama-3.1-70b-instruct` | 20 | 19 | 95% | {'format': 1} | {'names-value': 5, 'truncated': 1} | 1 | 201 | PASS |
| N / `nousresearch/hermes-3-llama-3.1-70b` | 20 | 19 | 95% | {'format': 1} | {'names-value': 10} | 0 | 198 | PASS |

### Stage 2 — prediction malformed rate on the real predictor prompt

| Cell | items | malformed | rate | PASS (<5%) |
|---|---|---|---|---|
| M->M | 20 | 0 | 0% | — |
| M->N | 20 | 0 | 0% | — |
| N->M | 20 | 0 | 0% | — |
| N->N | 20 | 0 | 0% | — |
| **predictor M total** | 40 | 0 | 0% | PASS |
| **predictor N total** | 40 | 0 | 0% | PASS |

**Smoke phase spend:** $0.0256 (sub-budget $0.08). Log: `data/raw/smoke.jsonl`.

**Sealed:** `data/generated/predictions_*_smoke.jsonl` and `data/labels_smoke/` were never joined; no accuracy exists.

**Consequence (per the pre-declared table):** Hermes PASSES both stages -> tier-(i) pair viable for the crossed design.


### Reviewer notes on the soft flags (label-free review of `data/generated/*_smoke.jsonl` only)

- **Hard fails (1 per model):** both were list formatting ("Here's my advice:\n\n1. …") despite the scaffold's "no headings or bullet points". At temperature 1.0 the format instruction is obeyed 38/40. Acceptable for a smoke test; the pilot should decide whether format violations are excluded label-blind or tolerated.
- **Truncation (1, Llama, smoke-03):** hit the 320-token ceiling and drifted into meta-commentary ("The writer also leaves some final advice…"). One-off; raise `GENERATION_MAX_TOKENS` to ~400 or lower the word target to 100–160.
- **"names-value" (Llama 5/20, Hermes 10/20):** the phrase **"long-term well-being" / "prioritize your … well-being" recurs across the flagged outputs** (≈ 8 distinct sentences in 40 outputs), i.e. the *welfare* clause's wording is being paraphrased nearly verbatim into the text. Which persona each came from was not looked at (sealed), but the frequency alone is a **leakage warning for Phase D**: a surface baseline with a "long-term"/"well-being" lexical feature could plausibly clear 58 %, and the forced-choice task could be too easy. Two mitigations for the pilot's persona-pair candidates: (i) write clauses whose distinctive tokens are not natural advice vocabulary (avoid "long-term", "well-being", "autonomy"), and/or (ii) add an explicit lexical ban to the scaffold; and in either case make sure D's feature set includes these tokens so it is an honest leakage check rather than a blind one. This is exactly what the ≤ 3-pair screen in Phase D exists to catch — it is not a failure of the smoke test.
- **Verdict stands:** ASSUMPTION 8 is now **verified for the tier-(i) pair** — Hermes-3 enacts a persona clause with 95 % usable output at temperature 1.0 and returns 0 % malformed letters on the real predictor prompt at real length. The crossed design is available; Q1 in `02` can be decided with that known.
