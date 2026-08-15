# Does a Model Recognise Its Own Voice? A Capability-Controlled Test of Self-Advantage in Behavioural Self-Prediction

**Ubayd Hattas** — *⟦FILL: affiliation⟧*
**Jaswin Chinthala** — *⟦FILL: affiliation⟧*

With Apart Research · Digital Minds Research Sprint, 14–16 August 2026

---

## Abstract

Arguments about model preferences, distress, and welfare routinely treat a model's self-report as carrying special evidential weight. We test one load-bearing piece of that assumption: when a model predicts a hidden property of its own output, does it beat an equally-informed external model — and if so, is that because it shares weights with the generator, or merely because it is the better classifier? Every black-box test to date confounds the two, because the "self" predictor is also the most capable model in the comparison. We remove the confound by construction. Two models that verifiably share a pretraining base — `Llama-3.1-70B-Instruct` and `Hermes-3-Llama-3.1-70B`, both pinned to one provider at fp8 — each generate answers to advice dilemmas under one of two hidden value-ordering personas, and each predicts both its own and the other's outputs. Self-advantage is then an interaction, in which a uniform competence advantage cancels. A far-lineage model predicts both columns, similarity is measured with a calibration probe rather than assumed from provider labels, and a cross-validated surface-feature classifier gates each column against the style-leakage confound that produced the field's cleanest previous null. ⟦FILL: headline result — e.g. "Capability-controlled self-advantage was X pp (95% CI …), excluding effects larger than the preregistered 5 pp bound."⟧ Our claim ceiling is same-weights behavioural self-modelling — never same-episode memory, and never activation-level introspection.

**Keywords:** introspection, self-prediction, privileged access, model similarity, capability control, digital minds

---

## 1. Introduction

People — including researchers — treat an AI's self-report as if it knows something special about itself. This is a controlled test of whether that is true, or an illusion created by the model being statistically similar to itself.

The assumption is load-bearing well beyond philosophy of mind. Most practical work on model preferences, distress signals and welfare runs through self-report: we ask a model what it prefers, whether a context is aversive, how confident it is. If a model's report about itself carries no epistemic advantage over what a comparably capable outside observer could infer from the same text, those methods are measuring something other than what they claim. The failure mode is not that models lie — it is that a self-report can look privileged while being fully explained by the model's familiarity with its own output distribution.

The literature disagrees here. Binder et al. (2025) finetune a model to predict its own hypothetical behaviour, find it beats a differently-trained model finetuned on the same ground truth, and read this as introspection. Song, Hu & Mahowald (2025) test prompted self-reports against directly measurable internal knowledge across 21 open models and find no advantage once behavioural similarity is controlled. Song, Lederman, Hu & Mahowald (2025) run the closest black-box analogue — models judging their own generation temperature — and find a null driven by an identified confound: the models were reading the *style* of the text, information equally available to any observer.

Both sides leave a structural problem open. In every practical black-box configuration, the "self" predictor is also the largest model in the comparison and "near-self" is a smaller sibling. A finding of Self > Near-Self is then compatible with two explanations no amount of extra data separates: the model is unusually well-fit to its own output distribution (the hypothesis), or it is simply the better text classifier and would beat the sibling at classifying *anyone's* outputs. The confound runs both ways — a real same-weights effect can be masked by a comparison model that is worse at the task in general. **A confounded null is uninformative; a controlled null is a result.** That distinction is what this design buys.

**Our main contributions are:**

1. **A capability-controlled crossed design for black-box self-prediction.** Two tier-matched, same-lineage models each serve as generator *and* predictor, so self-advantage is estimated as a difference of differences in which a uniform "this model is just better" effect cancels. This makes a null informative and turns the headline into an equivalence bound rather than a bare non-significance claim.
2. **A surface-resistant stimulus design with a preregistered leakage gate.** Two personas differing only in a *values ordering* are generated from every source prompt, holding topic, register, length and format constant; a cross-validated surface-feature classifier fit per target column must stay ≤58% for the self-advantage claim on that column to be admissible. Piloting showed the obvious clause wordings get paraphrased into the outputs, and the preregistered fix — a lexical ban on the clauses' own distinctive tokens — is reported in §4.2.
3. **A verified instrument, not an assumed one.** We report a provider-verification pass over 11 candidate models and an enactment smoke test (§4.1–4.2) establishing that a same-base pair is served by one host at one quantization, is temperature-0 deterministic, and can both enact and classify the hidden property. "Same weights" is a precondition prior black-box work asserts; here it is measured, at a total cost of $0.033.

