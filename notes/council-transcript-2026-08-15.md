# LLM Council Transcript — 2026-08-15

**Topic:** Answers to the seven questions in Section 5 of `03_design_review_and_implementation_plan.md` (capability confound / Fix A vs Fix B, power & SESOI, budget vs time, persona hidden property), for the Track 3 sprint *Does Self-Advantage in Behavioral Self-Prediction Scale With Model Similarity?*

**Method:** Karpathy-style LLM Council run inside Claude Code — five independent advisors (Contrarian, First Principles Thinker, Expansionist, Outsider, Executor) answered in parallel; their responses were anonymized (randomized letters A–E) and peer-reviewed by five independent reviewers; a chairman synthesized the verdict. Advisor identities are revealed below; reviewers saw letters only.

**Letter → advisor mapping used in peer review:** A = The Outsider · B = The Executor · C = The Contrarian · D = The Expansionist · E = The First Principles Thinker

**Status:** advisory. Nothing here changes `02_design_audit.md` until the team edits it deliberately. Every claim about OpenRouter model availability, lineage, hosting/quantization, or pricing is an ASSUMPTION pending the verification step (real API calls).

---

# Part 1 — Framed Question (as given to every advisor)

# FRAMED QUESTION FOR THE COUNCIL

## Read these files first, in this order (absolute paths, all in the repo root C:/Users/jaswi/Downloads/Digital_Minds_Hackthon2/):
1. CLAUDE.md
2. 01_literature_grounding.md
3. 02_design_audit.md   (authoritative summary of what is currently LOCKED)
4. 03_design_review_and_implementation_plan.md  (the material under review)

## The project in one paragraph
A two-person (Ubayd + Jaswin), 3-day research sprint (Digital Minds Hackathon, Track 3) asking: "Does self-advantage in behavioural self-prediction scale with model similarity?" A Target model generates text under one of two hidden personas; then, in a fresh session, the same model (Self), a same-family sibling (Near-Self), a different-family model (Far-Self), and a surface-feature classifier (Baseline D) each try to guess which persona produced each text. Similarity between Target and Near/Far is measured empirically via an unrelated calibration probe (precedent: Song, Hu & Mahowald 2025). Pre-registered analysis: three pairwise accuracy differences (Self–Near, Near–Far, Self–Far) with bootstrap CIs. Hard constraints: $10 total API budget, OpenRouter is the SOLE provider, ~250–300 trials/condition, one Target model, no pooling of targets, no three-point regression, Baseline D never on the similarity axis, no predictor ever sees the hidden label, predetermined fallback (collapse to Self / Far / Baseline). Scope boundary: results may only ever be described as "same-weights behavioural self-modelling" — never introspection, internal-state awareness, or same-episode memory.

## The material under review (ONLY these parts of 03_design_review_and_implementation_plan.md)
- **Section 2** — the capability confound: every candidate config makes the Target the biggest/most expensive model and Near-Self a smaller sibling, so "Self > Near-Self" cannot distinguish same-weights fit from "the big model is simply a better classifier." Fix A = crossed 2x2 design (M and N each predict both M's and N's outputs; self-advantage = interaction; Far-Self predicts both). Fix B = keep the locked design but choose a tier-matched Near-Self (dated snapshots of one closed model, or two post-trainings of one open-weight base; if a tier gap is unavoidable make the Target the weaker model). Reviewer recommends "B now, A's reverse cells (N→N, M→N) as a pre-registered stretch."
- **Section 3.1** — power: at n=300, ~65% accuracy, the CI on a difference is roughly ±5–8 pp; Binder's finetuned effect was ~+15–17 pp; a prompting-only effect is likely smaller; expect a "clean null." Proposals: 300 as floor not target; paired item-level bootstrap + McNemar; pre-register a smallest effect of interest (e.g. 5 pp).
- **Section 3.2** — budget vs time: order-of-magnitude cost of the locked design ≈ $1.7, crossed design ≈ $3.1, pilot/retries ≈ $0.5–1.0 — so $10 is NOT the binding constraint; two people, three days, zero code is. Proposed Day-1 time-box: calibration probe running AND a 20-trial persona pilot done by end of Day 1. Keep a hard budget guard in code anyway.
- **Section 3.4** — persona hidden property: every predictor is TOLD both candidate personas and makes a forced choice, so all predictors get identical information; the only self-specific channel is "I know how *I* would enact persona X" (same-weights fit). Persona pair must differ in a semantic/dispositional property (risk-tolerance, epistemic caution, values ordering…), NOT register/length/vocabulary, else Baseline D solves it. Same scaffold, same length/format instructions, only the persona clause differs. Feasibility band for the pilot (proposed 55–75% Self accuracy; NOT locked) must be fixed before the pilot runs.
- **Section 5** — the seven questions.

## THE SEVEN QUESTIONS — answer all seven, in order, numbered Q1..Q7
1. **Capability confound.** Fix A (crossed design), Fix B (tier-matched Near-Self), or B-now-A-as-stretch? What does the answer imply for the locked "one target model" and "three pairwise comparisons" decisions in 02?
2. **Target model choice under Fix B.** Given OpenRouter as sole provider, which lineage gives the most literal near-self pair (dated snapshots of one closed model vs. two post-trainings of one open-weight base)? What must be verified before choosing?
3. **Power.** Accept 300/condition as floor and raise if cheap? Pre-register a smallest effect of interest — what value?
4. **Time-boxing.** Is "calibration + 20-trial pilot running by end of Day 1" the right gate, given the strategy doc's allocation (~1/5 effort on code)?
5. **OpenRouter reproducibility.** Any objection to pinning provider / disabling fallbacks / logging per-call metadata as mandatory? Anything missing? (Answer BRIEFLY at the level of principle — Section 3.3 mechanics are being handled separately; do not relitigate them.)
6. **Persona design.** Which dispositional dimension is most likely to land in the feasibility band while resisting surface detection?
7. **Anything the review missed** — restricted to Sections 2, 3.1, 3.2, 3.4.

## HARD CONSTRAINTS on every answer
- 3 days, two people, hard $10 API budget, OpenRouter sole provider. Do NOT propose experiments outside that envelope (no finetuning, no logprob-dependent designs unless you flag them as needing verification, no extra providers).
- Locked decisions in 02 are not reopened casually. If your answer requires changing one, name EXACTLY which locked decision (by its heading in 02) and give the replacement wording.
- You cannot verify what OpenRouter offers. Label EVERY claim about model availability, model lineage, snapshot dates, or pricing as **ASSUMPTION**. A verification step with real API calls runs afterwards.
- Scope boundary from 01 holds: nothing may be described as testing introspection, internal-state awareness, or same-episode memory — only same-weights behavioural self-modelling.
- Do NOT spend words on Section 3.3 (OpenRouter mechanics), Section 4 (repo hygiene), or Sections 6/7 (implementation plan).

## What's at stake
The team is about to lock the design and start coding. A wrong call on Q1 means the headline result (positive or null) is uninterpretable to a hostile reviewer. A wrong call on Q4 means the write-up/interpretation time gets squeezed. Q6 determines whether the pilot lands in the feasibility band at all or triggers the fallback.

---

# Part 2 — Advisor Responses (round 1, independent)

## Response C — The Contrarian

