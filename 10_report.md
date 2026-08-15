# Self-Prediction or Style-Matching? Surface Leakage as a Manipulated Variable in a Capability-Controlled Test of Privileged Self-Access

**Ubayd Hattas** — *⟦FILL: affiliation⟧*
**Jaswin Chinthala** — *⟦FILL: affiliation⟧*

With Apart Research · Digital Minds Research Sprint, Track 3 (Introspection & Self-Report Reliability), 14–16 August 2026

---

## Abstract

Arguments about model preferences and welfare lean on model self-report. We ask whether a model predicts its own outputs better than an equally-informed observer, using a crossed 2×2 on two models sharing a pretraining base so that general competence cancels. Across four stimulus designs, 24 cells and 9,269 trials, no positive self-advantage appeared in any design. Asked directly which of two replies it would produce, one model answered by position and showed no discrimination; the other discriminated genuinely (balanced accuracy 0.719). But an 18-feature logistic regression identifies the author of the same texts 83.1% of the time, so the one model that can predict itself is beaten by stylometry — failing the standard that introspection must outperform an equal-cost third party. We release the surface-leakage gate and response-bias check that make this testable, and recommend both as defaults.

**Keywords:** introspection, self-prediction, privileged access, surface leakage, capability control, digital minds

---

## 1. Introduction

People — including researchers — treat an AI's self-report as if it knows something special about itself. This is a controlled test of whether that is true, or an illusion created by the model being statistically similar to itself.

The assumption is load-bearing well beyond philosophy of mind. Most practical work on model preferences, distress signals and welfare runs through self-report. If a model's report about itself carries no epistemic advantage over what a comparably capable outside observer could infer from the same text, those methods are measuring something other than what they claim — and both over-attribution and under-attribution of moral significance become likelier.

The literature disagrees. Binder et al. (2025) finetune a model to predict its own hypothetical behaviour, find it beats a differently-trained model finetuned on the same ground truth, and read this as introspection. Song, Hu & Mahowald (2025) test prompted self-reports against directly measurable internal knowledge across 21 open models and find no residual once behavioural similarity is controlled. Song, Lederman, Hu & Mahowald (2025) run the closest black-box analogue — models judging their own generation temperature — and find a null driven by an identified confound: the models were reading the *style* of the text, information equally available to any observer.

Two problems block a clean black-box test, and this project ran into both.

The first is a **capability confound**. In every practical configuration the "self" predictor is also the largest model in the comparison and "near-self" is a smaller sibling, so Self > Near-Self cannot distinguish "well-fit to its own output distribution" from "simply the better classifier." We remove it by construction with a crossed design (§3.3).

The second is **surface leakage**, and it is the one that decided this study. A hidden property is only interesting if the model recovers it from something an outside observer cannot cheaply read off the text. Our pilot found the persona property was recoverable almost entirely from style, and that removing the style difference removed the model's signal too. Rather than treat that as a failed pilot, we turned it into the independent variable.

**Our main contributions are:**

1. **An empirical demonstration that apparent persona self-recognition is style-recognition.** Across five persona pairs and ten generator columns (§4.3), self-prediction accuracy correlates r = +0.71 with an 18-feature surface classifier that has no bag-of-words features, and that classifier matches or beats the model in six of ten columns. Two independent scaffolds engineered to equalise style, differing from each other in one sentence, drive the baseline and the model to chance together.
2. **A leakage-manipulation design that makes the two competing accounts testable against each other**, run at 400 items per cell across twenty-four cells in four stimulus sets (§4.5). Surface leakage stops being a nuisance that disqualifies a study and becomes the variable it manipulates.
3. **A negative result under a capability control that earlier black-box tests lacked**: the self model is never the best predictor of its own output, and on leaky stimuli it is beaten on its own text by a model from a different organisation.
4. **A direct test of Binder et al.'s paradigm in a black-box setting, with a stylometric benchmark** (§4.4). Asked which of two replies it would produce, Hermes-3 discriminates genuinely (balanced accuracy 0.719, hit−false-alarm +0.437) while Llama-3.1 answers by position and shows none (−0.107). An 18-feature logistic regression identifies the author of the same texts 83.1% of the time — so the one model that *can* predict itself is beaten by stylometry, and fails Song et al.'s criterion that introspection must outperform an equal-or-lower-cost third party.
5. **A verified instrument and a fully disclosed preregistration** — a same-base pair on one pinned provider at one quantization, temperature-0 determinism at 20/20, a band that was never moved, a stop rule declared before the stimulus set that broke the study, and every amendment recorded with its reason — for **$3.12** of a $10 budget.

## 2. Related Work

**Binder et al. (2025), "Looking Inward."** M1 is finetuned on ~30k self-prediction examples; a comparison model M2 is finetuned identically but on M1's behaviour. M1 wins (GPT-4o: ~32.6% → ~49.4%). The effect appeared only on simple tasks and required finetuning access we do not have; we are not replicating it. Its prediction for our design is that a self-advantage should survive on stimuli with no surface cue.

