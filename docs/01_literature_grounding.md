# 01 — Literature Grounding

## Purpose

This document records the literature grounding completed during Phase 1A of the Track 3 project (Digital Minds Sprint — *Does Self-Advantage in Behavioral Self-Prediction Scale With Model Similarity?*). It exists so that anyone joining the project — including a version of this team returning after a break — can understand the academic disagreement this project engages with, what each source paper actually established, and where our project's own claims begin and the literature's claims end. It should be read before `02_design_audit.md`.

This document is a research record, not a design document. It does not choose a target model, a persona pair, or a calibration task — that belongs to `02_design_audit.md` and to decisions not yet made.

---

## The Core Academic Disagreement

### Binder et al. — "Looking Inward: Language Models Can Learn About Themselves by Introspection" (arXiv 2410.13787, ICLR 2025)

#### Research question
Can a model (M1) predict properties of its own hypothetical behavior more accurately than a different model (M2) can predict M1's behavior — even when M2 is trained on M1's ground-truth outputs?

#### Experimental setup
Both M1 and the comparison model M2 are **finetuned** for the task. M1 is finetuned on roughly 30,000 examples of self-prediction training: a hypothetical question about its own behavior paired with the ground-truth property of its own actual behavior on that input. M2 is finetuned the same way, but on M1's ground-truth behavior rather than its own. A second experiment ("behavioral change") intentionally shifts M1's ground-truth behavior via further finetuning and tests whether M1's hypothetical self-predictions update to track that shift on unseen cases.

#### Key findings
Self-prediction training substantially improves accuracy (GPT-4o rose from roughly 32.6% to 49.4% on held-out self-prediction questions after training). M1 outperforms M2 at predicting M1's own behavior. In the behavioral-change experiment, M1's hypothetical predictions tracked its own shifted ground-truth behavior on unseen cases, which the authors treat as harder-to-explain-away evidence, since a differently-trained model is unlikely to replicate M1's exact generalization pattern by coincidence.

#### Their interpretation
The authors interpret this pattern as evidence that M1 has privileged access to its own behavioral tendencies — introspection in their defined sense: knowledge not contained in or derivable from training data alone, but originating from the model's internal state.

#### Important methodological assumptions
That finetuning both M1 and M2 identically except for whose behavior is the training target isolates a genuine "self" effect, rather than some other artifact of the finetuning process itself. The authors also explicitly acknowledge that introspection was successfully elicited only on simple tasks — it did not generalize to more complex tasks or those requiring out-of-distribution generalization.

#### Limitations
Requires finetuning both the target and comparison model — this is compute- and access-intensive and was done on closed models (GPT-4, GPT-4o) and Llama-3 via provider finetuning APIs. The effect did not generalize past simple tasks in the paper's own results.

#### Relevance to our project
This is the paper our project is most directly in conversation with, but **our design does not replicate its method.** We have no finetuning access or budget. Our project tests an adjacent question — self-advantage in a purely black-box, prompting-only paradigm — and this difference must be stated plainly rather than implied away.

---

### Song, Hu & Mahowald — "Language Models Fail to Introspect About Their Knowledge of Language" (arXiv 2503.07513, COLM 2025)

#### Research question
Do models' prompted metalinguistic self-reports (e.g., judging whether a sentence is grammatical) actually track their internal linguistic knowledge, beyond what a highly similar model would predict?

#### Experimental setup
21 open-source LLMs across several families (Llama, Qwen, OLMo, Mistral variants), no finetuning. Internal knowledge is grounded directly in string probabilities (a domain where "ground truth" of internal knowledge is directly measurable). Introspection is operationalized as the degree to which a model's prompted responses predict its own string probabilities, beyond what a model with nearly identical internal knowledge would predict.

#### Key findings
A significant, systematic gap between actual performance (string-probability-based) and self-assessment (prompted) across all tested models, including larger and more capable ones — not attributable to noise.

#### Their interpretation
Prompted self-reports should not be conflated with a model's actual internal linguistic generalizations. By this operationalization, the tested models do not introspect.

#### Similarity control
This is the paper's most methodologically important contribution for us: the authors build **two independent similarity measures** to rule out the "any two similar models would agree" confound — a top-down, **feature-based** similarity (categorizing model pairs as self, same-seed variants, base/instruct variants, same-family, or unrelated) and a bottom-up, **empirical** similarity (measured via correlation between models' direct evaluations on held-out data). Our project's planned calibration probe — measuring agreement rate between predictor models and the target model on an unrelated task — is methodologically the same approach as their empirical-similarity measure. This should be credited as direct precedent, not presented as an original contribution of ours.