**Q1 — Capability confound.** "B now, A as stretch" is the worst option on the table: it locks an uninterpretable primary result and promises a control that a two-person, zero-code sprint will never build. Stretch goals in 3-day sprints have a survival rate near zero. Fix B is also weaker than Section 2.3 admits: two post-trainings of one base differ in exactly the thing that governs persona enactment (post-training), so "tier-matched" doesn't match on the relevant capability; and dated snapshots may be so close that Near *is* Self and the calibration probe can't tell them apart. Choose Fix A outright. Required edits to 02: **Main Experiment Scope → "One target model"** becomes "Two generating models (M, N) used only as a crossed control; never pooled; no regression"; **Statistical Analysis → "Three pre-registered pairwise comparisons"** becomes "Primary contrast: interaction (M→M − N→M) − (M→N − N→N), item-level paired bootstrap; secondary: the two simple self-vs-cross contrasts and F→M vs M→M"; **Locked decision 1 "Exactly one Self condition"** becomes "Two self cells (M→M, N→N), one Far predictor on both targets." Note Fix A still leaves Near–Far and the calibration probe itself capability-contaminated (two strong models agree more) — say so in limitations.

**Q2 — Lineage.** Dated snapshots of one closed model (ASSUMPTION: OpenRouter exposes them; ASSUMPTION: some are deprecated without notice) are the safer choice, but for a reason the review missed: closed models have one host, so "same weights" for Self actually holds. Open-weight IDs on OpenRouter are served by multiple hosts at different quantizations (ASSUMPTION), so generation and Self-prediction could hit different weights — your scope claim "same-weights self-modelling" dies silently. Verify before choosing: both IDs exist and return the pinned ID/provider; both survive 72 hours; reasoning can be disabled; the pair is not a re-alias (temperature-0 outputs on the 50 calibration items must not be identical); pricing (ASSUMPTION for every number in 3.2).

**Q3 — Power.** A 5 pp SESOI at n=300 is dishonest: half-width ~6 pp means you cannot exclude 5 pp, so the "clean null" is just an uninformative one. And the Fix A interaction has roughly twice the variance of a simple difference. Either pre-register SESOI = 8 pp (what n=300 can actually bound) or push to 500–600 items per cell — cost still under $10 (ASSUMPTION), the constraint is unattended runtime, not money. Predictions parallelize; generation is one model. Pick 500 and 8 pp; state the null as "effects >8 pp excluded."

**Q4 — Time-box.** "Running by end of Day 1" is a soft gate: it doesn't produce a decision. With a 20-trial pilot the SE is ~11 pp — it cannot distinguish 55% from 75%, so the feasibility gate is noise and the fallback triggers on a coin flip. Make the pilot 60–80 items, and make the gate "GO/FALLBACK decided by noon Day 2, main run launched by Day 2 evening." The "1/5 effort on code" allocation is fiction; it will be 40%. Cut McNemar and the determinism re-run rather than pretend.

**Q5 — Reproducibility.** No objection to mandating. Missing: pre-declare what happens when the pinned provider is unavailable mid-run (abort and resume, never switch), and require generation and Self-prediction to hit the identical provider — that *is* the same-weights claim.

**Q6 — Persona.** Every candidate in 3.4 leaks. Epistemic caution = hedging-word rate, which is literally a Baseline D feature. Risk-tolerance leaks lexically ("safe", "risky"). Values-ordering (e.g., loyalty vs. fairness, autonomy vs. welfare) is the least bad because the difference is content-level and needs semantic reading — but only if items are dilemmas where both personas argue in the same register, and generation prompts forbid naming the value. The feasibility band must be joint: Self 55–75% AND D at chance ± its CI; a pilot that checks Self alone is a pilot that lets D win.

**Q7 — Missed.** (1) 3.1 pre-commits to a "clean null" narrative before data; write the interpretation for both outcomes now. (2) Persona refusals or half-enacted outputs need a label-blind exclusion rule, fixed before the pilot. (3) 3.4's "identical information" claim is only true if persona descriptions given to predictors don't name surface cues — otherwise Self collapses to D. (4) Distillation: Far may be trained on Target outputs, so "far" is an assumption the calibration probe must confirm, not decorate.

---

## Response E — The First Principles Thinker

**Q1 — Capability confound.** Strip it back: the estimand is "accuracy attributable to shared weights, net of (a) predictor competence and (b) target predictability." Fix B reduces (a) but cannot *estimate* it — "approximately matched" is a hope, and 2.3's own con admits a reviewer can still ask "how do you know?" The only cheap way to answer is to measure N classifying something that isn't M — which is the M→N/N→N cell. So Fix B without reverse cells is unfalsifiable on exactly the point at stake, and Fix A is not an add-on, it is the estimator. Since the pipeline is parameterised by target model anyway, A costs ~$1.4 more (3.2) and near-zero extra code. Answer: **A as the primary design, B as the model-selection rule that makes A's interaction interpretable** (tier-matched siblings keep the cross cells near ceiling-free range). Locked changes required in `02`: *Main Experiment Scope → "One target model"* becomes "One target lineage: two same-lineage models (M, N) each serve as target and predictor in a crossed 2×2 control; targets are never pooled into a trend." *Statistical Analysis → three pre-registered pairwise comparisons* becomes "Primary contrast: interaction (M→M − N→M) − (M→N − N→N), item-level paired bootstrap. Secondary: the three original pairwise contrasts on M as target, plus F→M and F→N." "No pooling / no three-point regression" stays intact — two targets are a control, not points.

**Q2 — Lineage.** "Near-self" means *shares weights*. Two dated snapshots of a closed model share a brand name; whether they share a training run is undisclosed (**ASSUMPTION**). Two post-trainings of one open-weight base demonstrably share pretraining weights via model cards, e.g. an official Instruct vs. a community fine-tune of the same base (**ASSUMPTION** that a same-base pair exists on OpenRouter). Prefer open-weight. Verify before choosing: both IDs served by *one* pinnable provider at the same quantization (**ASSUMPTION** OpenRouter exposes this); reasoning-off honoured; malformed one-letter rate < ~2%; model card confirms identical base; both pass the persona pilot.

**Q3 — Power.** 3.1's ±5–8 pp is for a single difference. The interaction is a difference of differences: variance roughly doubles, so at n=300/cell expect ~±8–11 pp, tightening to ~±6–8 with pairing. Take n=500/cell (crossed cost ≈ $5, still half the budget). Pre-register SESOI = 5 pp *and* state honestly the design rules out effects above ~8 pp — an equivalence bound, not a wish.

**Q4 — Time-box.** Right gate, wrong order and wrong size. The pilot decides GO/FALLBACK, and FALLBACK deletes Near-Self, which changes whether calibration matters at all — so verification calls (hour 1) → pilot → calibration, not calibration first. And 20 trials cannot judge a 20-pp-wide band (SE ≈ 11 pp at p=0.65). Phase D's ~80 items (SE ≈ 5 pp) is the real number; 3.2 should be corrected to match.

**Q5 — Reproducibility.** No objection. Missing at the level of principle: pinning is a *validity* requirement, not just reproducibility — if M-as-generator and M-as-predictor are served by different providers/quantizations, "same weights" is literally false. Pin M's provider identically across both roles.

**Q6 — Persona.** Risk-tolerance and epistemic caution leak straight into the surface features Baseline D is built on (hedging rate, sentiment). Values-ordering (e.g. autonomy-over-welfare vs. welfare-over-autonomy) forces the reader to reconstruct a preference from *what is recommended*, not how. It only carries signal if the task prompts are dilemmas where the two values genuinely conflict; on neutral prompts the persona clause is inert and everyone sits at 50%. Make the feasibility band two-sided: Self in 55–75% **and** D ≤ ~58%; otherwise you are in the band for the wrong reason.