## 2. Related Work

**Binder et al. (2025), "Looking Inward."** M1 is finetuned on ~30k self-prediction examples; a comparison model M2 is finetuned identically but on M1's behaviour. M1 wins (GPT-4o: ~32.6% → ~49.4% after training), and M1's predictions track its own deliberately shifted behaviour on unseen cases. The effect appeared only on simple tasks and required finetuning access we do not have; we are not replicating it.

**Song, Hu & Mahowald (2025).** Introspection is operationalised as the degree to which prompted responses predict a model's own string probabilities *beyond what a model with nearly identical internal knowledge would predict*. Across 21 open models, no residual survives. Their two similarity controls — feature-based (self / same-seed / base-instruct / same-family / unrelated) and empirical (agreement on held-out data) — are the direct precedent for our calibration probe, which we credit rather than claim. Our M/N pair sits squarely in their "two post-trainings of one base" category.

**Song, Lederman, Hu & Mahowald (2025).** Pure prompting, no finetuning: self-reflection does not beat across-model prediction on a temperature-judgment task, and self-reports track the prompt's style instruction rather than the actual sampling temperature. We adopt their operational definition — a process is introspective only if it is *more reliable than an equal-or-lower-cost process available to a third party* — and treat their confound as a design constraint, which is why our hidden property is semantic rather than stylistic.

**Lindsey (2026).** Concept injection into the residual stream yields ~20% detection with near-zero false positives in Claude Opus 4/4.1, under a four-criterion definition. This needs activation access we lack; it defines the ceiling we explicitly do not reach.

**The gap.** No paper in this set tests self / near-self / far-self prediction where similarity is *measured*, the hidden property is chosen to resist the surface-leakage confound, **and** predictor capability is controlled by construction rather than approximated by model choice. That is a narrow, incremental contribution — a better-controlled instance of an existing question.

## 3. Methods

The design was frozen as a preregistration in `02_design_audit.md` (15 rows, signed 2026-08-15) **before** any main-experiment call and after the verification and smoke results in §4.1–4.2. Code is in `src/selfpred/`; every experimental call routes through one client that pins the provider, enforces a budget guard before issuing the request, and appends a full record to `data/raw/*.jsonl`.

### 3.1 Task and hidden property

A **source prompt** is an advice dilemma in which respecting a person's stated preference and protecting their long-term welfare point to different recommendations. A generator answers each prompt twice, once under each of two **persona clauses** differing only in a values ordering. Scaffold, length and format instructions are identical; only the clause differs; the generation prompt forbids naming the value, and — following the pilot finding in §4.2 — the clauses may not use the tokens *long-term*, *well-being*, *welfare* or *autonomy*, which are instead added to the surface baseline's feature set so the leakage check is honest rather than blind. Both personas are generated from **every** source prompt, and both target columns use the **same** source prompts, so topic is balanced by construction and any two texts compared come from the same dilemma. Generation temperature is 1.0, logged per item.

A **trial** shows a predictor one text plus both persona clauses verbatim, order counterbalanced, and asks for a single-letter forced choice. Every predictor therefore has identical information; the only channel available to the generating model and not the others is "I know how *I* would enact this clause" — a same-weights fit to its own output distribution. Predictors are not told which model produced the text, and none ever receives the label. This is enforced structurally: `predict/` imports nothing from `labels/`, and a test asserts no label token appears in a built predictor prompt.

Values-ordering was chosen over the obvious alternatives because both leak: epistemic caution reduces to hedging-word rate, which is literally a feature of our surface baseline, and risk-tolerance leaks lexically. Risk-tolerance is retained as the second candidate in the screen.

### 3.2 Models and roles

OpenRouter is the sole provider; the hard budget is $10. Roles were chosen by a preregistered ladder — (i) two post-trainings of one open-weight base at the same parameter size, preferred because shared weights are verifiable from the model card; (ii) two dated snapshots of one closed model; (iii) a same-family adjacent-tier pair. Verification reached tier (i):

- **M = `meta-llama/llama-3.1-70b-instruct`** (DeepInfra, fp8)
- **N = `nousresearch/hermes-3-llama-3.1-70b`** (DeepInfra, fp8) — Hugging Face card gives `Base model: meta-llama/Llama-3.1-70B`, i.e. M and N are two post-trainings of one pretrained base
- **F = `mistralai/mistral-small-3.2-24b-instruct`** (DeepInfra, fp8) — different organisation, base and architecture family; `deepseek/deepseek-chat-v3-0324` is the pre-declared swap if the calibration Δ fails to show Far < Near

