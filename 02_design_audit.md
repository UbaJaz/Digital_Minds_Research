# 02 — Experimental Design Audit

## Purpose

This document records the current state of the experimental design after Phase 1A (literature grounding, see `01_literature_grounding.md`) and the initial Phase 1B design audit. It captures what the source-of-truth document (`Track3_Strategy_Doc_Research_Focused.docx`) locks in, what remains genuinely open, and what this team must decide before Phase 1C (calibration probe design) and Phase 1D (hidden-property pilot design) can be written concretely rather than as placeholders.

**This is not yet a preregistration.** It is a snapshot of design status, meant to let anyone — including this team after a break — answer: where are we, what's decided, what isn't, what's next.

---

## Research Question

*Does Self-Advantage in Behavioral Self-Prediction Scale With Model Similarity? A Similarity-Controlled Test of Privileged Access.*

One-sentence form (source of truth): when predicting a hidden property of a model's own output, is self-prediction accuracy explained by the same similarity effect that governs near-self and far-self prediction, or does self show an advantage beyond what similarity predicts?

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
A different checkpoint or version in the same model family predicts the same property from the same text — the closest matched comparison available without access to the target's own weights.

### C — Far-Self
A model from a different provider or family predicts the same property from the same text — the low-similarity anchor.

### D — Statistical Baseline
A simple heuristic on surface text features. **D is exclusively a surface-leakage sanity check — it is never a point on the similarity axis and must never be used as evidence for or against a self-advantage.** This is a locked constraint from the source of truth, not a stylistic preference.

---

## Hidden Property

### Primary
Which of two subtly different underlying personas produced the response. Chosen because it should be more resistant to trivial surface-style detection than a purely stylistic manipulation would be.

### Fallback
Sampling temperature bucket.

**Why temperature is fallback only:** Song, Lederman, Hu & Mahowald's "Privileged Self-Access Matters for Introspection in AI" already ran a closely related temperature self-reflection paradigm and found a null result driven by a specific, identified confound (models inferring temperature from prompt style rather than genuine access to the sampling parameter). Using temperature as our primary property risks landing close to a replication of an already-published null, with a known leakage path. Persona is intended to avoid that specific confound; this is a design hypothesis, not yet validated.

---

## Similarity Calibration

The source of truth requires that near-self and far-self similarity to the target model be **empirically measured**, not assumed from provider or model-family labels — this directly addresses one of the most-exposed weaknesses identified in earlier design review (an assumed provider-based similarity ranking has no ground truth). The intended method is a calibration probe measuring how often each comparison model agrees with the target model on a task unrelated to the hidden-property test, following the "empirical similarity" approach used in Song, Hu & Mahowald (2025).

**The specific calibration task is not yet chosen.** This document does not select one — that is Phase 1C, blocked on target-model selection (see Unresolved Decisions below).

---

## Main Experiment Scope

- One target model.
- Approximately 250–300 trials per condition.
- One near-self model.
- One far-self model.
- A second target model only as a stretch goal, attempted after the core comparison and its interpretation are secured.
- **No pooling of multiple target models to manufacture additional regression points.**
- **No three-point regression.** This was explicitly identified as a design flaw in earlier review (a line through three points fits by construction and does not constitute a real statistical test) and was replaced with the pairwise-comparison structure below.

---

## Statistical Analysis

Three pre-registered pairwise comparisons:

1. **Self vs. Near-Self**
2. **Near-Self vs. Far-Self**
3. **Self vs. Far-Self**

For each: compute the accuracy difference, estimate a bootstrap confidence interval on that difference, report it as an effect size, and interpret the result substantively rather than relying on a bare significance threshold.

**Condition D's role:** reported entirely separately, as a floor/ceiling check on whether the hidden property is recoverable from surface style at all. It is never folded into the similarity argument or the pairwise comparisons above.

---

## Fallback

If the first day's feasibility check shows the hidden property is too easy or too hard to recover:

- Collapse to three conditions only: Self, Far-Self, Statistical Baseline.
- One target model.
- No Near-Self arm.
- No similarity-trend claim of any kind.
- Report three accuracy estimates with bootstrap confidence intervals, plus an honest account of why the fuller design wasn't reachable.

This fallback is a **predetermined research decision**, not an improvised response to a disappointing pilot result — deciding it now is itself part of the project's research discipline.

---

## Current Two-Person Responsibilities

### Ubayd
Experimental design, statistical reasoning, calibration probe design, bootstrap analysis, interpretation of outcomes, analysis and results writing, lightweight implementation once the design is locked.

### Jaswin
Literature grounding, hidden-property/task design, pilot design and feasibility judgment, plain-English framing, pitch preparation.

### Shared
Interpretation of results and final report writing are explicitly shared — not split so that one person only writes prose while the other only writes code.

