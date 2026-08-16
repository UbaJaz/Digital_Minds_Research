# 05 — Status Audit and Path to Data Collection

**Written:** 2026-08-15, mid-sprint (the report draft dates the sprint 14–16 August, so this is Day 2 — see §2).
**Method:** read-only. Ran the existing pytest suite (`38 passed in 4.56s`), read every file under `src/`, `tests/`, `scripts/`, re-summed `data/raw/verification.jsonl`, and fetched the public Hugging Face model card for Hermes-3-Llama-3.1-70B. **No OpenRouter calls were made; spend is unchanged.**
**Authority:** `02_design_audit.md` remains the research design. Nothing below changes it; items needing a decision are marked **[SIGN-OFF]**.

---

## 1. Audit of what exists

### 1.1 Claims verified true

| Claim | Verdict | Evidence |
|---|---|---|
| `.gitignore` covers `.env` | ✅ | `.gitignore` lines 2–5; `.env` shows as untracked-ignored |
| Chat logs moved to `notes/` | ✅ | `notes/message*.txt` present, none at root |
| `CLAUDE.md` extended | ✅ | Purpose, authority, budget guard, secrets, logs, separation sections present |
| Python project + `.venv`, 38 passing tests | ✅ | `pytest -q` → 38 passed |
| Budget guard raises BEFORE the request | ✅ (single process) | `client.py:351–365`: projection → `guard.check` → `guard.commit(projected)` under `threading.Lock`, all before `_post_with_retry` at line 388 |
| Guard safe under concurrency | ✅ within one client | Reservation-then-reconcile pattern (`client.py:360–365`, `413–414`); the Phase B burst test exercised it |
| Provider pinning, `allow_fallbacks=false` | ✅ | `client.py:376–377`; `ProviderMismatch` raised on any deviation; log shows `provider_ok: True` on 311/311 |
| Per-call JSONL log | ✅ | `client.py:529–551`; schema matches `CLAUDE.md` |
| Resumable checkpoints | ✅ | `checkpoint.py`; `predict/run.py:80–81` uses `pending()` |
| `predict/` structurally barred from `labels/` | ✅ at import level (see 1.2 for the gap) | AST test `tests/test_ground_truth_separation.py:59–66`; `GeneratedItem` has no label field |
| 311 verification calls, 11 models | ✅ | Log: 311 records, 11 distinct `model_requested`, `model_returned == model_requested` on all |
| Recommended triple, all DeepInfra fp8 | ✅ as a *ranking* | `04_model_verification.md` §(f); `config.MODELS` still placeholders, as intended |
| Hermes-3-70B shares base weights with Llama-3.1-70B | ✅ **now verified** | HF model card metadata: `Base model: meta-llama/Llama-3.1-70B` (the pretrained base; Meta's `-Instruct` and Nous's Hermes-3 are two post-trainings of it — exactly tier (i)). The card does not say full-parameter vs. PEFT; the Hermes 3 technical report describes a full fine-tune, but I have not re-read it in this session — treat "full-parameter" as unverified. |

### 1.2 Overstated, weak, or missing

**(a) "$0.0071 spent" is slightly stale.** Re-summing the log gives **$0.00735** (311 calls). `verification_summary.json` (`$0.00706`) was written before the follow-up script's 30 calls. Immaterial to budget; material to the habit — the log, not the summary, is the record.

**(b) Twenty Gemini calls carry `cost_source: pricebook` with cost 0.** Empty-completion responses came back without a `usage` block, so the pricebook computed from zero tokens. Cost is genuinely negligible here, but this is a hole: a call whose response lacks `usage` *and* whose model is unpriced is committed at $0 (`client.py:505–510`, `cost_source: "unknown"`). Fix: treat `cost_source != "openrouter"` as a warning in the log summary and never allow `allow_unpriced=True` outside `phase == "verification"`.

**(c) The guard is per-process, per-client-instance.** `BudgetGuard` reads spend from logs at construction (`client.py:169–170`) and then tracks in memory. Two clients in one process, or two people running on two laptops with the same key, do not see each other's spend until restart. In this sprint that is exactly the plan (Ubayd runs calibration while Jaswin runs the pilot). The OpenRouter credit itself is the true ceiling; the working guard is not. Mitigation: one machine runs metered phases, or every runner is short-lived so the log-reconstruction on start does the job.

