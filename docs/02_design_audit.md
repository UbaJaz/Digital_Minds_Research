# 02 — Experimental Design Audit

## Purpose

This document records the current state of the experimental design after Phase 1A (literature grounding, see `01_literature_grounding.md`) and the initial Phase 1B design audit. It captures what the source-of-truth document (`Track3_Strategy_Doc_Research_Focused.docx`) locks in, what remains genuinely open, and what this team must decide before Phase 1C (calibration probe design) and Phase 1D (hidden-property pilot design) can be written concretely rather than as placeholders.

> **Revision 2026-08-15 (post-council).** The council verdict (`notes/council-transcript-2026-08-15.md` Part 4) has been applied below. Mechanical transcriptions of the verdict are in place; every item that is a genuine decision is collected in **Post-Council Locked Decisions** with a Confirmed column. All rows were confirmed on 2026-08-15; this document is now the locked design and is frozen as the preregistration at the freeze commit. Verification (`04_model_verification.md`) and the enactment smoke test (`06_hermes_smoke_test.md`) are complete.

**This is not yet a preregistration.** It is a snapshot of design status, meant to let anyone — including this team after a break — answer: where are we, what's decided, what isn't, what's next.

---

## Research Question

*Does Self-Advantage in Behavioral Self-Prediction Scale With Model Similarity? A Similarity-Controlled Test of Privileged Access.*

One-sentence form (post-council, replaces the source-of-truth wording, which overclaimed a "scale" with one Near and one Far): when predicting a hidden property of a model's own output, is there a self-prediction residual beyond what a tier-matched same-lineage sibling achieves, once the predictor's general classification ability is controlled by a crossed design?

*Original source-of-truth wording, retained for the record:* when predicting a hidden property of a model's own output, is self-prediction accuracy explained by the same similarity effect that governs near-self and far-self prediction, or does self show an advantage beyond what similarity predicts?

## Plain English Framing

Source of truth: "People treat an AI's self-report as if it knows something special about itself. This is a controlled test for whether that's actually true, or just an illusion created by the model being statistically similar to itself." This framing leads any pitch or write-up, before the Binder/Song literature grounding is introduced.

## Hypotheses

### H_similarity
Accuracy declines from near-self to far-self, and self falls on the same trend — no self-specific advantage beyond similarity.

### H_privileged
Self-prediction accuracy exceeds what the near-self → far-self trend would predict — a genuine self-specific residual.

---

## Current Experimental Conditions

### A — Self
The target model, in a fresh session with no memory of generating the text, predicts a hidden property of its own output.

### B — Near-Self
A same-lineage model at the same capability tier that verifiably shares base weights with the target (per model card) predicts the same property from the same text — and also serves as the second target column of the crossed capability control (see Main Experiment Scope).

### C — Far-Self
A model from a different provider or family predicts the same property from the same text — the low-similarity anchor.

### D — Statistical Baseline
A simple heuristic on surface text features. **D is exclusively a surface-leakage sanity check — it is never a point on the similarity axis and must never be used as evidence for or against a self-advantage.** This is a locked constraint from the source of truth, not a stylistic preference.

---

## Hidden Property