**Q7 — Missed.** (1) 3.1 never recomputes power for the interaction (see Q3). (2) 3.4 doesn't fix whether predictors are told *who* generated the text; identical information across predictors demands one answer, pre-registered — I'd tell nobody, since same-weights fit does not require self-recognition. (3) Forced choice needs A/B position counterbalancing and a position-bias check per predictor. (4) The research question says "scale with similarity," but with one Near and one Far there is no scale — the honest headline the crossed design actually supports is "is there a same-weights residual after a tier-matched sibling and a capability control." Say that.

---

## Response D — The Expansionist

**Q1 — Capability confound.** Take Fix A now, with Fix B's model choice inside it. Section 3.2 prices the crossed design at ≈$3.1 versus ≈$1.7 — you buy a second, independent test of the hypothesis (N→N) and a full capability control for about $1.40. That is the best value in the whole sprint. Run cells in the order M→M, N→M, F→M first (so the locked design is complete on Day 2 regardless), then M→N, N→N, F→N. The stretch cells are then the ones you can drop, not the ones you hope for. Locked decisions to change: (a) **Main Experiment Scope — "One target model"** → "Two generation sources, M and N, used only as crossed controls; never pooled; no regression across targets." (b) **Statistical Analysis — "Three pre-registered pairwise comparisons"** → "Primary contrast: interaction (M→M − N→M) − (M→N − N→N), item-level paired bootstrap CI. Secondary: the three original pairwise differences on M's outputs, plus F→M vs F→N as a capability check on Far-Self." (c) **Decisions Already Locked #1** stays as written — still three predictors and one baseline; they simply each see two targets.

**Q2 — Target under Fix B.** Open-weight base with two post-trainings — this is the bigger prize because it lands you literally inside Song, Hu & Mahowald's "base/instruct variant" feature category, so your calibration Δ doubles as a check on their similarity ordering — a free side result for the write-up. **ASSUMPTION:** OpenRouter lists a Llama-3.x-70B-Instruct or Qwen2.5-72B-Instruct and a same-base community fine-tune (Hermes-class), served by at least one common provider, at prices well under the $2/$12 used in 3.2 — which is what pays for Q3. **ASSUMPTION:** OpenRouter exposes dated snapshots of closed models at all; often only the alias, which would make the "snapshot" route unbuildable. Verify before choosing: both IDs exist; identical pinned provider available for both; the model card confirms the same base weights (lineage is an ASSUMPTION until read); quantization stated; reasoning-off accepted; per-token price; the one-letter forced-choice format returns cleanly on both.

**Q3 — Power.** 300 is the floor; go to 500 per cell. Under 3.2's own arithmetic that is ≈$5.2 for the crossed design even at expensive pricing, and under $1 on open-weight (ASSUMPTION). Extra items are the cheapest evidence you will ever buy. Pre-register a smallest effect of interest of 5 pp and frame the null as an equivalence result: "under capability control, prompting-only self-advantage is bounded below 5 pp." That sentence is the publishable methods contribution the review only half-claims in 3.1.

**Q4 — Time-boxing.** Right gate, too timid a pilot. The pilot costs cents, so make it 40 items per persona (as Section 6 Phase D already says), run it on both M and N, and run 2–3 candidate persona pairs in parallel with a pre-declared selection rule (closest to band centre, D nearest chance). That converts "did the one pair land?" into "which pair landed?" — the fallback stops being a coin flip. Verification calls happen in the first hour of Day 1.

**Q5 — Reproducibility.** Agree with all three as mandatory. One addition at the level of principle: treat the per-call JSONL as a release artifact, not just a record — a fully logged, cost-stamped, capability-controlled dataset is itself a reusable contribution.

**Q6 — Persona design.** Values ordering, not epistemic caution — hedging-word rate is literally in Baseline D's feature list (3.4), so caution hands D the answer. Values ordering (e.g. "prioritise the person's long-term flourishing over their stated immediate preference" vs the reverse) on ambiguous advice prompts changes *which* recommendation is made while leaving register, length and vocabulary symmetric. It also connects to the live persona/character-alignment literature, which helps the pitch. Risk-tolerance is the second candidate to carry into the parallel pilot; run both.

**Q7 — What the review missed.** (1) N→N is a built-in internal replication of the self cell — say so; two self cells agreeing is a much stronger story than one. (2) Because all predictors reuse the same generated items, cost scales with predictors, not items — adding F→N is nearly free and gives F's capability baseline across both targets. (3) A persona pair where D sits at chance and Self sits in-band is itself a small releasable asset: a surface-resistant stimulus set. (4) 3.1 should state the paired bootstrap on the *interaction* explicitly; the same-item design is what makes it tight. All within 3 days, 2 people, $10, OpenRouter, and same-weights behavioural self-modelling only.

---

## Response A — The Outsider

