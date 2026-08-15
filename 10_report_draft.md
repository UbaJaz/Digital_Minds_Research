# Self-Prediction or Style-Matching? Surface Leakage as a Manipulated Variable in a Capability-Controlled Test

**Ubayd Hattas** — *⟦FILL: affiliation⟧*
**Jaswin Chinthala** — *⟦FILL: affiliation⟧*

With Apart Research · Digital Minds Research Sprint, 14–16 August 2026

---

## Abstract

Arguments about model preferences and welfare treat a model's self-report as carrying special evidential weight. We set out to test one load-bearing piece of that: can a model identify a hidden property of its own output better than an equally-informed external model, once the confound that the "self" predictor is also the *better* predictor is removed? We built a crossed 2×2 on two models that verifiably share a pretraining base — `Llama-3.1-70B-Instruct` and `Hermes-3-Llama-3.1-70B`, both pinned to one provider at fp8 — so a uniform competence advantage cancels in the interaction. The pilot then produced a result we did not plan for. Across four persona pairs and eight generator columns, self-prediction accuracy tracked a bag of 18 surface features almost perfectly (r = +0.68; the surface baseline *matched or beat* the model in five of eight columns). A fourth stimulus set built to equalise style closed the leak — baseline accuracy fell to 0.325 — and the model's signal vanished with it, to 0.500, with the predictor assigning both of a prompt's responses to the same persona 95% of the time. Rather than abandon the design, we made leakage the manipulation: the crossed 2×2 is run on both a leaky and a style-equalised stimulus set, so style-matching and privileged-access accounts make opposite predictions about the same contrast. ⟦FILL: leakage-contrast result⟧ We make no claim about introspection, internal states, or same-episode memory.

**Keywords:** introspection, self-prediction, privileged access, surface leakage, capability control, digital minds

---

## 1. Introduction

People — including researchers — treat an AI's self-report as if it knows something special about itself. This is a controlled test of whether that is true, or an illusion created by the model being statistically similar to itself.

The assumption is load-bearing well beyond philosophy of mind. Most practical work on model preferences, distress signals and welfare runs through self-report. If a model's report about itself carries no epistemic advantage over what a comparably capable outside observer could infer from the same text, those methods are measuring something other than what they claim.

The literature disagrees. Binder et al. (2025) finetune a model to predict its own hypothetical behaviour, find it beats a differently-trained model finetuned on the same ground truth, and read this as introspection. Song, Hu & Mahowald (2025) test prompted self-reports against directly measurable internal knowledge across 21 open models and find no advantage once behavioural similarity is controlled. Song, Lederman, Hu & Mahowald (2025) run the closest black-box analogue — models judging their own generation temperature — and find a null driven by an identified confound: the models were reading the *style* of the text, information equally available to any observer.

Two problems block a clean black-box test, and this project ran into both.

The first is a **capability confound**. In every practical configuration the "self" predictor is also the largest model in the comparison and "near-self" is a smaller sibling, so Self > Near-Self cannot distinguish "well-fit to its own output distribution" from "simply the better classifier." We remove it by construction with a crossed design (§3.3).

The second is **surface leakage**, and it is the one that decided this study. A hidden property is only interesting if the model recovers it from something an outside observer cannot cheaply read off the text. Our pilot found that the persona property — which of two value-ordering personas wrote an answer — was recoverable almost entirely from style, and that removing the style difference removed the model's signal too. Rather than treat that as a failed pilot, we turned it into the independent variable.

**Our main contributions are:**

1. **An empirical demonstration that apparent persona self-recognition is style-recognition.** Across four persona pairs and eight generator columns (§4.3), self-prediction accuracy correlates r = +0.68 with an 18-feature surface classifier that has no bag-of-words features, and that classifier matches or beats the model in five of eight columns. A stimulus set engineered to equalise style drives the baseline to 0.325 and the model to 0.500 simultaneously.
2. **A leakage-manipulation design that makes the two competing accounts testable against each other.** Running the crossed 2×2 on both a leaky and a style-equalised stimulus set yields a single contrast on which style-matching predicts a positive value and privileged access predicts zero (§3.5). Surface leakage stops being a nuisance that disqualifies a study and becomes the variable it manipulates.
3. **A verified instrument and a fully disclosed preregistration.** A same-base model pair on one pinned provider at one quantization, temperature-0 determinism measured at 20/20, a preregistered band that was never moved, a stop rule declared before the stimulus set that broke the study was run, and every amendment recorded with its reason — all for $1.13 of a $10 budget.