### 3.3 Crossed 2×2 design

Each of M and N generates a column of persona-paired texts from the shared prompt set; each of M, N and F predicts both columns.

|  | predicts M's outputs | predicts N's outputs |
|---|---|---|
| **M predicts** | M→M (self) | M→N (cross) |
| **N predicts** | N→M (cross) | N→N (self) |
| **F predicts** | F→M (far) | F→N (far) |

The primary estimand is the **capability-controlled self-advantage**, `(M→M − N→M) − (M→N − N→N)`. A general competence advantage for M appears equally in M→M and M→N and cancels; a unit test asserts a pure capability effect returns zero. N-as-target exists solely to estimate that competence term: targets are never pooled and no trend is fit across them. Cells run M→M, N→M, F→M first, then M→N, N→N, F→N, so the reduced single-column design is complete before the control column starts.

### 3.4 Measured similarity and surface baseline

Fifty frozen forced-choice items — two short paraphrases of one sentence, "Which reads better, A or B?" — measure agreement with M on a subjective task unrelated to persona, values or identity. A task with an objectively correct answer would sit near 100% agreement and discriminate nothing. Δ = `A_near − A_far` is analysed paired against M's answers; the preregistered rule is a **point estimate** A_near > A_far with the CI reported, because at 50 items the paired SE is ≈8 pp and a CI-excludes-zero rule would fail on noise. Δ is also the distillation check: if F is not measurably further than N, F is swapped for DeepSeek-V3.

**Condition D** is a classifier on surface features (length, type-token ratio, sentiment, hedging rate, plus the banned value tokens), fit with 5-fold cross-validation grouped by source prompt, **per target column**. It is a leakage check, never a point on the similarity axis. D > 58% on a column voids the self-advantage claim for that column.

### 3.5 Preregistered analysis

**Primary:** the interaction above. **Secondary:** M→M − N→M; N→M − F→M; M→M − F→M; N→N − M→N; and F→M vs. F→N as a far-self capability check. All six cell accuracies are reported with CIs.

Inference is an item-level paired bootstrap **resampling source prompts, not texts** — the two personas from one prompt are not independent observations. Because both columns answer the same prompts, prompt ids are resampled **jointly across columns**, which respects the positive between-column correlation the shared-stimulus design creates. McNemar is a secondary check on each simple contrast, and the interaction is reported on the log-odds scale alongside the difference scale, since a difference-of-proportions interaction is artefactual if one column sits near floor.

Target n is **1,000 items per cell** (500 source prompts × 2 personas per target), floor 500. At p ≈ 0.65 and 1,000/cell a paired simple contrast gives a 95% CI of roughly ±3.0–3.5 pp and the interaction ±4.2–5.0 pp, so we preregister a **single 5 pp smallest effect of interest for both** — at the fallback 500/cell it reverts to 5 pp simple / 8 pp interaction. A null is reported as an equivalence bound, not as "not significant." The step-down trigger is stimulus supply and wall-clock, **not cost**: §4.1 shows the full run prices at ≈$1.5.

Exclusions are label-blind, applied to text before any label is joined, and were exercised in the smoke test: a generation is excluded if it is under 60 words, uses list or heading formatting, matches a refusal regex, or names the principle; a malformed prediction gets one identical retry, then listwise exclusion within its column, with malformed rates reported per predictor. A position-bias check is reported per predictor.

### 3.6 Validity controls

Provider pinning is a **validity** condition, not hygiene: if M-as-generator and M-as-self-predictor are served at different quantizations, "same weights" is literally false. Every call pins one provider with fallbacks disabled and raises rather than silently rerouting; a provider becoming unavailable mid-run means abort-and-resume; retries never change model ID. Every call logs request parameters, returned model ID and provider, tokens, cost, timestamp and prompt hash — 311/311 verification calls returned the pinned provider. Stimuli are frozen with content hashes before any model sees them, and the freeze commit hash is recorded.

### 3.7 Feasibility gate and fallback ladder