### Primary
Which of two personas differing in a **values ordering** (e.g., prioritise the person's autonomy / stated preference vs. their long-term welfare) produced the response to an advice dilemma in which the two values genuinely conflict. Same system-prompt scaffold, same length and format instructions; only the persona clause differs; the generation prompt forbids naming the value. **Both personas are generated from every source prompt** (topic balanced by construction; analysis pairs within prompt). Predictors receive the text plus the two persona clauses verbatim, in counterbalanced order, and are **not told which model generated the text**; the only self-specific channel is same-weights fit to own output distribution. Chosen over epistemic caution (leaks via hedge-rate, a Baseline D feature) and risk-tolerance (leaks lexically); risk-tolerance is the second candidate in the pilot screen. Exact clause wording is a Post-Council decision (row P10).

### Fallback
Sampling temperature bucket.

**Why temperature is fallback only:** Song, Lederman, Hu & Mahowald's "Privileged Self-Access Matters for Introspection in AI" already ran a closely related temperature self-reflection paradigm and found a null result driven by a specific, identified confound (models inferring temperature from prompt style rather than genuine access to the sampling parameter). Using temperature as our primary property risks landing close to a replication of an already-published null, with a known leakage path. Persona is intended to avoid that specific confound; this is a design hypothesis, not yet validated.

---

## Similarity Calibration

The source of truth requires that near-self and far-self similarity to the target model be **empirically measured**, not assumed from provider or model-family labels — this directly addresses one of the most-exposed weaknesses identified in earlier design review (an assumed provider-based similarity ranking has no ground truth). The intended method is a calibration probe measuring how often each comparison model agrees with the target model on a task unrelated to the hidden-property test, following the "empirical similarity" approach used in Song, Hu & Mahowald (2025).

**The specific calibration task is a Post-Council decision (row P8).** Whatever task is chosen: 50 frozen forced-choice items (30 minimum), A/B order randomised and frozen with the items, temperature 0, one-letter answers, paired analysis against Target's labels (A_near, A_far, Δ with bootstrap CIs). The calibration Δ is also the check on the distillation risk (council ASSUMPTION 9): if Far is not measurably further than Near, Far is swapped before the main run.

---

## Main Experiment Scope

- One target **lineage**: two same-lineage, tier-matched models — M (primary target) and N (Near-Self). Each serves as both generator and predictor in a crossed 2×2 capability control (cells M→M, N→M, M→N, N→N); Far-Self F predicts both columns (F→M, F→N). N-as-target exists solely to estimate the capability term. It is never pooled with M and never used as an additional similarity point.
- n per cell: **Post-Council decision (row P4)** — council proposed ~500 items per cell (250 source prompts × 2 personas per target) with 300 as the floor; verified prices make ~1,000 per cell affordable.
- One near-self model.
- One far-self model.
- Cell run order: M→M, N→M, F→M first, then M→N, N→N, F→N — the M-row design is complete before the control column starts, so the pre-registered fallback is always whole.
- **No pooling of multiple target models to manufacture additional regression points.**
- **No three-point regression.** This was explicitly identified as a design flaw in earlier review (a line through three points fits by construction and does not constitute a real statistical test) and was replaced with the pairwise-comparison structure below.

---

## Statistical Analysis

Pre-registered contrasts, each with an item-level paired bootstrap CI (resampling by **source prompt**, not by text; pairing holds within a target column only):

**Primary:** capability-controlled self-advantage = (M→M − N→M) − (M→N − N→N).

**Secondary:** (1) Self vs. Near-Self on M's outputs (M→M − N→M); (2) Near-Self vs. Far-Self on M's outputs (N→M − F→M); (3) Self vs. Far-Self on M's outputs (M→M − F→M); (4) N→N − M→N; (5) F→M vs. F→N as a Far-Self capability check.

Report all six cell accuracies with CIs; McNemar's test as a secondary check on each simple contrast; report the interaction on the log-odds scale alongside the difference scale. Interpret substantively, not by a bare significance threshold.

**Power and smallest effect of interest.** At p ≈ 0.65 and 500 items per cell, a paired simple contrast has a 95 % CI of about ±4–5 pp; the interaction (two columns) about ±6–7 pp. At 1,000 items per cell: ±3–3.5 pp and ±4–5 pp respectively. Smallest effect of interest (SESOI): **Post-Council decision (row P5)** — council proposed 5 pp for simple contrasts and 8 pp for the interaction at 500/cell; at 1,000/cell a single 5 pp SESOI is excludable for both. A null is reported as an equivalence bound ("effects larger than X excluded"), not as "not significant." Malformed outputs: one retry with the identical prompt; a still-malformed item is excluded listwise within its column and malformed rates are reported per predictor. Refusals or half-enacted generations are excluded by a label-blind rule fixed before the pilot (row P11).

**Whether both target columns share the same source prompts** is a Post-Council decision (row P7); if they do, the interaction bootstrap resamples prompt ids jointly across columns rather than independently.

**Condition D's role:** fit separately per target column, cross-validated (grouped by source prompt), reported separately, never on the similarity axis. D above the pre-declared leakage threshold (row P9) on a column voids the self-advantage claim for that column.

---

## Fallback

Predetermined ladder, fired by the pilot gate (the earlier single-step collapse to Self / Far / D was removed because it reintroduced the capability confound in full):

- **Level 1 (pilot passes on M and N):** crossed design as specified.
- **Level 2 (passes on M only, or the N column cannot be run in time):** the M-row design only — Self, Near-Self, Far-Self, D on M's outputs; the three pairwise contrasts; the capability confound stated as the headline limitation. No "weaker model as Target" hedge is used; the direction in which any tier gap biases the result is stated.
- **Level 3 (no persona pair passes on M):** switch the hidden property to sampling-temperature bucket with the same gate and design ladder; if that also fails, collapse to Self / Far-Self / D on M's outputs, report three accuracy estimates with CIs, no self-advantage or similarity claim of any kind, and an honest account of why.

At every level: no pooling of targets, no regression, D never on the similarity axis. This ladder is a **predetermined research decision**, not an improvised response to a disappointing pilot result.

---

## Current Two-Person Responsibilities

### Ubayd
Experimental design, statistical reasoning, calibration probe design, bootstrap analysis, interpretation of outcomes, analysis and results writing, lightweight implementation once the design is locked. Owns `client.py`, the run loop and the budget guard; calibration item authoring is done in parallel and slips before the pilot does.

### Jaswin
Literature grounding, hidden-property/task design, pilot design and feasibility judgment, plain-English framing, pitch preparation.

### Shared
Interpretation of results and final report writing are explicitly shared — not split so that one person only writes prose while the other only writes code.

---

# Decisions Already Locked

### 1. Core predictor structure
Exactly one Self predictor (M), one Near-Self (N), one Far-Self (F), one statistical baseline (D). No additional predictors. Each of M, N, F predicts two target columns (M's outputs and N's outputs); N→N is a control cell produced by an existing predictor, not an added predictor and not an added similarity point. Adding predictors would reopen the "how many points" problem the source of truth explicitly closed by moving from a regression to pairwise comparisons.

### 2. Statistical approach
Python is the intended implementation environment. Analysis uses bootstrap confidence intervals on pairwise accuracy differences, not a significance-threshold-only approach.

### 3. Ground truth handling
Ground truth (which persona / which temperature bucket produced a given output) must be generated and stored programmatically, with strict separation between generation metadata and predictor inputs. No predictor — including Self — may ever receive the hidden label. This is required to keep any observed self-advantage attributable only to "which weights are predicting," not to an information leak. No predictor is told which model generated the text; persona option order is counterbalanced and logged; a position-bias check is reported per predictor. Enforced in code: `predict/` cannot import `labels/`, item ids are label-free hashes, and a test asserts no label token in any predictor prompt.

### 4. Pilot ownership
Jaswin leads the hidden-property task design and the pilot feasibility judgment. The feasibility criteria themselves must be fixed **before** the pilot is run and observed — not chosen or adjusted afterward.

### 5. Provider pinning
Every call pins one provider with fallbacks disabled; M-as-generator and M-as-Self-predictor (and N likewise) must hit the identical provider and quantization — this is a precondition of the "same-weights" scope claim, not a hygiene item. Provider unavailable mid-run → abort and resume, never switch. Retries never change model ID. Per-call log (returned model, provider, tokens, cost, prompt hash, timestamp) and the stimulus freeze commit hash are part of the research record; the temperature-0 repeat-call agreement is reported as data (verified 20/20 on DeepInfra for both pair members, `04_model_verification.md`).

These are the team's current working decisions, consistent with the source of truth. Where the source of truth is silent on a specific number or task (see below), that silence is preserved here rather than filled in.

---

## Post-Council Locked Decisions

**STATUS: LOCKED 2026-08-15** — every row confirmed (see Confirmed column). **Gate satisfied: `config.py` may be transcribed from this table.** From this point this section, together with the sections it references, is the preregistration; changes after the freeze commit are logged as amendments below the table. Recommendations are the reviewer's, informed by the council verdict, `04_model_verification.md` and `06_hermes_smoke_test.md`.

| Row | Decision | Proposed value | Why | Confirmed |
|---|---|---|---|---|
| P1 | Pre-registered design | **Crossed 2×2 (Fix A) primary**; M-row design as the pre-registered Level-2 fallback; interaction primary, the three pairwise comparisons secondary on M's outputs; M-row cells run first | Council unanimous; capability confound is otherwise unaddressed; Hermes enactment verified so the N column is buildable | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P2 | M and N | **M = `meta-llama/llama-3.1-70b-instruct`, N = `nousresearch/hermes-3-llama-3.1-70b`**, both pinned DeepInfra, fp8 | Only tier-(i) pair passing every check; base weights confirmed (HF card: `Base model: meta-llama/Llama-3.1-70B`); 95 % usable / 0 % malformed in the smoke test | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P3 | F | **`mistralai/mistral-small-3.2-24b-instruct`** (DeepInfra fp8), with `deepseek/deepseek-chat-v3-0324` (SiliconFlow fp8) as the pre-declared swap if calibration Δ does not show Far < Near | 04's recommendation: different organisation, base and architecture family; cheapest; the report draft's DeepSeek choice is the alternative | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P4 | n per cell | **Target 1,000 per cell (500 source prompts × 2 personas), floor 500**; step-down trigger is stimulus supply / wall-clock, not cost (cost cannot bind at verified prices: ≈ $1.5 total) | Interaction CI ±4–5 pp at 1,000/cell makes a 5 pp SESOI excludable; council's 500/400/300 was priced at 5–17× the real cost | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P5 | SESOI | **5 pp for simple contrasts and for the interaction if n ≥ 1,000/cell; otherwise 5 pp simple / 8 pp interaction** | Council arithmetic, re-run at achievable n | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P6 | Generation temperature | **1.0** (as verified usable in the smoke test), logged per item; DeepInfra seed reproducibility unverified, so reproducibility rests on the logged texts, not on re-sampling. *Alternative:* 0 (deterministic, verified 20/20 on this provider) — cleaner "same weights" story, unverified for usability and may flatten persona differences | The council was silent; the smoke test only tested 1.0 | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P7 | Shared prompts across columns | **Yes** — the same source prompts are answered by both M and N; the interaction bootstrap resamples prompt ids jointly across columns | Same stimuli for both generators is the cleaner control and buys precision; requires a code change in `analysis/stats.py` before Phase E | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P8 | Calibration probe task | **50 frozen forced-choice items: two short paraphrases of the same sentence, "Which reads better, A or B?"** — subjective, unrelated to values/persona/identity, high disagreement potential; temperature 0; paired analysis. **Δ rule: point estimate A_near > A_far, CI reported** (a "CI excludes zero" rule at 50 items fails on noise: paired SE ≈ 8 pp) | Council did not decide it; a task with an objectively right answer would give ~100 % agreement and no discrimination | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P9 | Pilot feasibility band | **Per column on ≥ 80 items: Self accuracy 60–80 % AND Baseline D (5-fold CV grouped by prompt) ≤ 58 %, both as point estimates**; selection among ≤ 3 pairs: in-band on both M and N, then D closest to 50 %, then Self closest to 70 %; pass on M and N → level 1, M only → level 2, none → level 3 | Council Q6; "point estimate" made explicit because at 80 items D's SE ≈ 5.5 pp | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P10 | Persona pair | **Dimension: values-ordering (autonomy / stated preference vs. long-term welfare); risk-tolerance as the second screen candidate.** ≤ 3 candidate clause pairs written by Jaswin (drafts may be prepared in Claude Code), each ≤ 40 words, same scaffold, **avoiding the tokens "long-term", "well-being/wellbeing/welfare", "autonomy"** or with those tokens banned in the scaffold; D's feature set must include them | Council Q6 plus the smoke-test parroting warning | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P11 | Exclusion rules (label-blind) | Generation excluded if: < 60 words; list/heading formatting; refusal regex; names the principle (regex on clause tokens). Prediction: one identical retry, then listwise exclusion within column; malformed rate reported per predictor. Rules applied mechanically to text only, before any label is joined | Council Q3/Q7; matches the smoke-test rules already exercised | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P12 | Predictor prompt | Freeze `src/selfpred/predict/prompts.py` `PREDICTOR_SYSTEM` + `PREDICTOR_TEMPLATE` as they are (0 % malformed on both models at real length) | Verified in the smoke test | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P13 | Stimulus authoring | **~500 source dilemma prompts and the 50 calibration items are drafted with Claude Code (no OpenRouter cost) and human-screened** (each dilemma must present a genuine autonomy-vs-welfare conflict); the 10 smoke-test dilemmas are excluded | Council's "Jaswin authors ~40" does not scale to 500 | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P14 | Schedule | **Hard deadline 2026-08-16 23:59; internal target 2026-08-16 16:00** (video + polish after). Plan: 15 Aug — lock, stimuli, code, calibration, pilot, freeze commit, launch main run; 16 Aug morning — analysis, results doc, report; 16:00 — done. cut order if slipping: n 1,000 → 750 → 500; calibration 50 → 30; D reduced to length + TTR; then drop the N column (level 2) | The council's Day-1/2/3 text is already a day behind | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |
| P15 | Freeze commit | Before Phase C runs, `git add` + commit the repo state (code, stimuli, this document) so `FREEZE.md` can cite a commit hash | Nothing is committed yet; a hash cannot exist otherwise | **YES** — Jaswin, 2026-08-15 (all recommendations confirmed) |

Rows P1–P3, P9–P12, P15 were transcriptions of decisions the council effectively made or verification settled; P4–P8, P13, P14 were the team's judgement calls. All confirmed 2026-08-15.

### Amendments after lock

> **Confirmation status — first note (added 2026-08-16, no status changed by it; SUPERSEDED later
> the same day by the second note below, and retained verbatim as the record of where the project
> stood at that moment).** Rows P1–P15
> above carry an explicit dated human confirmation. The amendments below do **not**: their status
> lines read "proposed by Claude Code", "drafted in Claude Code", and/or "awaiting Jaswin's
> confirmation", and they are left exactly as written. The outstanding confirmations for A1 and
> A3–A8 are itemised in `notes/AUTHOR_CONFIRMATION_REQUIRED.md`, which is a register of what needs
> signing and is itself unsigned. A post-experiment forensic review (2026-08-16) is drafted as
> **A9** in `notes/A9_DRAFT.md`; it is **not** filed here, is **not** preregistered, and is **not**
> approved — filing it is an author decision.
>
> *(Both statements in that note have since been overtaken: every amendment now carries a dated
> confirmation, and A9 is filed below. `notes/A9_DRAFT.md` is now a pointer stub — the final A9
> record is `notes/A9_post_hoc_audit.md`.)*
>
> **Confirmation status — second note (added 2026-08-16, later the same day; this one does change
> the confirmation lines).** **Jaswin Chinthala** and **Ubayd Hattas** have now read amendments
> **A1, A3, A4, A5, A6, A7 and A8** as recorded below and confirm each of them as an amendment to
> the preregistration, made on the date recorded against it. They have also confirmed **A9** and
> directed that it be filed here. A **Confirmation** line has been *added* to each entry; **no
> original text — reason, disclosure, outcome or original status line — has been edited or
> removed**, and the "proposed by Claude Code" / "drafted in Claude Code" provenance stands exactly
> as first written.
>
> **What a confirmation does and does not mean.** It means: *"I have read the amendment as recorded
> here and I accept it as part of the research record, made on the date shown."* It does **not**
> convert any amendment into a preregistered decision. The chronology is unchanged and remains the
> thing to read: rows P1–P15 were locked **2026-08-15 before any main-experiment call**; A1 and A3
> follow the pilot; **A4 is a post-pilot substitution of the primary reported estimand**; A5–A7
> follow A4; **A8 introduces the self-prediction probe** that supplies the report's headline
> positive result; and **A9 is a post-hoc audit of already-collected data, declared in advance of
> nothing**. Two items in `notes/AUTHOR_CONFIRMATION_REQUIRED.md` remain **open and are not resolved
> by these confirmations**: who screened `VO-D`/`VO-E` and when, and the reason for the sample-size
> step-down (no reason has been located, and none has been invented).

- **Pilot gate (2026-08-15, Phase D):** Level 3: no pair in band on M — temperature fallback would be next; NOT run in this session (see 02 Fallback). Winning pair `None` (see `08_pilot_results.md`).

- **Pilot gate (2026-08-15, Phase D):** Level 3: no pair in band on M — temperature fallback would be next; NOT run in this session (see 02 Fallback). Winning pair `None` (see `08_pilot_results.md`).

- **A1 — Fourth persona pair `VO-D` on a style-equalising scaffold (2026-08-15).**
  **What changed:** row P10's "≤ 3 candidate clause pairs" is extended to four. `VO-D` keeps the
  locked values-ordering dimension; what changes is the *generation scaffold*, which is now
  specified per pair. `VO-D`'s scaffold fixes the response at four sentences / 85–105 words in a
  fixed rhetorical skeleton (recommendation → one supporting reason → **one drawback of the
  recommended course** → one next step) and instructs the generator not to hedge.
  **Reason:** VO-A/B/C failed the gate on the Baseline-D leakage criterion in 6 of 6 columns
  (D = 0.588–0.766) while Self was *in band in 5 of 6 columns* (0.600–0.744). The design failed on
  stimulus style, not on model capability. Baseline D's feature set contains no bag-of-words
  features — it measures length, sentence count, hedge rate, modal rate, sentiment balance and
  second-person rate — so the leak is carried by exactly those, and the fixed skeleton equalises
  each of them across the two personas (in particular, requiring *both* personas to state a
  drawback removes the sentiment asymmetry that let D separate them). What remains different is
  which consideration governs, which is semantic; since D is cross-validated grouped by source
  prompt, it cannot exploit prompt-specific content.
  **What did NOT change:** the band (Self 60–80 % AND D ≤ 58 %, point estimates, ≥ 80 items per
  column), the selection rule, the fallback ladder, M/N/F, n, SESOI, the contrasts, the predictor
  prompt (P12), the exclusion rules (P11), and D's feature set. `VO-D` is screened by the same
  fixed rule as the other three, and **all four pairs are reported** in `08_pilot_results.md`
  whatever the outcome.
  **Disclosure:** this is a second pass at the pilot after seeing the first pass fail. It is
  recorded here rather than silently absorbed, and the write-up must state that the reported pair
  was chosen on the second attempt under an unchanged, pre-registered band.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** drafted in Claude Code under P10 ("drafts may be prepared in Claude Code") and
  P13 (Claude-drafted, human-screened). **Awaiting Jaswin's screening sign-off.**
  **Stop rule:** if `VO-D` also fails on M, no further pairs are written — the project takes the
  Level-3 branch and reports the pilot itself as the finding.
  **Outcome (2026-08-15):** `VO-D` **failed on both columns** — M: Self 0.500, D 0.325;
  N: Self 0.478, D 0.597. The scaffold did what it was designed to do (D fell from 0.588–0.766 to
  0.325 on M, i.e. the surface leak was closed) but Self fell to chance with it. **The stop rule
  fires: no fifth pair.** Gate remains Level 3, winner `None`.
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. A1 remains a **second pass at the pilot written after seeing
  VO-A/B/C fail**, not a preregistered decision. **Still open, and not resolved by this
  confirmation:** the P10/P13 screening of the `VO-D` clause pair and scaffold is not dated and no
  screener is named — see `notes/AUTHOR_CONFIRMATION_REQUIRED.md` §2.2.

- **A3 — Level-3 branch taken: no main run; the pilot is the result (2026-08-15).**
  All four pairs failed the pre-registered band, so there is no validated hidden property and
  Phase E is not run. The locked ladder's next rung is the sampling-temperature property; it is
  **not** taken, for a reason the pilot itself supplies: the temperature paradigm's known
  confound (Song, Lederman, Hu & Mahowald — models inferring temperature *from prompt style*) is
  the same surface-leakage failure that killed all four persona pairs here, so it is predicted to
  fail the identical D check while costing the remaining sprint time. Instead the four-pair pilot
  is reported as the primary result (`09_pilot_finding.md`), which is supported entirely by data
  already collected under the pre-registered band.
  **Consequence for claims:** no self-advantage, similarity or privileged-access claim of any
  kind is made. The reported result is about the *recoverability of the hidden property*, and the
  self-vs-other comparison was never reached — `VO-D` was run only on the Self cells (M→M, N→N),
  never on N→M or F→M, so nothing here speaks to self-versus-other prediction.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** taken under the stop rule declared in A1 before `VO-D` was run. Awaiting Jaswin's
  confirmation.
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. A3 is confirmed **as a decision that was taken and then reversed
  the same day by A4** — it is part of the record, not a description of what the study finally did.
  No proposer was recorded for A3 at the time and none is being supplied now.

- **A4 — Crossed design run on TWO stimulus sets as a leakage manipulation (2026-08-15).**
  **What changed:** A3 said no main run. That is reversed: the crossed 2×2 *is* run, but on two
  stimulus sets rather than on one "winning" pair, because the pilot handed us something better
  than a pair that passes the band — a pair that leaks (`VO-C`, D = 0.650 on M) and a pair that
  does not (`VO-D`, D = 0.325 on M). Surface leakage becomes a manipulated variable instead of a
  nuisance that disqualified the study.
  **Reason:** the locked design asks whether a self-prediction residual survives a capability
  control. The pilot says the recoverable signal is surface style. Running the crossed design on
  both sets tests the two accounts against each other directly: under the *style-matching*
  account (Song et al.) any self-advantage is a similarity artifact and should appear on `VO-C`
  and vanish on `VO-D`; under the *privileged-access* account (Binder et al.) a self-advantage
  should survive on `VO-D`, where no surface cue remains.
  **Pre-specified analysis, declared before the cells were run:**
  - **Primary:** the leakage contrast — [(M→M − N→M) on `VO-C`] − [(M→M − N→M) on `VO-D`].
    Style-matching predicts **> 0**; privileged access predicts **≈ 0**.
  - **Secondary (per stimulus set):** the capability-controlled interaction
    (M→M − N→M) − (M→N − N→N); the three M-column pairwise contrasts; all six cell accuracies
    with prompt-clustered bootstrap CIs; Baseline D per column; A-share position-bias per cell;
    within-prompt discrimination rate per cell.
  - CIs are prompt-clustered bootstrap resampling source prompts. Cross-set contrasts resample
    the two sets independently (different items). SESOI stays 5 pp simple / 8 pp interaction;
    at the n actually achieved a null is reported as whatever equivalence bound the data support,
    stated explicitly rather than rounded to the pre-registered figure.
  - **Interpretation guard:** if *no* predictor beats chance on `VO-D`, the interaction there is
    undefined and **no self-advantage claim is made in either direction** — the reported result
    is that removing surface style removes the recoverable signal for every predictor alike.
  **What did NOT change:** M/N/F and their pins, the predictor prompt (P12), exclusion rules
  (P11), generation temperature (P6), both-personas-per-prompt (P10), prompt-clustered
  resampling (P7), D's feature set, and the ban on D as a similarity point.
  **Disclosure:** this is a post-pilot decision made after seeing the pilot results, and the
  stimulus sets were selected *because* of their D values. The analysis above was written down
  before the new cells were run, and all six cells of both sets are reported whatever they show.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** proposed by Claude Code, run under time pressure on 2026-08-15. **Awaiting
  Jaswin's confirmation**, and the write-up states that this contrast was specified after the
  pilot rather than before it.
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. The authors confirm specifically, and this is the most consequential
  item they are confirming: **A4 is a post-pilot substitution of the primary reported estimand.**
  Row P1 made the capability-controlled *interaction* primary with the pairwise contrasts
  secondary; A4, written **after** the pilot results were known and after the stimulus sets had been
  selected **on their Baseline-D values**, promoted the raw M-target leakage contrast to primary and
  demoted the interaction. Confirming A4 accepts it as a recorded amendment; it does **not** make
  the leakage contrast preregistered, and it does not retire the original estimand. Both are
  reported in `10_report.md` §4.2, and the interaction — the estimand that was replaced — is the one
  that is positive on `VO-C` (+0.089 [+0.048, +0.131]). A4 also reversed A3 on the record, and the
  direction predicted for the new primary contrast was wrong.

- **A5 — Fifth pair `VO-E`: a second style-equalisation, changing exactly one sentence (2026-08-15).**
  **What changed:** a fifth clause pair is added. `VO-E` uses **the same two persona clauses as
  `VO-D`** and the same scaffold in every respect — four sentences, 85–105 words, no hedging,
  same opening move — except **sentence 3**, which becomes *"name one concrete cost of the
  alternative course"* in place of `VO-D`'s *"name one concrete drawback of the course you
  recommend."*
  **Reason:** `VO-D` succeeded at its stated purpose (D fell to 0.325 on M) but took Self to
  chance with it, and A4's clean condition was consequently uninformative — no predictor beat
  chance, so "no self-advantage" there could not be separated from "no readable signal for
  anyone." The diagnosis is that the drawback requirement forced *both* personas to undercut
  their own recommendation, converging them semantically while equalising them stylistically.
  Costing the *alternative* preserves the one-positive-one-negative balance that keeps Baseline
  D's sentiment, hedge and modality features level, without making each persona argue against
  itself.
  **This is a single-factor manipulation.** `VO-D` and `VO-E` differ in one sentence of the
  generation instruction and nothing else, so any difference between them is attributable to
  that instruction rather than to a bundle of scaffold changes.
  **Gate, fixed before running:** the unchanged band (Self 60–80 % AND D ≤ 58 %, point estimates,
  per column, ≥ 80 items). `VO-E` proceeds to the crossed 2×2 **only if** it separates Self from
  D on the M column — operationally, Self ≥ 0.60 and D ≤ 0.58. If it does not, no sixth pair is
  written and `VO-E` is reported as a second failed equalisation attempt, which strengthens
  rather than weakens the §4.3 claim.
  **Pre-specified analysis if it proceeds:** identical to A4, with `VO-E` entering the leakage
  contrast as a third stimulus set — the self-advantage on a set that is *readable but not
  style-readable* is the quantity A4 could not supply.
  **What did NOT change:** clauses, band, models, pins, predictor prompt, exclusion rules,
  D's feature set, resampling unit.
  **Disclosure:** this is a third pass at the stimulus design, made after seeing A4's clean
  condition come back uninformative. All five pairs are reported. The write-up states that
  `VO-E` was designed to fix a diagnosed failure of `VO-D`, and that its gate was fixed before
  it ran.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** proposed by Claude Code 2026-08-15. **Awaiting Jaswin's confirmation.**
  **Outcome (2026-08-15):** `VO-E` **failed the gate on M** — Self 0.519, D 0.506 (N column:
  Self 0.565, D 0.581). The style equalisation worked again (D at chance) but the signal did
  not return, so the A5 hypothesis — that `VO-D`'s drawback requirement was what converged the
  personas — is **falsified**. Two scaffolds differing in exactly one sentence produce the same
  collapse. The stop rule fires: no sixth pair, no crossed run on `VO-E`. This strengthens rather
  than weakens the §4.3 claim, because the inseparability of Self and D now rests on two
  independent interventions rather than one.
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. A5 remains a **third pass at the stimulus design, made after A4's
  clean condition came back uninformative**. **Still open, and not resolved by this confirmation:**
  the P10/P13 screening of the `VO-E` clause pair and scaffold is not dated and no screener is
  named. The report's own reading of A5 has since been qualified by A9 §2.1 — `VO-D` and `VO-E` are
  two instances of one failure mode rather than two independent tests, because both scaffolds also
  converged what the personas recommended.

- **A6 — Self-recognition probe on already-collected texts (2026-08-15).**
  **What changed:** a second hidden property is tested — *"did you write this?"* — on the
  `VO-C` main texts, which already contain an M-authored and an N-authored answer to every
  source prompt under the same persona clause. No new stimuli; no change to any locked rule.
  **Reason:** A4's clean condition could not separate "no privileged access" from "no readable
  signal for anyone." Authorship is a property that demonstrably *is* readable from these texts,
  so it supplies the missing test — and it is closer to what the self-report literature actually
  relies on than persona identification is.
  **Two framings were run, both pre-specified as exploratory:**
  (i) forced choice — two replies to one prompt, "one of these is yours, which?";
  (ii) single text, "did you write this reply? yes or no", scored as hit rate minus
  false-alarm rate so that response bias cancels.
  **Outcome — an elicitation failure, reported as such, not as a measurement.** In (i) M
  answered "A" on 99.0 % of trials and N answered "B" on 98.7 %; with counterbalanced order the
  resulting ~50 % is an artifact of position bias. In (ii) **both models answered "no" to 100 %
  of texts**, giving hit = false-alarm = 0 and discrimination exactly 0 by construction.
  Neither framing produced a content-dependent response, so **no self-recognition accuracy is
  claimed in either direction.** Meanwhile the surface baseline, fit to the same authorship
  discrimination with grouped cross-validation, reaches **0.831 on 791 texts** — the
  information is plainly present in the text.
  **Interpretation guard:** the honest statement is "we could not elicit a non-degenerate
  self-recognition response from either model," not "models cannot recognise their own text."
  Response distributions are reported alongside every accuracy figure.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** run 2026-08-15. **Awaiting Jaswin's confirmation.**
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. A6 remains a **post-hoc addition of a second hidden property
  (authorship) on already-collected texts**, and the authors confirm the "elicitation failure, not a
  measurement" reading as their own: no self-recognition ability is claimed or denied in either
  direction. No proposer was recorded for A6 at the time and none is being supplied now.

- **A8 — Self-PREDICTION reframing of the A6 probe (2026-08-15).**
  **What changed:** the self-referential probe is re-run as a *prediction* task instead of a
  *recognition* task. The model is given the original dilemma, the persona clause it was
  operating under, and two candidate replies — its own and the same-base sibling's — and asked
  which reply **it would produce**. Order counterbalanced; ground truth is which it actually
  wrote.
  **Reason:** A6's two framings both asked a memory question ("did you write this?") and both
  produced degenerate answers, so A6 measures nothing about self-knowledge. Binder et al.'s
  paradigm is prediction of one's own behaviour, not recall, and a model can answer it without
  any claim to memory of the episode. This is the construct the study set out to test, asked in
  the form the literature actually uses.
  **Pre-specified before running:** accuracy with prompt-clustered CI for M and N; **the answer
  distribution is reported with every accuracy figure, and an A-share above 0.9 or below 0.1 is
  declared degenerate in advance**, in which case no accuracy is claimed — the same rule that
  caught A6. Benchmark is the 18-feature authorship baseline (0.831). No direction is
  hypothesised: above chance would be a positive self-modelling result contradicting our persona
  findings; at chance with non-degenerate answers would be the clean null A4 could not supply.
  **What did NOT change:** models, pins, exclusion rules, resampling unit, D's feature set.
  **Disclosure:** this is the third framing attempted for the self-referential probe. All three
  are reported, including the two that failed. **No further framings will be tried** — searching
  prompt space until a framing yields a publishable number is precisely the practice this paper
  criticises.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** proposed by Claude Code 2026-08-15. **Awaiting Jaswin's confirmation.**
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. The authors confirm specifically: **A8 is the amendment that
  introduced the self-prediction probe**, it is the **third framing** of the self-referential probe
  after A6's two failures, and **the report's headline positive result (Hermes-3, balanced accuracy
  0.719, discrimination +0.437) therefore rests on an amendment, not on the signed
  preregistration.** A8 pre-specified — within an amendment, not in the frozen design — the point
  estimates, the answer-distribution rule and the 0.90/0.10 degeneracy threshold; reporting
  Llama-3.1's 0.897 A-share as "just under the threshold, rule did not fire" is the authors' chosen
  treatment. A8 did **not** pre-specify the confidence intervals or the length analysis in
  `10_report.md` §4.3; those are **post hoc** and are filed under A9 §3.4–§3.5. "No further
  framings" stands.

- **A7 — Dose-response: the crossed design on four stimulus sets spanning the leakage axis (2026-08-15).**
  **What changed:** the crossed 2×2 is additionally run on `VO-A` and `VO-B`, giving four
  stimulus sets whose Baseline D spans roughly 0.33–0.85. A4 compared two points (leaky vs
  clean); this makes leakage a graded independent variable.
  **Reason:** A4 established that the self-advantage is absent at both ends of the leakage axis,
  but two points cannot show a *relationship*. The quantity of interest is the
  capability-controlled **interaction** — the estimator the crossed design exists to provide —
  which was +0.089 [+0.048, +0.131] on the leaky set and −0.006 [−0.033, +0.021] on the clean
  one. If the interaction scales with D across four sets, then **the crossed design does not
  rescue a leaky stimulus set**: its headline estimator is itself contaminated by surface
  leakage. That is a methodological claim about the design most often proposed as the fix, and
  it is testable with stimuli already frozen.
  **Pre-specified analysis, declared before these cells were run:** for each of the four sets,
  the interaction and the simple self-advantage with prompt-clustered CIs, plotted against that
  set's Baseline D (per column and averaged). Primary summary: the slope of the interaction on D
  across the four sets, with the four points shown individually rather than only as a fitted
  line. **Four points is a small n for a slope and no significance claim is attached to it** —
  the four interaction estimates with their CIs are the result; the slope is descriptive.
  **What did NOT change:** models, pins, predictor prompt, exclusion rules, D's feature set,
  resampling unit, or any locked row.
  **Disclosure:** post-hoc in the sense that the leakage axis was discovered in the pilot; the
  analysis above was written before the `VO-A`/`VO-B` cells were run, and all four sets are
  reported whatever the shape.
  **Status (as originally recorded 2026-08-15; superseded by the Confirmation below, and kept
  verbatim):** proposed by Claude Code 2026-08-15. **Awaiting Jaswin's confirmation.**
  **Confirmation (added 2026-08-16; the status line above is unchanged):** confirmed as an
  amendment to the preregistration, made on 2026-08-15, by **Jaswin Chinthala** and
  **Ubayd Hattas**, 2026-08-16. A7 remains **post hoc in the sense recorded above** — the leakage
  axis was discovered in the pilot — and the "descriptive slope, four points, no significance claim"
  restriction stands and is honoured in `10_report.md` §4.2. The authors also confirm the scope
  correction A9 §2.2 attaches to A7: these are **four stimulus constructions on one shared
  200-prompt pool**, not four independent prompt samples.

- **A9 — Post-hoc verification and supplementary analyses after forensic review (2026-08-16).**
  **Read this first: A9 is not a preregistration and nothing in it was declared in advance of
  anything.** Every item was produced *after* all data collection ended (2026-08-15) and after the
  results were known, during an adversarial/forensic review of the completed project
  (`notes/council-transcript-2026-08-16-hostile-review.md`) and the fix passes that followed it.
  A9 is filed here because the authors directed that the review be part of the record — **not**
  because it acquires preregistered status by being filed. **No API call was made, no data was
  collected, and no point estimate, interval, sample count, model or statistical conclusion was
  altered in producing it.** The full record, with the definitional notes needed to reproduce every
  figure, is `notes/A9_post_hoc_audit.md`.
  **A9 divides into two kinds of item, and the division is the point of the amendment:**
  **(i) Discovered *after* the original experiment** — corrections to interpretation and scope, not
  to numbers:
  - **`VO-D`/`VO-E` manipulation-check finding** (descriptive). The style-equalising scaffolds did
    not only flatten surface style, they also converged what the two personas recommended:
    sentence-1 content-word overlap 0.364 (`VO-D`) and 0.343 (`VO-E`) against 0.082–0.107 for the
    original scaffolds, whole-text overlap unchanged at 0.17–0.21; in a hand-checked sample of 25
    `VO-D` prompts roughly four in five gave the same recommendation under both clauses.
    **No manipulation check was preregistered and none was run before the main run.** This is the
    single largest threat to the leakage interpretation and it was found by post-hoc inspection of
    our own texts.
  - **Shared-prompt-pool clarification** (descriptive/scope). The four sets are four stimulus
    constructions on **one shared 200-prompt pool**, not four independent prompt samples; the
    earlier phrase "four independent stimulus designs" overstated the replication and was retracted.
  - **What the crossed interaction does and does not remove** (conceptual). It cancels an additive
    predictor-level competence effect but **not** a predictor-by-column difference, and `VO-C`
    exhibits exactly such a difference — so `VO-C`'s +0.089 [+0.048, +0.131] cannot be separated by
    this estimator from a genuine self-advantage.
  - **The surface-leakage gate is necessary but not sufficient** (conceptual). `VO-D` passed on D
    and was still uninformative. `tools/surface_leakage_gate.py` was **not** changed.
  - **Post-hoc prompt-clustered intervals on the A8 self-prediction figures** (inferential,
    **POST HOC**). A8 pre-specified the point estimates and the degeneracy rule; it did **not**
    pre-specify these intervals. Hermes-3 balanced accuracy 0.719 [0.675, 0.762], discrimination
    +0.437 [+0.349, +0.519]; Llama-3.1 discrimination −0.107 [−0.166, −0.048]. **No point estimate
    changed** — all six match `data/results/selfpred_corrected.json`, which was not modified.
  - **Length-only rule, the paired comparison against it, and the own-not-longer residual**
    (inferential, **POST HOC**). "Pick the longer reply" scores 0.808 [0.768, 0.847] on exactly
    Hermes's 391 pairs; paired difference +0.095 [+0.036, +0.155] in the rule's favour (exact
    McNemar p ≈ 0.0018, b = 86 / c = 49); and on the 75 pairs where Hermes's own reply is **not**
    the longer one Hermes still discriminates at **+0.381 [+0.188, +0.566]**. The adopted reading is
    that a one-feature external rule beats Hermes *overall*, and that **length does not explain
    Hermes's model-specific residual** — not that length explains Hermes.
  - **Task-mismatch clarification between 0.719 and 0.831** (descriptive/conceptual). Hermes's probe
    is a zero-shot **pairwise** forced choice; the 18-feature classifier does **supervised
    single-text** authorship labelling. They are **different evaluation procedures**, so this is a
    criterion comparison and **no test is run between them**. No number changed.

  **(ii) Already present in the raw data or the design history, but outside the preregistered
  analysis** — surfaced by the review, not generated by it:
  - **Sample-size deviation.** Row P4 preregistered 1,000 items/cell (500 prompts × 2 personas)
    with a floor of 500; the main run used 200 source prompts for ≈400/cell, and `VO-D`'s N column
    retained 323. **No amendment authorises the reduction and no reason is recorded.** The deviation
    is disclosed **without retrospective justification, and no reason has been invented for it.**
  - **The A4 estimand substitution.** Recorded above under A4 and cross-referenced here; the
    replaced estimand (the interaction) is the one that is positive on `VO-C`, and the report says
    so rather than burying it.
  - **SESOI verification (no change).** Row P5 gives 5 pp for a simple contrast and, at n < 1,000
    per cell, 8 pp for the interaction. Achieved n ≈ 400/cell, so **5 pp simple / 8 pp interaction**
    are the applicable bounds; the report already stated this and no edit was required.
  - **Self-recognition → self-prediction framing history.** Three framings were run: A6's two
    recognition framings (elicitation failures) and A8's self-prediction framing. All three are
    reported.

  **What A9 does not do.** No re-bootstrap across the four sets; no manipulation-check statistics
  beyond the descriptive overlap figures; **no test between 0.719 and 0.831**; no further length or
  lexical analysis; no other new inferential analysis. Anything beyond the items listed above is a
  **new** analysis and belongs in a further amendment with its own date and status.
  **Open items A9 cannot resolve, carried forward:** the manipulation-check overlap figures and the
  §3.4–§3.5 analyses have no committed script (both are labelled in-text as computed ad hoc from the
  logged texts); the reason for the sample-size step-down is unknown and must not be reconstructed;
  and the `VO-D`/`VO-E` screening date and screener are unrecorded.
  **Status (as originally recorded 2026-08-16; superseded by the Confirmation below, and kept
  verbatim):** drafted by Claude Code 2026-08-16 during a forensic verification pass and two
  subsequent fix passes.
  **Confirmation (2026-08-16):** read and confirmed as a **post-hoc audit and supplementary-analysis
  amendment** by **Jaswin Chinthala** and **Ubayd Hattas**, 2026-08-16, who directed that it be
  filed here. Confirming A9 accepts it as a post-hoc record of the forensic review; it does **not**
  make any item in it preregistered, and it changes no result.

- **A2 — `load_column` prompt-subset filter (2026-08-15, bug fix, no research content).**
  `_pilot_column` loaded every item present in a column's checkpoint regardless of which prompts
  the call requested, so on a *resumed* run the 20-prompt screen silently read the 80 items the
  full pilot had since written. The screen numbers in the first `08_pilot_results.md` were
  therefore mislabelled (VO-B 80 items, VO-C 79, VO-A 40, all reported as a 40-item screen). The
  gate is applied at the full-pilot stage, so no gate outcome was affected. Fixed by passing an
  explicit `prompt_ids` filter.
  **Confirmation status (noted 2026-08-16):** A2 is a bug fix with no research content and **no
  research sign-off is requested for it**. It is listed here for completeness only.

**Confirmation summary (2026-08-16).** A1, A3, A4, A5, A6, A7, A8 and A9 are confirmed by
**Jaswin Chinthala** and **Ubayd Hattas** on 2026-08-16, each by an added Confirmation line that
leaves the original entry intact. A2 needs no sign-off. **Confirmation is not preregistration:**
P1–P15 were locked 2026-08-15 before any main-experiment call; A1/A3 follow the pilot; **A4 is a
post-pilot substitution of the primary reported estimand**; **A8 introduces the self-prediction
probe**; **A9 is post hoc throughout**. The register of what was outstanding, and the two items
that remain open, is `notes/AUTHOR_CONFIRMATION_REQUIRED.md`.


---

# Unresolved Decisions

| Decision | Why it matters | Current status | Owner |
|---|---|---|---|
| 1. Target model (M) | Determines whether a genuine same-family near-self checkpoint and a different-family far-self model are actually available via API | **Resolved (rows P2, P3).** Selection rule (council): (i) two post-trainings of one open-weight base at the same size, one pinnable provider at stated quantization; (ii) two dated snapshots of one closed model; (iii) same-family adjacent tier (crossed design only). `04_model_verification.md`: the only tier-(i) pair passing every check is `meta-llama/llama-3.1-70b-instruct` + `nousresearch/hermes-3-llama-3.1-70b`, both DeepInfra fp8; base weights confirmed from the Hugging Face card; enactment verified in `06_hermes_smoke_test.md` | Ubayd + Jaswin |
| 2. Exact persona design | The two personas must differ in a meaningful underlying property while minimizing trivial stylistic leakage; no concrete pair exists yet | **Resolved — row P10 (values-ordering); clause wording chosen from ≤ 3 candidates by the pilot screen.** Smoke test warning: clause vocabulary ("long-term well-being") is parroted into the text — candidate clauses must avoid natural advice vocabulary or the scaffold must ban it, and D's features must include those tokens | Jaswin, with Ubayd input |
| 3. Calibration probe task | Determines what "unrelated task" is used to measure Target/Near-Self/Far-Self agreement | **Resolved — row P8** (paraphrase-preference forced choice, 50 items, point-estimate Δ rule) | Ubayd leads, Jaswin contributes |
| 4. Pilot feasibility threshold | Defines what accuracy range counts as too easy, feasible, or too hard for the hidden-property task | **Resolved — row P9.** Council: joint per-column band on ≥ 80 items — Self 60–80 % AND Baseline D (5-fold CV, grouped by prompt) ≤ 58 %; selection among ≤ 3 pairs: in-band on both M and N, then D closest to 50 %, then Self closest to 70 %. Pass on M and N → level 1; M only → level 2; none → level 3. (The earlier 55–75 % figure is superseded.) | Ubayd + Jaswin, with Jaswin owning the final pilot judgment |
| 5. API and compute budget | Bounds what's realistic for the trial volume in practice | **Resolved.** OpenRouter sole provider; $10 hard ceiling; $7.50 working guard with per-phase sub-budgets in `config.py`. Verified prices: M $0.40/$0.40, N $0.70/$0.70, F (Mistral) $0.094/$0.25 per M tokens; crossed design ≈ $0.75 at 500/cell, ≈ $1.5 at 1,000/cell; DeepInfra 30-way burst 0×429. Spend to date $0.033. | Ubayd |
| 6. Exact sprint schedule | Maps the three research phases onto actual available wall-clock time | **Resolved — row P14 (deadline 16 Aug 23:59, target 16:00).** Council's plan (verification hour 1 → pilot afternoon → GO/FALLBACK by 10:00 next morning → main run that morning → final day code-free; cut order n → calibration 50→30 → D reduced → drop N column) is adopted in shape; the dates must be re-anchored to the real deadline | Ubayd + Jaswin |

---

# What We Have Completed

## Phase 1A — Literature Grounding
**STATUS: COMPLETED**

Grounded the project in Binder et al. (2024), Song, Hu & Mahowald (2025), Song, Lederman, Hu & Mahowald (2025), and Lindsey (2026). Established what each paper actually demonstrates, what our project is and is not replicating, and the specific literature-based rationale for keeping temperature as fallback-only. Full detail in `01_literature_grounding.md`.

## Phase 1B — Experimental Design Audit
**STATUS: COMPLETED — post-council revision applied and every Post-Council row confirmed 2026-08-15**

Current design: four-condition structure (Self / Near-Self / Far-Self / Statistical Baseline), persona as primary hidden property, empirically-measured similarity via calibration probe, three pre-registered pairwise bootstrap comparisons, predetermined fallback plan.

Methodological weaknesses identified and already fixed: an unfounded three-point regression was replaced with pairwise comparisons; an assumed provider-based similarity ranking was replaced with a measurement requirement; the statistical baseline was explicitly excluded from any similarity claim; a same-weights-vs-same-episode distinction was made mandatory for the abstract, not just the limitations section; a predetermined fallback was written down instead of left to be improvised.

Unresolved decisions remain and are listed above. **The final experimental design is not yet frozen** — Phase 1C and 1D cannot be written concretely until target-model access, persona content, calibration task, and feasibility threshold are resolved.

## Phase 1C — Calibration Probe
**STATUS: NOT STARTED**

Reason: the target, near-self, and far-self models must be selected before the calibration task can be concretely specified.

## Phase 1D — Hidden Property Pilot
**STATUS: NOT STARTED**

Reason: the exact persona design and feasibility thresholds must be resolved first.

## Phase 1B′ — Model verification and enactment smoke test
**STATUS: COMPLETED** — `04_model_verification.md` (311 calls, $0.0074, 11 models; tier-(i) pair found and pinnable) and `06_hermes_smoke_test.md` (120 calls, $0.026; Hermes-3 95 % usable as generator, 0 % malformed as predictor; accuracies sealed).

## Phase 1E — Implementation
**STATUS: SCAFFOLD ~60 %** — client with budget guard/pinning/logging, checkpoints, predictor prompt + cell runner, persona generation, baseline D, paired/interaction bootstrap exist (38 tests). Missing: calibration run/analyze, scoring join, generator-provider assertion, concurrency, joint-resampling variant. Nothing runs against the main design until this document's Post-Council table is confirmed and transcribed to `config.py`.

Reason: implementation is intentionally blocked until the experimental design is locked.

---

# What We Need To Do Next

```text
Phase 1A — Literature grounding
        DONE
          ↓
Phase 1B — Design audit
        DONE / OPEN DECISIONS REMAIN
          ↓
Resolve target model + API access
          ↓
Resolve persona candidates
          ↓
Resolve pilot feasibility criterion
          ↓
Phase 1C — Design and run calibration probe
          ↓
Phase 1D — Design and run hidden property pilot
          ↓
Predefined GO / FALLBACK decision
          ↓
Freeze experimental design / preregistration
          ↓
Phase 1E — Build lightweight implementation
          ↓
Phase 2 — Main data collection
          ↓
Phase 3 — Analysis
          ↓
Interpretation against Binder / Song
          ↓
Final report + pitch
```

> **The immediate next task is NOT coding. The immediate next task is resolving the model selection and remaining methodological decisions needed to make Phase 1C and Phase 1D concrete.**

---

## Immediate Next Session

The next research session should:

1. Confirm every row of the Post-Council Locked Decisions table — this is the sign-off session.
2. Transcribe M/N/F, active cells, n ladder, temperature into `config.py`; flip the "nothing locked" test.
3. Author and freeze stimuli (calibration items; ≤ 3 persona-clause pairs; source dilemma prompts) and **commit** so a freeze hash exists.
4. Phase 1C calibration → Phase 1D pilot → GO/FALLBACK recorded here → freeze this document as the preregistration → main run.