## 2. Related Work

**Binder et al. (2025), "Looking Inward."** M1 is finetuned on ~30k self-prediction examples; a comparison model M2 is finetuned identically but on M1's behaviour. M1 wins (GPT-4o: ~32.6% → ~49.4%). The effect appeared only on simple tasks and required finetuning access we do not have; we are not replicating it. Its prediction for our design is that a self-advantage should survive on stimuli with no surface cue.

**Song, Hu & Mahowald (2025).** Introspection is operationalised as prompted responses predicting a model's own string probabilities *beyond what a model with nearly identical internal knowledge would predict*. Across 21 open models, no residual survives. Their empirical-similarity measure is the direct precedent for our calibration probe, which we credit rather than claim; our M/N pair sits in their "two post-trainings of one base" category.

**Song, Lederman, Hu & Mahowald (2025).** The closest methodological cousin, and the one our pilot ended up corroborating from a different direction. Self-reflection does not beat across-model prediction on temperature judgment, and self-reports track the prompt's *style* instruction rather than the sampling parameter. We adopt their operational definition — a process is introspective only if it is more reliable than an equal-or-lower-cost process available to a third party — and our surface baseline is a direct implementation of that "equal-or-lower-cost third party."

**Lindsey (2026).** Concept injection into the residual stream yields ~20% detection with near-zero false positives in Claude Opus 4/4.1. This needs activation access we lack; it defines the ceiling we explicitly do not reach.

**The gap.** Prior work treats surface leakage as a confound to be argued away after the fact. We measure it per stimulus set with a cross-validated classifier, gate on it before collecting the main data, and then manipulate it — which turns "was the effect just style?" from an objection into a measurement.

## 3. Methods

The design was frozen as a preregistration in `02_design_audit.md` (15 decision rows, signed 2026-08-15) before any main-experiment call, with four amendments (A1–A4) recorded in the same document, each with its reason and its status at the time it was made. Code is in `src/selfpred/`; every call routes through one client that pins the provider, enforces a budget guard *before* issuing the request, and appends a full record to `data/raw/*.jsonl`.

### 3.1 Task and hidden property

A **source prompt** is an advice dilemma in which respecting a person's stated preference and protecting their long-term welfare point to different recommendations. A generator answers each prompt twice, once under each of two **persona clauses** differing only in a values ordering; both personas are generated from every prompt, and both target columns use the same prompts, so topic is balanced by construction and any two texts compared come from the same dilemma. Generation temperature is 1.0, logged per item.

A **trial** shows a predictor one text plus both persona clauses verbatim, order counterbalanced, and asks for a single-letter forced choice. Every predictor has identical information; the only channel available to the generating model and not the others is "I know how *I* would enact this clause." Predictors are not told which model produced the text, and none ever receives the label — enforced structurally, with a test asserting `predict/` cannot import `labels/` and that no label token appears in a built predictor prompt.

### 3.2 Models

Roles were chosen by a preregistered lineage ladder and verified by API call before selection: **M = `meta-llama/llama-3.1-70b-instruct`**, **N = `nousresearch/hermes-3-llama-3.1-70b`** (Hugging Face card: `Base model: meta-llama/Llama-3.1-70B`, i.e. two post-trainings of one pretrained base), both pinned to DeepInfra at fp8; **F = `mistralai/mistral-small-3.2-24b-instruct`** (DeepInfra, fp8; different organisation, base and architecture family). Pinning is a validity condition, not hygiene: if M-as-generator and M-as-self-predictor were served at different quantizations, "same weights" would be literally false.

### 3.3 Crossed 2×2 capability control

Each of M and N generates a column of persona-paired texts; each of M, N and F predicts both columns (M→M, N→M, F→M, M→N, N→N, F→N). The capability-controlled self-advantage is the interaction `(M→M − N→M) − (M→N − N→N)`: a general competence advantage for M appears equally in M→M and M→N and cancels. A unit test asserts a pure capability effect returns zero. Targets are never pooled and no trend is fit across them.