---

# Decisions Already Locked

### 1. Core predictor structure
Exactly one Self condition, one Near-Self model, one Far-Self model, one statistical baseline. No additional predictors in the core experiment — adding more would reopen the "how many points" problem the source of truth explicitly closed by moving from a regression to pairwise comparisons.

### 2. Statistical approach
Python is the intended implementation environment. Analysis uses bootstrap confidence intervals on pairwise accuracy differences, not a significance-threshold-only approach.

### 3. Ground truth handling
Ground truth (which persona / which temperature bucket produced a given output) must be generated and stored programmatically, with strict separation between generation metadata and predictor inputs. No predictor — including Self — may ever receive the hidden label. This is required to keep any observed self-advantage attributable only to "which weights are predicting," not to an information leak.

### 4. Pilot ownership
Jaswin leads the hidden-property task design and the pilot feasibility judgment. The feasibility criteria themselves must be fixed **before** the pilot is run and observed — not chosen or adjusted afterward.

These are the team's current working decisions, consistent with the source of truth. Where the source of truth is silent on a specific number or task (see below), that silence is preserved here rather than filled in.

---

# Unresolved Decisions

| Decision | Why it matters | Current status | Owner |
|---|---|---|---|
| 1. Target model (M) | Determines whether a genuine same-family near-self checkpoint and a different-family far-self model are actually available via API | **Unresolved** — need to confirm real API access to all three roles before anything downstream can be concrete | Ubayd + Jaswin |
| 2. Exact persona design | The two personas must differ in a meaningful underlying property while minimizing trivial stylistic leakage; no concrete pair exists yet | **Unresolved** | Jaswin, with Ubayd input |
| 3. Calibration probe task | Determines what "unrelated task" is used to measure Target/Near-Self/Far-Self agreement | **Unresolved** — intentionally not chosen yet | Ubayd leads, Jaswin contributes |
| 4. Pilot feasibility threshold | Defines what accuracy range counts as too easy, feasible, or too hard for the hidden-property task | **Unresolved.** A ~55–75% band was discussed in earlier conversation as a candidate, but the source-of-truth document requires a predetermined threshold without itself locking a specific numeric range. **That 55–75% figure should not be treated as already approved** — it is a proposal, not a locked decision, until confirmed | Ubayd + Jaswin, with Jaswin owning the final pilot judgment |
| 5. API and compute budget | Bounds what's realistic for the ~250–300 trials/condition target in practice | **Unresolved** — need concrete provider access, cost ceiling, and rate limits | Ubayd |
| 6. Exact sprint schedule | Maps the three research phases onto actual available wall-clock time | **Unresolved** | Ubayd + Jaswin |

---

# What We Have Completed

## Phase 1A — Literature Grounding
**STATUS: COMPLETED**

Grounded the project in Binder et al. (2024), Song, Hu & Mahowald (2025), Song, Lederman, Hu & Mahowald (2025), and Lindsey (2026). Established what each paper actually demonstrates, what our project is and is not replicating, and the specific literature-based rationale for keeping temperature as fallback-only. Full detail in `01_literature_grounding.md`.

## Phase 1B — Experimental Design Audit
**STATUS: SUBSTANTIALLY COMPLETED**

Current design: four-condition structure (Self / Near-Self / Far-Self / Statistical Baseline), persona as primary hidden property, empirically-measured similarity via calibration probe, three pre-registered pairwise bootstrap comparisons, predetermined fallback plan.

Methodological weaknesses identified and already fixed: an unfounded three-point regression was replaced with pairwise comparisons; an assumed provider-based similarity ranking was replaced with a measurement requirement; the statistical baseline was explicitly excluded from any similarity claim; a same-weights-vs-same-episode distinction was made mandatory for the abstract, not just the limitations section; a predetermined fallback was written down instead of left to be improvised.

Unresolved decisions remain and are listed above. **The final experimental design is not yet frozen** — Phase 1C and 1D cannot be written concretely until target-model access, persona content, calibration task, and feasibility threshold are resolved.

## Phase 1C — Calibration Probe
**STATUS: NOT STARTED**

Reason: the target, near-self, and far-self models must be selected before the calibration task can be concretely specified.

## Phase 1D — Hidden Property Pilot
**STATUS: NOT STARTED**

Reason: the exact persona design and feasibility thresholds must be resolved first.

## Phase 1E — Implementation
**STATUS: NOT STARTED**

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

1. Confirm the target model and available APIs.
2. Identify viable Near-Self and Far-Self candidates.
3. Generate and evaluate several candidate persona pairs.
4. Define the criteria for selecting the persona pair.
5. Define a principled pilot feasibility threshold.
6. Then move into Phase 1C and design the calibration probe.

No implementation begins in this session either — its output should be a set of locked decisions, not code.