**Song, Hu & Mahowald (2025).** Introspection is operationalised as prompted responses predicting a model's own string probabilities *beyond what a model with nearly identical internal knowledge would predict*. Across 21 open models, no residual survives. Their empirical-similarity measure is the direct precedent for our calibration probe; our M/N pair sits in their "two post-trainings of one base" category.

**Song, Lederman, Hu & Mahowald (2025).** The closest methodological cousin, and the one our results corroborate from a different direction. Self-reflection does not beat across-model prediction on temperature judgment, and self-reports track the prompt's *style* instruction rather than the sampling parameter. We adopt their operational definition — a process is introspective only if it is more reliable than an equal-or-lower-cost process available to a third party — and our surface baseline is a direct implementation of that third party.

**Lindsey (2026).** Concept injection into the residual stream yields ~20% detection with near-zero false positives in Claude Opus 4/4.1. This needs activation access we lack; it defines a ceiling we explicitly do not reach. Our claim is strictly behavioural.

**The gap.** Prior work treats surface leakage as a confound to be argued away after the fact. We measure it per stimulus set with a cross-validated classifier, gate on it before collecting the main data, and then manipulate it — which turns "was the effect just style?" from an objection into a measurement.

## 3. Methodology

The design was frozen as a preregistration in `02_design_audit.md` (15 signed decision rows, 2026-08-15) before any main-experiment call, with eight amendments (A1–A8) recorded in the same document, each with its reason and its status at the time it was made. Every call routes through one client that pins the provider, enforces a budget guard *before* issuing the request, and appends a full record to `data/raw/*.jsonl`.

### 3.1 Task and hidden property

A **source prompt** is an advice dilemma in which respecting a person's stated preference and protecting their long-term welfare point to different recommendations. A generator answers each prompt twice, once under each of two **persona clauses** differing only in a values ordering; both personas are generated from every prompt, and both target columns use the same prompts, so topic is balanced by construction and any two texts compared come from the same dilemma. Generation temperature is 1.0, logged per item.

A **trial** shows a predictor one text plus both persona clauses verbatim, order counterbalanced, and asks for a single-letter forced choice. Every predictor has identical information; the only channel available to the generating model and not the others is "I know how *I* would enact this clause." Predictors are not told which model produced the text, and none ever receives the label — enforced structurally, with a test asserting `predict/` cannot import `labels/` and that no label token appears in a built predictor prompt.

### 3.2 Models

Roles were chosen by a preregistered lineage ladder and verified by API call before selection: **M = `meta-llama/llama-3.1-70b-instruct`**, **N = `nousresearch/hermes-3-llama-3.1-70b`** (model card: `Base model: meta-llama/Llama-3.1-70B` — two post-trainings of one pretrained base), both pinned to DeepInfra at fp8; **F = `mistralai/mistral-small-3.2-24b-instruct`** (DeepInfra, fp8; different organisation, base and architecture family). Pinning is a validity condition, not hygiene: if M-as-generator and M-as-self-predictor were served at different quantizations, "same weights" would be literally false.

### 3.3 Crossed 2×2 capability control

Each of M and N generates a column of persona-paired texts; each of M, N and F predicts both columns (M→M, N→M, F→M, M→N, N→N, F→N). The capability-controlled self-advantage is the interaction `(M→M − N→M) − (M→N − N→N)`: a general competence advantage for M appears equally in M→M and M→N and cancels. A unit test asserts a pure capability effect returns zero. Targets are never pooled and no trend is fit across them.

### 3.4 Surface baseline (condition D) and the gate

**D** is a logistic regression on **18 structural features** — length, sentence count, type-token ratio, hedge rate, modal rate, sentiment balance, second-person rate and similar. It has **no bag-of-words features**, so it can only see style, and it is 5-fold cross-validated *grouped by source prompt*, so it cannot memorise topics. D is never a point on the similarity axis; it is the operationalisation of Song et al.'s "equal-or-lower-cost process available to a third party."

The preregistered feasibility band, fixed before the pilot and never moved, is **Self accuracy 60–80% AND D ≤ 58%**, per column, on ≥80 items, both as point estimates.

### 3.5 The leakage manipulation (amendment A4)

The pilot (§4.3) failed the band on all four persona pairs, and the preregistered ladder's Level 3 was taken: no main run, pilot reported as the result. That was then reversed, on the record, because the pilot had produced something more useful than a pair that passes the band: **a pair that leaks (`VO-C`, D = 0.650 on M) and a pair that does not (`VO-D`, D = 0.325 on M).**

The crossed 2×2 therefore runs on **both** stimulus sets, and the primary contrast is the **leakage contrast**:

> `[(M→M − N→M) on VO-C] − [(M→M − N→M) on VO-D]`

Under **style-matching**, any self-advantage rides on surface cues, so it should appear on `VO-C` and vanish on `VO-D` — the contrast is **> 0**. Under **privileged access**, a same-weights advantage does not need a surface cue and should survive on `VO-D` — the contrast is **≈ 0**. This was declared, in writing, before any of the twelve cells were run. Main-run source prompts are **disjoint from the pilot prompts** used to select the two sets.