### 3.4 Surface baseline (condition D) and the gate

**D** is a logistic regression on **18 structural features** — length, sentence count, type-token ratio, hedge rate, modal rate, sentiment balance, second-person rate and similar. It has **no bag-of-words features**, so it can only see style, and it is 5-fold cross-validated *grouped by source prompt*, so it cannot memorise topics. D is never a point on the similarity axis; it is the operationalisation of Song et al.'s "equal-or-lower-cost process available to a third party."

The preregistered feasibility band, fixed before the pilot and never moved, is **Self accuracy 60–80% AND D ≤ 58%**, per column, on ≥80 items, both as point estimates. A column that fails on D is a column where every predictor may be solving the task from style.

### 3.5 The leakage manipulation (amendment A4)

The pilot (§4.3) failed the band on all four persona pairs, and the preregistered ladder's Level 3 was taken: no main run, with the pilot reported as the result. That was then reversed, on the record, for a reason the pilot itself supplied — it had produced something more useful than a pair that passes the band: **a pair that leaks (`VO-C`, D = 0.650 on M) and a pair that does not (`VO-D`, D = 0.325 on M).**

The crossed 2×2 is therefore run on **both** stimulus sets, and the primary contrast is the **leakage contrast**:

> `[(M→M − N→M) on VO-C] − [(M→M − N→M) on VO-D]`

The two accounts make opposite predictions. Under **style-matching** (Song et al.), any self-advantage is a similarity artefact riding on surface cues, so it should appear on `VO-C` and vanish on `VO-D` — the contrast is **> 0**. Under **privileged access** (Binder et al.), a genuine same-weights advantage does not need a surface cue, so it should survive on `VO-D` — the contrast is **≈ 0**. This was declared before the cells were run.

**Secondary, per stimulus set:** the capability-controlled interaction; the three M-column pairwise contrasts; all six cell accuracies with prompt-clustered bootstrap CIs; D per column; A-share position bias per cell; within-prompt discrimination rate per cell.

Inference is an item-level bootstrap **resampling source prompts, not texts** — the two personas from one prompt are not independent observations. Because both columns answer the same prompts, prompt ids are resampled jointly across columns. The interaction is reported on the log-odds scale alongside the difference scale.

### 3.6 What we tried that did not work

Six versions were discarded, three on paper and three against data. On paper: a **three-point regression** placing self above a near/far trend (a line through three points fits by construction); **condition D as a point on the similarity axis** (a heuristic classifier has no defensible position on a similarity continuum); and **provider-label similarity**, replaced by a measured probe. Against data: **a cheaper, better-behaved model pair** (`llama-3.3-70b-instruct` + `hermes-4-70b`) that passed every mechanical check but whose members do not share a pretraining base — the base match *is* the construct, so mechanical quality lost; **`gemini-3.5-flash-lite`** as far-self, which rejected the reasoning-off parameter and needed a laxer decode than the other models, breaking the equal-information requirement; and **three persona pairs on the original scaffold**, all of which leaked. We also rejected making the weaker model the target as a conservatism hedge, because it biases toward the null.

## 4. Results

> **STATUS.** §4.1–4.3 are complete and report real measurements. §4.4 is collected but not yet scored (`VO-C` complete, `VO-D` in progress); §4.5 is the scaffold for it.

### 4.1 Instrument verification

311 metered calls across 11 candidate models, **$0.0074** total. All 11 resolved, honoured an explicit provider pin with fallbacks disabled (311/311 returned the pinned provider), and billed zero reasoning tokens. Temperature-0 sampling was deterministic on both hosts (20/20 modal answers per shortlisted model). A separate enactment test confirmed both M and N can hold a persona clause through a ~200-word answer (95% usable each, 20 outputs per model) and return a clean letter on the real predictor template at full input length (0% malformed, 40 items each). Verified per-token prices were 5–17× below the planning assumption, which removed cost as a binding constraint on n and let the smallest effect of interest be tightened rather than loosened.