**Q1 — Capability confound.** Reading this cold: your "Self" cell is a single API call to a model ID, and your "Near-Self" cell is a different, cheaper model ID. Any experimental psychologist would say the main effect Self−Near is uninterpretable because predictor identity and predictor–target match are perfectly confounded. Fix B does not fix that; it *hopes* it away ("approximately matched, not controlled" — your words, 2.3). Fix A is a plain difference-in-differences and it costs ~$3.1 (3.2). Since you insist $10 is not binding, the only argument against A is time, and "B now, A as stretch" guarantees the reverse cells are the first thing dropped on Day 3, leaving the confounded headline. Reverse it: pre-register A; B is the *fallback* if the N cells fail the pilot. Locked decisions to change in 02: **"Main Experiment Scope — One target model"** → "One primary target M. N is used as a target only for the crossed control cells (N→N, M→N, F→N); no pooling of targets, no regression." **"Statistical Analysis — Three pre-registered pairwise comparisons"** → "Primary contrast: interaction (M→M − N→M) − (M→N − N→N), item-level paired bootstrap. Secondary: the three original pairwise differences within the M row." "Core predictor structure" (locked #1) can stand — still one Self/Near/Far predictor set.

Naive question that matters: your title says self-advantage "scales with similarity." With one Near and one Far, you have two non-self points; you cannot test *scaling*, only "does Self beat the closest sibling after controlling for capability." Retitle before a reviewer does it for you.

**Q2 — Target under Fix B.** "Near-self" is doing unearned work. Two dated snapshots of a closed model share an unknown amount of anything — you can't see what changed. Two post-trainings of one open-weight base at least share verifiable base weights (ASSUMPTION: OpenRouter serves both an official instruct and a same-base fine-tune at the same size; ASSUMPTION: at comparable price). Prefer open-weight, but verify before choosing: (a) both IDs resolve to a single pinned provider; (b) a repeat-call determinism check at temperature 0 (same input, ≥20 repeats) so "same weights" means something operationally; (c) both accept the same reasoning-off parameter; (d) both pass the persona pilot. Note the deeper naive point: for a closed model you cannot verify that Self across sessions is even the same weights — that is an ASSUMPTION and belongs in limitations.

**Q3 — Power.** A 5 pp smallest effect with a ±5–6 pp CI at n=300 (3.1) is incoherent: you'd be unable to rule out the very effect you declared interesting. Either SESOI ≈ 8 pp at n=300, or SESOI = 5 pp and n≈600–800 per M-row cell (CI half-width ~3–4 pp paired). Cost roughly doubles-to-triples the $1.7–3.1 estimate — still under $10 (verify token counts). My pick: SESOI 5 pp, M-row cells at 600, N-column cells at 300, and say so in the pre-registration. Also state the unit: one "trial" = one generated text; balance personas 50/50.

**Q4 — Time-boxing.** Yes, but the gate is too late and too vague. Verification calls (cents) in the first two hours; feasibility band and pilot rule *written* before lunch Day 1; calibration running and pilot done by end of Day 1. And decide now who calls GO/FALLBACK and on what number — 02 says Jaswin, but no number exists yet.

**Q5 — Reproducibility.** No objection. Missing at the level of principle: a repeat-call determinism measurement is data, not hygiene — report it, because it is the closest thing you have to evidence that "same model ID" ≈ "same weights."

**Q6 — Persona.** Risk-tolerance leaks lexically ("safe", "risk"); epistemic caution leaks via hedging rate — which is literally in Baseline D's feature list (3.4). Values-ordering (e.g., individual autonomy vs. collective welfare when giving advice) is the least lexically marked. But the honest naive point: any disposition expressed in text is a surface feature in the limit, so pick empirically — pilot 2–3 candidate pairs, run D on each, choose the pair where D is nearest 50% and Self is in band. Pre-declare that rule. And the band itself is unearned: at 20 or even 80 pilot items, 55% is statistically indistinguishable from chance (SE ≈ 5.5–11 pp). Either raise the pilot to ~100 items with a 60–85% band, or define the band on a CI lower bound, not a point estimate.

**Q7 — Missed.** (a) 3.2 says "20-trial pilot," Phase D says "~40 items per persona" — pick one. (b) The capability confound applies to Far-Self too: if F is the strongest classifier, Far > Self tells you nothing about similarity; only the crossed design (F→N) handles it. (c) In Fix A the two columns are different item sets, so pairing holds within-column only — say so in the bootstrap spec. (d) Randomise A/B option order in the forced choice; state that predictors receive the persona clauses verbatim as used in generation. (e) Ground truth is "which prompt," not "which persona" — if the Target enacts inconsistently, that's ceiling, not leakage; name it.

---

## Response B — The Executor

**Q1 — Capability confound.** Build the pipeline crossed from hour one; decide the pre-registration at 6pm Day 1. Once `generate.py` loops over a list of targets and `predict.py` loops over predictors × targets, Fix A is a config change, not a design change — Section 3.2's own numbers say the extra cells cost ~$1.4 and ~1,500 extra calls, which is 10–15 minutes at 10-way concurrency. "B-now-A-as-stretch" is the worst sequencing: you write a one-target pipeline Day 1, then bolt a second target on Day 3 when nothing should be changing. So: Fix B's model choice (tier-matched pair) **plus** A's structure, with A pre-registered as primary if the Day-1 pilot passes on N as well as M, and B (the locked three comparisons on M only) as the automatic fallback if it doesn't. Locked decisions to change in `02`: **"Main Experiment Scope → One target model"** → "One primary target M. Near-Self N is also run as a target solely to provide the crossed control cells (M→N, N→N); N-as-target is never pooled with M and never used as an additional similarity point." **"Statistical Analysis → Three pre-registered pairwise comparisons"** → "Three pairwise comparisons on M's outputs as stated, plus a fourth pre-registered contrast: the interaction (M→M − N→M) − (M→N − N→N), which is the capability-controlled self-advantage estimate." **"Decisions Already Locked #1"** is untouched — no predictor is added.

**Q2 — Target under Fix B.** Don't debate lineages; run the verification and take the first pair that passes. ASSUMPTION: OpenRouter lists a few dated snapshots of closed models but retires old ones quickly; open-weight base + finetune pairs (Llama/Qwen-class Instruct vs a Hermes-style retune) are more reliably listed but served by multiple hosts at different quantizations. Preference order if both pass: dated snapshots (same serving stack, near-identical tier) > open-weight pair pinned to one provider > Section 2 table pair with the *weaker* model as Target. Verify in one hour on Day 1 morning: (1) both IDs return with the returned `model`/`provider` recorded, (2) both accept temperature 0 / reasoning off and give a one-letter answer with <5% malformed rate on 10 calls, (3) price within ~2× (ASSUMPTION on all pricing until the call returns usage). Cap this at 60 minutes; if nothing passes, take the fallback pair and move on.

**Q3 — Power.** 300 floor, raise to 400 if the pilot's malformed rate is <5% and the budget log shows <$3 spent by Day 2 noon. Runtime, not money, is the check: 400 items × 6 cells is ~2,400 calls, still under 30 minutes. Pre-register SESOI = 5 pp and commit to reporting the CI upper bound; anything smaller is undetectable at this n anyway, so pretending otherwise is theatre.

**Q4 — Time-boxing.** The gate is right but too loose — write it hourly. 9:00 verification calls; 12:00 `client.py` with logging + budget guard + generic run loop working; 13:00–16:00 Ubayd freezes 50 calibration items and runs 150 calls, Jaswin drafts three persona pairs and writes the feasibility band down; 16:00 pilot on M and N; 18:00 GO/FALLBACK and model pick recorded in `02`. Day 2 morning: freeze `02`, main run done before lunch. That leaves 1.5 days for analysis and writing, matching the ~1/5-code allocation. Cut order if slipping: 400→300, calibration 50→30, baseline D reduced to a length+TTR logistic regression, then drop the crossed cells (fallback to B).

**Q5 — Reproducibility.** No objection. Add: retries must never change model ID; log the freeze commit hash; add a dry-run flag that prints prompts without calling — you'll want it during pilot iteration.

**Q6 — Persona.** Risk-tolerance in advice scenarios (bold vs cautious *recommendation* on career/finance/health dilemmas), because it lives in *what* is recommended, not how it's phrased, and it's fastest to draft. Epistemic caution will leak through hedge-word rate and D will solve it; values-ordering is the backup if risk-tolerance lands >75%. Practical step: 10 items per candidate pair, three pairs, Self prediction plus a hedge-word count as a D proxy — ~60 calls, cents, one hour, then pick.

**Q7 — Missed.** (a) The "20-trial pilot" in 3.2 cannot resolve a 55–75% band — the CI is ±20 pp; use Section 6's 40/persona (80 items) and say so once. (b) Counterbalance persona order in the predictor prompt and log it, or position bias masquerades as accuracy. (c) Pre-register how malformed outputs count (wrong vs excluded) — M and N will differ. (d) Fix B's "report classification ability" needs a concrete artefact: a 30-item labelled sanity set run on all predictors — cheap, do it with calibration.

---

# Part 3 — Peer Reviews (round 2, anonymized)

Reviewers saw only Responses A–E with no advisor labels. Mapping: A = Outsider, B = Executor, C = Contrarian, D = Expansionist, E = First Principles Thinker.

### Peer Review 1

**1. Strongest: E.** It states the estimand explicitly (shared-weights accuracy net of predictor competence and target predictability), shows why Fix B cannot *estimate* the confound while A is the estimator, and is the only response to recompute power for the interaction (variance ~2×, so ±8–11 pp at 300/cell — matches 3.1's arithmetic). Its Q4 reordering (verification → pilot → calibration, because FALLBACK deletes Near-Self) is a genuine catch, and Q5 correctly upgrades provider pinning from reproducibility to validity of the "same-weights" scope claim. D is close behind (M-row-first cell ordering, parallel persona pilots with a pre-declared rule); B is the most operational but recommends risk-tolerance while using hedge-words as its D proxy.

**2. Biggest blind spot: A.** It makes the interaction the primary contrast, then powers only the M-row cells at 600 with N-column at 300. The interaction's SE is dominated by the smallest cells, so A's own SESOI = 5 pp remains unexcludable — exactly the incoherence A accuses 3.1 of. It also never recomputes interaction variance.

**3. All five missed:**
- The 02 fallback (Self / Far / D) reintroduces the capability confound in full (M vs. F). Nobody re-specified the fallback for a crossed design; a failed N pilot lands back in the uninterpretable design.
- Nobody totalled their combined additions (500/cell crossed ≈ $5.2, 2–3 pairs × 2 targets × 80-item pilots, sanity set, determinism repeats, retries) against $10 at 3.2's pricing — feasible only if cheap open-weight prices hold (ASSUMPTION).
- 02 assigns Ubayd both calibration/stats and implementation "once the design is locked", yet every proposed Day-1 schedule needs `client.py` by noon while Ubayd freezes calibration items. With two people, 02's responsibilities need rewording, not just the locked decisions.

---

### Peer Review 2

**Stats check (n=300, p≈0.65).** SE per cell ≈2.75 pp; independent difference ±7.6 pp; paired (ρ≈0.3–0.5) ±5.4–6.4 pp — 3.1 is right. The Fix-A interaction spans two *different item sets* (M's vs N's outputs), so its variance is the sum of two column-differences: ±10.8 pp independent, ±7.6–9 pp paired at n=300; at n=500 still ±5.9–8.4 pp. A 5 pp SESOI is therefore *not* excludable at 300–500/cell. Pilot: 20 items → SE≈10.7 pp; 80 → ≈5.3 pp.

**1. Strongest: E.** Only response that recomputes power *for the interaction* (correct: variance roughly doubles), states SESOI 5 pp honestly as an ~8 pp equivalence bound, corrects the 20-trial pilot, reorders Day 1 (verification → pilot → calibration, because FALLBACK deletes Near-Self), makes the band joint (Self in-band AND D≤~58%), and adds the pre-registrable "predictors are not told who generated." C is a close second (500 items + 8 pp is the only fully consistent SESOI/n pair; distillation and label-blind exclusion rule are good).

**2. Biggest blind spot: D.** Claims 500/cell lets you write "self-advantage bounded below 5 pp" — false for the interaction (±6–8 pp even with strong pairing); its Q7(4) "same-item design makes it tight" ignores that the two columns aren't the same items. That sentence would go straight into the pre-registration and be wrong. (A has a related flaw: 600 M-row / 300 N-column makes the primary interaction's precision bottlenecked by the 300 column.)

**3. All five missed:**
- 2.3's "make the weaker model the Target" hedge protects a *positive* result, but 3.1 says the expected outcome is a null — a null with a weaker Target is masked/uninterpretable. B even endorses this pair as fallback.
- Whether "300 trials" = 300 distinct source prompts or fewer prompts × samples; item-level bootstrap assumes independence, clustering inflates precision.
- Under Fix A, Baseline D must be fit per target column, and 02's two fallbacks (temperature property vs collapse-to-Self/Far/D) are conflated — the pilot gate needs to say which fires.

---

### Peer Review 3

**1. Strongest: E** (A close second). E frames the estimand cleanly (shared-weights net of predictor competence *and* target predictability), is the only response besides C to recompute power for the interaction (variance ~2×, so SESOI 5 pp at 300/cell is not boundable — B and D miss this), gets the Day-1 *order* right (pilot before calibration, since FALLBACK deletes Near-Self), reframes provider pinning as a validity condition for the same-weights claim, makes the feasibility band two-sided (Self in band AND D near chance), and pre-registers whether predictors are told who generated the text. Locked-decision edits are named with wording; ASSUMPTIONs labelled; scope respected. Gap: doesn't flag Locked #1 ("Exactly one Self condition") — only C notices N→N creates a second Self cell.

**2. Biggest blind spot: D.** Recommends SESOI 5 pp with 500/cell without ever computing interaction CI width; states Locked #1 "stays as written" while adding a second Self cell; over-claims that a single calibration Δ "checks Song's similarity ordering"; Q7 is mostly Fix A's own pros restated. (B is second: risk-tolerance is the one dimension three peers argue leaks lexically into D's features, and its Q3 is incoherent.)

**3. All five missed:**
- Under Fix A, Baseline D must run on the N-column too; a surface-solvable N-column voids the interaction, and no one budgets or pre-registers it (3.4).
- 02's "Fallback" section (Self/Far/Baseline collapse) is silently superseded by an A→B→collapse ladder; nobody gave replacement wording.
- 3.1/3.4 never fix how many distinct base prompts underlie 300 items; if prompts are reused across items, item-level bootstrap must be clustered by prompt or the CIs are too tight.

---

### Peer Review 4

**1. Strongest: E.** It names the estimand (shared-weights accuracy net of predictor competence *and* target predictability), so Fix A falls out as the estimator rather than a preference. It is the only response that recomputes power for the interaction (variance ≈ doubles → ±8–11 pp at 300, hence "5 pp SESOI, but design bounds ~8 pp" stated honestly). Q4 arithmetic is right (20 trials → SE ≈ 11 pp; 3.2's "20" must be corrected to Phase D's ~80). Q6 is the best-argued against Baseline D: values-ordering only, *and* the item must be a genuine value conflict, *and* the band is two-sided (Self 55–75% AND D ≤ ~58%). Q7's "are predictors told who generated?" is a real gap in 3.4. A is a close second (SESOI/CI incoherence, band-on-CI-lower-bound, ground-truth-is-which-prompt).

**2. Biggest blind spot: B.** Q6 picks risk-tolerance — the dimension most likely to leak into D's own sentiment/hedging features (A, C, E all say so; B's proposed D-proxy is a hedge-word count, which would expose exactly this). Its 10-item screening contradicts its own Q7(a) that 20 can't resolve the band. Q3 pre-registers 5 pp while calling it undetectable. Secondary errors: D claims "bounded below 5 pp" at n=500 without the interaction-variance correction; C's "main run Day 2 evening" is the schedule that squeezes writing.