Inference is an item-level bootstrap **resampling source prompts, not texts** — the two personas from one prompt are not independent observations. Because both columns answer the same prompts, prompt ids are resampled jointly across columns; the two stimulus sets are resampled independently of each other.

### 3.6 What we tried that did not work

Six versions were discarded, three on paper and three against data. On paper: a **three-point regression** placing self above a near/far trend (a line through three points fits by construction); **condition D as a point on the similarity axis** (a heuristic classifier has no defensible position on a similarity continuum); and **provider-label similarity**, replaced by a measured probe. Against data: **a cheaper, better-behaved model pair** (`llama-3.3-70b-instruct` + `hermes-4-70b`) that passed every mechanical check but whose members do not share a pretraining base — the base match *is* the construct, so mechanical quality lost; **`gemini-3.5-flash-lite`** as far-self, which rejected the reasoning-off parameter and needed a laxer decode, breaking the equal-information requirement; and **three persona pairs on the original scaffold**, all of which leaked. We also rejected making the weaker model the target as a conservatism hedge, because it biases toward the null.

## 4. Results

### 4.1 Instrument verification

311 metered calls across 11 candidate models, **$0.0074** total. All 11 resolved, honoured an explicit provider pin with fallbacks disabled (311/311 returned the pinned provider), and billed zero reasoning tokens. Temperature-0 sampling was deterministic on both hosts (20/20 modal answers per shortlisted model). A separate enactment test confirmed both M and N can hold a persona clause through a ~200-word answer (95% usable each) and return a clean letter on the real predictor template at full input length (0% malformed, 40 items each). Verified per-token prices were 5–17× below the planning assumption, removing cost as a binding constraint on n.

That pass also caught the first leakage warning: the phrase *"long-term well-being"* recurred across roughly eight distinct sentences in 40 enactment outputs — the welfare clause's own wording paraphrased into the answers. Candidate clauses were barred from those tokens, and the tokens were added to D's feature set so the leakage check would be honest rather than blind. **The lexical fix was not enough**, which is what §4.3 is about.

### 4.2 Measured similarity (calibration probe)

Fifty frozen forced-choice items — two paraphrases of one sentence, "Which reads better?" — measure agreement with M on a subjective task unrelated to persona, values or identity.

**Table 1.** Agreement with M, 47 items with all three answers, paired bootstrap.

| Quantity | Value | 95% CI |
|---|---|---|
| A_near (Hermes-3 vs. Llama-3.1) | 0.660 | [0.532, 0.787] |
| A_far (Mistral-Small vs. Llama-3.1) | 0.638 | [0.489, 0.766] |
| **Δ = A_near − A_far** | **+0.021** | **[−0.064, +0.106]** |

The preregistered rule was a point estimate (A_near > A_far) with the CI reported, chosen in advance because at 50 items the paired SE is ≈8 pp. The rule is satisfied and no far-self swap was triggered — but **the honest reading is that Near and Far are 2.1 pp apart and the interval spans zero.** The similarity axis this design was named for is barely established, and we say so rather than lean on it.

### 4.3 The pilot is a result: persona detection is style detection

Four persona pairs × two generator columns = eight column-results, 40 source prompts × 2 personas per column (80 items), all bought under the band fixed before the pilot ran.

**Table 2.** Pilot. Band: Self 60–80% **and** D ≤ 58%. CIs are prompt-clustered bootstrap.

| Pair | Column | Scaffold | Self accuracy [95% CI] | Baseline D | Mean words | In band |
|---|---|---|---|---|---|---|
| VO-A | M | original | 0.575 [0.500, 0.650] | 0.637 | 185 | no |
| VO-A | N | original | 0.610 [0.545, 0.680] | 0.766 | 201 | no |
| VO-B | M | original | 0.600 [0.525, 0.675] | 0.588 | 193 | no |
| VO-B | N | original | 0.675 [0.600, 0.750] | 0.662 | 217 | no |
| VO-C | M | original | 0.650 [0.575, 0.725] | 0.650 | 181 | no |
| VO-C | N | original | 0.744 [0.667, 0.821] | 0.756 | 226 | no |
| VO-D | M | style-equalised | 0.500 [0.463, 0.537] | **0.325** | 92 | no |
| VO-D | N | style-equalised | 0.478 [0.412, 0.540] | 0.597 | 79 | no |
| VO-E | M | style-equalised | 0.519 [0.463, 0.577] | 0.506 | 89 | no |
| VO-E | N | style-equalised | 0.565 [0.492, 0.644] | 0.581 | 77 | no |

**Every column failed, and every original-scaffold column failed on D** — while Self was *inside* the 60–80% band in five of six. The models could read the persona. What they could not do was read it without an 18-feature style classifier reading it too.

**(a) Self-prediction tracks the surface baseline.** Across the ten columns, **corr(Self, D) = +0.71**, with Self ≈ 0.47·D + 0.31, and **D ≥ Self in six of ten columns**. VO-A's N column is the clearest: D 0.766 against Self 0.610. This is **Figure 1**.