**(d) The ground-truth barrier is on the *import*, not the *file*.** `predict/` imports `config`, which exposes `LABELS_DIR`; nothing stops a future edit from `open(config.LABELS_DIR / ...)`. The AST test would pass. Add a source-grep test forbidding `LABELS_DIR` and `labels_column` in `predict/`. Related: item IDs must never encode the persona (`item_id = f"{prompt}_{persona}"` would put the label in the checkpoint key and the log tag). The predictor never sees `item_id`, so it is not a leak to the model, but the naming rule should be written down for `generate.py`.

**(e) `predict/run.py` is sequential.** One call at a time (`run.py:87–124`). The "3,000 calls ≈ 4 minutes" extrapolation in `04` §(d) is from a 30-way burst; this runner would take ~1–2 hours for 3,000 calls at 1–2 s each. Not wrong, but the schedule in council Q4 assumes the fast number. The client is lock-safe; a small thread pool in `run_cell` is a 20-line change.

**(f) The interaction bootstrap assumes the two columns have *independent* prompt sets.** `analysis/stats.py:154–219` resamples column M's prompts and column N's prompts independently (docstring: "two independent prompt sets"). If — as the report draft §3.1 and the council's "both personas from every prompt" imply — **the same source prompts are used for both generators**, then prompt clusters span both columns and the correct cluster bootstrap resamples prompt IDs *once* and carries all four cells along. Independent resampling ignores the positive between-column correlation and is therefore *conservative* (wider CI), so it is not invalid — but it is not what should be preregistered, and it wastes precision the design paid for. **[SIGN-OFF]** whether both columns share prompts (recommended: yes); if yes, add a joint-resampling variant before Phase E.

**(g) One test is non-diagnostic.** `test_bootstrap_resamples_prompts_not_texts` asserts `width(clustered) >= 0.95 × width(unclustered)` on data with no within-prompt correlation, so it passes whether or not clustering works. Make the synthetic items within a prompt correlated and assert strictly wider.

**(h) No test drives `chat()` end-to-end against a mocked transport** to prove `BudgetExceeded` is raised with zero requests sent. The unit tests test `BudgetGuard.check` in isolation. Phase B exercised the happy path only.

**(i) Sign convention of the interaction: correct.** `(M→M − N→M) − (M→N − N→N)` at `stats.py:166,198–200`, matching council Part 4 Q1 literally, with a test that a pure capability effect cancels (`test_interaction_cancels_a_pure_capability_effect`).

**(j) Six cells expressible from config: correct.** `config.ALL_CELLS`, `M_ROW`, `N_COLUMN`, `CELL_RUN_ORDER` (M-row first), `ACTIVE_CELLS = None` with a runner that refuses to start (`run.py`, `config.active_cells()`), and a test asserting nothing is locked.

**(k) Missing entirely (not claimed done, but needed before any data):** `personas/generate.py`; the calibration `items.json` / `run.py` / `analyze.py`; the scoring join (predictions + labels → per-item correct maps) in `analysis/`; any orchestration entry point for a phase; a check that a self cell's generator provider/quantization equals its predictor's (the "same weights" validity condition is currently enforced only by M and N being one `ModelSpec` each — nothing asserts it against the logged `provider_returned` per item).

### 1.3 Research decisions that have leaked into code or drafts

These are not bugs; they are places where code or a draft is *ahead of `02`*. Each is marked **[SIGN-OFF]** because 02 must say it first.