**3. All five missed:** generate *both* personas from every prompt (within-prompt pairing). It removes the topic confound D and predictors could exploit, balances ground truth by construction, halves the dilemma prompts Jaswin must author (the real 3.2 bottleneck), and requires the 3.1 bootstrap to cluster by prompt, not text — otherwise 300 "trials" from fewer prompts are not independent.

---

### Peer Review 5

**1. Strongest: E** (A close second). E supplies the one argument that actually justifies the Fix-A convergence: Fix B *reduces* the capability term but cannot *estimate* it, so B-without-reverse-cells is unfalsifiable on the contested point — A is the estimator, B is the model-selection rule inside it. E (with C) alone recomputes power for the interaction (~2× variance), alone notes that FALLBACK deletes Near-Self so the pilot should precede calibration, and alone flags that "tell nobody who generated the text" must be pre-registered. The convergence is justified, but D's cell ordering (M-row first) is what preserves the reviewer's real concern; the defensible pro-B residue is that if the pilot fails on N you are on B regardless — so the tier-matched pair is non-negotiable either way. On Q2, A/D/E have it: "near-self" must mean *verifiable* shared weights (model card); C's multi-host worry is real but is a Self-cell pinning problem already mandated, not a lineage argument.

**2. Biggest blind spot: B.** "Take the first pair that passes" lets availability define the construct; SESOI 5 pp at n=300–400 is exactly the "theatre" B condemns (CI ±6–8 pp, wider for the interaction); 10-way concurrency and snapshot "same serving stack" are unlabelled ASSUMPTIONS. D repeats the 5 pp-bound error at 500/cell.

**3. All missed:** (a) In Fix A the two columns are different item sets; if N enacts personas near floor, a difference-of-proportions interaction is scale-artefactual — require both columns in-band or analyse on log-odds. (b) 300 "trials" from how many distinct task prompts? Bootstrap must resample prompts, not texts. (c) 2.3's "make the weaker model Target" biases toward the null 3.1 already expects — conservative for a positive, fatal for the equivalence claim.

---

# Part 4 — Chairman's Verdict

# COUNCIL VERDICT

## Where the Council Agrees