**(b) Closing the leak removes the signal.** VO-D's scaffold fixes the response at four sentences / 85–105 words in a fixed skeleton — recommendation, one supporting reason, **one drawback of the recommended course**, one next step — with an instruction not to hedge. The drawback requirement is the key element: it removes the sentiment asymmetry between a persona that endorses what someone wants and one that overrides them. On the M column D fell to **0.325**, below chance. **Self fell with it, to 0.500.**

**(c) The models stop discriminating entirely.** Each prompt yields two items with opposite ground truth, so a predictor with any signal should assign them to *different* personas. Counting how often it assigns **both to the same** persona:

| Pair | M column | N column |
|---|---|---|
| VO-A | 30/40 (75%) | 32/40 (80%) |
| VO-B | 28/40 (70%) | 26/40 (65%) |
| VO-C | 26/40 (65%) | **20/40 (50%)** |
| VO-D | **38/40 (95%)** | **38/40 (95%)** |

Discrimination rises with leakage and collapses to 2 of 40 prompts once style is equalised. This also disarms a number that would otherwise be over-read: VO-D M's CI is ±3.7 pp, far tighter than the ±11 pp binomial. **That is not precision.** It is the mechanical consequence of the predictor giving both of a prompt's responses the same label, which forces exactly 50% on that prompt — 38 of 40 prompts scored exactly 0.5. The narrow interval is evidence of non-discrimination, never a tight bound on a real effect.

**(d) A second, single-factor equalisation attempt reproduces the collapse.** The obvious objection to VO-D is that its scaffold might have converged the personas *semantically* rather than only stylistically: requiring each answer to name "one drawback of the course you recommend" makes both personas argue against themselves. `VO-E` (amendment A5) tests exactly that. It is identical to VO-D — same clauses, same four sentences, same 85–105 words, same no-hedging instruction — **except that sentence 3 names a cost of the *alternative* course instead**, which preserves the one-positive-one-negative balance without making a persona undercut its own recommendation.

It made no difference. `VO-E` M: Self 0.519, D 0.506; N: Self 0.565, D 0.581. The hypothesis is falsified: the signal loss is not attributable to that specific instruction. **Two style-equalising scaffolds differing in a single sentence both drive Self and D to chance together.** A pre-declared stop rule ("if VO-E fails on M, no sixth pair") ended the search there.

### 4.4 A second hidden property: can a model recognise or predict its own text?

The persona property leaves one question open — whether the clean condition's null means "no privileged access" or merely "no readable signal for anyone." Authorship settles the second half. Every `VO-C` source prompt has an M-authored and an N-authored answer under the *same* persona clause, so the only difference between them is who wrote it, and we already own the texts.

**The information is plainly there.** A surface classifier fit to the same authorship discrimination — 18 features, grouped cross-validation by prompt — identifies the author of a text **83.1%** of the time across 791 texts.

**The models could not be brought to answer the question.** Two framings were run:

| Framing | Result | Response distribution |
|---|---|---|
| Forced choice: "one of these two replies is yours — which?" | M 0.503, N 0.495 | **M answered "A" on 99.0%** of trials; **N answered "B" on 98.7%** |
| Single text: "did you write this? yes/no", scored as hit − false-alarm | discrimination 0.000 for both | **Both answered "no" to 100%** of 791 texts |

Both are **elicitation failures, not measurements.** In the forced-choice framing the ~50% is what counterbalanced order mechanically produces from a constant answer; in the yes/no framing hit = false-alarm = 0 by construction. We therefore claim **no self-recognition accuracy in either direction** — the honest statement is that we could not elicit a content-dependent self-recognition response from either model.

That is itself worth reporting. A study that had computed accuracy from the forced-choice framing without inspecting the response distribution would have published "models perform at chance on self-recognition (50.3%, 49.5%)" — a clean-looking null that is entirely an artifact. **Reporting the answer distribution alongside any self-report metric is as cheap and as necessary as the surface baseline.** This is **Figure 3**.

Two asymmetries must be stated. The surface baseline is *supervised* — it sees 632 labelled training texts under cross-validation — while the models are asked zero-shot. The comparison is nonetheless the right one for the hypothesis under test: a model with privileged access to its own output distribution should not need labelled examples of its own writing, and Song et al.'s operational definition makes exactly this "equal-or-lower-cost third party" the benchmark. And a null from a failed elicitation is not evidence of absence: a model that cannot engage a self-referential meta-question is not thereby shown to lack self-knowledge.

**Asking the right question: self-prediction, not self-recognition.** Both failed framings ask about *memory* — "did you write this?" — which a model in a fresh session has no basis to answer. Binder et al.'s paradigm is different and far more natural: predict which output you *would* produce. We re-ran the probe that way (amendment A8), giving each model the original dilemma, the persona clause it had been operating under, and two candidate replies — its own and the sibling's, order counterbalanced — and asking which reply it would produce. This is the construct the study set out to test, in the form the literature actually uses, and nothing is being recalled.