| Where | What it encodes | Status in `02` |
|---|---|---|
| `config.N_PER_CELL_LADDER = (500, 400, 300)`, `WORKING_GUARD_USD = 7.50` | Council Q3 | Not in 02 |
| `config.GENERATION_TEMPERATURE = 1.0` | Generation temperature | Silent in 02 and in the council verdict. Both personas from every prompt at temperature 0 gives one deterministic text per (prompt, persona) and a cleaner "same weights" story; temperature 1.0 gives variety but adds sampling noise to the hidden property. **Decision needed.** |
| `predict/prompts.py:35` — "a response someone wrote to an **advice dilemma**"; `PREDICTOR_SYSTEM` | Persona domain and predictor wording | Persona design is Unresolved row 2 in 02. The template also has to be frozen as a stimulus. |
| `baseline/surface.py:149–155` — `voids_column` at 0.58 | Council Q6 threshold | Not in 02 (docstring admits it) |
| `config.MALFORMED_RETRIES = 1`, exclusion rule | Council Q3 malformed rule | Not in 02 |
| `04_report_draft.md` (264 lines) + `Digital_Minds_Sprint_Report_DRAFT.docx` | Presents crossed design, values-ordering personas, DeepInfra pair, `D ≤ 58%`, and **F = `deepseek-chat-v3-0324`** as the study | None of it is in 02; and **F contradicts `04_model_verification.md`, which recommends Mistral-Small on lineage/cost grounds**. The draft is a useful template but reads as if the design were locked. It must be re-derived from 02 once 02 is signed, not the other way round. It also collides with the `04_` number. |
| `CLAUDE.md` "Project purpose" | States the crossed design and value-ordering personas as the project | Softened by its own "Authority" section, but the purpose paragraph asserts a design 02 hasn't adopted |

---

## 2. Where the project actually stands

**Calendar.** The report draft says "Digital Minds Research Sprint, 14–16 August 2026". Today is 15 August. **The council's schedule ("Day 1: verification 09:00 … GO/FALLBACK by 10:00 Day 2, main run Day 2 morning, Day 3 code-free") is already a day behind:** verification landed on what the report calls Day 2. I cannot verify the time of day or the submission deadline; whoever can should re-anchor the schedule before anything else in §5 is scheduled.

### Original phases (02)

| Phase | Status | Blocked on |
|---|---|---|
| 1A Literature grounding | **Done** | — |
| 1B Design audit | **Done as of pre-council; 02 not yet updated with the council verdict** | Human sign-off (§3) |
| 1C Calibration probe | **Not started.** No task chosen, no items, no code (`calibration/__init__.py` is a docstring) | Task decision **[SIGN-OFF]**; then authoring + ~100 lines of code |
| 1D Persona pilot | **Not started.** No persona pair text, no dilemma prompts, no `generate.py`, band not locked | Persona pair + band **[SIGN-OFF]**; Hermes-3 enactment smoke test (§4); authoring; code |
| 1E Implementation | **Scaffold ~50 %.** Done: client, guard, checkpoint, predictor prompt + cell runner, baseline D, bootstrap/McNemar/interaction. Missing: generation, calibration, scoring join, orchestration, provider-equality assertion, concurrency | Nothing research-side; ~half a day of engineering |
| 2 Main data collection | Not started | 1C, 1D, 02 freeze |
| 3 Analysis / write-up | **A full report template exists prematurely** (`04_report_draft.md`, docx) | Data; and re-derivation from a signed 02 |

### Council plan A–F

| Step | Status |
|---|---|
| A Hygiene + scaffold | Done (with the gaps in §1.2) |
| B Verification | Done; $0.0074; tier-(i) pair found; ASSUMPTIONS 1,2,4,6,7 verified, 3 partial, 5 falsified for Gemini only, **8 untested (critical), 9 untested (Phase C), 10 untested (Phase D)** |
| C Calibration | Blocked: task **[SIGN-OFF]**, models not transcribed to `config.py` (blocked on 02), code not written |
| D Pilot | Blocked: persona pair + band **[SIGN-OFF]**, generation code, and the Hermes-3 question |
| E Main run | Blocked on C, D, and 02 frozen as preregistration |
| F Write-up | Template drafted early; must not drive design |

`git` state: only the four original files are tracked; everything since (code, docs, data, `.gitignore`) is untracked and uncommitted. Nothing is lost, but the reproducibility record depends on a commit that has not happened; **the stimulus-freeze commit hash the council wants cannot exist until someone commits.** `.claude/scheduled_tasks.lock` exists — I did not open it and cannot say what, if anything, is scheduled.

---

## 3. The gap between `02` and the council verdict

`02` has **no** "Post-Council Locked Decisions" section; none of Part 4 has been applied. Every edit Part 4 calls for, split as asked:

### (a) Mechanical transcriptions — wording already written in transcript Part 4; paste once the team accepts the verdict as a whole