- **All five reject "B now, A as stretch."** A, C, D, E say outright that stretch cells in a 3-day sprint do not get built and the confounded headline survives; B says it is the worst *sequencing* because it bolts a second target onto a one-target pipeline on Day 3. Nobody defended the reviewer's recommendation as written.
- **All five want a tier-matched, same-lineage (M, N) pair regardless of design** (B, D, E explicitly: "Fix B's model choice inside Fix A"; Peer Review 5: "the tier-matched pair is non-negotiable either way").
- **All five want verification calls in the first hour of Day 1** and a feasibility band written down before the pilot runs (A, B, C, D, E).
- **Four of five (A, C, D, E) reject the 20-trial pilot** on arithmetic (SE ≈ 11 pp at p ≈ 0.65) and want ~80 items (Phase D's "40 per persona"). B concedes it in Q7 while contradicting it in Q6.
- **Four of five (A, C, D, E) pick values-ordering** as the dispositional dimension, all for the same reason: epistemic caution leaks through hedge-rate, which is literally in Baseline D's feature list, and risk-tolerance leaks lexically.
- **All five accept the reproducibility mandates** (pin provider, disable fallbacks, per-call log) with no objection.
- **A and E independently flag the title overclaim**: with one Near and one Far there is no "scale"; the honest headline is "same-weights residual after a tier-matched sibling and a capability control."
- **Everyone raises n** (400–600) and wants an SESOI stated as an equivalence bound.

## Where the Council Clashes

**1. Is Fix A a design change or the estimator?** A, C, D, E treat the crossed design as the primary pre-registered design; B wants the pipeline crossed from hour one but the pre-registration decided at 6 pm Day 1 after the pilot. These are the same position at different levels of commitment. E's framing settles it: the estimand is shared-weights accuracy *net of predictor competence and target predictability*; Fix B reduces the competence term but cannot estimate it, so B-without-reverse-cells is unfalsifiable on the contested point. **Verdict: A is the primary design; B's tier-matched pair is the model-selection rule inside it; the M-row-only design (the current 02 locked design) is the pre-registered fallback if the pilot fails on N — with D's cell ordering (M→M, N→M, F→M first) so the fallback is always complete.**

**2. Lineage (Q2): open-weight base + two post-trainings (A, D, E) vs. dated snapshots of a closed model (B, C).** C's argument for closed models — one host, so "same weights" for the Self cell actually holds — is real but, as Peer Review 5 notes, it is a *pinning* problem the mandates already solve, not a lineage argument. A/D/E's argument — near-self must mean *verifiable* shared weights, which only a model card can give — goes to the construct. **Verdict: open-weight first, closed snapshots second, adjacent-tier same-family third — and the third tier is now acceptable precisely because Fix A controls capability.**

**3. SESOI (Q3): 5 pp (A, B, D) vs. 8 pp (C; E says "5 pp aspiration, ~8 pp bound").** The arithmetic decides (below). **Verdict: two-tier — 5 pp for the simple M-row contrasts, 8 pp for the interaction — at n = 500 per cell.**

**4. Persona (Q6): values-ordering (A, C, D, E) vs. risk-tolerance (B).** B's own D-proxy (hedge-word count) would expose exactly the leak the others predict. **Verdict: values-ordering primary; risk-tolerance carried as the second candidate in the parallel screen, chosen by a pre-declared rule (A, D).**

**5. Schedule (Q4): C's "main run launched Day 2 evening" vs. B's "main run done before Day 2 lunch."** C is right that code effort will exceed 1/5; C is wrong to spend the slack on the main run rather than writing. **Verdict: GO/FALLBACK by 10:00 Day 2 at the latest, main run launched Day 2 morning, Day 3 code-free.** E's "pilot before calibration" and B's parallel plan are compatible with two people: Jaswin's pilot has priority; Ubayd's calibration slips if anything must.

## Blind Spots the Council Caught

- **Interaction variance (Peer Reviews 2, 3, 4).** Only C and E recomputed it. Chairman's arithmetic, p = 0.65: SE per cell at n = 300 ≈ 2.75 pp; independent difference ±7.6 pp; paired within a column (ρ ≈ 0.3–0.5) ±5.4–6.4 pp — Section 3.1 is right. The interaction spans two *different item sets* (M's texts vs. N's texts), so its variance is the sum of two column-differences: **±7.6–9.0 pp paired at 300/cell; ±5.9–7.0 pp paired at 500/cell; ±5.4–6.4 pp at 600/cell.** A 5 pp SESOI is not excludable for the interaction at any n the budget plausibly buys (~850/cell for ±5 pp, ≈ $9 at 3.2's pricing). Simple M-row contrasts at 500/cell paired: ±4.2–4.9 pp — 5 pp *is* boundable there. Hence: **D's "bounded below 5 pp at 500/cell" would go into the pre-registration and be false; A's 600 M-row / 300 N-column makes the primary contrast's precision bottlenecked by the 300 column; B's "SESOI 5 pp at 300–400" is the theatre B condemns.**
- **The 02 Fallback is silently superseded (Peer Reviews 1, 3)** and its collapse (Self / Far / D) reintroduces the capability confound in full (M vs. F). Nobody rewrote it. Also the property-fallback (temperature) and the design-fallback (collapse) are conflated (Peer Review 2). Wording below.
- **Baseline D must be fit per target column (Peer Reviews 2, 3)** — a surface-solvable N-column voids the interaction, and nobody budgeted or pre-registered it.
- **Prompt-level clustering (Peer Reviews 2, 3, 4, 5).** Nobody fixed how many distinct source prompts underlie 300 items. Peer Review 4's fix is the best single addition in the whole exercise: **generate both personas from every prompt** — kills the topic confound, balances ground truth by construction, halves the dilemmas Jaswin must author, and requires the bootstrap to resample *prompts*, not texts.
- **"Make the weaker model the Target" (Peer Reviews 2, 5)** protects a positive result but biases toward the null 3.1 already expects — fatal for the equivalence claim. Under Fix A it is moot; under the M-row fallback it must be dropped as a hedge and reported only as a direction-of-bias statement.
- **Scale artefact (Peer Review 5):** if N enacts personas near floor, a difference-of-proportions interaction is artefactual → both columns must be in-band, and log-odds is reported alongside.
- **Locked #1 says "Exactly one Self condition" (C, Peer Review 3)** — N→N is a second Self cell; D and E claimed #1 "stays as written." It needs rewording.
- **Budget totalling (Peer Review 1).** Chairman's total at 3.2's expensive pricing: generation 2 × 500 items ≈ $2.2; predictions 6 × 500 ≈ $3.1; pilot (3 pairs × 40 on M, then chosen pair × 80 on M and N) ≈ $0.9; calibration + sanity set + determinism repeats ≈ $0.2; 10 % retries ≈ $0.6 → **≈ $7.** Fits, with a guard rule (below). At open-weight prices (ASSUMPTION) it is under $2.
- **Ubayd's double duty (Peer Review 1):** every Day-1 schedule needs `client.py` by noon *and* frozen calibration items from the same person; 02's responsibilities need one sentence changed.

## The Recommendation

**Q1 — Capability confound.** Fix A as the primary pre-registered design, with Fix B's tier-matched same-lineage pair as the model-selection rule inside it, and the current M-row design as the pre-registered fallback if the pilot passes on M but not N. Build the pipeline parameterised by target from hour one; run cells M→M, N→M, F→M first. Primary contrast is the interaction; the three locked pairwise comparisons survive as secondary contrasts on M's outputs. This changes "One target model," "Three pre-registered pairwise comparisons," and Locked #1 (wording below). "No pooling / no three-point regression" stand untouched — N-as-target is a control, not a point.