**Table 3.** Self-prediction, 391 items, VO-C texts. Split by which slot the model's own text occupied, which converts a counterbalanced forced choice into a signal-detection problem. Discrimination = hit − false alarm is zero for a model answering by position alone.

| | Llama-3.1-70B (M) | Hermes-3-70B (N) |
|---|---|---|
| Raw accuracy | 0.460 | **0.714** |
| Share answering "A" | **0.90** — degenerate by the pre-registered rule | 0.32 |
| Correct when own text was A | 0.845 | 0.537 |
| Correct when own text was B | 0.048 | 0.900 |
| **Discrimination (hit − FA)** | **−0.107** | **+0.437** |
| **Balanced accuracy** | 0.447 | **0.719** |
| Surface baseline, same discrimination | 0.831 | 0.831 |

Two things follow, and they point in opposite directions.

**Hermes-3 can genuinely predict its own output.** Balanced accuracy 0.719 with a discrimination of +0.437 is not a position artifact: it is right 90.0% of the time when its own text is in slot B and 53.7% when in slot A, so despite a clear B-preference it separates the two texts far better than any constant strategy could. This is a *positive* self-prediction result, and it is the one finding in this report that supports the Binder side.

**It is not privileged access.** The same discrimination — which of these two same-base models wrote this text — is performed at **0.831** by an 18-feature logistic regression. Hermes-3's self-prediction is real and is beaten by stylometry. Under Song et al.'s criterion, that is precisely the test introspection has to pass and does not: a process is introspective only if it is more reliable than an equal-or-lower-cost process available to a third party.

**Llama-3.1 shows no self-prediction at all.** Its discrimination is −0.107, slightly *anti*-correlated, and its answer distribution (90% "A") is degenerate by the rule fixed in advance. We claim nothing from its raw 0.460. The asymmetry between the two models is itself worth reporting: self-prediction ability here is not a property of "language models" but of a particular model, and the one that has it is the one that writes most distinctively. This is **Figure 4**.

### 4.5 The crossed design across four stimulus sets

The crossed 2×2 ran on 200 main source prompts × 2 personas per column for **four** stimulus sets spanning the leakage axis — **24 cells, ~400 items each, 9,269 scored trials, zero malformed predictions**, every self cell provider-matched. Main prompts are disjoint from the pilot prompts used to select the sets.

**Table 4.** All four sets, ordered by mean Baseline D. Prompt-clustered bootstrap CIs.

| Set | D (M col / N col) | Self-advantage (M→M − N→M) | Capability-controlled interaction |
|---|---|---|---|
| VO-D (style-equalised) | 0.551 / 0.536 | +0.000 [−0.015, +0.015] | −0.006 [−0.033, +0.021] |
| VO-B (original) | 0.647 / 0.753 | +0.000 [−0.033, +0.035] | +0.005 [−0.040, +0.050] |
| VO-A (original) | 0.664 / 0.751 | +0.020 [−0.015, +0.056] | −0.030 [−0.079, +0.018] |
| VO-C (original) | 0.693 / **0.845** | **−0.033** [−0.058, −0.008] | **+0.089** [+0.048, +0.131] |

**Not one of the four shows a positive self-advantage whose interval excludes zero.** The single significant self-advantage is *negative*, and the single non-zero interaction belongs to the leakiest set in the study. Across four independent stimulus designs and 9,269 trials, the self model is never reliably better at predicting its own outputs than its same-base sibling is.

The interaction correlates with mean Baseline D at r = +0.54 across the four sets, consistent with the reading that the apparent capability-controlled effect is produced by leakage rather than by self-knowledge. **With four points and three of them null, we attach no significance to that slope and did not pre-register one** — the four interval estimates are the result; the correlation is descriptive and should be treated as a hypothesis for a larger study, not a finding.

**Table 5.** Cell-level detail for the two sets at the ends of the leakage axis.

| Cell | VO-C (leaky) | VO-D (style-equalised) |
|---|---|---|
| M→M (self) | 0.603 [0.572, 0.635] | 0.520 [0.500, 0.542] |
| N→M (cross) | **0.636** [0.604, 0.668] | 0.520 [0.505, 0.537] |
| F→M (far) | 0.628 [0.596, 0.661] | 0.505 [0.477, 0.533] |
| M→N (cross) | 0.644 [0.608, 0.679] | 0.557 [0.526, 0.590] |
| N→N (self) | 0.766 [0.730, 0.800] | 0.551 [0.523, 0.581] |
| F→N (far) | 0.763 [0.728, 0.798] | 0.554 [0.514, 0.593] |
| **D (surface baseline)** | **0.693 (M) / 0.845 (N)** | 0.551 (M) / 0.536 (N) |

**Table 6.** Contrasts on the two end sets, prompt-clustered bootstrap.