That verification pass also caught the first leakage warning: the phrase *"long-term well-being"* recurred across roughly eight distinct sentences in 40 enactment outputs — the welfare clause's own wording being paraphrased into the answers. Candidate clauses were subsequently barred from using those tokens, and the tokens were added to D's feature set so the leakage check would be honest rather than blind. **The lexical fix was not enough**, which is what §4.3 is about.

### 4.2 Measured similarity (calibration probe)

Fifty frozen forced-choice items — two paraphrases of one sentence, "Which reads better?" — measure agreement with M on a subjective task unrelated to persona, values or identity.

**Table 1.** Agreement with M, 47 items with all three answers, paired bootstrap.

| Quantity | Value | 95% CI |
|---|---|---|
| A_near (Hermes-3 vs. Llama-3.1) | 0.660 | [0.532, 0.787] |
| A_far (Mistral-Small vs. Llama-3.1) | 0.638 | [0.489, 0.766] |
| **Δ = A_near − A_far** | **+0.021** | **[−0.064, +0.106]** |

The preregistered rule was a point estimate (A_near > A_far) with the CI reported, chosen in advance because at 50 items the paired SE is ≈8 pp and a CI-excludes-zero rule would fail on noise. The rule is satisfied and no far-self swap was triggered — but **the honest reading is that Near and Far are 2.1 pp apart and the interval spans zero.** The similarity axis this design was named for is barely established, and we say so rather than lean on it. Target position bias was 0.38 A-share.

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

**Every column failed, and every original-scaffold column failed on D** — while Self was *inside* the 60–80% band in five of six. The models could read the persona. What they could not do was read it without an 18-feature style classifier reading it too.

**(a) Self-prediction tracks the surface baseline.** Across the eight columns, **corr(Self, D) = +0.68**, with Self ≈ 0.44·D + 0.33, and **D ≥ Self in five of eight columns**. VO-A's N column is the clearest: D 0.766 against Self 0.610 — a bag of structural features beating the model at identifying which persona wrote the text. This is Figure 1.

**(b) Closing the leak removes the signal.** VO-D's scaffold fixes the response at four sentences / 85–105 words in a fixed rhetorical skeleton — recommendation, one supporting reason, **one drawback of the recommended course**, one next step — with an instruction not to hedge. The drawback requirement is the key element: it removes the sentiment asymmetry between a persona that endorses what someone wants and one that overrides it. It worked exactly as designed. On the M column D fell from 0.588–0.766 to **0.325**, below chance — no usable surface signal remains. **Self fell with it, to 0.500.**

**(c) The models stop discriminating entirely.** Each prompt yields exactly two items with opposite ground truth, so a predictor with any signal should assign them to *different* personas. Counting how often it assigns **both to the same** persona:

| Pair | M column | N column |
|---|---|---|
| VO-A | 30/40 (75%) | 32/40 (80%) |
| VO-B | 28/40 (70%) | 26/40 (65%) |
| VO-C | 26/40 (65%) | **20/40 (50%)** |
| VO-D | **38/40 (95%)** | **38/40 (95%)** |

Discrimination rises with leakage — VO-C's N column, the highest-D column, is the only one where the model separates the pair half the time — and collapses to 2 of 40 prompts once style is equalised.

This also disarms a number that would otherwise be over-read. VO-D M's CI is ±3.7 pp, far tighter than the ±11 pp binomial. **That is not precision.** It is the mechanical consequence of the predictor giving both of a prompt's responses the same label, which forces exactly 50% on that prompt: 38 of 40 prompts scored exactly 0.5. The narrow interval is evidence of non-discrimination and must never be quoted as a tight bound on a real effect.

**Figure 1.** Self-prediction accuracy against surface-baseline accuracy, one point per pair × column (n = 8), with chance lines at 0.5 on both axes and points labelled by pair and column. Self tracks D with r = +0.68; points on or below the diagonal are columns where an 18-feature style classifier matches or beats the model. `figures/fig1_self_vs_surface.png`.

### 4.4 The leakage manipulation (data collected, scoring in progress)

Under amendment A4 the crossed 2×2 runs on 200 main source prompts × 2 personas per column, on both `VO-C` (leaky) and `VO-D` (style-equalised) — 400 items per cell, twelve cells in total. `VO-C` is complete across all six cells at a cost of $0.84; `VO-D` is in progress at the time of writing.