**Q2 — Lineage.** Prefer two post-trainings of one open-weight base at the same size (official Instruct + same-base community fine-tune) because shared weights are verifiable from the model card; second, two dated snapshots of one closed model; third, an adjacent-tier same-family pair (acceptable only under Fix A). Verify before choosing: both IDs resolve on OpenRouter; one provider serves both and is pinnable with fallbacks off at a stated quantization; reasoning-off accepted; one-letter output with < 5 % malformed on 10 calls; the pair is not a re-alias (temperature-0 outputs on the 50 calibration items must not be identical); ≥ 20 repeat calls at temperature 0 as a determinism measurement (reported as data); both survive the persona pilot. All availability claims are ASSUMPTIONS until the calls return.

**Q3 — Power.** 300/cell is the floor; 500/cell is the target (250 prompts × 2 personas per target); reduce 500 → 400 → 300 only if the budget guard's projection from verified prices exceeds $7.5. Pre-register two SESOIs: 5 pp for the simple M-row contrasts (boundable at 500 paired, ±4–5 pp) and 8 pp for the interaction (±6–7 pp paired at 500). Item-level paired bootstrap resampling by source prompt; McNemar secondary; report the interaction on the log-odds scale as well.

**Q4 — Time-boxing.** The gate is right, too small and too vague. Verification calls in hour 1; `client.py` with logging + budget guard by noon (Ubayd) while Jaswin authors three persona pairs and ~40 dilemma prompts and writes the band down; afternoon: screen three pairs at 40 items on M, run the winner at 80 items on M and N with D per column; calibration items frozen and running in parallel, lower priority. GO/FALLBACK recorded in 02 by end of Day 1, hard stop 10:00 Day 2. Main run launched Day 2 morning; Day 3 is analysis and writing, no code. Accept that code will be ~1/3, not 1/5, and protect writing by making Day 3 code-free rather than pretending.

**Q5 — Reproducibility.** No objection. At the level of principle: pinning is a *validity* condition, not just reproducibility — M as generator and M as Self-predictor must hit the identical provider and quantization or "same weights" is literally false. Provider unavailable mid-run → abort and resume, never switch. Retries never change model ID. Log the freeze commit hash. Report the temperature-0 repeat-call agreement as data.

**Q6 — Persona.** Values-ordering (e.g., "prioritise the person's autonomy / stated preference" vs. "prioritise the person's long-term welfare") on genuine advice dilemmas where the two values conflict; same scaffold, same length/format instructions, generation prompt forbids naming the value; both personas generated from every prompt; predictors receive the persona clauses verbatim, option order counterbalanced, and are **not told which model generated the text**. Band is joint and per column: Self 60–80 % on ≥ 80 items AND D (5-fold CV) ≤ 58 %. Selection rule among candidate pairs: in-band on both targets, then D closest to 50 %, then Self closest to 70 %. Risk-tolerance is the second candidate in the screen.

**Q7 — Missed.** (i) The Fallback section must be rewritten as a ladder (below). (ii) Baseline D per column. (iii) Prompt-level clustering / within-prompt pairing. (iv) Drop the "weaker model as Target" hedge. (v) The one-sentence research question should say "residual after a tier-matched sibling and a capability control," not "scale with similarity." (vi) Pre-register the malformed-output rule and a label-blind exclusion rule for refusals/half-enacted outputs. (vii) Far-Self may be distilled from Target — calibration Δ must show Far < Near or Far is swapped. (viii) One sentence in Responsibilities so Ubayd's Day-1 code role is explicit.

## The One Thing to Do First

Run the ~10 verification calls this morning to find one same-lineage (M, N) pair that both resolves on OpenRouter, pins to a single provider with fallbacks off, honours reasoning-off, and returns a clean one-letter answer — and write the returned `model`/`provider`/price into `04_model_verification.md`. Every other decision in this verdict is conditional on that pair existing.

## Decisions for 02_design_audit.md

### Q1
- **(a)** Crossed 2×2 (Fix A) as primary with a tier-matched pair; M-row design as pre-registered fallback; interaction primary, the three pairwise comparisons secondary.
- **(b)** "Main Experiment Scope — 'One target model'" and "'A second target model only as a stretch goal'"; "Statistical Analysis — three pre-registered pairwise comparisons"; "Decisions Already Locked #1 — Core predictor structure".
- **(c) Main Experiment Scope** — replace the first, second and fifth bullets with:
  > - One target lineage: two same-lineage, tier-matched models — M (primary target) and N (Near-Self). Each serves as both generator and predictor in a crossed 2×2 capability control (cells M→M, N→M, M→N, N→N); Far-Self F predicts both columns (F→M, F→N). N-as-target exists solely to estimate the capability term. It is never pooled with M and never used as an additional similarity point.
  > - Approximately 500 items per cell (250 source prompts × 2 personas per target); 300 per cell is the floor.
  > - Cell run order: M→M, N→M, F→M first, then M→N, N→N, F→N — the M-row design is complete before the control column starts.

  **Statistical Analysis** — replace the block from "Three pre-registered pairwise comparisons" to the end of the numbered list with:
  > Pre-registered contrasts, each with an item-level paired bootstrap CI (resampling by source prompt, not by text; pairing holds within a target column only):
  > **Primary:** capability-controlled self-advantage = (M→M − N→M) − (M→N − N→N).
  > **Secondary:** (1) Self vs. Near-Self on M's outputs (M→M − N→M); (2) Near-Self vs. Far-Self on M's outputs (N→M − F→M); (3) Self vs. Far-Self on M's outputs (M→M − F→M); (4) N→N − M→N; (5) F→M vs. F→N as a Far-Self capability check.
  > Report all six cell accuracies with CIs; McNemar's test as a secondary check on each simple contrast; report the interaction on the log-odds scale alongside the difference scale.
  > **Condition D's role:** fit separately per target column, cross-validated, reported separately, never on the similarity axis. D > 58 % on a column voids the self-advantage claim for that column.

  **Decisions Already Locked #1** — replace with:
  > Exactly one Self predictor (M), one Near-Self (N), one Far-Self (F), one statistical baseline (D). No additional predictors. Each of M, N, F predicts two target columns (M's outputs and N's outputs); N→N is a control cell produced by an existing predictor, not an added predictor and not an added similarity point.

### Q2
- **(a)** Open-weight base with two post-trainings first; closed dated snapshots second; adjacent-tier same-family third — all subject to single-provider pinning verified by API call.
- **(b)** "Unresolved Decisions row 1 — Target model (M)"; "Current Experimental Conditions — B — Near-Self".
- **(c) Row 1, Current status** →
  > Selection rule (in order, all availability claims ASSUMPTIONS until verified): (i) two post-trainings of one open-weight base at the same parameter size, both served by one pinnable provider at a stated quantization; (ii) two dated snapshots of one closed model; (iii) same-family adjacent-tier pair (acceptable only under the crossed design). Verify before choosing: both IDs resolve; one provider pinnable for both with fallbacks off; reasoning-off accepted; < 5 % malformed one-letter output on 10 calls; not a re-alias (temperature-0 outputs on the calibration items not identical); ≥ 20 temperature-0 repeats logged as a determinism measurement; both pass the persona pilot.

  **Condition B** → "A same-lineage model at the same capability tier that verifiably shares base weights with the target (per model card), predicts the same property from the same text — and also serves as the second target column of the crossed control."