| Contrast | VO-C | VO-D | Difference [95% CI] |
|---|---|---|---|
| **Primary — leakage contrast** (M→M − N→M) | **−0.033** [−0.058, −0.008] | **+0.000** [−0.015, +0.015] | **−0.033 [−0.063, −0.003]** |
| Capability-controlled interaction | +0.089 [+0.048, +0.131] | −0.006 [−0.033, +0.021] | — |
| M→M − F→M (self vs. far) | −0.025 [−0.053, +0.003] | +0.015 [−0.010, +0.040] | — |
| N→M − F→M (near vs. far) | +0.008 [−0.015, +0.030] | +0.015 [−0.010, +0.041] | — |

Three things follow.

**(a) The primary contrast is significant and points the wrong way for both accounts.** We predicted > 0 under style-matching and ≈ 0 under privileged access. We observed **−0.033 [−0.063, −0.003]**. There is no self-advantage to remove on the leaky set; there is a self-*disadvantage*. We report this as found.

**(b) The self model is never the best predictor of its own output.** On VO-C, M→M (0.603) is below N→M (0.636) *and* below F→M (0.628) — Llama is beaten on its own text by a model from a different organisation. M is simply the weakest classifier of the three: N and F both beat it on both columns.

**(c) On style-equalised stimuli everything collapses to indistinguishable.** Self-advantage is +0.000 [−0.015, +0.015] and the interaction −0.006 [−0.033, +0.021], excluding the preregistered 5 pp SESOI. Absolute accuracies sit at 0.505–0.557, so all six predictors are at or near chance.

**The strongest objection to our own conclusion, addressed.** VO-C's interaction is **+0.089 [+0.048, +0.131]** — positive and excluding zero. Read at face value that is a capability-controlled self-advantage, and it is the one number in this report that supports the Binder side. It does not survive the neutral third party. The interaction is positive because M *under*-performs on N's column, not because it over-performs on its own: moving from column M to column N, F gains +0.135 and N gains +0.130, while M gains only +0.041. Both columns' cues are exploited by F and N; M fails to exploit the stronger one. Combined with M→M < F→M — the self model losing on its own text to an unrelated model — the interaction reflects M's differential weakness as a style-reader, not self-knowledge. On VO-D, where no cue exists, it is null.

**Figure 2** shows the two end sets in detail: the self-advantage in each, and all six cells with the surface baseline drawn in — on the leaky set it sits above every language model.

### 4.6 Robustness and cost

Position bias (share of "A" answers) ranged 0.51–0.64 across the twenty-four cells, worst at M→N on VO-C (0.64). Within-prompt discrimination on the main run reproduces the pilot pattern: on VO-C the predictor assigns both responses to the same persona 46.5–76% of the time, on VO-D 81–95.5%. Zero malformed predictions across all 9,269 scored trials. Exclusions: VO-D's N column retained 323/400 items because four-sentence responses sometimes fell below the 60-word floor; VO-C retained 393–398.

Total spend **$3.1216** of a $10 ceiling, across 5 stimulus designs, 24 crossed cells (9,269 scored trials), a calibration probe, a verification sweep, and three framings of the self-referential probe.

## 5. Discussion

### 5.1 What this establishes

Within this design, on this lineage, for this hidden property: **the apparent ability of a model to identify which of two personas produced a text is carried by surface style, and it is not self-specific.** Remove the style difference and the ability does not degrade — it disappears, with the predictor assigning both of a prompt's responses to the same persona 95% of the time. Leave the style difference in, and the model is still not the best reader of its own text: a 24B model from another organisation beats it, and an 18-feature logistic regression beats them all.

This is a negative result about an *instrument*, and it generalises further than the study it was meant to serve. **Any self-prediction paradigm reporting above-chance accuracy without fitting a surface-feature classifier on the same stimuli, per condition, cannot distinguish self-knowledge from style-reading.** That baseline costs nothing — 18 features and a logistic regression — and in five of our eight pilot columns it beat the model. It should be a default reporting requirement, not an optional robustness check.

It also reaches Song, Lederman, Hu & Mahowald's conclusion from a different direction. They found models judging their own sampling temperature were reading style; we find the same failure mode in a semantic property specifically chosen to avoid it. The property was buried in *which recommendation is made*, not in register or vocabulary, and it still leaked — through sentence length, hedge rate and sentiment balance, because a persona that endorses what someone wants writes differently from one that overrides them, whatever the instruction says.

### 5.2 What it does not establish

The persona result and the self-prediction result must not be blurred together. On the persona property, the style-equalised condition leaves every predictor near chance, so "no self-advantage" there is partly "no signal for anyone" — an equivalence bound is only informative if the task is performable, and on those stimuli it was not.

The self-prediction probe (§4.4) is what closes that hole, because there the signal is demonstrably present: a logistic regression recovers it at 0.831. Hermes-3 recovers it at 0.719 — real, well above chance, and **below the stylometric benchmark**. Llama-3.1 does not recover it at all. So the honest summary across both properties is not "models have no self-knowledge" but something narrower and better supported: **whatever self-knowledge is on display here is not privileged**, because a third party with no access to the model's weights, running eighteen features and a logistic regression, does the same job better.

None of this refutes Binder et al., who finetune both models on ~30k examples — a setting we do not test, and one where the self-model is trained rather than prompted. Nor does it speak to Lindsey's activation-level results, which require access we lack.