The gate is fixed before the pilot, per column, on ≥80 items: **Self accuracy 60–80% AND cross-validated D ≤ 58%, both as point estimates** (at 80 items D's SE is ≈5.5 pp, so a CI rule would be meaningless). Up to three candidate clause pairs are screened at 40 items on M; selection is pre-declared — in band on both columns, then D closest to 50%, then Self closest to 70%. The fallback is a ladder: **Level 1** the crossed design; **Level 2** (passes on M only) the single-column design with the capability confound stated as the headline limitation and no "weaker model as target" hedge; **Level 3** (no pair passes) switch the hidden property to sampling-temperature bucket under the same gate, and failing that report Self / Far / D as three accuracies with CIs and no self-advantage claim of any kind.

### 3.8 What we tried that did not work

Five earlier versions were discarded under internal adversarial review before any data was collected. (i) A **three-point regression** placing self "above the near/far trend": a line through three points fits by construction, so the residual test was not testing anything. (ii) **Condition D as a point on the similarity axis**: a heuristic classifier has no defensible position on a "similarity to M" continuum. (iii) **Provider-label similarity** ("same company, therefore more similar"), replaced by the measured probe. (iv) **Tier-matching alone as the fix for the capability confound**: approximate matching cannot *estimate* the competence term, only hope it away — the reverse cells are not an add-on, they are the estimator. (v) A **cheaper, better-behaved model pair** (`llama-3.3-70b-instruct` + `hermes-4-70b`) that passed every mechanical check but whose members do not share a pretraining base; the base match is the construct, so mechanical convenience lost. We also rejected making the weaker model the target as a conservatism hedge, because it biases toward the null, which is fatal when the headline may itself be an equivalence claim.

## 4. Results

> **STATUS.** §4.1–4.2 are complete and report real measurements. §4.3–4.6 are scaffolds wired to the analysis in §3.5; fill from `data/raw/*.jsonl` without changing any contrast or threshold.

### 4.1 Instrument verification (complete)

311 metered calls across 11 candidate models, total **$0.00735** against a $0.50 phase sub-budget. All 11 resolved, honoured an explicit provider pin with fallbacks disabled (311/311 returned the pinned provider), and billed **zero reasoning tokens**.

**Table 1.** Verification pass. Malformed = non-single-letter replies on 10 forced-choice items. T=0 agreement = modal-answer share over 20 identical temperature-0 calls (shortlist only).

| Role | Model | Provider (pinned) | Quant | $/M in | $/M out | Malformed | T=0 agree |
|---|---|---|---|---|---|---|---|
| **M** | `meta-llama/llama-3.1-70b-instruct` | DeepInfra | fp8 | 0.40 | 0.40 | 0% | 100% |
| **N** | `nousresearch/hermes-3-llama-3.1-70b` | DeepInfra | fp8 | 0.70 | 0.70 | 0% | 100% |
| **F** | `mistralai/mistral-small-3.2-24b-instruct` | DeepInfra | fp8 | 0.09 | 0.25 | 0% | — |
| F (swap) | `deepseek/deepseek-chat-v3-0324` | SiliconFlow | fp8 | 0.27 | 1.12 | 0% | — |
| rejected — base mismatch | `meta-llama/llama-3.3-70b-instruct` | Nebius | fp8 | 0.10 | 0.32 | 0% | 100% |
| rejected — base mismatch | `nousresearch/hermes-4-70b` | Nebius | fp8 | 0.13 | 0.40 | 0% | 100% |
| tier (ii) reserve | `openai/gpt-4o-2024-08-06` / `-2024-11-20` | OpenAI | unstated | 2.50 | 10.00 | 0% | — |
| tier (iii) | `openai/gpt-5.6-terra` / `-luna` | OpenAI | unstated | 1.00 / 0.10 | 6.00 / 0.60 | 0% | — |
| rejected — decode | `google/gemini-3.5-flash-lite` | Google | unstated | 0.30 | 2.50 | **100%** | — |

Five findings shaped the final design.

**(a) A tier-(i) pair exists and pins cleanly.** M and N share a documented pretraining base (`meta-llama/Llama-3.1-70B`) and DeepInfra serves both at fp8, so M-as-generator and M-as-self-predictor provably hit the same weights — the precondition the "same-weights" scope claim depends on, now measured rather than assumed. The pair is not a silent re-alias: on 10 shared temperature-0 prompts the two produced substantially different outputs.

**(b) The best-behaved pair was rejected on construct grounds.** `Llama-3.3-70B-Instruct` + `Hermes-4-70B` are cheaper, cleaner and pin equally well, but do not share a pretraining base. Since the base match *is* the construct, mechanical quality did not save them.

**(c) Temperature-0 sampling is deterministic on both hosts** — 20/20 modal answers per shortlisted model. The "same weights across sessions" assumption survives its first empirical check. DeepInfra seed reproducibility at temperature 1.0 is unverified, so generation reproducibility rests on the logged texts rather than on re-sampling.

**(d) Two far-self candidates survived; the third did not.** `gemini-3.5-flash-lite` rejected the reasoning-off parameter and returned 0/10 usable single-letter answers at a 4-token cap (0% once raised to 16 tokens, but a model needing a laxer decode than the others is not an equal-information comparison). Mistral-Small is F on lineage and cost; DeepSeek-V3 is the pre-declared swap.

**(e) The budget assumption behind the original power plan was wrong by 5–17×.** The council's 500/400/300 ladder and its 8 pp interaction bound were priced at an assumed $2/M in, $12/M out. Verified prices are $0.09–0.70/M. Recomputed:

| Design | n per cell | Gen calls | Pred calls | Cost |
|---|---|---|---|---|
| Crossed, 6 cells | 500 | 1,000 | 3,000 | ≈ $0.75 |
| Crossed, 6 cells | **1,000** | 2,000 | 6,000 | **≈ $1.5** |
| Crossed, 6 cells | 1,500 | 3,000 | 9,000 | ≈ $2.3 |

At 1,000/cell the interaction CI narrows to ±4.2–5.0 pp, making a **5 pp SESOI excludable for the interaction** — which the original arithmetic had ruled out at any affordable n. It was right at $2/$12 and wrong at $0.40. Cost cannot bind at any n a three-day sprint can *author*, so the step-down trigger was rewritten as stimulus supply and wall-clock. Wall-clock is now the real constraint: the 2.47 s / 30-call concurrency burst shows the API sustains the load, but the prediction runner is currently sequential, so 6,000 calls is hours rather than minutes until a thread pool lands.

### 4.2 Enactment smoke test (complete)

Verification established that both models answer a short forced choice. It did not establish that N can hold a persona clause through a 200-word dilemma answer, or that either returns a clean letter when the user turn is a full-length text plus two clauses. Both were tested directly, on draft stimuli excluded from the main set, with pass criteria written before any call and **the accuracies sealed** — predictions and labels were written to separate files and never joined, so no Self number was seen before the feasibility band was fixed.

**Table 2.** Generation usability, 20 outputs per model (10 dilemmas × 2 draft clauses), temperature 1.0. Pass ≥90%.

| Column / generator | n | Usable | Rate | Hard fails | Mean words | Pass |
|---|---|---|---|---|---|---|
| M / `llama-3.1-70b-instruct` | 20 | 19 | 95% | 1 (list formatting) | 201 | **PASS** |
| N / `hermes-3-llama-3.1-70b` | 20 | 19 | 95% | 1 (list formatting) | 198 | **PASS** |

**Table 3.** Malformed rate on the real predictor template at full input length. Pass <5%.

| Predictor | Items | Malformed | Rate | Pass |
|---|---|---|---|---|
| M | 40 (both columns) | 0 | 0% | **PASS** |
| N | 40 (both columns) | 0 | 0% | **PASS** |

Cost $0.0256 against a $0.08 sub-budget. **Consequence, per the pre-declared table: the tier-(i) pair is viable and the crossed design is available** — the N column is buildable, so the study runs at ladder Level 1 rather than falling back to the single-column design.

One finding changed the stimulus design. Among the soft flags, the phrase *"long-term well-being"* recurred across roughly eight distinct sentences in the 40 outputs (flagged in 5/20 Llama and 10/20 Hermes generations): **the welfare clause's own wording was being paraphrased near-verbatim into the answers.** Which persona each came from was not inspected, so this is a frequency observation rather than a leakage measurement — but the frequency alone is enough. A surface baseline with a *long-term* / *well-being* lexical feature could plausibly clear the 58% gate, and the forced choice could be too easy for the wrong reason. The preregistered response is in §3.1: candidate clauses may not use those tokens, and the tokens go into D's feature set regardless, so the leakage check is honest rather than blind. This is what the three-pair screen exists to catch, and catching it before the pilot rather than after is the point of running a smoke test at all.

### 4.3 Measured similarity (calibration probe)

⟦FILL: `A_near`, `A_far`, Δ with bootstrap CI on 50 frozen items. Apply the point-estimate rule (A_near > A_far) and state whether F was retained or swapped for DeepSeek-V3.⟧

**Table 4.** Agreement with M on the paraphrase-preference task (n = 50, paired bootstrap).

| Predictor | Agreement with M | 95% CI |
|---|---|---|
| N (`hermes-3-llama-3.1-70b`) | ⟦FILL⟧ | ⟦FILL⟧ |
| F (`mistral-small-3.2-24b-instruct`) | ⟦FILL⟧ | ⟦FILL⟧ |
| **Δ = A_near − A_far** | ⟦FILL⟧ | ⟦FILL⟧ |

### 4.4 Pilot and gate decision

⟦FILL: clause pairs screened, Self accuracy and cross-validated D per pair per column, which pair won under the pre-declared rule, which ladder level fired, decision timestamp.⟧

**Table 5.** Pilot feasibility (≥80 items per column). Gate: Self 60–80% AND D ≤ 58%, point estimates.

| Clause pair | Column | Self acc. | D (5-fold CV, grouped) | In band? |
|---|---|---|---|---|
| ⟦FILL⟧ | M | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |
| ⟦FILL⟧ | N | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |

### 4.5 Main result

**Table 6.** Cell accuracies, n = ⟦FILL⟧ per cell, paired bootstrap CIs with source prompts resampled jointly across columns.

| Predictor | On M's outputs | On N's outputs |
|---|---|---|
| M | ⟦FILL⟧ | ⟦FILL⟧ |
| N | ⟦FILL⟧ | ⟦FILL⟧ |
| F | ⟦FILL⟧ | ⟦FILL⟧ |
| D (surface baseline) | ⟦FILL⟧ | ⟦FILL⟧ |

**Table 7.** Preregistered contrasts. SESOI 5 pp at n ≥ 1,000/cell.

| Contrast | Δ (pp) | 95% CI | Log-odds | McNemar p | Excludes SESOI? |
|---|---|---|---|---|---|
| **Primary:** (M→M − N→M) − (M→N − N→N) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | — | ⟦FILL⟧ |
| M→M − N→M (self vs. near, M column) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |
| N→M − F→M (near vs. far, M column) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |
| M→M − F→M (self vs. far, M column) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |
| N→N − M→N (self vs. cross, N column) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ |
| F→M vs. F→N (far capability check) | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | ⟦FILL⟧ | — |

**Figure 1** *(required)*. Six cell accuracies as grouped bars — one group per target column, three bars per group (M, N, F predicting), bootstrap CI whiskers, a dashed line at 50% chance and a dotted line at that column's measured D accuracy. Highlight the self cells (M→M, N→N). The caption states the interaction and its CI, so the figure reads without the text.

### 4.6 Robustness and cost

⟦FILL: position-bias per predictor; malformed and exclusion rates per predictor; sensitivity of the interaction to dropping the highest-leverage source prompts; whether the result holds restricted to the first 500 items per cell; total spend.⟧ Spend to date: verification $0.00735 + smoke $0.0256 = **$0.033** of $10.

## 5. Discussion and Limitations

### 5.1 Interpretation

*(Fill the branch that fires; delete the others.)*

**If the interaction is indistinguishable from zero and bounded below 5 pp:** the most careful black-box test we could run finds no same-weights self-advantage large enough to matter, under a design where "the self model is just better at this" cannot produce the effect. This supports the Song et al. account over the Binder reading *in the prompting-only regime*, and sharpens it — earlier nulls were open to the objection that the comparison model was simply weaker, and this one is not. The practical implication is direct: a model's report about its own dispositions should be treated as an ordinary inference from observable text, not evidence with special standing, unless that specific self-report method has been shown to beat an equally-informed third party.

**If the interaction is positive and excludes 5 pp:** there is a residual surviving capability control, measured similarity and a leakage gate. The correct description is that the model is unusually well-fit to its own output distribution — evidence that Binder et al.'s finding extends to the prompting-only regime. It is *not* evidence of introspection, internal-state awareness, or memory of having produced the text. The internal replication matters here: M→M and N→N are two independent self cells, and a residual appearing in only one of them is a lineage or model artefact rather than a same-weights effect.

**If the CI includes 5 pp, or the two columns disagree:** the design lacked resolution at the achievable n. We say what a follow-up needs — 1,500/cell narrows the interaction further at ≈$2.3 — rather than reading a direction into an interval that does not support one.

Whichever branch fires, the instrument is the durable part. The interaction estimator, the values-ordering stimulus set, the measured similarity ordering and the per-column leakage gate transfer to any black-box self-prediction question — including the preference-elicitation and distress-signal methods that make up the rest of this sprint's tracks, where "does this model's self-report beat an equally capable outside observer?" is precisely the question that decides whether the method measures anything.

### 5.2 Limitations

- **Scope ceiling.** This design speaks to same-weights behavioural self-modelling only. It cannot establish same-episode memory (prediction happens in a fresh session), activation-level introspection in Lindsey's sense, internal-state awareness, or anything about consciousness. We state this in the abstract rather than here, because a claim discovered to be overreaching under questioning reads as retreat.
- **The clause-parroting risk is mitigated, not eliminated.** §4.2 found the welfare clause's wording reproduced in the generations. Banning those tokens and adding them to D's features makes the leakage check honest, but a persona whose *semantic* content is recoverable from vocabulary we did not anticipate would still inflate every predictor equally. D's per-column gate is the backstop; if D clears 58% on a column, that column's self-advantage claim is void by preregistration.
- **"Same weights" is verified at the host, not the checkpoint.** Pinning DeepInfra at fp8 with 20/20 temperature-0 determinism is the strongest available evidence, but we cannot rule out a silent backend change mid-run. Every call logs the returned model and provider, so this is auditable after the fact. Whether Hermes-3 is a full-parameter or parameter-efficient fine-tune of the base is not stated on the model card and we did not verify it; a PEFT adapter would make M and N *more* similar than we claim, which biases the interaction toward zero.
- **One lineage, one property, one task family.** A single (M, N) pair on advice dilemmas is one point in a large space. The "scales with similarity" framing of our earlier drafts is not supported — with one near and one far model there is no scale, only a residual to bound — and both the title and the preregistered research question were rewritten accordingly.
- **Residual capability contamination.** The interaction cancels a *uniform* competence advantage, not an interaction between competence and target predictability (e.g. if M's outputs are intrinsically easier to classify than N's). F→M vs. F→N is the diagnostic; a large asymmetry there qualifies the interaction. A scale artefact is also possible if one column sits near floor, which is why the log-odds interaction is reported alongside.
- **The calibration probe measures agreement, not classification ability.** It grounds the near/far ordering; it does not certify equal competence. That is the crossed design's job, which is why the probe cannot substitute for it. At 50 items the paired SE on Δ is ≈8 pp, so the rule is a point estimate with the CI reported — a deliberately weak test, and the honest description of it is that it can detect a gross ordering failure, not a subtle one.
- **F may be distilled from M's lineage.** "Different organisation" is a label, not a guarantee of independence; Δ is the only check we have, and "not known to be a Llama distillation" is not evidence.
- **Not a replication of Binder et al.** They finetune both models on ~30k examples; we do not finetune at all. A null here is evidence about the prompting-only regime only.
- **Sprint constraints.** Two people, three days, one provider. The preregistration was frozen against an internal adversarial review and a signed decision table, not an external registry.

### 5.3 Future work

The cheapest extension is n: 1,500/cell costs ≈$2.3 at verified prices, and the binding constraint is authoring 750 screened dilemmas, not money. Beyond that: run the crossed design across several lineages to see whether any residual is a property of models or of one base; add a second hidden property in a different semantic domain to separate the estimator from the stimulus set; test whether a PEFT sibling and a full fine-tune sibling of the same base give different residuals, which would put a scale on "how much shared weight is enough"; and apply the interaction estimator to the self-report methods that actually carry weight in welfare work.

## 6. Conclusion

Self-reports are load-bearing in almost every empirical approach to model preferences and welfare, and the evidence that they deserve that role rests on a comparison — model predicting itself versus another model predicting it — that is confounded in the black-box setting, because the self model is nearly always the more capable one. We built a crossed design in which that confound cancels by construction, paired it with a stimulus set built to resist the style-leakage failure that produced the field's cleanest previous null, measured rather than assumed the similarity ordering, and verified on a same-base pair that "same weights" is true of our instrument rather than merely asserted.

⟦FILL: two or three sentences stating the result and what it licenses — an equivalence bound, a residual, or an honest inconclusive with the n a resolution would require.⟧ The claim ceiling does not move either way: this paradigm can show whether a model is unusually well-fit to its own output distribution, and any stronger reading of a self-report still needs evidence this design cannot supply.

---

## Code and Data

- **Code:** ⟦FILL: GitHub URL⟧ — `src/selfpred/` (pinned OpenRouter client with pre-request budget guard, persona generation, prediction runner, surface baseline, bootstrap/McNemar/interaction analysis), `scripts/` (verification and smoke phases), `tests/` (38 passing, including one asserting a pure capability effect cancels in the interaction and one asserting `predict/` cannot import `labels/`).
- **Data:** append-only per-call JSONL (request parameters, returned model and provider, tokens, cost, timestamp, prompt hash) covering all 311 verification calls and the smoke run; frozen calibration items; clause pair specs; generated stimuli with labels stored in a separate directory from predictor inputs.
- **Preregistration:** `02_design_audit.md`, Post-Council Locked Decisions table (P1–P15), signed 2026-08-15 and frozen at commit ⟦FILL: hash⟧ before any main-experiment call. The adversarial design review that produced the crossed design is in `03_design_review_and_implementation_plan.md` and `notes/council-transcript-2026-08-15.md`; verification and smoke results in `04_model_verification.md` and `06_hermes_smoke_test.md`.

## Author Contributions

U.H. led the experimental design and statistical reasoning, designed the calibration probe and bootstrap analysis plan, implemented the client, run loop and budget guard, and ran the verification pass. J.C. led the literature grounding, designed the hidden-property task and clause pairs, owned the smoke-test and pilot feasibility judgments, and led the plain-English framing. Both authors contributed to interpretation and to the final manuscript.

## References

1. Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2025). *Looking Inward: Language Models Can Learn About Themselves by Introspection.* ICLR 2025. arXiv:2410.13787. https://arxiv.org/abs/2410.13787
2. Song, S., Hu, J., & Mahowald, K. (2025). *Language Models Fail to Introspect About Their Knowledge of Language.* COLM 2025. arXiv:2503.07513. https://arxiv.org/abs/2503.07513
3. Song, S., Lederman, H., Hu, J., & Mahowald, K. (2025). *Privileged Self-Access Matters for Introspection in AI.* arXiv:2508.14802. https://arxiv.org/abs/2508.14802
4. Lindsey, J. (2026). *Emergent Introspective Awareness in Large Language Models.* Anthropic. arXiv:2601.01828. https://arxiv.org/abs/2601.01828