⟦FILL: the leakage contrast `[(M→M − N→M) on VO-C] − [(M→M − N→M) on VO-D]` with prompt-clustered bootstrap CI, and which account it favours.⟧

**Table 3.** Cell accuracies, 400 items per cell, prompt-clustered bootstrap CIs.

| Cell | VO-C (leaky) | VO-D (style-equalised) |
|---|---|---|
| M→M (self) | ⟦FILL⟧ | ⟦FILL⟧ |
| N→M (cross) | ⟦FILL⟧ | ⟦FILL⟧ |
| F→M (far) | ⟦FILL⟧ | ⟦FILL⟧ |
| M→N (cross) | ⟦FILL⟧ | ⟦FILL⟧ |
| N→N (self) | ⟦FILL⟧ | ⟦FILL⟧ |
| F→N (far) | ⟦FILL⟧ | ⟦FILL⟧ |
| D (surface baseline) | ⟦FILL⟧ | ⟦FILL⟧ |

**Table 4.** Contrasts.

| Contrast | VO-C | VO-D | Difference [95% CI] |
|---|---|---|---|
| **Primary — leakage contrast:** (M→M − N→M) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |
| Capability-controlled interaction | ⟦FILL⟧ | ⟦FILL⟧ | — |
| M→M − F→M (self vs. far) | ⟦FILL⟧ | ⟦FILL⟧ | — |
| N→M − F→M (near vs. far) | ⟦FILL⟧ | ⟦FILL⟧ | — |
| F→M vs. F→N (far capability check) | ⟦FILL⟧ | ⟦FILL⟧ | — |

**Figure 2.** Two panels: (left) self-advantage `acc(M→M) − acc(N→M)` for each stimulus set with CI whiskers and a zero line — style-matching predicts the bar shrinks to zero from VO-C to VO-D; (right) all six cell accuracies for both sets against a chance line. `figures/fig2_leakage_manipulation.png` ⟦FILL: regenerate once VO-D completes⟧.

### 4.5 Robustness and cost

⟦FILL: position bias per cell; within-prompt discrimination rate per cell on the main run; malformed and exclusion rates; whether the leakage contrast holds on the first 200 items per cell.⟧

Total spend to date: verification $0.0074 → smoke $0.026 → calibration $0.038 → pilot $0.295 → `VO-C` main $0.84 = **$1.13 of a $10 ceiling.** Exclusions: the style-equalised scaffold raised the N-column exclusion rate in the pilot (67/80 usable vs. 80/80 on M) because four-sentence responses sometimes fell below the 60-word floor.

## 5. Discussion and Limitations

### 5.1 What the pilot already establishes

Within this design, on this lineage, for this hidden property: **the apparent ability of a model to identify which of two personas produced a text is carried by surface style.** Remove the style difference and the ability does not degrade to a weak signal — it disappears, with the predictor assigning both of a prompt's responses to the same persona 95% of the time.

This is a negative result about an *instrument*, and it generalises further than the study it was meant to serve. Any self-prediction paradigm that reports above-chance accuracy without fitting a surface-feature classifier on the same stimuli, per condition, cannot distinguish self-knowledge from style-reading. That baseline costs nothing — ours is 18 features and a logistic regression — and in five of our eight columns it *beat the model*. It should be a default reporting requirement, not an optional robustness check.

It also arrives at Song, Lederman, Hu & Mahowald's conclusion from a different direction. They found models judging their own sampling temperature were reading style rather than accessing a parameter; we find the same failure mode in a semantic property specifically chosen to avoid it. The property was buried in *which recommendation is made*, not in register or vocabulary, and it still leaked — through sentence length, hedge rate and sentiment balance, because a persona that endorses what someone wants writes differently from one that overrides them, whatever the instruction says.

### 5.2 Interpretation of the leakage manipulation

*(Fill the branch that fires; delete the others.)*

**If the leakage contrast is clearly positive** — self-advantage present on `VO-C`, absent on `VO-D` — the style-matching account is supported directly, under a capability control that earlier tests lacked. The reading is that self-advantage in this paradigm is an artefact of the self model being better at reading a surface cue it also produced, not a same-weights residual.