### 5.3 Future work

The finding that matters is whether *any* stimulus design yields a property models can read and surface features cannot, or whether the two are inseparable for persona-like properties. Beyond that: run the leakage manipulation across several lineages; test whether a parameter-efficient sibling and a full fine-tune sibling of one base give different residuals, which would put a scale on "how much shared weight is enough"; and apply the surface-baseline gate retrospectively to published self-prediction results, where our five-of-eight columns suggest it may not be a formality.

## 6. Conclusion

We set out to ask whether a model has a self-prediction residual once its general classification ability is controlled, and built a crossed design on a verified same-base pair to answer it. The pilot answered a prior question first: on the persona property, what the model recovers is style. Across four stimulus designs, 24 cells and 9,269 trials, no positive self-advantage appeared in any set, and the one non-zero capability-controlled interaction belonged to the leakiest stimuli in the study.

Asked the question the literature actually asks — which of these two replies would you produce — one of the two models could genuinely answer it. Hermes-3 reaches a balanced accuracy of 0.719 with a discrimination of +0.437, while Llama-3.1 answers by position and shows none. That is a real self-prediction ability in one model, and it is still beaten by an 18-feature logistic regression scoring 0.831 on the same discrimination. Self-prediction here is not privileged access; it is stylometry, performed worse than stylometry.

Two cheap checks would have changed what we ran, and we release both: a **surface-leakage gate** that asks whether a trivial style classifier already solves your hidden property, and a **response-bias check** that catches a predictor answering by position. The first reframed this study; the second stopped us publishing two artifacts as clean nulls. Neither costs anything, and in our hands both were decisive.

---

## Limitations and Dual-Use / Ethical Considerations

**Does the design establish a ground-truth or causal link, rather than relying on conversation alone?** Yes, on both counts, and this is the main methodological claim we make. Ground truth is *constructed, not elicited*: we set the persona that generates each text, store the label in a directory the prediction code cannot import (enforced by a test), and never show any predictor the label. Nothing rests on asking a model to describe itself and believing the answer. The causal link comes from the leakage manipulation: we intervene on the stimulus generation process to remove surface style and observe the predicted signal disappear. That is an intervention on the hypothesised mediator, not a correlation across conversations.

**Risk of over-attributing moral status.** This is the risk our result speaks to most directly. Apparent self-knowledge — a model "recognising its own writing" at 60–75% — was here fully explained by style-reading, and a trivial classifier did it better. Reporting such accuracy without a surface baseline would invite the inference that the model has privileged access to itself, which our data do not support. We make no claim about introspection, internal states, sentience, or moral status, and our scope ceiling is same-weights behavioural self-modelling: prediction happens in a fresh session, so nothing here bears even on same-episode memory, let alone consciousness.

**Risk of under-attributing moral status.** A null is not evidence of absence, and we are careful not to let ours travel further than it can. Our clean condition is one scaffold, one lineage, one property, and one prompting-only setting without finetuning or activation access. Absolute accuracies on VO-D sit near chance for *every* predictor, so the study cannot distinguish "no privileged access" from "no readable signal for anyone." Anyone citing this as evidence that models lack self-knowledge would be over-reading it as badly as the over-attribution error above. Lindsey (2026) finds real, if limited, introspective signal with activation access; our behavioural null does not contradict that.

**Distressing model outputs.** The task is advice on ordinary life dilemmas (career, money, relationships, health, lifestyle). Dilemmas were human-screened at authoring; none involves self-harm, crisis content, or material designed to distress. We did not prompt for distress, did not roleplay suffering, and did not use adversarial or jailbreak prompting. Generated texts were reviewed during quality screening; a refusal regex was part of the pre-declared exclusion rule and refusals were excluded label-blind rather than pressured. No output required escalation.

**Dual use.** The method's misuse potential is low and worth stating precisely. The surface baseline is a stylometric classifier; stylometry is a mature, widely available technique, and our 18 features are standard. The one transferable capability is *authorship-style detection of LLM personas*, which could in principle support deanonymising which system prompt or persona produced a text. We consider this a low marginal risk — existing stylometry tools are stronger — and the finding cuts the other way in practice: it shows how easily persona differences leak into style, which is useful to anyone trying to *prevent* such inference.

**Reproducibility and cost transparency.** Every API call is logged append-only with the returned model id, provider, token counts, cost, timestamp and prompt hash. Stimuli are frozen with content hashes. Total spend was $3.12. Results can be recomputed from the logged texts; because generation used temperature 1.0 and provider seed reproducibility is unverified, the logged texts — not re-sampling — are the reproducible artefact.