#### Limitations
Relies on token-level string probabilities (logprobs) across open-weight models, accessed via a library built for Hugging Face models. This access pattern may not transfer cleanly to closed commercial APIs, depending on what logprob access each provider exposes — worth checking early if any part of our design leans on logprobs rather than pure text output.

#### Relevance to our project
Provides the direct methodological precedent for our empirical-similarity calibration approach, and is the paper most responsible for making "similarity must be measured, not assumed from provider labels" a defensible, literature-grounded design requirement rather than our own invention.

---

### Song, Lederman, Hu & Mahowald — "Privileged Self-Access Matters for Introspection in AI" (arXiv 2508.14802)

#### Research question
Does a model have genuinely privileged access to one of its own generation parameters (sampling temperature), or does apparent self-awareness of that parameter reduce to reasoning about surface features of its own text that any observer could use?

#### Experimental setup
No finetuning; pure prompting. A generator model produces a sentence at a varied sampling temperature. In a "self-reflection" condition, the same model is asked to judge its own temperature from the prompt and its generated sentence. In an "across-model prediction" condition, a different model judges the generator's temperature from the same observable information. As an explicit confound check, the authors also varied sentence style (factual / neutral / "crazy") and subject matter independently of actual temperature.

#### Key findings
Self-reported temperature was highly sensitive to the prompt's style instruction rather than to the actual sampling temperature used — models tended to report "high" for stylistically "crazy" prompts and "low" for factual ones, regardless of true temperature. Self-reflection did not outperform across-model prediction.

#### Their interpretation
No evidence of privileged self-access on this task. The authors argue models are reasoning about the creativity or typicality of the generated text — information equally available to an external observer — rather than accessing any genuine internal state. They also propose an operational definition of introspection worth adopting for our own framing: a process is introspective only if it is more reliable than an equal-or-lower-cost process available to a third party. The authors note, as a point of contrast, that Binder et al. did find evidence of privileged self-access, but only in larger models with finetuning — a relevant prior for what to expect from a finetuning-free design like ours.

#### Why temperature matters for our design
This paper is close to a direct precedent for a temperature-based self-vs-external design and reports a clean null result with an identified confound (style leakage). Using temperature as our *primary* hidden property would risk landing very close to a replication of an already-published finding, with less room for a genuinely new contribution. This is the specific, literature-grounded reason the source-of-truth document keeps temperature as fallback only, rather than primary.

#### Relevance to our project
The closest methodological cousin of our own design (black-box, prompting-only, self vs. external-model comparison on a generation-time hidden property) and the source of the operational definition of introspection we intend to use in our own framing.

---

### Lindsey — "Emergent Introspective Awareness in Large Language Models" (Anthropic, arXiv 2601.01828, published January 2026)

#### Research question
Can models notice and correctly identify concepts artificially injected into their own internal activations?

#### Experimental setup
Steering vectors representing known concepts are injected directly into a model's residual stream (activation space). The model is then asked whether it detects an "injected thought" and, if so, to identify it.

#### Key findings
Claude Opus 4 and 4.1 achieved roughly a 20% introspection detection rate with close to 0% false positives. Opus 4 and 4.1 generally showed the greatest introspective awareness among tested models, though the pattern across models was complex and sensitive to post-training strategy.