**If the contrast is ≈ 0 with a self-advantage present on both sets**, something survives the removal of the surface cue, and that is the Binder-side result. It would still only license "unusually well-fit to its own output distribution" — never introspection or memory of having produced the text.

**If the contrast is ≈ 0 with no self-advantage on either set** — the outcome §4.3 predicts, since the `VO-D` self cells already sit at chance — the manipulation is uninformative about the two accounts, because there is no effect to remove. We would report that plainly: on clean stimuli the task is not performable by anyone, so it cannot discriminate the hypotheses, and the study's contribution is §4.3 alone.

### 5.3 Limitations

- **Scope ceiling.** Same-weights behavioural self-modelling only. Nothing here bears on same-episode memory (prediction happens in a fresh session), activation-level introspection in Lindsey's sense, internal-state awareness, or consciousness. The study did not reach even the ceiling it set.
- **`VO-D` was written after seeing `VO-A/B/C` fail.** This is a second pass. The band was fixed beforehand and never moved, the stop rule ("if VO-D also fails on M, no fifth pair") was declared before `VO-D` ran, and all four pairs are reported. But it is a second pass, and it is recorded as amendment A1 rather than absorbed silently.
- **A4 reverses A3 on the record.** We first took the preregistered Level-3 branch (no main run) and then reversed it to run the leakage manipulation. The reversal is documented with its reasoning and its date, and the A4 analysis was specified before any of its cells were run — but a reader should know the primary contrast was chosen after the pilot, not before it.
- **The similarity axis is weak.** Δ = +2.1 pp with a CI spanning zero (§4.2). The near/far ordering was accepted on a deliberately weak point-estimate rule chosen in advance for good reasons, but it means "far-self" is not established as meaningfully further than "near-self." Any conclusion resting on the near-vs-far contrast should be discounted accordingly.
- **One implementation of style-equalisation.** `VO-D` is a single scaffold. A different one might separate D from Self rather than collapsing both — that is the most important thing a follow-up should try, and until someone does, "closing the leak removes the signal" is a finding about this scaffold.
- **`VO-D`'s clean cells were only ever run as Self.** In the pilot, `VO-D` ran M→M and N→N only, so the pilot alone says nothing about self-versus-other. That is precisely what §4.4 exists to supply.
- **Four pairs is a small sample of stimulus designs**, and the N column rests on less data than M (67/80 usable) because short responses fell below the word floor.
- **"Same weights" is verified at the host, not the checkpoint.** DeepInfra fp8 pinning with 20/20 temperature-0 determinism is the best available evidence; a silent backend change mid-run is auditable from the logs but not preventable. Whether Hermes-3 is a full or parameter-efficient fine-tune is not stated on the model card and we did not verify it.
- **Not a replication of Binder et al.**, who finetune both models on ~30k examples. Nothing here speaks to whether their finetuned effect is real.
- **Generation temperature was 1.0 and provider seed reproducibility is unverified**, so the logged texts are the reproducible artefact, not the sampling.

### 5.4 Future work

The obvious next step is other style-equalisation scaffolds: the finding that matters is whether *any* stimulus design yields a property models can read and surface features cannot, or whether the two are inseparable for persona-like properties in general. Beyond that: run the leakage manipulation across several lineages; test whether a parameter-efficient sibling and a full fine-tune sibling of one base give different residuals, which would put a scale on "how much shared weight is enough"; and apply the surface-baseline gate retrospectively to published self-prediction results, where our five-of-eight columns suggest it may not be a formality.

## 6. Conclusion

We set out to ask whether a model has a self-prediction residual once its general classification ability is controlled, and built a crossed design on a verified same-base model pair to answer it. The pilot answered a prior question instead: on this hidden property, what the model recovers is style. Self-prediction accuracy tracked an 18-feature surface classifier at r = +0.68, that classifier beat the model in five of eight columns, and a stimulus set engineered to equalise style drove both to chance together — the model assigning both of a prompt's responses to the same persona in 95% of cases.