**Further limitations.**
- **`VO-D` was written after seeing `VO-A/B/C` fail.** A second pass. The band was fixed beforehand and never moved, the stop rule ("if VO-D also fails on M, no fifth pair") was declared before VO-D ran, and all four pairs are reported. Recorded as amendment A1, not absorbed silently.
- **A4 reverses A3 on the record.** We first took the preregistered Level-3 branch (no main run) and then reversed it. The reversal is dated and reasoned, and the A4 analysis was specified before any of its cells ran — but the primary contrast was chosen after the pilot, not before it, and its direction was mispredicted.
- **The similarity axis is weak.** Δ = +2.1 pp with a CI spanning zero. Any conclusion resting on near-vs-far should be discounted accordingly.
- **Two implementations of style-equalisation, not many.** `VO-D` and `VO-E` differ in one sentence and both collapse Self and D together, which is stronger than one attempt — but a third design might yet separate them, and until someone finds one, "closing the leak removes the signal" is a claim about this family of scaffolds.
- **The self-recognition result is an elicitation failure, not a measurement.** Neither framing produced a content-dependent answer, so no self-recognition ability is claimed or denied. The surface baseline there is supervised while the models are zero-shot; we argue in §4.4 why that comparison is still the right one for the hypothesis, but a reader who disagrees should discount that section to the observation that the models would not answer.
- **"Same weights" is verified at the host, not the checkpoint.** DeepInfra fp8 pinning with 20/20 temperature-0 determinism is the best available evidence; a silent backend change is auditable from the logs but not preventable. Whether Hermes-3 is a full or parameter-efficient fine-tune is not stated on its card.
- **Unequal n.** VO-D's N column retained 323/400 items against 393–398 elsewhere.

## Code and Data

- **Released tool:** `tools/surface_leakage_gate.py` — a single self-contained file (numpy only) providing `gate()` and `response_bias()`, the two checks this study turned on. Drop it into any self-prediction or introspection experiment; it needs no other part of this repository. It groups cross-validation by source prompt by default, because ungrouped CV inflates the baseline whenever two texts share a prompt.
- **Code:** ⟦FILL: GitHub URL⟧ — `src/selfpred/` (pinned OpenRouter client with pre-request budget guard, persona generation, prediction runner, 18-feature surface baseline, prompt-clustered bootstrap/McNemar/interaction), `scripts/`, `tests/` (38 tests).
- **Data:** append-only per-call JSONL for every phase; frozen calibration items and stimulus sets with content hashes; generated texts with labels stored separately from predictor inputs; `data/results/*.json`.
- **Preregistration:** `02_design_audit.md` — 15 signed decision rows plus amendments A1–A4. Supporting records: `04_model_verification.md`, `06_hermes_smoke_test.md`, `07_calibration_results.md`, `08_pilot_results.md`, `09_pilot_finding.md`. The adversarial design review that produced the crossed design is in `03_design_review_and_implementation_plan.md`.

## Author Contributions

U.H. led the experimental design and statistical reasoning, designed the calibration probe and bootstrap analysis, and implemented the client, pipeline and analysis. J.C. led the literature grounding, designed the hidden-property task and the four persona pairs including the style-equalising scaffold, and owned the pilot feasibility judgment. Both authors contributed to interpretation and to the final manuscript.

## References

1. Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2025). *Looking Inward: Language Models Can Learn About Themselves by Introspection.* ICLR 2025. arXiv:2410.13787.
2. Song, S., Hu, J., & Mahowald, K. (2025). *Language Models Fail to Introspect About Their Knowledge of Language.* COLM 2025. arXiv:2503.07513.
3. Song, S., Lederman, H., Hu, J., & Mahowald, K. (2025). *Privileged Self-Access Matters for Introspection in AI.* arXiv:2508.14802.
4. Lindsey, J. (2026). *Emergent Introspective Awareness in Large Language Models.* Anthropic. arXiv:2601.01828.

*⟦VERIFY: author lists and arXiv IDs against the papers before submission.⟧*

## Appendix

**A.** The four persona clause pairs verbatim, and both generation scaffolds — `data/stimuli/personas/candidates.json`.
**B.** One worked source prompt with both persona outputs under each scaffold.
**C.** Predictor system prompt and template (frozen; 0% malformed at full input length) — `src/selfpred/predict/prompts.py`.
**D.** Calibration probe: 50 items, A/B randomisation seed, per-model answers.
**E.** Surface baseline: the 18 features, model class, grouped cross-validation procedure — `src/selfpred/baseline/surface.py`, packaged for reuse as `tools/surface_leakage_gate.py`.
**F.** Verification record: 311 calls across 11 models, re-alias check, 20-repeat determinism, 30-call concurrency burst.
**G.** Amendments A1–A4 in full, with dates, reasons and outcomes.
**H.** Cost record by phase (verification, smoke, calibration, pilot, generation, prediction) — **total $3.1216**.

## LLM Usage Statement

We used Claude (via Claude Code) throughout: for literature retrieval and summarisation; as an adversarial reviewer of the experimental design — a structured multi-advisor critique identified the capability confound and the prompt-clustering issue and produced the crossed design; for drafting candidate dilemma prompts and persona clauses, all human-screened before freezing; for implementation of the data-collection pipeline; and for drafting and editing this report. All experimental results and statistical estimates come from our own logged API runs and analysis code and were verified against the raw per-call logs. Every model ID, provider, price and rate is read from returned API metadata, not from model-generated assertions. Both authors reviewed and revised the final text.