#### Their definition / criteria for introspective awareness
Four criteria are required for a self-description to count as genuinely introspective: **accuracy** (the description is correct), **grounding** (the description is causally dependent on the actual internal state — manipulating the state changes the description), **internality** (the knowledge comes from an internal process, not from observing the model's own outputs and inferring backward), and **metacognitive representation**.

#### Why this is outside our experimental scope
This paradigm requires direct access to and manipulation of model activations. We have no such access — our project is entirely API-based and black-box. This paper defines the ceiling our project explicitly does not attempt to reach.

#### Relevance to our project
Sets the vocabulary and the outer boundary for our scope-limiting language: our project can speak to same-weights behavioral self-modeling at most, never to activation-level introspective awareness in Lindsey's sense. This distinction must appear early in any write-up we produce, not buried in a limitations section.

---

## What the Literature Actually Establishes

**1. Claims directly supported by the papers themselves:**
- Binder et al.: finetuned self-prediction shows a measurable, replicated self-vs-cross-model advantage on simple tasks, which fails to generalize to complex or out-of-distribution tasks.
- Song, Hu & Mahowald: across 21 open-source models, prompted metalinguistic self-reports do not track internal knowledge (string probabilities) beyond what a similar model would predict, using both a feature-based and an empirical similarity control.
- Song, Lederman, Hu & Mahowald: in a pure-prompting, no-finetuning temperature-judgment task, self-reflection does not outperform across-model prediction; apparent self-awareness is explainable by surface-style reasoning.
- Lindsey: concept injection into activations yields a roughly 20% correct-detection rate with near-zero false positives in Claude Opus 4/4.1, meeting a four-criterion definition of introspective awareness.

**2. Interpretations we are making, not claims the papers make:**
- That an *unfinetuned*, purely black-box design (ours) is likely, based on the pattern across these papers, to land closer to a null result than a positive one. This is a reasonable prior grounded in the contrast between Binder's (finetuned, positive) and Song et al.'s (unfinetuned, null) results — but it is our extrapolation, not a finding any single paper states.
- That persona identity is a "semantically buried" property less prone to the surface-leakage confound that undermined the temperature paradigm. This is a design hypothesis on our part, not yet tested.
- That our calibration-probe approach is a legitimate, precedented method because it mirrors Song, Hu & Mahowald's empirical-similarity measure — this is a reasonable methodological borrowing, but applying it to a different hidden-property task (persona rather than linguistic knowledge) is untested by any of these papers.

**3. Implications for our experimental design:**
- Similarity must be measured, not assumed — directly supported by Song, Hu & Mahowald's methodology.
- Temperature should be fallback-only — directly supported by the null result and identified confound in the temperature paper.
- Any positive self-advantage finding needs to be reported cautiously, given that the one paper reporting a positive result required finetuning we cannot replicate.

---

## The Disagreement Our Experiment Targets

In plain English:

**Binder et al.:** self-prediction may contain something genuinely self-specific — evidence of privileged access, at least under finetuning.

**Song et al. (both papers):** apparent self-advantage is better explained by behavioral similarity between predictor and target than by anything self-specific — and where tested without finetuning, no self-advantage survives a careful similarity control.

**Our project:** we will empirically measure similarity between the target model and its comparison models (near-self, far-self), rather than assuming it from provider labels, and test whether self-prediction shows any advantage beyond that measured similarity, on a hidden property chosen specifically to avoid the surface-leakage problem that affected the existing temperature-based test.

This is **not** a direct replication of Binder et al. (no finetuning) and **not** a direct replication of either Song et al. paper (different hidden-property domain, different predictor structure). It is a smaller, more narrowly scoped test that borrows methodological pieces from both sides of the disagreement.

---

## Our Specific Research Gap

Conservatively stated: no paper found in this literature review has tested a self-vs-near-self-vs-far-self design, with similarity measured empirically via an unrelated calibration task, on a hidden property specifically selected to resist the surface-leakage confound identified in prior work. That is the gap this project targets. This is a modest, incremental contribution — a better-controlled instance of an existing question — not a new theoretical claim about introspection.

---

## Scope Boundary

This project's design can speak to, at most:

- **Same-weights behavioral self-modeling** — whether a model is unusually well-fit to its own output distribution.

This project's design cannot establish, and no result from it should be described as showing:

- Same-episode memory (the model "remembering" producing a specific text)
- Activation-level introspection in Lindsey's sense
- Internal-state awareness
- Consciousness or subjective experience
- Genuine introspection in any strong philosophical sense

Any self-advantage found, if it survives the similarity control, should be described as evidence the model is unusually well-fit to its own output distribution — nothing stronger.

---

## References

- Binder, F. J. et al. "Looking Inward: Language Models Can Learn About Themselves by Introspection." arXiv:2410.13787. ICLR 2025.
- Song, S., Hu, J., & Mahowald, K. "Language Models Fail to Introspect About Their Knowledge of Language." arXiv:2503.07513. COLM 2025.
- Song, S., Lederman, H., Hu, J., & Mahowald, K. "Privileged Self-Access Matters for Introspection in AI." arXiv:2508.14802.
- Lindsey, J. "Emergent Introspective Awareness in Large Language Models." arXiv:2601.01828. Anthropic, 2026.

All summaries above are drawn from the abstracts, methods, and results sections of these primary sources as retrieved during Phase 1A research. Where a claim above could not be directly traced to one of these sources, it is marked in the "interpretations we are making" section rather than presented as an established finding.