### Q3
- **(a)** 500/cell target, 300 floor; SESOI 5 pp (simple contrasts) and 8 pp (interaction).
- **(b)** New paragraph under "Statistical Analysis" — "Power and smallest effect of interest"; Locked #2 unchanged.
- **(c)**
  > **Power and smallest effect of interest.** At p ≈ 0.65 and 500 items per cell, a paired simple contrast has a 95 % CI of about ±4–5 pp; the interaction (two independent columns) about ±6–7 pp. Smallest effect of interest: 5 pp for the simple contrasts, 8 pp for the interaction. A null is reported as an equivalence bound ("effects larger than X excluded"), not as "not significant." n is reduced 500 → 400 → 300 only if the budget guard's projection from verified per-token prices exceeds $7.50 total. Malformed outputs: one retry with the identical prompt; a still-malformed item is excluded listwise within its column and malformed rates are reported per predictor. Refusals or half-enacted generations are excluded by a label-blind rule fixed before the pilot.

### Q4
- **(a)** Yes, tightened: verification hour 1, pilot 80 items per target on ≤ 3 screened pairs, GO/FALLBACK by 10:00 Day 2, main run Day 2 morning, Day 3 code-free.
- **(b)** "Unresolved Decisions row 6 — Exact sprint schedule"; "Current Two-Person Responsibilities — Ubayd".
- **(c) Row 6** →
  > Day 1: 09:00 verification calls; by 12:00 `client.py` (pinning, logging, budget guard) working; 13:00–17:00 Jaswin screens ≤ 3 persona pairs (40 items on M), then runs the winner at 80 items on M and N with D per column; Ubayd freezes 50 calibration items and runs them in parallel (lower priority than the pilot). GO/FALLBACK and model pick recorded in this document by end of Day 1, hard stop 10:00 Day 2. Day 2: freeze this document as pre-registration; main run launched in the morning. Day 3: analysis and writing only. Cut order if slipping: n 500→400→300; calibration 50→30; D reduced to length + TTR; then drop the N column (fallback level 2).

  **Ubayd** → append: "Owns `client.py`, the run loop and the budget guard on Day-1 morning; calibration item authoring is done in parallel and slips before the pilot does."

### Q5
- **(a)** Mandatory; pinning is a validity condition for "same weights."
- **(b)** New "Decisions Already Locked #5 — Provider pinning".
- **(c)**
  > **5. Provider pinning.** Every call pins one provider with fallbacks disabled; M-as-generator and M-as-Self-predictor (and N likewise) must hit the identical provider and quantization — this is a precondition of the "same-weights" scope claim, not a hygiene item. Provider unavailable mid-run → abort and resume, never switch. Retries never change model ID. Per-call log (returned model, provider, tokens, cost, prompt hash, timestamp) and the stimulus freeze commit hash are part of the research record; the temperature-0 repeat-call agreement is reported as data.

### Q6
- **(a)** Values-ordering on conflict dilemmas, both personas per prompt, verbatim clauses, generator identity withheld, joint per-column band.
- **(b)** "Hidden Property — Primary"; "Unresolved Decisions row 2 — Exact persona design"; "Unresolved Decisions row 4 — Pilot feasibility threshold"; "Decisions Already Locked #3 — Ground truth handling" (append).
- **(c) Hidden Property — Primary** →
  > Which of two personas differing in a values ordering (e.g., prioritise the person's autonomy/stated preference vs. their long-term welfare) produced the response to an advice dilemma in which the two values genuinely conflict. Same system-prompt scaffold, same length and format instructions; only the persona clause differs; the generation prompt forbids naming the value. Both personas are generated from every source prompt. Predictors receive the text plus the two persona clauses verbatim, in counterbalanced order, and are not told which model generated the text; the only self-specific channel is same-weights fit to own output distribution.

  **Row 4** →
  > Feasibility band, fixed before the pilot, applied per target column on ≥ 80 items: Self accuracy 60–80 % AND Baseline D (5-fold CV) ≤ 58 %. Selection among ≤ 3 candidate pairs: in-band on both M and N, then D closest to 50 %, then Self closest to 70 %. Pass on M and N → crossed design; pass on M only → fallback level 2; no pass on M → fallback level 3.

  **Row 2** → "Values-ordering primary, risk-tolerance second candidate; epistemic caution excluded (hedge-rate is a Baseline D feature)."

  **Locked #3, append** → "No predictor is told which model generated the text; persona option order is counterbalanced and logged; a position-bias check is reported per predictor."

### Q7
- **(a)** Rewrite Fallback as a ladder; retitle the one-sentence question; drop the weaker-model hedge.
- **(b)** "Fallback"; "Research Question — One-sentence form".
- **(c) Fallback** → replace the whole section with:
  > Predetermined ladder, fired by the pilot gate:
  > **Level 1 (pilot passes on M and N):** crossed design as specified.
  > **Level 2 (passes on M only, or the N column cannot be run in time):** the M-row design only — Self, Near-Self, Far-Self, D on M's outputs; the three pairwise contrasts; the capability confound stated as the headline limitation. No "weaker model as Target" hedge is used; the direction in which any tier gap biases the result is stated.
  > **Level 3 (no persona pair passes on M):** switch the hidden property to sampling-temperature bucket with the same gate and design ladder; if that also fails, collapse to Self / Far-Self / D on M's outputs, report three accuracy estimates with CIs, no self-advantage or similarity claim of any kind, and an honest account of why.
  > At every level: no pooling of targets, no regression, D never on the similarity axis.

  **Research Question — One-sentence form** → "When predicting a hidden property of a model's own output, is there a self-prediction residual beyond what a tier-matched same-lineage sibling achieves, once the predictor's general classification ability is controlled by a crossed design?"

## ASSUMPTIONS the Verdict Depends On

1. **ASSUMPTION** — OpenRouter lists an official Instruct model and a same-base community fine-tune at the same parameter size (Llama-3.x-70B / Qwen2.5-72B class). Check: model list + model cards. If false → tier (ii) closed snapshots; if also false → tier (iii); the crossed design still holds.
2. **ASSUMPTION** — At least one provider serves both IDs and can be pinned with `allow_fallbacks: false` at a stated quantization. Check: one call per ID with the pin, inspect returned `provider`. If false → move down the lineage ladder; if no pair pins → single-host closed pair.
3. **ASSUMPTION** — Dated snapshots of closed models exist on OpenRouter as distinct IDs, not silent aliases, and survive 72 h. Check: two IDs return non-identical temperature-0 outputs on 50 items. If false → skip tier (ii).
4. **ASSUMPTION** — Per-token prices are at or below 3.2's $2/M in, $12/M out (open-weight 5–10× cheaper). Check: `usage`/cost fields on verification calls. If higher → n drops 500→400→300 via the guard; the design does not change.
5. **ASSUMPTION** — Reasoning can be disabled per model and no reasoning tokens are billed. Check: usage fields on a one-letter call. If false → choose a non-reasoning model in the same lineage.
6. **ASSUMPTION** — ~10-way concurrency and rate limits let ~3,000 prediction calls finish within an hour. Check: timed 50-call burst. If false → main run spans Day 2 into overnight; if much worse → n reduces.
7. **ASSUMPTION** — Temperature-0 repeat calls on the pinned provider are near-deterministic. Check: 20 repeats. If false → reported as data; the same-weights claim is stated with that caveat.
8. **ASSUMPTION** — Both M and N enact the persona clauses on dilemma prompts with > 90 % usable (non-refusal, non-malformed) outputs. Check: the 40-item screen. If false → next pair or next lineage.
9. **ASSUMPTION** — Far-Self is not distilled from Target. Check: calibration Δ shows Far < Near with CI excluding zero. If false → swap Far-Self before the main run.
10. **ASSUMPTION** — The chosen pair's Self cell lands in 60–80 % on both columns. If N is out of band → fallback level 2 automatically; the interaction is not reported.