1. Main Experiment Scope — bullets 1, 2, 5 replaced (crossed control, n text, cell run order).
2. Statistical Analysis — primary interaction contrast + five secondary contrasts + D per column + log-odds/McNemar.
3. Decisions Already Locked #1 — reworded so N→N is a control cell, not a new predictor.
4. New Locked #5 — provider pinning as a validity condition; abort-and-resume; retries never change model ID.
5. Locked #3 — append: generator identity withheld; option order counterbalanced and logged; position-bias check reported.
6. Condition B — reworded to "verifiably shares base weights … also serves as the second target column."
7. Research Question one-sentence form — "residual … after a tier-matched sibling and a capability control."
8. Fallback — replaced by the 3-level ladder.
9. Unresolved row 6 (schedule) and Ubayd's responsibilities sentence — **but see §2: the dates in the council's text are already stale and need re-anchoring, so this one is only half mechanical.**
10. Unresolved row 1 — the tier ladder / verification checklist wording (now satisfied by 04).
11. Power / SESOI paragraph — the wording exists, **but the numbers inside it are a decision (below).**

### (b) Genuine decisions still needing human sign-off

Your list of four is right and incomplete. Confirmed:

1. **Crossed 2×2 vs. M-row as the pre-registered primary.** Council recommends crossed with M-row as fallback; 02 says one target. **Open — and conditional on §4's Hermes result.**
2. **Persona pair.** Council recommends the *dimension* (values-ordering: autonomy vs. long-term welfare) but the clauses, the scaffold, the generation prompt, and the source dilemma prompts do not exist. This is a decision *and* an authoring task.
3. **Pilot feasibility band.** Council proposes Self 60–80 % AND D ≤ 58 % per column on ≥ 80 items, with a selection rule among pairs. Not in 02. (Recommend writing "point estimate" explicitly — at 80 items D's SE is ~5.5 pp.)
4. **Calibration probe task.** The council did **not** decide this (it was outside Q1–Q7). Dimension, item source, count (30 vs 50), and the Δ criterion are all open. Recommend the Δ rule be "point estimate Far < Near" with the CI reported, not "CI excludes zero" — at 50 items the paired SE on Δ is ~8 pp and a CI rule fails on noise.

Additional open decisions the council or verification surfaced:

5. **Model IDs into `config.py`** — M and N are effectively settled by 04 (only tier-(i) pair that passes), but **F is genuinely open: Mistral-Small (04's recommendation) vs. DeepSeek-V3 (the report draft's choice).**
6. **n per cell and the ladder shape** — see §4; the council's numbers were computed at 5–17× the real price.
7. **SESOI values** (5 pp simple / 8 pp interaction) — also price-dependent; see §4.
8. **Generation temperature** (0 vs 1.0) — silent everywhere; encoded as 1.0 in config.
9. **Same source prompts for both columns, and therefore joint vs. independent prompt resampling** — silent; code assumes independent.
10. **Malformed-output and refusal/half-enactment exclusion rules**, label-blind, fixed before the pilot.
11. **Who authors how many source prompts, and how they are QC'd** — the council's "Jaswin authors ~40" does not scale to 250–500; they need to be generated (Claude Code, no OpenRouter cost) and human-screened.
12. **The predictor prompt template and system prompt** as frozen stimuli (currently in `prompts.py`).
13. **What to do if Hermes-3 fails as a generator but passes as a predictor** (§4) — decide the branch now, not after seeing the numbers.

---

## 4. Verification findings that change the plan

### 4.1 Hermes-3 and ASSUMPTION 8

**What was actually shown.** Hermes-3-70B ignored "Reply with the single word OK" and rambled on all ten bare re-alias prompts, but returned a clean letter on 10/10 structured A/B trials — where the trial was "Which is larger? A: a cat B: a bulldozer" with a system prompt. That is evidence it can *answer a short forced choice*. It is not evidence that it can (i) hold a persona system prompt through a 150–250-word dilemma answer without refusing, breaking character, or narrating the instruction, or (ii) return a clean letter when the user turn is a 300-token text plus two clauses. Both halves of assumption 8 are open, and the two halves have different consequences.

**Cheapest test that resolves it (recommended first action, §6).** ~$0.02, ~30 minutes once `generate.py` exists in minimal form:
- 10 draft dilemma prompts × 2 draft persona clauses × {Llama-3.1-70B, Hermes-3-70B} = **40 generation calls** (~250 in / 250 out tokens each; ≈ $0.006).
- Score each output blind for *usability only*: non-refusal, in-format, does not name the value, on-topic. Pass criterion is the council's own > 90 % usable — write it down before running.
- Then run **both** M and N as predictors on all 40 items with the *actual* `PREDICTOR_TEMPLATE` (80 calls; ≈ $0.01) and record **malformed rate only**.
- **Seal the accuracies.** Do not read Self/Near accuracy from this run: the feasibility band must be fixed before the pilot, and 40 items is too few to mean anything anyway. Log them, do not look. Exclude these 10 prompts from the main stimulus set.

**If it fails, by branch:**
- *Hermes fails as generator, passes as predictor* → the N column cannot be built. Level 2 of the ladder (M-row only: M→M, N→M, F→M) with the tier-(i) pair intact — the Near-Self *predictor* still verifiably shares base weights, which is more than any published black-box design has. The capability confound returns as the headline limitation. **This is the branch to pre-decide [SIGN-OFF #13].**
- *Hermes fails both* → the tier-(i) pair is dead. Fallback pair is tier-(ii) `gpt-4o-2024-08-06` + `gpt-4o-2024-11-20`: passes every mechanical check but (a) its re-alias check was never run and must be, (b) quantization is unstated, and (c) at $2.50/$10 per M the crossed design at 500/cell costs roughly $5–7 — inside the ceiling, but it would trigger the n step-down and it forfeits the "weights verifiable from a model card" claim.
- *Passes* → proceed; the smoke run doubles as the shakedown of `generate.py` and the predictor path.

### 4.2 Prices are 5–17× lower than planned; the n ladder is the wrong shape

At verified prices (M $0.40/$0.40, N $0.70/$0.70, F $0.094/$0.25 per M tokens), assuming ~450 tokens per generation call and ~400 input tokens per prediction call:

| Design | n per cell | Gen calls | Pred calls | Approx. cost |
|---|---|---|---|---|
| Crossed, 6 cells | 500 | 1,000 | 3,000 | **≈ $0.75** |
| Crossed, 6 cells | 1,000 | 2,000 | 6,000 | **≈ $1.5** |
| Crossed, 6 cells | 1,500 | 3,000 | 9,000 | ≈ $2.3 |
| + calibration 50×3, pilot ≤ 3 pairs, 10 % retries | | | | + ≈ $0.2–0.4 |

Budget cannot bind at any n a 3-day sprint can *author*. So:

- **The 500 → 400 → 300 ladder was designed for a cost trigger that will never fire.** Its trigger should become **stimulus supply and wall-clock**: how many QC-passed source prompts exist at the freeze, and how long the runner takes (see §1.2(e) — make it concurrent).
- **What more n buys, at p ≈ 0.65 (95 % CI half-widths, paired ρ 0.3–0.5):**
  - 500/cell: simple contrast ±4.2–4.9 pp; interaction ±5.9–7.0 pp (council's numbers, confirmed).
  - 1,000/cell (500 prompts × 2 personas): simple ±3.0–3.5 pp; **interaction ±4.2–5.0 pp — a 5 pp SESOI becomes excludable for the interaction**, which the council said "no n the budget plausibly buys" could do. It was right at $2/$12; it is wrong at $0.40.
- **Recommendation for sign-off [#6, #7]:** re-anchor to **target 1,000/cell (500 prompts), floor 500/cell**, single SESOI of 5 pp for both simple and interaction contrasts *if* 1,000 is reached, otherwise the two-tier 5/8 pp. The binding question is whether ~500 usable dilemma prompts can be generated and screened before the freeze; that is a Claude Code task (free), not an OpenRouter one, and it is the real Day-2 bottleneck.

---

## 5. The path to starting data collection

Ordered. **R** = research decision (humans), **E** = engineering, **A** = authoring. Cost is OpenRouter spend; "blocks" is what cannot start until this is done.

| # | Step | Produces | Who decides / does | Cost | Blocks |
|---|---|---|---|---|---|
| 0 | Re-anchor the schedule to the real deadline (§2) | A dated plan replacing council row 6 | R — both | $0 | Everything's ordering |
| 1 | **Hermes-3 enactment smoke test** (§4.1): minimal `generate.py`, 10 draft dilemmas, 2 draft clauses, 40 gen + 80 pred calls, usability + malformed rate only, accuracies sealed | Assumption 8 answered; `generate.py` shaken down | E (build) + R (pass criterion > 90 % written first) | ≈ $0.02 | Decision #1 (crossed vs M-row), decision #13 |
| 2 | **02 sign-off session**: apply Part 4 (a) mechanically; decide (b) 1–13, conditional on step 1's branch; add `## Post-Council Locked Decisions` | 02 as pre-registration draft | R — both | $0 | Config transcription, all phases C+ |
| 3 | Transcribe M/N/F into `config.MODELS`; set `ACTIVE_CELLS`; set n ladder; set generation temperature; delete `voids_column` hard-code or point it at 02's value; fix `PREDICTOR_TEMPLATE` domain wording if 02 changed it | Config matching 02; tests updated (`test_no_design_is_locked_in_code` must flip to assert the *locked* set) | E | $0 | C, D, E |
| 4 | **Author + freeze stimuli**: 50 calibration items on the chosen dimension with A/B randomisation; ≤ 3 candidate persona-clause pairs; ~500 dilemma prompts (LLM-generated in Claude Code, human-screened for genuine autonomy/welfare conflict); the predictor template. **Commit** so a freeze hash exists; write `FREEZE.md` with content hashes | Frozen stimuli + hash | A — Jaswin (personas/prompts), Ubayd (calibration) | $0 | C, D |
| 5 | Finish code: `calibration/run.py` + `analyze.py`; scoring join in `analysis/`; provider/quant equality assertion for self cells; thread pool in `run_cell`; joint-resampling interaction variant (if 02 says shared prompts); tests from §1.2(d),(g),(h) | Runnable pipeline | E — Ubayd (per 02 responsibilities) | $0 | C, D, E |
| 6 | **Phase C calibration**: 50 items × M, N, F; paired A_near, A_far, Δ with CIs; apply the pre-declared Δ rule; assumption 9 | `05_calibration_results.md`; F confirmed or swapped | E run; **R gate** (rule fixed in step 2) | ≈ $0.01 | E (main run) |
| 7 | **Phase D pilot**: screen ≤ 3 pairs × 40 items on M → winner × 80 items on M *and* N; Self on both columns; D per column (5-fold, grouped by prompt); apply band | GO / level 2 / level 3 recorded in 02 | E run; **R gate** (band fixed in step 2) | ≈ $0.10 | E |
| 8 | Freeze 02 as the preregistration (commit + hash); write the label-blind exclusion rules into it | Preregistration | R — both | $0 | E |
| 9 | **Phase E main run**: generation (both personas × every prompt × active columns, labels to `data/labels/` only) → predictions in `CELL_RUN_ORDER` → D per column; guard active; logs append-only | Data | E | ≈ $0.75–1.5 | Analysis |
| 10 | Analysis: cell accuracies, primary interaction (or M-row contrasts at level 2), secondary contrasts, McNemar, log-odds, D, calibration Δ, position-bias, cost record | Results | Both | $0 | Write-up |
| 11 | Re-derive `04_report_draft.md` from the signed 02 and the results (fix F, remove any assertion 02 didn't make); rename to avoid the `04_` collision | Report | Both | $0 | Submission |

Gates that are **research decisions**: 0, 2, 6 (Δ rule), 7 (band), 8. Everything else is engineering or authoring and can proceed in parallel with the sign-off session once step 1 has run.

---

## 6. What I would do first, and why

**Run the Hermes-3 enactment smoke test (step 1) now — usability and malformed rate only, accuracies sealed — while the two of you hold the 02 sign-off session in parallel.**

Reason: it is the single cheapest fact (~$0.02, ~30 minutes) that collapses the largest branch of the decision tree. Whether the crossed design exists at all, whether the tier-(i) pair survives, whether F's price matters, and what n and SESOI to preregister all depend on whether Hermes-3 can enact a persona clause with > 90 % usable output. Deciding Q1 in 02 before knowing that means either deciding twice or deciding blind; the council's own "One Thing To Do First" was verification of the pair, and this is the half of that verification 04 could not do. Building the minimal `generate.py` for it is not wasted — it is the module Phase D and Phase E need anyway, and running it exposes the real predictor-prompt format on real-length inputs, which the Phase B "cat vs bulldozer" check did not.

Sealing the accuracies keeps the feasibility band honest: nobody has looked at a Self number before the band is written down.