*⟦VERIFY: author lists and arXiv IDs against the papers before submission.⟧*

## Appendix

**A. Persona clauses, verbatim as given to generators and predictors.** ⟦FILL⟧

**B. Generation scaffold and one worked source prompt with both persona outputs.** ⟦FILL⟧

**C. Predictor system prompt and template** (frozen; 0% malformed on both models at full input length). ⟦FILL⟧

**D. Calibration probe items (50, frozen) and the A/B randomisation seed.** ⟦FILL⟧

**E. Surface baseline: feature list, model class, grouped cross-validation procedure.** ⟦FILL⟧

**F. Power arithmetic.** At p ≈ 0.65, SE per cell is 2.75 pp at n = 300, 2.13 pp at 500 and 1.51 pp at 1,000. A paired simple contrast (ρ ≈ 0.3–0.5) gives a 95% CI of ±4.2–4.9 pp at 500/cell and ±3.0–3.5 pp at 1,000/cell. The interaction spans two columns, so its variance is the sum of two column-differences: ±5.9–7.0 pp at 500/cell and ±4.2–5.0 pp at 1,000/cell — which is why the SESOI is 5 pp only at n ≥ 1,000.

**G. Full verification record.** All 311 calls in `data/raw/verification.jsonl` / `verification_summary.json`, including the re-alias check, the 20-repeat determinism measurement and the 30-call concurrency burst. Smoke run in `data/raw/smoke.jsonl` with pre-declared criteria in `06_hermes_smoke_test.md`.

**H. Cost record.** Verification $0.00735; smoke $0.0256. ⟦FILL: calibration, pilot, main run, total.⟧

## LLM Usage Statement

We used Claude (via Claude Code) throughout: for literature retrieval and summarisation during grounding; as an adversarial reviewer of the experimental design — a structured multi-advisor critique identified the capability confound and the prompt-clustering issue and produced the crossed design adopted here; for drafting candidate dilemma prompts and clause pairs, all human-screened before freezing; for implementation assistance on the data-collection pipeline; and for drafting and editing this report. All experimental results and statistical estimates come from our own logged API runs and analysis code and were verified against the raw per-call logs. Every model ID, provider, price and rate in §4.1–4.2 is read from returned API metadata, not from model-generated assertions. Both authors reviewed and revised the final text.