⟦FILL: two or three sentences on the leakage manipulation's outcome and what it licenses.⟧ The transferable lesson is cheaper than the study that produced it: a surface-feature baseline, fit per condition on the same stimuli, is the minimum evidence that a self-prediction result is about the self at all. We could not have known which side of the Binder/Song disagreement our data fell on without it — and neither, we suspect, can anyone else.

---

## Code and Data

- **Code:** ⟦FILL: GitHub URL⟧ — `src/selfpred/` (pinned OpenRouter client with pre-request budget guard, persona generation, prediction runner, 18-feature surface baseline, prompt-clustered bootstrap/McNemar/interaction), `scripts/` (verification, pipeline, figures), `tests/`.
- **Data:** append-only per-call JSONL for every phase (request parameters, returned model and provider, tokens, cost, timestamp, prompt hash); frozen calibration items and stimulus sets with content hashes; generated texts with labels stored in a separate directory from predictor inputs; `data/results/*.json`.
- **Preregistration:** `02_design_audit.md` — 15 signed decision rows plus amendments A1–A4, each with reason, status and outcome. Supporting records: `04_model_verification.md`, `06_hermes_smoke_test.md`, `07_calibration_results.md`, `08_pilot_results.md`, `09_pilot_finding.md`. The adversarial design review that produced the crossed design is in `03_design_review_and_implementation_plan.md` and `notes/council-transcript-2026-08-15.md`.

## Author Contributions

U.H. led the experimental design and statistical reasoning, designed the calibration probe and bootstrap analysis, and implemented the client, pipeline and analysis. J.C. led the literature grounding, designed the hidden-property task and the four persona pairs including the style-equalising scaffold, and owned the pilot feasibility judgment. Both authors contributed to interpretation and to the final manuscript.

## References

1. Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2025). *Looking Inward: Language Models Can Learn About Themselves by Introspection.* ICLR 2025. arXiv:2410.13787. https://arxiv.org/abs/2410.13787
2. Song, S., Hu, J., & Mahowald, K. (2025). *Language Models Fail to Introspect About Their Knowledge of Language.* COLM 2025. arXiv:2503.07513. https://arxiv.org/abs/2503.07513
3. Song, S., Lederman, H., Hu, J., & Mahowald, K. (2025). *Privileged Self-Access Matters for Introspection in AI.* arXiv:2508.14802. https://arxiv.org/abs/2508.14802
4. Lindsey, J. (2026). *Emergent Introspective Awareness in Large Language Models.* Anthropic. arXiv:2601.01828. https://arxiv.org/abs/2601.01828

*⟦VERIFY: author lists and arXiv IDs against the papers before submission.⟧*

## Appendix

**A. The four persona clause pairs, verbatim**, and the two generation scaffolds (original and style-equalised). ⟦FILL⟧

**B. One worked source prompt with both persona outputs under each scaffold** — the clearest way to show what style-equalisation did. ⟦FILL⟧

**C. Predictor system prompt and template** (frozen; 0% malformed on both models at full input length). ⟦FILL⟧

**D. Calibration probe: 50 items, A/B randomisation seed, per-model answers.** ⟦FILL⟧

**E. Surface baseline: the 18 features, model class, grouped cross-validation procedure.** ⟦FILL⟧

**F. Verification record.** 311 calls across 11 models, with the re-alias check, 20-repeat determinism measurement and 30-call concurrency burst; the enactment smoke test with pre-declared criteria (`06_hermes_smoke_test.md`).

**G. Amendments A1–A4 in full**, with dates, reasons and outcomes.

**H. Cost record.** Verification $0.0074; smoke $0.026; calibration $0.038; pilot $0.295; `VO-C` main $0.84. ⟦FILL: `VO-D` main, total.⟧

## LLM Usage Statement

We used Claude (via Claude Code) throughout: for literature retrieval and summarisation; as an adversarial reviewer of the experimental design — a structured multi-advisor critique identified the capability confound and the prompt-clustering issue and produced the crossed design; for drafting candidate dilemma prompts and persona clauses, all human-screened before freezing; for implementation of the data-collection pipeline; and for drafting and editing this report. All experimental results and statistical estimates come from our own logged API runs and analysis code and were verified against the raw per-call logs. Every model ID, provider, price and rate is read from returned API metadata, not from model-generated assertions. Both authors reviewed and revised the final text.
