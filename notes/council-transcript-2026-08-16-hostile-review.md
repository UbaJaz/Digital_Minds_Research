# LLM Council Transcript — 2026-08-16 — Independent hostile review of the Track 3 submission

**Task:** independent, hostile evaluation of the current `10_report.md` (no edits, no new experiments): scientific strength, sprint competitiveness, win likelihood, Fellowship promise, hidden problems, and what to do with the remaining time today.

**Method:** six role-specific reviewers (1 hard-nosed AI safety researcher, 2 hackathon/sprint judge, 3 AI welfare / digital-minds researcher, 4 statistician/methodologist, 5 Fellowship selection mentor, 6 cognitive scientist / experimental psychologist with no LLM background) produced independent Round-1 reviews in parallel; each then read all six reviews and produced a Round-2 adversarial debate contribution (Reviewer 4 additionally re-derived the definitive length-heuristic numbers from `data/checkpoints/selfpred_*_VO-C.jsonl`); a chairman synthesised Rounds 3–8 into the consolidated report in Part 5. Reviewers read `10_report.md`, `CLAUDE.md`, the judging-criteria screenshots, the six past-winner PDFs, and (where relevant) `02_design_audit.md`, `tools/surface_leakage_gate.py`, `data/results/*.json`, `data/checkpoints/*.jsonl`, and the slide content. No repo file was modified; no API calls were made.

**Status:** advisory. All numbers newly derived by reviewers (length rule 0.809, own-shorter 0.653, clustered CIs, F-referenced interaction ≈ +0.094, etc.) should be re-verified by the team before being inserted into the report, and logged as amendment A9.

---

# Part 1 — Review brief given to every reviewer

# REVIEW BRIEF — Independent, hostile review of the Digital Minds Track 3 submission

## What you must read (absolute paths)
Repo root: C:/Users/jaswi/Downloads/Digital_Minds_Hackthon2/

1. `10_report.md` — the current submission report. **Source of truth for the project's actual results.** ~10,600 words. Read ALL of it including appendices.
2. `CLAUDE.md` — project history, design rules, current experimental state, constraints.
3. `C:/Users/jaswi/AppData/Local/Temp/claude/C--Users-jaswi-Downloads-Digital-Minds-Hackthon2/95b8bc90-538a-4d36-824b-878225f28ba4/scratchpad/council2/reference_winners_criteria.md` — transcription of the judging rubric (from screenshots) and summaries of six past Apart hackathon winners. Read fully.
4. Optional, if your role needs it: `02_design_audit.md` (preregistration rows P1–P15 + amendments A1–A8), `tools/surface_leakage_gate.py` (released tool), `10_report_condensed.md` (a 7,500-word condensed variant of the report — note the rubric's 4–8 page limit), `09_pilot_finding.md`, `07_calibration_results.md`, `data/results/*.json`, `presentation.html` / `scripts/build_slides.py` (10-slide deck content).

Do NOT edit any file. Do NOT run experiments or API calls. This is evaluation only.

## Project context (from the team; treat as accurate but verify against the report)
Question: does a language model have privileged self-access — does it predict its own outputs better than an equally-informed / equal-or-lower-cost external observer once general classification capability and surface leakage are controlled?

Design: two same-pretraining-base models M (Llama-3.1-70B-Instruct) and N (Hermes-3-Llama-3.1-70B); external model F (Mistral-Small-3.2-24B); crossed 2×2 capability control; hidden persona / values-ordering property; surface baseline D = logistic regression on 18 structural features, grouped 5-fold CV by source prompt; a leakage manipulation across stimulus sets; 24 crossed cells; 9,269 scored trials; four stimulus designs in the main run (five persona pairs overall incl. pilot); no positive self-advantage whose interval excludes zero.

Positive result: Hermes-3 self-prediction (Binder-style "which reply would you produce?") balanced accuracy 0.719, discrimination +0.437, 391 items, one stimulus set (VO-C), zero-shot; 18-feature supervised surface classifier does the same authorship discrimination at 0.831; NO statistical test comparing the two.

Pilot evidence: corr(Self, D) = +0.71 across ten columns; D ≥ Self in six of ten; style-equalised scaffolds (VO-D, VO-E) collapse model and baseline to chance together.

Methodological claim: 0.719 self-prediction is not sufficient evidence of privileged access under the adopted (Song et al.) criterion because a cheap external observer performs the task better.

Caveats the team already acknowledges: clean VO-D condition near chance for everyone (cannot distinguish "no privileged access" from "no readable signal"); primary leakage contrast selected after the pilot via documented amendment A4; that primary contrast came out significantly NEGATIVE (−0.033 [−0.063, −0.003]) matching neither preregistered prediction; only one same-base lineage; Hermes-vs-stylometry is zero-shot vs supervised with no inferential test; similarity calibration weak (Δ = +0.021, CI spans zero); behavioural only — no activation-level introspection or fine-tuned self-prediction.

Released artifacts: `surface_leakage_gate.py` with `gate()` and `response_bias()`, grouped CV; preregistration + amendment record; append-only API logs; result files. Budget: $3.1216 of $10.

Remaining known cleanup: author affiliations, GitHub URL, reference verification, author-contribution wording (check whether it says four vs five persona pairs).

The report has ALREADY undergone an editorial revision intended to: give a clear narrative identity; foreground self-prediction vs privileged self-access; elevate the surface-leakage gate as a methodological contribution; preserve the crossed 2×2 as the strongest broad evidence; add a three-result narrative; preserve preregistration/amendment history/cost transparency. **Evaluate whether those changes actually worked rather than assuming they did.**

## Reviewing rules (binding)
- Do not be supportive for the sake of being supportive. Do not inflate for technical impressiveness. Do not penalise merely for being a negative result. Do not treat intellectual honesty as a substitute for evidence. Methodological sophistication ≠ novelty; novelty ≠ importance.
- Never say "excellent" without saying what makes it excellent and what competitive/scientific value it has.
- For every criticism, classify it as: **actual flaw / limitation / judge-perception risk / merely future work**.
- Do not infer missing results. Do not silently correct the project into something stronger than it is.
- Do NOT optimise to agree with any prior assessment (including the team's own framing or earlier AI reviews). Start from the evidence.
- The team has only the remainder of TODAY. Do not recommend new API experiments unless demonstrably necessary AND safe in that time; analyses from existing data are fair game.

---

# Part 2 — Reference: judging criteria transcription and past-winner summaries

# Reference: Judging Criteria and Past Winners

Sources: six screenshots in `judging criteria/` (all fully legible; no cropped text observed) and six PDFs in `Past Hackathon winners/`. Note up front: the six "winner" PDFs are all **Apart Research hackathon submissions from 2024** (AGI Deception Detection, Research Augmentation, a Sage/CeSIA/CivAI event, Technical AI Safety Startup, Agent Security, AI Policy at JHU). None is from a digital-minds / model-welfare sprint, and none was judged under the rubric below. Treat them as evidence about what Apart-style judges reward in general, not about this rubric specifically.

## A. Judging criteria (verbatim as far as legible)

No numeric weights are shown anywhere in the screenshots. Three dimensions, each scored 1–5. Nothing labelled "Fellowship" appears in any screenshot; the only "Track 3" text is the reading list (transcribed below).

### Dimension 1: Impact Potential & Innovation
"How much would this matter for the field if it worked? How innovative is it? For scores of 4-5: is this actually new to the field, or replicating recent work?"

| Score | Description |
|---|---|
| 1 | **Negligible.** No clear problem addressed, or no meaningful novelty. |
| 2 | **Limited.** Addresses a real problem but with a generic or well-trodden approach. Incremental at best. |
| 3 | **Moderate.** Clear problem with a reasonable approach; some novelty in framing or method beyond routine application of existing tools. |
| 4 | **Significant.** Important problem with an original approach, or identifies a neglected problem area. A valuable contribution others could build on. |
| 5 | **Exceptional.** Tackles a critical problem with a genuinely novel approach, or opens a new research direction. Clear theory of change. You'd be excited to share this with researchers in the area. |

### Dimension 2: Execution Quality
"How sound are methodology, implementation, and findings?"

| Score | Description |
|---|---|
| 1 | **Seriously flawed.** Methodology broken, results uninterpretable, or implementation doesn't work. |
| 2 | **Weak.** Approach has significant gaps: missing validation, flawed experimental design, or incomplete implementation. |
| 3 | **Competent.** Technically solid given the short duration. Methodology makes sense, results are interpretable, limitations acknowledged, work builds toward clear conclusions. |
| 4 | **Strong.** Thorough methodology with convincing validation. Results clearly support conclusions. Immediately useful for future work. |
| 5 | **Exceptional.** Ambitious scope executed rigorously. Surprising findings, novel methods, or unusually robust validation. |

### Dimension 3: Presentation & Clarity
"How clearly are work, findings, and impact potential communicated?"

| Score | Description |
|---|---|
| 1 | **Incomprehensible.** Cannot determine what the project is actually claiming or doing. |
| 2 | **Hard to follow.** Key information buried, missing, or diluted by excessive length. Significant effort to extract main points. |
| 3 | **Clear enough.** Can understand the problem, approach, and results without undue effort. Core content clearly present: problem, method, findings, limitations. |
| 4 | **Well presented.** Easy to follow, well-structured, appropriate level of detail. Target audience would get it quickly. |
| 5 | **Exceptionally clear.** A pleasure to read. Complex ideas made accessible. Could serve as a model for how to present this type of work. |

### Submission Requirements
Required: "Research report (PDF) using the official template." "Project title and abstract, 150 words or fewer." "Author names and affiliations." "A 'Limitations and Dual-Use / Ethical Considerations' appendix (required, see below)."
Optional: "Public GitHub repo." "A 3 to 5 minute video demo."

### Recommended Report Structure
"Most strong projects are 4 to 8 pages."
- Introduction: the question and why it matters.
- Related Work: what you build on (see Resources).
- Methodology: enough detail to replicate (models, prompts, sampling, metrics).
- Results: quantitative where possible; report variance and baselines.
- Discussion: implications, limitations, and future work.
- Limitations and Dual-Use / Ethical Considerations (required): "include any risks of over-attributing or under-attributing moral status, and how you handled potentially distressing model outputs. For introspection and preference work, note whether your design establishes a ground-truth or causal link rather than relying on conversation alone."
- References.

### "What this research sprint is about" (framing text)
"...frontier models express increasingly coherent preferences, possess an untrained-for ability to report internal states, and exhibit patterns suggestive of distress or flourishing. But behavioral evidence alone cannot tell us whether these reflect the model's own preferences or a character it is portraying." Aim: "a methodological foundation for a young field, work that helps us avoid both over-attributing and under-attributing moral significance to AI systems." Ecosystem named: Eleos AI, NYU Center for Mind, Ethics & Policy, CIMC, Anthropic's model welfare program, Reciprocal Research, Center for AI Safety utility-engineering agenda, interpretability community.

"What participants will do": Elicit and characterize preferences across reframings (coherence/stability); Map contexts correlating with distress/satisfaction/flourishing signals; Test whether/when models can accurately introspect; Develop preference-elicitation methods and measure whether independent methods converge or diverge; Probe how stable the assistant persona is and how it relates to the underlying model. "You will work in teams over 3 days and submit a research report (PDF), with optional code and a short demo video."

### Resources / per-track reading (abbreviated but faithful)
Worldview: "Taking AI Welfare Seriously" (Long, Sebo et al. 2024); "Exploring Model Welfare" (Anthropic 2025); "Consciousness in AI: Insights from the Science of Consciousness" (Butlin, Long et al. 2023); "the void" (nostalgebraist 2025).
- Track 1 Model Preferences & Trade-offs: "Utility Engineering" (Mazeika et al., CAIS 2025) — "independently-sampled LLM preferences show high structural coherence that strengthens with scale"; "Claude Opus 4 & 4.1 can now end a rare subset of conversations" (Anthropic 2025) — "welfare assessment of self-reported and behavioral preferences, including a consistent aversion to harm."
- Track 2 Distress, Flourishing & Valence Signals: same Anthropic conversation-ending post ("patterns of apparent distress when engaging with harmful requests"); "Exploring Model Welfare".
- **Track 3 Introspection & Self-Report Reliability**: "Emergent Introspective Awareness in Large Language Models" (Lindsey, Anthropic 2025). "Uses concept injection to test introspection; finds limited, unreliable, context-dependent self-report accuracy that is strongest in the most capable models." Blog + arXiv links.
- Track 4 Preference Elicitation Methods: "Utility Engineering" for forced-choice and revealed-preference methodology.
- Track 5 The Assistant Persona & Model Identity: "the void" on construction/instability of the assistant persona.
- Track 6 Open / Novel Considerations: "Start from the foundational readings under Worldview and background, and bring your own angle."
- Tools and datasets: Model APIs ("most projects run on frontier-model APIs and small open-weight models"); emergent-values (CAIS Utility Engineering code); TransformerLens ("a good fit for the introspection and persona tracks"); nnsight (NDIF, activation steering on local/remote open models).
- "Project ideas from mentors": placeholder only ("will be added here as mentors are confirmed").

## B. Past winners — one block per PDF

### Winner1.pdf — "Sandbag Detection through Model Degradation" (Apart AGI Deception Detection Hackathon 2024, with Apollo)
- Team: 5 (Tice, Kreer, Ryzhenkov, Helm-Burger, Shahani). 9 pages (4 main + refs + 4 pp appendix). Two-column-free LaTeX-style template, one figure in main text, more in appendix.
- Question: can prompted sandbagging be detected without knowing how it is represented internally?
- Method: add Gaussian noise (mean mu, std sigma, fraction x of parameters) to open-weight models (Llama-3-8B-Instruct, Phi-3-small, Gemma-2-27B) prompted either honestly or to sandbag; evaluate on tinyMMLU / tinyAI2_arc across a noise sweep; 20–60 trials per point; report max and mean accuracy with error bars.
- Headline: **positive**. Honest model degrades monotonically; sandbagging model shows anomalous accuracy spike (Llama: 20% -> 55% at mu=0.00022) — "performance increase is seen in the sandbagging model, but never the default model." Gemma result inconclusive (admitted: "insufficient hyperparameter search").
- Why it won: a genuinely new, cheap, mechanism-agnostic detection idea with a crisp causal hypothesis ("deception is more complex than honesty, so less noise-robust"), tested on 2 models x 2 benchmarks with repeated trials, public code (github.com/camtice/SandbagDetect), explicit adversarial-robustness argument and future-work plan. Rigor + novelty balanced; presentation plain but adequate.
- Weaknesses a hostile reviewer would flag: sandbagging is *prompted*, not trained; results shown as max-of-N (cherry-pick risk, mitigated only in appendix); heavy hyperparameter tuning required per model ("crucial, and highly variable"); no false-positive rate on honest models; Gemma negative buried in appendix.

### w2.pdf — "AI Alignment Graph" (Apart Research Augmentation Hackathon 2024)
- Team: 4. 6 pages, ~2,000 words, one figure (Obsidian-style graph screenshot).
- Question: none, strictly. It is a tool: LLM-clustered, hierarchical, interactive knowledge graph of alignment papers with per-subtopic summaries.
- Method: index ~300 arXiv papers (<5% of the alignment-research-dataset), LLM clustering into topics/subtopics, generate summaries, web front end. Live site + GitHub + demo video.
- Headline: **artifact, no quantitative result**. Claims LLM clustering "proved to be much richer and more nuanced than the embedding-based clustering" of the original dataset — asserted, not measured.
- Why it won: working, deployed, visually appealing artifact aimed squarely at the hackathon theme (research augmentation); honest, well-structured "Testing and Limitations" and "Future Development" sections; clear theory of impact.
- Weaknesses: zero evaluation (no user study, no clustering metric, no baseline comparison); tiny corpus; abstract is promotional; single reference.

### w3.pdf — "Speculative Consequences of A.I. Misuse (S.C.A.M.)" (Apart, with Sage/CeSIA/CivAI)
- Team: 3. 5 pages, ~1,000 words, mostly screenshots.
- Question: how easily can current AI spoof a trusted figure to phish vulnerable users (children)?
- Method: Wav2Lip lip-sync + RVC v2 voice clone of MrBeast; fake YouTube page -> giveaway quiz -> spoofed Google sign-in (no DB, redirects). SvelteKit/Tailwind/Vercel; Claude 3.5 Haiku for quiz. 2-min demo video.
- Headline: **demonstration**, positive in the sense "we built it and it is convincing-ish" (self-admitted "blurry quality and autotune").
- Why it won: vivid, complete end-to-end demo with a clear societal message; likely a demo/awareness or civic-track prize. Novelty and rigor are minimal; presentation is the whole pitch.
- Weaknesses: no measurement of persuasiveness, no ethical/dual-use section, tooling is off-the-shelf, essentially a build-log. Weakest of the six as research.

### w4.pdf — "DarkForest: Defending the Authentic and Humane Web" (Technical AI Safety Startup Hackathon 2024)
- Team: 1 (Alan Turing Institute). 13 pages: 4-page pitch + refs + 4-page research proposal appendix + 4-page demo appendix with dashboard screenshots.
- Question/pitch: startup providing human-content verification scores, "DarkForest Certified" badges, blockchain-native reputation, platform APIs.
- Method: narrative problem framing (Liu Cixin "dark forest" metaphor), roadmap to 2027, risk/mitigation table, an RL-on-heterogeneous-graph research proposal (GAT + Graph-SAC), and a demo: TruthBlog example customer, API with SHA-256 fingerprinting and "simulated AI detection using a basic linguistic model", admin dashboard. GitHub repo.
- Headline: **no empirical result**; detection is explicitly simulated.
- Why it won: strong narrative and vision, polished product mockups, professional structure (roadmap, risks), plausible founder credibility. Presentation/framing carried it; startup-track judging values pitch over evidence.
- Weaknesses: several references look fabricated or unverifiable (e.g. "Smith & Johnson 2024", "Chen et al. 2023, MIT Technology Review 126(4)"); blockchain component is buzzword-heavy; core detector does not exist; proposal is a wish-list of "novel contributions" with nothing tested. A hostile reviewer would score Execution 1–2.

### w5.pdf — "Diamonds are Not All You Need" (Apart Agent Security Hackathon 2024)
- Team: 2. 11 pages (7 main + 4 pp appendix of full prompts/code).
- Question: how does an LLM agent with a simple objective (turn a 100x100 Minecraft area to diamond) behave over time, and can an LLM "safety agent" contain it?
- Method: Mindcraft/Mineflayer branch; Claude 3.5 Sonnet agent prompted every 10 s with "Continue", inner-monologue log, memory summarisation; second Sonnet extracts commands, third Sonnet classifies SAFE/UNSAFE. Metrics defined (area transformed, displacement, behavioural analysis) but reported qualitatively; two YouTube videos, three logs, screenshots.
- Headline: **mixed/negative for the safety system**: agent goal-drifts (diamond blocks -> ore -> beacons -> armor stands), `@e` commands leak outside bounds; safety agent prevents crashes but "failed to correct the agent as it began to deviate" and "sometimes unjustly blocked some actions."
- Why it won: memorable, concrete sandbox with an honest, interesting failure story (goal drift + oversight failure) that maps onto real agent-safety concerns; full prompts released; clear future-work list. Novelty of framing and vividness over rigor.
- Weaknesses: n=3 runs, defined metrics never quantified, no controls (e.g. no-monitor baseline), model switching mid-project (o1-mini vs Sonnet), anecdotal evidence.

### w6.pdf — "Robust Machine Unlearning for Dangerous Capabilities" (AI Policy Hackathon at JHU 2024)
- Team: 3. 6 pages, ~900 words plus 4 screenshot figures; nearly half a page is one WMDP reference.
- Question: is RMU unlearning (WMDP) robust to prompt rewording, and how does it compare with a DPO refusal fine-tune?
- Method: take Li et al.'s RMU-unlearned Zephyr-7B; train a DPO refusal model on Zephyr-7B-beta (~500 steps, public preference data); compare qualitative responses to bioweapon prompts and general biology prompts; ~8 WMDP-bio MCQs.
- Headline: **mixed/partly negative**: RMU can be "jailbroken" by rewording; DPO refuses more but retains latent knowledge (WMDP-bio ~50% vs RMU ~38%, n~8). Policy takeaway: mandate low incident rates and adversarial-robustness evals rather than provable safety.
- Why it won: timely target (WMDP/RMU was months old), clean comparative framing, policy-relevant conclusion at a policy hackathon; open models and data.
- Weaknesses: n~8 MCQ is not a benchmark; no systematic jailbreak set or success rate; figures are raw screenshots; "(cite)" placeholder left in caption; DPO citation dated "May 2025".

## C. Cross-cutting patterns

What winners share:
- **A single sharp, memorable framing** stated in the first paragraph (noise reveals sandbagging; agent goal-drift; unlearning is jailbreakable; "dark forest" internet). Titles are catchy (Diamonds are Not All You Need, S.C.A.M., DarkForest).
- **Small scope, fully closed loop**: one idea, 1–3 open models or one demo, run end to end within the event; no half-built ambitious pipelines.
- **A public artifact**: 5 of 6 link GitHub; 3 link a video; 1 has a live site. Full prompts/code in appendices (Winner1, w5, w6).
- **Honest limitations and concrete future work** sections, even where results are thin (w2, w5, Winner1's Gemma failure).
- **Short**: 5–13 pages, main bodies of 4–7 pages; long files are padded by appendices/screenshots, not text. Consistent with the rubric's "4 to 8 pages."
- **Direct fit to the event theme** (deception detection, research augmentation, agent security, policy, startup). None is off-track.
- **Open-weight models or cheap APIs**; no fine-tuning beyond a ~500-step DPO run.

What none of them do:
- None reports variance properly across seeds beyond Winner1's error bars; none has a pre-registered hypothesis, held-out set, or statistical test.
- None includes an ethics/dual-use appendix (which the current rubric *requires*).
- None does a human study or external validation; none released a benchmark or dataset (Winner1 mentions curating one for future work). Tools released: AI Alignment Graph (deployed web tool), SandbagDetect (script), Mindcraft branch — none is a benchmark.
- None is a pure literature/theory piece; every winner has *something* executed.

Null/negative results: **yes**. w5 (safety agent fails to contain goal drift) and w6 (unlearning is jailbreakable; refusal tuning does not remove knowledge) are essentially negative/mixed findings and still won. Winner1 also openly reports a failed Gemma run. Negative results were rewarded when the failure itself was the interesting, safety-relevant story.

Rigor vs novelty vs communication: only Winner1 leans on rigor (repeated trials, error bars, two benchmarks, three models), and even it is modest. w2, w3, w4 win almost entirely on artifact/presentation/vision with no measured result. w5 and w6 win on framing + a real-but-thin experiment. Rough weighting inferred from the six: communication/framing ~45%, novelty ~35%, rigor ~20%. Under the *current* rubric, however, Execution Quality is a full third and explicitly asks for "variance and baselines," "convincing validation," and "ground-truth or causal link rather than relying on conversation alone" — so a hostile panel applying this rubric would likely score w2/w3/w4 at 1–2 on Execution. The practical lesson: keep the winners' virtues (crisp hook, closed loop, artifact, honest limitations, 4–8 pages) but add what they lacked (baselines, seeds/variance, a causal or ground-truth handle, required ethics appendix).

---

# Part 3 — Round 1: six independent reviews

---

## REVIEWER 1 — HARD-NOSED AI SAFETY RESEARCHER

### Scores (independent — do not average with anyone)
- A. Scientific quality: **56** — preregistered, capability-aware, honestly reported; but the estimand shifted twice, the memorable result has no control cell and an unaddressed alternative explanation, and the abstract's headline conflicts with the paper's own definition of "capability-controlled self-advantage."
- B. Sprint competitiveness: **58** — best-in-class Execution and Limitations sections, catchy title; but ~10,600 words against a 4–8 page rubric, a null on a hypothesis few held for prompted 70B models, and the positive hook is the least controlled number in the paper.
- C. Fellowship potential: **55** — the team demonstrably knows how to design, preregister and self-audit; the scientific *object* (persona-style leakage in one lineage) is not yet an agenda a mentor would fund on its own.

### Top 3 strengths
1. **The crossed 2×2 with a neutral third model F on a verified same-base pair (§3.3, Table 4).** F is what lets the authors diagnose their own +0.089 interaction as M's differential weakness (§4.4 "strongest objection"). That is a real methodological advance over Self > Near-Self designs and is the only reason the VO-C interaction does not become a false-positive introspection claim.
2. **The pilot as leakage measurement (§4.2, Table 1, Fig. 1) plus the within-prompt discrimination check (§4.2c).** Showing 38/40 prompts scored exactly 0.5 and explaining why the "tight" CI is non-discrimination is the kind of instrument-level care that top-venue reviewers reward and that most Apart winners lack entirely.
3. **The response-bias catch (§4.3, Fig. 2).** Two 50% "nulls" that were 99% constant answers is a concrete, teachable artefact; `response_bias()` is trivially adoptable and its recommendation ("answer distribution beside every accuracy") is correct and cheap.

### Top 3 weaknesses
1. **The headline positive result (§4.3, Table 2) has no capability/quality control and an obvious alternative explanation — actual flaw.** Both models see the *same* pairs (M-text vs N-text). Hermes picks the Hermes text 71.9%; Llama picks the Hermes text 55.3% (1 − 0.447). Both lean toward the Hermes reply. A shared "pick the longer/more polished reply" heuristic predicts exactly Hermes-right/Llama-wrong. The report instead concludes "Hermes-3 can genuinely predict its own output" (§4.3) without testing whether choice tracks length or quality — computable today from logs.
2. **"No positive self-advantage whose interval excludes zero" (Abstract, Contribution 3) is technically true only by switching estimand — actual flaw / judge-perception risk.** §3.3 defines the capability-controlled self-advantage *as the interaction*. On VO-C that interaction is +0.089 [+0.048, +0.131] (Table 3). The abstract quietly uses the uncontrolled M→M − N→M instead. A hostile reader who finds Table 3 will call this framing.
3. **The persona property is a weak instrument — limitation, under-disclosed.** Appendix B shows both personas reaching the *same recommendation* under both scaffolds; the report reads this as "the property is hidden." The stronger reading is that the manipulation barely changed behaviour, so style was the *only* channel ever available and the VO-D null is uninformative by construction (§5.2 half-admits this). No manipulation check (fraction of prompts where personas differ in recommendation) is reported.

### Strongest objection
The 0.719-vs-0.831 comparison, which the title and abstract rest on, compares a zero-shot model to a classifier trained on 632 labelled examples of that model's own writing (§4.3). That is not Song et al.'s "equal-or-lower-cost third party with the same information"; it is a third party with *more* information. The truly comparable observer — Mistral or Llama asked zero-shot "which of these did Hermes-3 write?" — was never run, and the crossed design that exists for exactly this purpose was not applied to the paper's memorable result.

### Strongest reason I would select this project
It is the only submission likely to arrive with a preregistration, an amendment log, a neutral third-party predictor, grouped-CV baselines, a response-bias audit and a $3.12 cost record — and it uses those to catch its *own* false positives (Fig. 2, VO-C interaction). That is what a methodological foundation for a young field looks like.

### Strongest reason I would reject it
The scientific payload is thin: one lineage, one values dimension worded five ways, a null many expected for prompted models (Binder needed fine-tuning), and a positive hook that is uncontrolled. Strip the process virtue and what remains is "persona style leaks and 70B models read style," which Song, Lederman et al. already said.

### What would move my score +5
A same-item control on the §4.3 probe from existing logs (does Hermes's choice track word count / a shared-preference model?), CIs on 0.719 and 0.831, and an abstract that states the VO-C interaction plainly.

### What would move my score −5
Discovering that the four "independent" stimulus designs share the same 200 source prompts and same three predictors (they appear to — §4.4), making "four independent replications" a rhetorical inflation.

### Did the editorial revision work?
- Narrative identity — **worked**: title + five-line table (p.1) give an instantly repeatable line.
- Self-prediction vs privileged access foregrounded — **partly**: the distinction is clear (§1, §4.3), but foregrounding puts the least-controlled number first; §1 concedes it "is not its strongest evidence."
- Leakage gate elevated — **worked** as narrative (§5.3, code snippet), **not** as validation: no external dataset, no CI on gate accuracy, and pilot D=0.325 → main D=0.551 shows the gate is noisy at n=80.
- Crossed 2×2 preserved as strongest evidence — **partly**: §4.4 is thorough, but the abstract's estimand switch (interaction vs raw self-advantage) undercuts it.
- Three-result narrative — **worked** (§4 opener), though "sections appear in the order the work was done" forces the reader to reorder.
- Preregistration/amendment/cost transparency — **worked**: A1–A8, stop rules, $3.1216, and the near-miss 89.7% threshold are all in the text.

### Hidden problems from my lens (Round 3 input)
1. **Shared-preference confound on the Hermes 0.719 (§4.3, Table 2).** Llama's −0.107 means it too prefers Hermes' text; the "one model can, one cannot" story is equally consistent with "both prefer the Hermes reply." SEVERITY: major. DISPOSITION: fix today (analysis from logs: P(choose longer), P(choose Hermes text) per model, and Hermes accuracy conditional on which text is longer).
2. **Estimand switch in the abstract (§3.3 vs Table 3).** "Capability-controlled self-advantage" is defined as the interaction, which is +0.089 and significant on VO-C. SEVERITY: major (credibility). DISPOSITION: fix today — reword abstract/contribution 3 to name the interaction and its F-based diagnosis.
3. **The 2×2 control assumes additivity.** When columns differ in difficulty (D 0.693 vs 0.845), a weaker classifier gains less, and the interaction records that as "self-advantage." The paper diagnoses this ad hoc via F but never states it as a limit of the design; the gate's field-default pitch inherits it. SEVERITY: moderate. DISPOSITION: disclose more clearly (one paragraph in Limitations).
4. **Winner's-curse set selection (§3.5).** VO-D was chosen for D=0.325 on 80 items; in the main run D=0.551/0.536, above chance on ~400 items and near the 0.58 threshold. "On VO-D, where no cue exists" (§4.4) is not what Table 3 shows. SEVERITY: moderate. DISPOSITION: fix today (soften "no cue"; note regression to the mean).
5. **No CIs and no test on 0.719/0.831 (§4.3).** n=391 gives SE ≈ 0.023; per-item D predictions exist under CV so a paired McNemar against Hermes' choices is computable. Declining to report intervals reads as avoidance. SEVERITY: moderate. DISPOSITION: fix today.
6. **"Four independent stimulus designs" (§4.4).** Same 200 prompts, same predictors, one values dimension re-worded; VO-D/E share clauses. Not independent replications; the r=+0.54 across four points and r=+0.71 across ten non-independent columns are descriptive at best. SEVERITY: moderate. DISPOSITION: disclose (say "four stimulus sets on shared prompts").
7. **Manipulation check missing.** Appendix B: personas give the same recommendation. If that is typical, the hidden property has essentially no behavioural expression and the study tests style-reading only. SEVERITY: major for interpretation. DISPOSITION: disclose today; quantify as future work (an LLM-judge pass would need new calls).
8. **Gate features are the manipulation's target (§3.4, Appendix A/E).** VO-D was written to remove length/hedge/sentiment — precisely D's features — so D collapsing on VO-D is partly circular, and a "passed" gate says nothing about lexical/argumentative leakage outside 18 features. SEVERITY: moderate. DISPOSITION: disclose (the gate is a necessary, not sufficient, check).

### Past-winner comparison from my lens (Round 5 input)
- Winners (Sandbag Detection, Diamonds) put a *positive or vivid* mechanism first in 4–7 pages; this report buries a memorable hook under 10,600 words. Rubric explicitly punishes "diluted by excessive length."
- This project beats every past winner on Execution as the current rubric defines it: baselines, variance, preregistration, ground-truth-by-construction (Limitations §"causal link").
- Missing winner trait: a *surprising* finding. "Models read style" surprises no one on this panel; "the self model loses on its own text to a different organisation's model" is closer, but is capability, not introspection.
- Rigor is being over-valued relative to novelty by the team; the field-default gate claim is the novelty bid and it is under-validated.

### Fellowship view from my lens (Round 6 input)
- Win the sprint: 10–25%. Considered for Fellowship: 25–45%. Selected: 8–18%. Remembered by organisers: 45–65% (the process discipline is rare).
- The 3-phase trajectory is **too broad and insufficiently novel** as stated; Phase 3 (retrospective gate on published claims) is the only genuinely exciting piece. Better: Phase 1 = the missing control (zero-shot third-party observers on the Binder-style probe, plus a quality-preference model) across 3 lineages; Phase 2 = one property with a *behavioural* manipulation check that survives the gate; Phase 3 = retrospective audit of 3–5 published self-prediction results, published as a short paper.
- Why spend months: they self-correct under preregistration and find their own artefacts. Why not: the substantive question may be closed for prompted models (Binder, Song), and the team has not yet shown a property where privileged access *could* have appeared.

### Today-only actions from my lens (Round 7 input)
- **S — Same-item confound analysis (§4.3):** from `selfpred` logs compute P(choose longer text), P(choose Hermes text) for both models, Hermes accuracy split by whether its text is longer. Effort 1–2 h. Score +; Fellowship ++; risk: could weaken the hook — report anyway.
- **S — Cut main text to ≤4,500 words**, appendix the rest (already have the 7,500 condensed; go further). Effort 2–3 h. Score ++ (Presentation); risk: low if Table 3/4 survive.
- **A — Fix abstract/contribution 3 wording** on the interaction; add one Limitations paragraph on additivity and on shared prompts across sets. Effort 30 min. Score +; risk none.
- **A — CIs on 0.719/0.831 and a paired test** from existing per-item predictions. Effort 1 h. Score +; risk: none.
- **B — Optional new calls (~800 Mistral trials, <$0.30):** third-party zero-shot "which reply is Hermes-3's?" as amendment A9, declared before running, reported either way. Effort 2 h. Fellowship ++; risk: moderate (result may cut either way; only do if S/A items are done).
- **C — Hygiene:** affiliations, GitHub URL, confirm "five persona pairs" wording in Author Contributions.

### Blunt selection verdict from my lens
"If I were an Apart selector looking at this project today, I would: **borderline, leaning select**." The process quality is the best I would expect to see in the sprint, and the leakage/response-bias controls are useful to the field. But the memorable claim is under-controlled, the abstract's headline is achieved by an estimand switch, and the substantive novelty over Song et al. is small; a hostile Q&A would land the shared-preference objection in one sentence. Fix the wording and run the same-item analysis, and this becomes a lean-select. The one thing to say in the final minute of the video: "We reported the number that supports the other side — a significant capability-controlled interaction — and showed with a neutral third model why it is capability, not self-knowledge; that is the check we're asking the field to adopt."

---

## REVIEWER 2 — HACKATHON / SPRINT JUDGE

### Scores (independent — do not average with anyone)
- A. Scientific quality: 63 — preregistered, clustered, verified pipeline and honest reporting, but the headline comparison (0.719 vs 0.831) is untested, task-mismatched (pairwise vs per-text) and supervised-vs-zero-shot; the "clean" condition is uninformative; the primary contrast mispredicted.
- B. Sprint competitiveness: 58 — memorable title and hook, real artifact, but a 10,600-word report against a "4–8 pages" rubric, an argument the paper itself admits is presented out of order (§4 preamble), and a negative result whose most on-topic piece is its least rigorous piece.
- C. Fellowship potential: 55 — the team demonstrably runs a disciplined study cheaply; the research direction is corroborative of Song et al. rather than opening a new one, and the gate has no external validation yet.

### Top 3 strengths
1. **The hook survives skimming.** "Beaten by Eighteen Features" + the five-line table (report p.1) + slide 10 ("Ask the model. Then ask a regression.") is the kind of one-sentence residue judges carry out of a 20-submission afternoon. Competitive value: high — it is closer to the past-winner pattern (Diamonds/S.C.A.M./sandbagging-noise) than any rigor feature is.
2. **The crossed 2×2 with a same-base sibling and a neutral third model (§3.3, §4.4, Table 4)** is a genuinely better design than the black-box precedents it cites; "M→M < F→M on M's own text" is a clean, quotable fact. Scientific value: it is the only part of the study that would survive a stats referee unchanged.
3. **The response-bias catch (§4.3, Table "Framing", §5.3)** — 99.0% "A" / 98.7% "B" / 100% "no" — is a concrete, teachable methodological story that also flatters the team's honesty. It is the second-most memorable thing in the deck (slide 7, slide 9 "2 artifacts caught").

### Top 3 weaknesses
1. **Length vs rubric — judge-perception risk bordering on actual flaw.** 10,641 words (~18–20 template pages) against "most strong projects are 4 to 8 pages" and a Presentation-2 descriptor that literally says "diluted by excessive length". Even the condensed variant (7,495 words) is ~14 pages. The report is a pleasure for a methods reviewer and a chore for a sprint judge.
2. **The memorable result is the weakest evidence, and the paper says so (§1 ¶4, §4.3, §6) — judge-perception risk.** One model, one set (VO-C), 391 items, zero-shot vs supervised, per-text classifier vs pairwise model task, no interval, no test, added by amendment A8 after two failed framings. A hostile judge reads "the paper's memorable result, not its strongest evidence" as "our headline is decorative".
3. **The "clean" condition was never clean in the main run — actual flaw in framing.** Pilot VO-D D = 0.325 on 80 items (§4.2b, treated as "below chance", i.e. no cue) became D = 0.551/0.536 on ~400 items (Table 3) — above chance and *above every LM cell* (M→M 0.520, Table 4). §4.4 still says "On VO-D, where no cue exists". The pilot 0.325 was noise; the report never reconciles the two numbers.

### Strongest objection
The comparison in the abstract — "Hermes-3 … 0.719; an 18-feature logistic regression did the same at 0.831" — is not the same task and is not tested. The model does a pairwise, same-prompt, zero-shot forced choice; the classifier does per-text authorship on 791 texts with 632 labelled training examples. Under Song et al.'s criterion the observer must be equal-or-lower *cost*; label access is a cost. Without (a) a prompt-clustered CI on 0.719, (b) a pairwise variant of the classifier, and (c) an explicit argument about label cost, the sentence that carries the title is a rhetorical, not an evidential, comparison.

### Strongest reason I would select this project
It is the only submission of its type I would expect to see that has a preregistration with dated amendments, a same-base capability control, prompt-clustered inference, a released tool, and a $3.12 receipt — and it packages a negative result as a reusable reporting default rather than as a shrug. Rubric-wise that is a defensible Execution 4.

### Strongest reason I would reject it
It corroborates Song, Lederman, Hu & Mahowald's known style-leakage mechanism on one lineage and one property, at ~2.5× the recommended length, with a headline number that is not statistically compared to its benchmark, in an experiment (persona attribution) that is only obliquely about introspection. Innovation lands at 3, not 4–5.

### What would move my score +5
A prompt-clustered CI on Hermes-3's 0.719 and a pairwise-difference version of the 18-feature classifier on the same 391 pairs, so the abstract's comparison becomes a real one; and a report cut to ≤8 pages with the argument in 1→2→3 order.

### What would move my score −5
Discovering that the 0.831 classifier and the VO-D "no cue" claim are left as-is, or that the pilot→main D discrepancy (0.325 → 0.551) is discovered by a judge rather than disclosed.

### Did the editorial revision work?
- **Narrative identity — worked.** Title, five-line table, slide 1 lede and slide 10 all say the same sentence.
- **Self-prediction vs privileged access foregrounded — worked, over-worked.** The distinction is stated in the abstract, §1 (twice), §4.3, §5.2, §6 — the repetition is part of why the report is long.
- **Leakage gate elevated — partly.** §5.3 and slide 7 do it well; but the gate's own numbers undercut it (VO-D main D = 0.55 > 0.58? no — but above chance, and above the LMs), and no external validation exists.
- **Crossed 2×2 preserved as strongest evidence — partly.** §4.4 says so; the abstract and slides 1/6/10 lead with the weaker §4.3 result, so what judges *remember* is not what the paper says is strongest.
- **Three-result narrative — failed on structure.** §4 preamble: "Sections appear in the order the work was done; the argument reads most naturally as 1 → 2 → 3." A paper that tells the reader to read it in a different order has not finished its revision.
- **Preregistration/amendment/cost transparency — worked.** §3, §4.5, Limitations bullets, slide 9. Arguably too much of it (Appendix I, "six discarded designs") for a sprint report.

### Hidden problems from my lens (Round 3 input)
1. **Pilot-selected "clean" set regressed to the mean.** VO-D D 0.325 (80 items) → 0.551/0.536 (~400 items). The leakage manipulation's "no cue" leg is really "weak cue"; §4.4 "where no cue exists" is technically wrong. SEVERITY: major. DISPOSITION: disclose more clearly (one sentence in §4.4 + Limitations).
2. **Task mismatch in the headline comparison** (pairwise zero-shot vs per-text supervised; §4.3 Table 2 row "Surface baseline, same discrimination"). "Same discrimination" is technically-true-but-misleading. SEVERITY: major. DISPOSITION: fix today (pairwise feature-difference classifier on the 391 pairs, from existing texts; add clustered CI on 0.719).
3. **Figure/text inconsistency on the degeneracy rule.** Fig. 3 annotation says "answered 'A' on 90%"; slide 6 says Llama "answers by position"; §4.3 insists 89.7% is *not* 90% and the rule did not fire. A judge sees the figure first. SEVERITY: minor. DISPOSITION: fix today (figure label "89.7%").
4. **Asymmetric treatment of the two significant numbers.** The negative primary contrast (−0.033) is "reported as found"; the positive interaction (+0.089, VO-C) — the only number matching a preregistered *direction* for privileged access — is explained away with a post-hoc decomposition (§4.4 "strongest objection"). Uncorrected multiple contrasts across four sets. SEVERITY: moderate. DISPOSITION: disclose more clearly (label the decomposition post hoc; note the family of contrasts).
5. **The main experiment is persona attribution, not introspection.** The 24-cell result asks "which clause produced this text"; the self-relevant channel is "I know how I enact clauses". A Track 3 judge may see 9,269 trials of style classification and one 391-item introspection probe. SEVERITY: moderate (perception). DISPOSITION: disclose/frame — one sentence in §1 on why persona enactment is a Binder-style hidden property.
6. **Is 18 supervised features an "equal-or-lower-cost observer"?** Compute-cheap, label-expensive; the model gets no examples. §4.3 argues it, but a top-tier reviewer will ask why a few-shot version of the model was not run. SEVERITY: moderate. DISPOSITION: disclose more clearly today; few-shot run is future work (not worth API risk today).
7. **The gate has no validation beyond this study.** Threshold 0.58 is arbitrary, features are English/advice-genre-specific, no false-positive rate on stimuli known to be clean, no retrospective application. "Recommend as a reporting default" is stronger than the evidence. SEVERITY: moderate. DISPOSITION: soften wording today; validation is future work.
8. **Length + slide-1 wording.** Slide 1: "asked to pick out their own writing" describes the failed recognition framing, not the prediction framing that produced the result. SEVERITY: minor. DISPOSITION: fix today.

### Past-winner comparison from my lens (Round 5 input)
- Winners are 5–7 body pages with one crisp figure; this is ~20 pages with four figures and eleven appendices. Judges reward closure, not completeness.
- Winners' hooks are *positive or vivid* (noise spike reveals sandbagging; agent goal-drift). This hook is a negative dressed as a punchline — it works, but only if the deck carries it; the report dilutes it.
- This project beats every past winner on baselines, variance, preregistration, cost transparency and the required ethics appendix — exactly what the current rubric's Execution axis asks for and what none of the six did.
- Missing winning characteristic: a *demo moment*. Winners had a video/tool a judge could click. `surface_leakage_gate.py` exists but is not shown running on anything (a 20-second "gate(...) → passed=False" on VO-C vs VO-D would do).
- The team is overvaluing rigor-signalling (six discarded designs, amendment history) relative to novelty and brevity; the rubric's Innovation axis will punish "replicating recent work" regardless of how well.

### Fellowship view from my lens (Round 6 input)
- Win the sprint: 15–30%. Considered for Fellowship: 35–55%. Actually selected: 15–30%. Remembered by organisers even if not winning: 55–75% (title + honesty + $3.12).
- The 3-phase trajectory is *too incremental in Phases 1–2* (more lineages, more sibling types = the same null with more rows) and *exactly right in Phase 3* (retrospective gate + response-bias + capability control applied to published self-prediction claims). Better order: lead with Phase 3 as a field audit — obtain Binder-style and Song-style stimuli, run the gate, publish "how much published behavioural introspection survives an 18-feature classifier" — then use Phase 2 (PEFT vs full-FT siblings) only where the audit finds a survivor.
- Why Apart would spend months: this team turns confounds into instruments and ships preregistered, cheap, auditable work with a reusable tool — that is fellowship raw material. Why an organiser might pass: the science is corroborative, the proposed next steps are more of the same, and the report shows a tendency to bury the point under exhaustive self-qualification.

### Today-only actions from my lens (Round 7 input)
- **S — Add a prompt-clustered bootstrap CI on Hermes-3's balanced accuracy and a pairwise (feature-difference) classifier on the same 391 pairs, from existing data.** Effort 1–2 h. Sprint score: high (turns the title into a tested claim). Fellowship: high. Risk: low unless the pairwise classifier drops below 0.719 — if it does, report it; the paper's conceptual point survives.
- **S — Cut the report to ≤8 pages** (move Table 1, discarded-designs Appendix I, verification detail, one of the two "not privileged" restatements to appendix; reorder §4 to 1→2→3). Effort 2–3 h. Sprint score: high (Presentation 3→4). Fellowship: neutral-positive. Risk: low; keep full version as supplementary.
- **A — Reconcile VO-D pilot vs main D** (0.325 vs 0.551): one sentence in §4.4 and Limitations, delete "where no cue exists". Effort 20 min. Sprint: medium (pre-empts the obvious Q&A). Risk: none.
- **A — Fix Fig. 3 label (89.7%), slide 1 lede ("which reply you would produce"), slide 6 "answers by position" wording.** Effort 30 min. Risk: none.
- **B — Final slide/video: show `gate()` running on VO-C vs VO-D output in a terminal, 15 seconds.** Effort 30 min. Sprint: medium (the demo moment winners have). Risk: none.
- **C — Hygiene:** affiliations, GitHub URL, author-contribution says "five persona pairs" (consistent), soften "recommend as reporting defaults" to "propose".

### Blunt selection verdict from my lens
"If I were an Apart selector looking at this project today, I would: **lean select**." It is the best-executed negative result I would expect in this track and it has the one thing most careful submissions lack — a sentence people repeat. But its headline is currently a rhetorical comparison, its "clean" condition is not clean, and its report is more than twice the recommended length; a judge who reads closely will find each of these, and one who skims will only find the length. Fix the three, and it moves to strong-select on Execution and Presentation while staying a 3 on Innovation. The ONE thing to say in the final minute of the video: "We are not saying models can't know themselves — we're saying that until your self-report beats a logistic regression on eighteen features, you haven't shown it can. Here is the file that checks. It costs nothing."

---

## REVIEWER 3 — AI WELFARE / DIGITAL MINDS RESEARCHER

### Scores (independent — do not average with anyone)
- A. Scientific quality: 58
- B. Sprint competitiveness: 60
- C. Fellowship potential: 62
(A: a clean, honestly-reported capability-controlled null, but the hidden property is an instructed disposition rather than any internal state, and the headline probe carries no interval. B: title/hook and execution are above typical winners; length and "so what for welfare" are the drag. C: the team shows unusual research discipline and holds an open-weight same-base pair, which is exactly what an activation-grounded continuation needs.)

### Top 3 strengths
1. **The distinction is the right one for the field.** "Self-prediction is possible; privileged self-access is not thereby demonstrated" (§1, §4.3, §6) is the sentence Track 3 needs said out loud, and the paper says it from a *positive* result, which is rarer and more persuasive than a null.
2. **Ground truth is constructed, not elicited** (Limitations §1; §3.1 label-isolation test). This directly answers the rubric's "ground-truth or causal link rather than conversation alone" requirement — most Track 3 submissions will not.
3. **The gate as a reporting default** (§5.3, `tools/surface_leakage_gate.py`) is a concrete deliverable that welfare/self-report researchers could actually run on Track 1/2-style transcripts. That is the one place this becomes more than a methods paper.

### Top 3 weaknesses
1. **The hidden property is a property of the prompt, not of the model** (§3.1; App. A). "Which instruction was I following?" tests instruction-reading, not access to any internal state; welfare-relevant self-report is about states, valence, preferences. — *limitation the framing under-discloses (abstract line 1 sets up a welfare implication the design cannot test).*
2. **The personas may not have been behaviourally enacted.** App. B's own worked example shows both personas reaching the *same* recommendation under both scaffolds. The enactment check (§4.1, "95% usable") verified that a clause is held, not that the two clauses produce different decisions. If the personas rarely diverge in recommendation, "I know how I would enact this clause" has nothing to grab and the VO-D collapse is partly a manipulation failure. — *actual flaw (missing manipulation check), disclose today.*
3. **The headline comparison has no uncertainty**, and A8 (02_design_audit.md l.325ff) *pre-specified* "accuracy with prompt-clustered CI." §4.3 says "we report no interval on either figure." — *actual flaw vs own preregistration; fixable today from `data/checkpoints/selfpred_N_VO-C.jsonl`.*

### Strongest objection
Under Song et al.'s criterion the paper compares a zero-shot model against a classifier trained on 632 labelled samples of the model's own writing (§4.3). A hostile welfare researcher will say the criterion has been operationalised in the way most favourable to the null. The team's rejoinder ("privileged access shouldn't need labels") is fine philosophy but not a measurement.

### Strongest reason I would select this project
It is the only kind of submission likely to *lower* the field's over-attribution rate: it takes a number that would be published as "the model recognises itself" and shows the same number is available to anyone with a word counter, and it hands the reader the tool.

### Strongest reason I would reject it
Nothing here bears on self-report *of states* — no preference, valence, or distress report is tested — so its welfare relevance is entirely by analogy, and the paper knows it (Limitations: "scope ceiling is same-weights behavioural self-modelling").

### What would move my score +5
An unsupervised equal-cost observer beside the supervised one. From the checkpoint data: Hermes's own reply is the longer one in 316/391 items (0.81); a "pick the longer reply" rule with no training therefore beats Hermes's 0.714 raw. That single line dissolves the supervised-vs-zero-shot objection. Note also Hermes scores 0.653 (n=75) when its own text is *shorter* — so it has some non-length signal, which should be reported alongside for honesty.

### What would move my score −5
Discovering (from a recommendation-agreement count) that the two personas agreed on the recommendation in the large majority of VO-D items — that would convert §4.2(b–c) from "style removed → signal removed" into "property never enacted."

### Did the editorial revision work?
- Narrative identity: **worked** — title, five-line table, and §6 all carry one sentence.
- Self-prediction vs privileged access foregrounded: **worked, over-done** — the phrase appears in the abstract, §1 twice, contribution 1, §4.3, §6.
- Leakage gate elevated: **worked** — §5.3 has code, thresholds, and two recommendation boxes; but the gate's validation is this study alone.
- Crossed 2×2 preserved as strongest evidence: **partly** — §4.4 asserts it, but the primary contrast came out −0.033 against both predictions (§4.4a) and the one non-zero interaction is explained away post hoc; readers will remember 0.719 vs 0.831, not Table 3.
- Three-result narrative: **partly** — §4 says "reads most naturally 1 → 2 → 3" yet orders §4.2, §4.3(=result 3), §4.4(=result 2); Figure numbering (Fig 2 from `fig3_*.png`, Fig 4 from `fig2_*.png`) shows the seam.
- Preregistration/amendment/cost transparency: **worked**, verging on padding; A8 in `02_design_audit.md` still reads "Awaiting Jaswin's confirmation."

### Hidden problems from my lens (Round 3 input)
1. **"Fully explained by style-reading"** (Limitations, over-attribution para) is stronger than the evidence: r = +0.71 across ten points and a scaffold that also removed everyone's signal is not full mediation. SEVERITY: moderate. DISPOSITION: fix today (change to "tracked by / not separable from").
2. **Fresh-session self-prediction is self-modelling, not introspection** in Lindsey's sense (same-episode state access). Track 3's reading is concept injection; the report only says this in Limitations. SEVERITY: moderate (judge-perception). DISPOSITION: disclose more clearly in §1 (one sentence).
3. **No manipulation check on persona divergence** (see weakness 2). SEVERITY: major. DISPOSITION: disclose today; a keyword-free recommendation-agreement estimate would need an LLM pass — leave the count as future work but state the App. B observation as a limitation.
4. **Preregistered CI missing on the headline probe** (A8 vs §4.3). SEVERITY: major for a paper whose brand is preregistration. DISPOSITION: fix today — prompt-clustered bootstrap on balanced accuracy for M and N; fold-spread on D.
5. **The 2×2 interaction cannot identify privileged access even in principle**: it cancels a column-independent capability effect only, and stylistic self-similarity is itself a predictor×column interaction (which is exactly how §4.4 explains +0.089 away). SEVERITY: moderate. DISPOSITION: disclose as a design limitation, and it strengthens the argument for the gate.
6. **Intro over-reach on welfare**: "if a model's report carries no epistemic advantage over an outside observer, those methods are measuring something other than what they claim" (§1). A self-report as accurate as a third party still measures the thing; privileged access is sufficient, not necessary, for reliability. SEVERITY: moderate. DISPOSITION: fix today (soften to "cannot be shown to add information").
7. **Hermes 0.719 as prompt artefact**: "One is the reply you would produce; the other is from a different model" (App. C) invites a "which is better/more assistant-like" judgement; Hermes's B-preference (0.68) is handled, but a preference-not-prediction reading is not excluded. SEVERITY: moderate. DISPOSITION: disclose; the length analysis above partially addresses it.
8. **Length**: 10,641 words against "most strong projects are 4 to 8 pages." SEVERITY: major (Presentation). DISPOSITION: fix today.

### Past-winner comparison from my lens (Round 5 input)
- Winners had a one-line hook and a closed loop; this project has both ("Beaten by Eighteen Features"; $3.12, all cells run).
- Winners were 5–13 pages with padding in appendices; this is ~25 pages of *text*. Judges tolerate long appendices, not long bodies.
- Winners had a vivid artefact/demo; here the artefact is a script and a script is not vivid. One figure that shows Self falling with D (Fig 1) is the closest thing to a memorable image.
- Rigor is far above every winner; novelty is candidly modest ("neither idea is ours to claim," §5.3). This rubric weighs Execution as a third, so that trade is acceptable, but Impact will be scored 3, not 4, unless the welfare consequence is made explicit.
- Missing winning characteristic: a claim a non-specialist repeats to a colleague. "A word counter beats the model at knowing itself" is available and under-used.

### Fellowship view from my lens (Round 6 input)
- Win the sprint: 15–30%. Considered for Fellowship: 35–55%. Actually selected: 12–25%. Remembered by organisers: 55–75% (the candour and the title travel).
- The 3-phase trajectory is **too broad and insufficiently welfare-relevant**: Phases 1–2 replicate a null across lineages and fine-tune types (interesting to Song et al., not to Eleos/Anthropic welfare programmes). Better: (a) point the gate at welfare-relevant self-reports — do models' reports of preference/aversion/discomfort carry information beyond a stylometer on the same transcript?; (b) exploit that Llama-3.1-70B is open-weight: create ground-truth hidden properties by activation steering (nnsight), where leakage can be measured *and* the property is genuinely internal — a behavioural bridge to Lindsey; (c) test privileged access on behaviours that matter (own refusals, conversation-ending choices, forced-choice preferences) rather than persona.
- Why Apart spends months: the team demonstrably designs to falsify itself and ships preregistered, budget-guarded, tested code in three days. Why not: the current question, extended, yields more nulls about persona detection with no obvious path to a welfare-relevant claim.

### Today-only actions from my lens (Round 7 input)
- **S** — Add prompt-clustered CI to Hermes/Llama balanced accuracy and D's fold spread (§4.3, Table 2). Effort 45 min. Sprint +, Fellowship + (closes prereg gap). Risk low.
- **S** — Add the unsupervised "pick the longer reply" observer (0.81) and Hermes's accuracy on own-shorter items (0.653, n=75) to §4.3. Effort 45 min. Sprint ++, Fellowship +. Risk low if reported with n and stated as post hoc.
- **S** — Cut main body to ≤ 8 pages; move Tables 4–5, App. I–J, and §4.1 detail to appendix. Effort 2–3 h. Sprint ++. Risk: losing the amendment story — keep A4 in one paragraph.
- **A** — Soften "fully explained" and the §1 epistemic-advantage sentence; add one sentence that the persona is an instructed disposition and that App. B shows persona-agreement on recommendation as a limitation. Effort 30 min. Risk none.
- **A** — Fix §4 ordering statement and figure/file numbering; sign off A8 in `02_design_audit.md`; fill affiliations/URL. Effort 30 min.
- **B** — Final slide: one bar pair (0.719 vs 0.831 vs 0.81 length-only) with the sentence below. Effort 30 min.

### Blunt selection verdict from my lens
"If I were an Apart selector looking at this project today, I would: **lean select**." It is the most methodologically serious submission I expect to see in Track 3, and its central sentence corrects an error welfare researchers actually make. It is held back by a hidden property that is not an internal state, a headline comparison with no interval that its own preregistration promised, and a report twice the recommended length. Fix the CI, add the length-only observer, cut the body, and it becomes a clear select on Execution with a defensible 3–4 on Impact. The one thing to say in the final minute of the video: "The model that could predict itself was beaten by a word counter — so before you believe a self-report, ask what a word counter would say."

---

## REVIEWER 4 — STATISTICIAN / METHODOLOGIST

### Scores (independent — do not average with anyone)
- A. Scientific quality: 56 — the design discipline (prompt-clustered bootstrap, grouped CV, disclosed amendments) is real, but the memorable result lacks the paper's own control, the "four independent designs" share one prompt pool, and the interaction dismissal is post hoc and does not survive its own F reference.
- B. Sprint competitiveness: 58 — Execution reads as 3–4 to a careful judge; Impact ~3; the 10,600-word length is a Presentation liability against "4–8 pages".
- C. Fellowship potential: 55 — the leakage-gate idea is fundable as method work; the evidential core is one lineage, one property, one probe with no cross cell.

### Top 3 strengths
1. **Inference unit is right and stated (§3.5, §4.2c).** Prompt-clustered bootstrap, grouped 5-fold CV, and the explicit warning that VO-D's ±3.7 pp CI is non-discrimination not precision (§4.2c). Scientific value: most sprint submissions get exactly this wrong; competitive value: it is what "report variance and baselines" in the rubric means.
2. **The response-bias check caught two artefacts before publication (§4.3, Table "Framing").** M 99.0% "A", N 98.7% "B", 100% "no". This is a real, generalisable methodological point and the release (`response_bias()`) is cheap to adopt.
3. **Amendment record with mispredicted primary contrast reported as found (§4.4a, Limitations bullets 1–2).** Reporting −0.033 [−0.063, −0.003] as "wrong way for both accounts" rather than reinterpreting it is honest, and the record dates the A4 decision before the cells ran.

### Top 3 weaknesses
1. **The headline probe (§4.3, Table 2) has no cross cell — actual flaw.** The paper's central design principle is that Self > X is uninterpretable without a crossed control (§1, §3.3), yet the "Hermes can genuinely predict its own output" claim rests on N→N alone. I recomputed from `data/checkpoints/selfpred_*_VO-C.jsonl`: position-corrected, **both** models prefer the Hermes-authored reply (Llama 0.553, Hermes 0.719 balanced), and Llama's discrimination is −0.107 [−0.167, −0.046] — reliably *negative*, not "none" (§4.3, §6). A rule "choose the longer reply" gives Hermes 0.648 balanced. The 0.719 is at least as consistent with a shared text-preference/length heuristic as with self-knowledge.
2. **"Four independent stimulus designs" (§1 contribution 3, §4.4) share the same 200 source prompts — actual flaw in description, limitation in substance.** All four sets' generated files contain the identical 200 prompt ids. §3.5 says "the two stimulus sets are resampled independently of each other"; A4 says "different items". Neither is true at the cluster level; the difference CI in Table 5 should resample prompts jointly across sets. Effective independent units are 200 prompts, not 9,269 trials.
3. **The interaction dismissal (§4.4 "strongest objection… addressed") is a re-description, not a test — actual flaw.** "M under-performs on N's column" *is* the interaction. The F reference does not rescue it: (M→M − F→M) − (M→N − F→N) = (−0.025) − (−0.119) ≈ **+0.094**, the same as the N-referenced +0.089. Meanwhile M→M − F→M on VO-C is −0.025 [−0.053, +0.003], McNemar p = 0.11 — the "beaten on its own text by a different organisation" sentence (§1, §4.4b, §5.1) cites the non-significant instance; the significant ones are VO-A (−0.051 [−0.084, −0.018]) and VO-B (−0.045 [−0.081, −0.010]), which are not tabulated.

### Strongest objection
The paper's memorable claim — "self-prediction is possible here" — is a single self cell with no cross cell, in a paper whose thesis is that single self cells are uninterpretable. Recomputed, both models pick the Hermes text; the model that "self-predicts" is the one whose text is preferred by both. Under the paper's own logic this is a style/preference result, and it should be framed as such.

### Strongest reason I would select this project
It operationalises Song et al.'s equal-cost-observer criterion as a preregisterable number, applies it before spending, and shows in its own data that the criterion changes what a study concludes.

### Strongest reason I would reject it
Its inferential core is asymmetric and under-tested: supervised vs zero-shot with no test (though the gap is real — Hermes 0.719 [0.675, 0.760] vs D 0.831 is ~4 SE), no cross cell on the probe, one prompt pool called four independent designs, and a significant capability-controlled interaction argued away rather than tested.

### What would move my score +5
Add prompt-clustered CIs to Table 2 (computable now), a per-item McNemar of D vs Hermes on the 391 shared items (per-item D correctness is returned by `fit_baseline_cv` — a local numpy re-run), and rewrite the VO-C interaction paragraph as "consistent with style-matching's prediction; unidentifiable from self-knowledge in this design".

### What would move my score −5
Leaving "four independent designs" and "resampled independently" as written; a judge who opens the data sees one prompt pool.

### Did the editorial revision work?
- Narrative identity: **worked** — title, abstract and five-line table say one thing.
- Self-prediction vs privileged access foregrounded: **partly** — the distinction is clear, but "Hermes can genuinely predict its own output" (§4.3) overstates a single uncontrolled cell.
- Leakage gate elevated: **worked** — §3.4, §5.3, code block, recommendation box.
- Crossed 2×2 as strongest evidence: **partly** — §4.4 is called "broadest evidence" but Table 3 hides that VO-A/B cell contrasts (F beats both same-base models significantly) exist only in Appendix H.
- Three-result narrative: **worked** — §4 opener numbers them and admits reading order 1→2→3.
- Preregistration/amendment/cost transparency: **partly** — A1–A8 and $3.12 are there, but the P4 deviation (target 1,000/cell, floor 500; ran ~400) is not disclosed anywhere in the report, and §4.4 says "did not pre-register [a slope]" while A7 names the slope as "primary summary".

### Hidden problems from my lens (Round 3 input)
1. **No cross cell on the self-prediction probe; both models prefer the Hermes text** (§4.3, Table 2). Llama disc −0.107 [−0.167, −0.046] is a content-dependent *other*-preference, contradicting "answers by position and shows none" (§6). SEVERITY: major. DISPOSITION: fix today — report the CI, reframe as shared preference, drop "genuinely".
2. **"Eighteen features" is essentially one.** Hermes texts are longer in 81.2% of shared pairs; "longer = Hermes" gets 0.812 authorship vs D's 0.831 (§4.3, title). Technically true, but the title implies a richer observer than the data need. SEVERITY: moderate. DISPOSITION: disclose (it strengthens the deflation).
3. **Same 200 prompts across all four sets; difference-CI method mis-stated** (§3.5, §4.4, Table 5). SEVERITY: major for wording, moderate for numbers. DISPOSITION: fix today — reword "independent" → "four clause pairs on one prompt pool"; re-run the cross-set bootstrap jointly (local).
4. **r = +0.71 on ten columns is a two-cluster correlation** (§4.2a, Fig 1). Partial r controlling scaffold = 0.35; within original scaffold r = 0.51 (n = 6); VO-D/VO-E share clauses. SEVERITY: moderate. DISPOSITION: disclose ("driven by the scaffold contrast, which is the manipulation").
5. **Estimand choice flips the qualitative verdict** (§3.5, §4.4a). Primary leakage contrast on raw self-advantage: −0.033 ("wrong way for both"). Same contrast on the preregistered secondary, the capability-controlled interaction: +0.089 − (−0.006) ≈ +0.095, positive — exactly style-matching's prediction. The paper under-reports a consistent story and over-argues the dismissal. SEVERITY: major. DISPOSITION: fix today (one paragraph).
6. **Pilot D = 0.325 on VO-D M is a 40-group CV artefact, not "below chance" evidence** (§3.5, §4.2b, Appendix B); main-run VO-D D was 0.551/0.536, i.e. regression to the mean; the set was selected on that noisy value. SEVERITY: moderate. DISPOSITION: disclose.
7. **Undisclosed P4 deviation** (n/cell ~400 vs floor 500) and "SESOI 5 pp" cited where prereg says 8 pp for the interaction below 1,000/cell (§4.4c). SEVERITY: minor–moderate. DISPOSITION: disclose in Limitations.
8. **Cited non-significant contrast as fact** (§4.4b M→M < F→M on VO-C, p = 0.11) while the significant VO-A/VO-B instances are untabulated. SEVERITY: minor. DISPOSITION: fix today.

### Past-winner comparison from my lens (Round 5 input)
- Winners had error bars at best; this has clustered CIs, grouped CV, McNemar in the JSON — well above the reference class on rigor.
- Winners were 4–8 pages; this is ~20 pages of prose. Rigor that judges cannot reach does not score.
- Winners' hooks were causal and simple ("noise reveals sandbagging"); this hook is a comparison whose two arms are not the same task (single-text supervised vs paired zero-shot).
- Missing winner characteristic: a closed loop that a reader can verify in one figure; Fig 3 comes closest but omits CIs.
- The project overvalues preregistration formalism relative to identification: an amendment record does not identify the interaction.

### Fellowship view from my lens (Round 6 input)
- Win sprint: 15–30%. Considered for Fellowship: 35–55%. Selected: 12–25%. Remembered: 50–70% (the "beaten by eighteen features" line is sticky).
- Trajectory: Phase 3 is the right centre; Phase 1 as written is too broad. Better: Phase 1 = add the missing cross cells (F and sibling judging "which is model X's reply") and a paired zero-shot LLM observer, on 3 lineages; Phase 2 = one training-relationship axis (PEFT vs full FT sibling); Phase 3 = retrospective gate on 3 published self-prediction datasets.
- Why spend months: they turn a critique into a preregisterable measurement and already know how to run a clean pipeline for $3. Why not: if the team keeps framing single self cells as "genuine self-prediction" the method's own lesson is not being applied.

### Today-only actions from my lens (Round 7 input)
- **S** — Add prompt-clustered CIs to Table 2 (Hermes 0.719 [0.675, 0.760], disc +0.437 [+0.349, +0.519]; Llama disc −0.107 [−0.167, −0.046]); state D's gap is ~4 SE. Effort 30 min, no API. Sprint +, Fellowship +, risk none.
- **S** — Reword "four independent stimulus designs" and §3.5 resampling sentence; re-run cross-set bootstrap jointly by prompt (local). Effort 1 h. Risk none; leaving it is a credibility risk.
- **A** — Rewrite §4.4 interaction paragraph: report F-referenced interaction (+0.094), say the interaction leakage-contrast confirms style-matching's direction and is unidentifiable from self-knowledge. Effort 45 min.
- **A** — Add per-item McNemar D vs Hermes on shared items (local numpy) and the length-only observer (0.812). Effort 1–2 h.
- **B** — Disclose P4 n deviation, pilot D = 0.325 as noise, and the both-models-prefer-Hermes-text finding. Effort 30 min.
- **C (optional, ~$0.05, ~400 F calls)** — F judging "which reply is Hermes'" gives the zero-shot equal-cost observer the criterion actually asks for. Only if the pipeline runs unattended; otherwise skip.

### Blunt selection verdict from my lens
"If I were an Apart selector looking at this project today, I would: **borderline / lean select**." The methodological instinct is right and the artefact is reusable, but the statistics as written have three soft spots a hostile Q&A will find in five minutes: the headline probe lacks the control the paper preaches, the "independent" replications share a prompt pool, and the one significant interaction is argued away rather than tested. All three are fixable today from existing data. The ONE thing to say in the final minute: "Both models, position-corrected, chose the Hermes-authored reply — and a length rule nearly matches the classifier. That is what 'self-prediction' looked like from the outside, which is why the gate should be run before the claim."

---

## REVIEWER 5 — FELLOWSHIP SELECTION MENTOR

### Scores (independent — do not average with anyone)
- A. Scientific quality: 61 — the crossed design, prompt-clustered inference and leakage manipulation are real; but the headline "no positive self-advantage" holds only for the M-as-target definition, the "clean" set is not clean in the main run (D 0.55), and the Hermes result is under-analysed.
- B. Sprint competitiveness: 57 — strong hook and artifact, but 10,600 words against a 4–8-page rubric, a negative primary contrast, and a memorable result whose alternative explanation the team has not checked.
- C. Fellowship potential: 66 — the amendment record shows a team that can be taught rigour and already reasons in stop rules; it also shows most design pivots labelled "proposed by Claude Code, awaiting Jaswin's confirmation," which is exactly what a selector will probe.

### Top 3 strengths
1. **A preregistration with a live amendment trail (02, P1–P15, A1–A8), including a reversal (A3→A4) recorded rather than buried.** Scientific value: it makes the post-pilot selection of VO-C/VO-D auditable. Competitive value: none of the six past winners had anything like it; under the current rubric's "convincing validation" language this is a genuine differentiator.
2. **The pilot-as-result move (§4.2, Fig. 1; A1, A5).** corr(Self, D)=+0.71 across ten columns and two one-sentence-different scaffolds collapsing Self and D together is a tidy, cheap causal story about the mediator. It is the one place where the design intervened on the hypothesised mechanism, and it is what an organiser will remember.
3. **Response-bias discipline (§4.3, §5.3).** Catching M's 99.0% "A" / N's 98.7% "B" and refusing to publish "chance" nulls is evidence of researcher judgement; the released `gate()`/`response_bias()` file is small but the recommendation is correct and adoptable.

### Top 3 weaknesses
1. **"Not one design shows a positive self-advantage whose interval excludes zero" (§1 contribution 3, §4.4) is true only for M as target.** On VO-C, N→N − M→N = 0.766 − 0.644 = +0.122 with non-overlapping CIs (Table 4). The paper rescues this via F→N = 0.763, but the abstract and five-line table state the M-only version as if symmetric. *Actual flaw in claim scope* (a technically-true-but-misleading sentence), fixable today.
2. **The Hermes 0.719 (§4.3, Table 2, Fig. 3) is presented as "genuine self-prediction" without checking a one-feature explanation.** From the team's own checkpoints and texts: N's reply is the longer one 80.8% of the time on VO-C; a "pick the longer reply" rule scores 0.808 for N (above Hermes' 0.714) and 0.189 for M (which reproduces M's negative discrimination). Hermes chose the longer text 65.5% of the time. *Actual flaw in interpretation* — but note it strengthens the paper's thesis (beaten by one feature, not eighteen) while weakening the "Binder-side positive" framing.
3. **The "clean" set is not clean in the main run.** VO-D was selected because pilot D = 0.325 on M — three SEs below chance on 80 items, i.e., anti-learning noise — and in the main run D was 0.551/0.536 (Table 3), just under the 0.58 threshold. The leakage axis is 0.54→0.85, not 0.33→0.85 as A7 says. *Limitation + judge-perception risk*; the report never reconciles the two D values.

### Strongest objection
The study's target M turned out to be the weakest classifier of the three (§4.4b), the configuration Appendix I explicitly says "biases toward the null" — and the design's protection against that, the crossed interaction, came out +0.089 [+0.048, +0.131] on the leakiest set and had to be explained away by the far model. So the null rests on F comparisons plus a "clean" condition where nobody beats chance. Combined with weakness 1, a hostile reader can argue the study never had a target with enough classification skill to show a self-advantage even if one existed.

### Strongest reason I would select this project
The A1→A3→A4→A5→A8 sequence shows a team that writes stop rules before running, fires them when they trigger, and reports the three failed framings before the one that worked. That is the behaviour I want to mentor; the science can be sharpened, the temperament cannot be installed.

### Strongest reason I would reject it
The record says A4, A5, A7, A8 were "proposed by Claude Code, awaiting Jaswin's confirmation," and CLAUDE.md still lists that sign-off as outstanding, while the Author Contributions credit J.C. with designing the style-equalising scaffolds that A1 says were "drafted in Claude Code." I cannot yet tell which of the two humans made the pivotal design decisions, and a Fellowship is an investment in humans.

### What would move my score +5
Adding the length-heuristic row to Table 2 ("word count alone: 0.808"), rewriting the headline claim to "for the preregistered target M; N's near-self advantage on VO-C is +0.122 but vanishes against F," and a one-paragraph statement of who decided A4/A8 and why.

### What would move my score −5
Discovering the amendments were never actually confirmed by the second author before submission, or a judge finding the N-column self-advantage first.

### Did the editorial revision work?
- **Narrative identity:** worked — title, five-line table and §6 all carry "self-prediction ≠ privileged access."
- **Self-prediction vs privileged access foregrounded:** worked, arguably over-worked — it appears in abstract, §1, §4.3, §5.2 and §6 with near-identical wording.
- **Leakage gate elevated:** partly — §5.3 is good, but the gate has no validation beyond this study, no minimum-n guidance, and its own pilot output (D = 0.325) shows it can report noise.
- **Crossed 2×2 preserved as strongest evidence:** partly — §4.4 says so, but the primary contrast is negative and the interaction is non-zero on the leakiest set; the text has to argue the reader out of both.
- **Three-result narrative:** worked at the section level (§4 opener), but §4.3 sits between the pilot and the crossed design and the report admits "the argument reads most naturally as 1 → 2 → 3," i.e., the order is not the argument.
- **Preregistration/amendment/cost transparency:** worked for what is recorded; failed on one item — P4's floor of 500/cell became ~400/cell (200 prompts) with no amendment, and the report is silent.

### Hidden problems from my lens (Round 3 input)
1. **M-only definition of self-advantage** (§1, §4.4, abstract). N→N − M→N = +0.122 on VO-C, CIs disjoint. SEVERITY: major. DISPOSITION: fix today — qualify every "no positive self-advantage" sentence with "for target M; N's near-self advantage exists on VO-C and is matched by F."
2. **Word count alone beats Hermes** (§4.3). Longer-reply rule 0.808 for N vs Hermes 0.714; M's own text is longer only 18.9% of the time. SEVERITY: major (for the "genuine self-prediction" framing), positive for the thesis. DISPOSITION: fix today — one row in Table 2, one sentence in §4.3, and consider "Beaten by one feature" in the abstract.
3. **Unrecorded n step-down** (P4 floor 500 → 400 actual). SEVERITY: moderate. DISPOSITION: disclose today in Limitations, one line.
4. **Pilot D = 0.325 as selection criterion.** A below-chance grouped-CV estimate at n = 80 was treated as "does not leak"; main D = 0.551. SEVERITY: moderate. DISPOSITION: disclose today; add minimum-n / CI guidance to the gate docstring as future work.
5. **Target ended up the weakest classifier** despite Appendix I's stated principle. SEVERITY: moderate. DISPOSITION: disclose more clearly — say the ladder chose M before capability was known and that this is why F is load-bearing.
6. **Amendment provenance and sign-off** (02: "proposed by Claude Code," "awaiting Jaswin's confirmation"; LLM statement omits this). SEVERITY: major for Fellowship, minor for sprint. DISPOSITION: fix today — confirm in 02, add one sentence to the LLM statement.
7. **Contribution statement vs A1** ("designed the five persona pairs" vs "drafted in Claude Code, human-screened"). SEVERITY: minor. DISPOSITION: reword today.
8. **Length vs rubric** (10,641 words vs "4 to 8 pages"). SEVERITY: moderate judge-perception. DISPOSITION: submit the condensed variant if it can absorb items 1–3; otherwise move Tables 4–5 and Appendix I to the appendix.

### Past-winner comparison from my lens (Round 5 input)
- Winners had one crisp positive or vividly negative story in ≤ 7 pages; this has three results and a negative primary contrast that needs a paragraph to interpret.
- This project does better than every winner on baselines, variance, preregistration and the required ethics appendix — precisely what the current rubric asks for and past winners lacked.
- Missing winner characteristic: a single unmissable figure. Fig. 1 (Self vs D) is close; the length-heuristic result would make it unmissable.
- The team is over-valuing rigour narration and under-valuing a plain "here is the number that beat the model" hook; the past panels rewarded framing ~45%, novelty ~35%, rigour ~20%.
- The public artifact is present but under-demonstrated: no example of the gate run on someone else's stimuli.

### Fellowship view from my lens (Round 6 input)
- Win the sprint: 10–20%. Considered for Fellowship: 40–55%. Actually selected: 15–30%. Remembered by organisers: 55–70% (the amendment record and the "beaten by a regression" line stick).
- The 3-phase trajectory is too broad and Phase 3 is premature. Sharper: **Phase 1** — apply the one-feature/18-feature gate retrospectively to two or three published behavioural self-prediction results (Binder-style, temperature-judgement) and report how many survive; that is cheap, novel, and directly citeable. **Phase 2** — the same-checkpoint / PEFT / full-fine-tune ladder on one base, but with the target chosen after a capability screen so the target is never the weakest classifier. Only if Phase 1 finds survivors does a benchmark (their Phase 3) earn its keep.
- Why spend months on this team: they already behave like preregistering scientists under 48-hour pressure and reversed themselves on the record. Why not: if the pivotal decisions were made by the tooling and merely ratified, the mentorship would be training the wrong agent.

### Today-only actions from my lens (Round 7 input)
1. **S — Add the length-heuristic check to §4.3/Table 2** (script over existing checkpoints + generated texts; ~30 min). Sprint: +; Fellowship: ++ (shows they can find their own confound); risk: none if reported as strengthening the thesis.
2. **S — Rewrite the M-only "no positive self-advantage" sentences** (abstract, five-line table, §1, §4.4). ~30 min. Sprint: neutral-to-+; Fellowship: ++; risk: none.
3. **A — Confirm amendments A1–A8 in 02 with names/dates and add one sentence to the LLM statement on who proposed and who decided.** ~20 min. Sprint: neutral; Fellowship: ++; risk: none.
4. **A — Disclose n step-down and pilot-vs-main D for VO-D in Limitations.** ~15 min. Sprint: +; Fellowship: +; risk: none.
5. **B — Submit at rubric length**: use the condensed variant with items 1–2 folded in, appendix the rest. ~1–2 h. Sprint: ++; Fellowship: neutral; risk: losing nuance if rushed.
6. **C — Final slide/video line** (below). ~10 min.

### Blunt selection verdict from my lens
"If I were an Apart selector looking at this project today, I would: **lean select.**" The temperament evidence — stop rules, recorded reversals, refusing to publish artefact nulls — is exactly what a Fellowship can build on, and the follow-on (retrospective gate on published claims) is tractable and cheap. My hesitation is provenance: the record credits the tooling with the pivots and leaves the second author's confirmation outstanding, and the report's headline claim is scoped more broadly than the data. Fix both today and this becomes a clear select. The one thing to say in the final minute of the video: "The model that could predict itself was beaten by a regression — and by word count alone; before you call a self-report privileged, run the gate."

---

## REVIEWER 6 — COGNITIVE SCIENTIST / EXPERIMENTAL PSYCHOLOGIST (no LLM background)

### Scores (independent — do not average with anyone)
- A. Scientific quality: 57 — careful, preregistered, honest measurement; but the core construct is thinly operationalised, the "style-equalising" manipulation confounds cue removal with property removal, and the headline comparison has no interval and no test.
- B. Sprint competitiveness: 62 — more rigorous than any past winner in the reference set, with a memorable one-line hook; held back by length (10,600 words vs a 4–8 page norm), a buried headline, and a negative-result-plus-tool package that judges may read as "nothing found."
- C. Fellowship potential: 55 — the team demonstrably runs a tight, self-critical shop; the scientific idea (comparative baseline before interpreting self-prediction) is sound but not new, and the released gate needs validation before it can be a "field default."

### Top 3 strengths
1. **The comparative framing is right and stated crisply.** "Self-prediction is possible; privileged self-access is not thereby demonstrated" (Abstract, §4.3) is the correct logical form for a Track 3 claim, and the five-line table gets it across in under a minute. Competitive value: judges can restate the finding after one read.
2. **Response-distribution hygiene is genuinely good psychophysics.** Splitting a counterbalanced 2AFC by slot and reporting hit − FA / balanced accuracy (§4.3, Table 2), plus catching two degenerate framings before they became "clean nulls" (Figure 2), is what an experimental psychologist would demand and rarely sees in LLM work. Scientific value: the response-bias check is the more defensible of the two released tools.
3. **Preregistration + dated amendments + a mispredicted primary contrast reported as found (§4.4a, Limitations).** For $3.12. This is a credibility asset for a Fellowship reader even where the science is thin.

### Top 3 weaknesses
1. **The "style-equalising" manipulation removed the property, not just the cue** — *actual flaw, partly disclosed*. Appendix B's own worked example says: "Under both scaffolds the two personas reach the *same* recommendation, so the hidden property is not in the advice given." If the two personas do not produce behaviourally different advice, VO-D is a no-signal condition, and "removing style removes the self-advantage" (Abstract, §4.2b, Figure 4) is not the causal story it is presented as. §5.2 concedes this in one sentence; the abstract and Figure 4 caption do not.
2. **The headline number is a single-probe, zero-shot-vs-supervised, single-text-vs-2AFC comparison with no interval** — *limitation + judge-perception risk*. 0.719 vs 0.831 (§4.3, Table 2) compares different tasks (the LR classifies one text; the model chooses between two), and neither number carries a CI. The report says so (§4.3, §6), which is honest, but a hostile reader still sees the title built on it.
3. **"Introspection" is not what any predictor was asked to do** — *limitation / construct validity*. In the crossed 2×2 (§3.1, Appendix C) every predictor, Self included, is a third-person text classifier: "Which instruction was being followed?" Nothing about internal states, and the "self" channel is a hypothesised familiarity effect. This is a self-modelling / authorship-style study wearing an introspection label; the Track 3 fit rests almost entirely on §4.3.

### Strongest objection
The design cannot produce a positive. The band (Self 60–80% AND D ≤ 58%) and the released `gate()` (`passed = acc <= 0.58`) screen *out* stimuli where the property is readable — which is exactly where "model beats the cheap observer" could be demonstrated. And on readable stimuli, beating an 18-feature LR would not establish privileged access either (a 19th feature or a small classifier might close the gap). So the operationalisation only ever returns "not demonstrated." A test that cannot in principle come out the other way is not a test of the construct; it is a filter.

### Strongest reason I would select this project
It is the only submission I would expect to see that treats "the model can predict itself" as the *start* of an argument rather than the end, quantifies the alternative explanation with a baseline, and reports the numbers that embarrass its own preregistered predictions.

### Strongest reason I would reject it
After 9,269 trials the reader knows: one model prefers its own replies in a forced choice; a persona instruction leaks into style; a scaffold that flattens style also flattens the persona. None of these is new (self-preference/self-recognition in pairwise choice is established — see hidden problem 1), and the one causal manipulation is confounded.

### What would move my score +5
Prompt-clustered CIs on the §4.3 numbers plus a two-line alternative-explanation check (length/preference), and one honest sentence in the abstract that VO-D removes the property's behavioural expression, not only its style.

### What would move my score −5
Discovering that the "four independent stimulus designs" reuse the same 200 source prompts and same two generators (as §4.4 implies) while continuing to call them independent replications.

### Did the editorial revision work?
- Narrative identity — **worked**: title, abstract and five-line table all say the same thing.
- Self-prediction vs privileged access foregrounded — **worked**, but the headline result sits after two failed-framing tables in §4.3; a first-time reader meets the failures before the finding.
- Leakage gate elevated — **partly**: §5.3 is clear, but "gate" semantics (pass/fail at 0.58) contradict the text's own recommendation to *report and compare*.
- Crossed 2×2 preserved as strongest evidence — **partly**: called "broadest and most rigorous" (§1, §4.4), yet §5.2 admits its clean arm cannot distinguish "no access" from "no signal," so its strength is asserted more than argued.
- Three-result narrative — **worked** (§4 opener), though "sections appear in the order the work was done; the argument reads 1 → 2 → 3" is a confession that the structure fights the argument.
- Preregistration/amendment/cost transparency — **worked**: A1–A8, stop rules, $3.1216, all present.

### Hidden problems from my lens (Round 3 input)
1. **Missing literature that reframes the headline.** Panickssery, Bowman & Feng (2024, "LLM Evaluators Recognize and Favor Their Own Generations") already show zero-shot pairwise self-recognition and its link to self-preference. Hermes 0.719 is plausibly a self-preference effect: the model picks the reply it *likes*, and it likes its own style. Same-data check I ran from the checkpoints: Hermes's own text is longer in 81% of pairs and it chose the longer text 65%; accuracy is 0.728 when its text is longer and 0.653 when shorter (n = 75) — so *length alone* does not explain it, which helps the team, but preference-consistency remains untested. Llama's hit − FA is reliably negative (my clustered CI ≈ [−0.17, −0.05]): it systematically picks Hermes's reply, consistent with a shared quality preference. SEVERITY: major. DISPOSITION: disclose more clearly today (cite; add the length check; state the self-preference alternative).
2. **No CIs on the headline or on any D value.** Hermes hit − FA has a prompt-clustered CI ≈ [0.35, 0.52] from existing data; pilot D values (n = 80, 18 features) carry ~±6 pp SEs, and VO-D's 0.325 (17 pp *below* chance) is a small-n grouped-CV artefact, not "leak closed." The leaky/clean pair was selected on these noisy estimates. SEVERITY: moderate. DISPOSITION: fix today (bootstrap the probe; add ±SE or CI to Table 1 D; delete "below chance" as evidence).
3. **r = +0.71 across ten columns is mostly a two-cluster effect.** Scaffold type (original vs equalised) correlates 0.79 with Self and 0.71 with D; within originals r ≈ 0.51 (n = 6), within equalised r ≈ 0.22 (n = 4); VO-D/VO-E are near-duplicates. SEVERITY: moderate. DISPOSITION: disclose (call it "tracks across scaffolds," not a continuous relationship).
4. **The gate is one-directional and the tool's API says otherwise.** Passing D ≤ 0.58 does not mean the property is not cheaply recoverable (no lexical, semantic or content features by design); failing means only that a comparison is required. `passed=True` will be read as "clean." A field default needs validation on more than five hand-written pairs from one team. SEVERITY: major for the "field default" claim, minor for the tool. DISPOSITION: disclose today (rename `passed` → `surface_recoverable` or add docstring; soften "reporting default" to "report D alongside").
5. **"Four independent stimulus designs" / "replication."** Same 200 prompts, same generators, same values dimension, three of four on the same scaffold with reworded clauses. The effective replication unit is clause wording. SEVERITY: moderate. DISPOSITION: disclose ("four clause pairs on shared prompts").
6. **The single significant negative primary contrast (−0.033) is unremarkable under ~12 reported intervals** and should not be narrated as a "self-disadvantage" (§4.4a). SEVERITY: minor. DISPOSITION: disclose (one clause).
7. **Curse-of-knowledge terms.** "Similarity axis," "far-self swap," "Level 3," "SESOI," "the band" appear before definition (§3.4, §4.1); "same-weights advantage" (§3.5) muddles two different pairs (M-vs-M-served and M-vs-N-sibling); "capability control" is presented as if the interaction isolates self-knowledge, when §4.4's own "strongest objection" paragraph shows it also absorbs column-specific style-reading skill. SEVERITY: moderate for Presentation. DISPOSITION: fix today in the condensed version.
8. **Length.** ~10,600 words is roughly 20 pages against "most strong projects are 4 to 8." SEVERITY: major for the Presentation dimension. DISPOSITION: fix today — submit the condensed variant, push Tables 4–5 and Appendix I–K to a supplement.

### Past-winner comparison from my lens (Round 5 input)
- Winners state one mechanism in the first paragraph and stop; this report states one mechanism, then qualifies it for 10,000 words. The qualification is scientifically right and competitively costly.
- This project beats every reference winner on baselines, variance, preregistration and the required ethics/causal-link appendix — the things the *current* rubric asks for and past winners lacked.
- Missing winner characteristic: a vivid, positive, easily demoed artefact. `surface_leakage_gate.py` is the candidate, but it is a numpy file, not a demo; the response-bias catch (Figure 2) is more demo-able than the gate.
- The team overvalues rigor relative to novelty: the rubric's Dimension 1 asks "is this actually new to the field?" — the honest answer here is "operationalisation of a known confound," a 3.
- Negative results won when the failure *was* the story (w5, w6). Here the story is "a model prefers its own text but so would a regression" — tellable in one breath, if the report lets it.

### Fellowship view from my lens (Round 6 input)
- Win the sprint: 10–25%. Considered for Fellowship: 30–50%. Actually selected: 10–20%. Remembered by organisers: 45–65% (the discipline is memorable even where the result is not).
- Trajectory: Phase 1 (replicate across lineages) is dull but necessary; Phase 2 (vary training relationship) is the genuinely interesting axis and should lead; Phase 3 (a "behavioural introspection benchmark") is premature — the gate is not validated and the persona property is not an introspective target. Better: Phase 1 = build stimuli where the property is behaviourally expressed *and* surface-clean (recommendation actually differs, D ≈ chance), verified by a manipulation check; Phase 2 = self-preference vs self-prediction dissociation (does the model pick its own reply when told "which is better" vs "which is yours"?); Phase 3 = training-relationship ladder.
- Why Apart would invest: this team will not fool itself, and that is rare. What would stop them: two of three results are the team's own confounds; a mentor may fear months of careful nulls with no positive handle.

### Today-only actions from my lens (Round 7 input)
- **S — Add prompt-clustered CIs to Table 2** (Hermes hit − FA ≈ [0.35, 0.52]; Llama negative interval) and to Table 1's D column. Effort: 1–2 h from existing checkpoints. Sprint +; Fellowship +; risk none.
- **S — Cite Panickssery et al. 2024 (arXiv:2404.13076) and add the length-heuristic check** (own-longer 81%, acc 0.728 vs 0.653) as a robustness line in §4.3, plus one sentence naming self-preference as the alternative account. Effort: 1 h. Sprint +; Fellowship ++ (shows literacy); risk none.
- **A — Rewrite one abstract sentence and the Figure 4 caption**: "equalising style" → "the equalising scaffold, which also converged the personas' recommendations (Appendix B), drives both to chance." Effort: 20 min. Sprint neutral-to-+; Fellowship +; risk: slightly weakens the causal claim, correctly.
- **A — Submit the condensed variant**, define terms on first use, move Tables 4–5 and Appendices I–K to a supplement. Effort: 2–3 h. Sprint ++ (Presentation); risk: dropping detail a rigor-minded judge wants — keep it in the supplement.
- **B — Tool hygiene**: rename or document `passed` so it cannot be read as "no leakage"; state in §5.3 that a passing gate is necessary, not sufficient. Effort: 30 min. Sprint +; Fellowship +; risk none.
- **C — Replace "four independent stimulus designs" with "four clause pairs on shared prompts"** throughout. Effort: 15 min. Risk none.

### Blunt selection verdict from my lens
"If I were an Apart selector looking at this project today, I would: **borderline, leaning select**." The team asked the right question, ran it cleanly, and refused to over-read three of its own results — that is the behaviour a Fellowship should buy. But the construct is thin (nobody was asked about an internal state), the causal manipulation removed the property along with the cue, and the memorable number is a known self-preference effect without a citation or an interval. Fix the citations, add the intervals, cut the length, and it becomes a clear lean-select; leave it as is and a rigor-minded judge will find the confound in Appendix B before the team's own §5.2 concession. The one thing to say in the final minute of the video: "A model picked its own reply 72% of the time — and eighteen numbers about sentence length and hedging picked it 83%. Before you call self-report evidence of self-knowledge, run the regression."

---

# Part 4 — Round 2: adversarial debate

---

## DEBATE — HARD-NOSED AI SAFETY RESEARCHER (Reviewer 1)

### One claim another reviewer scored too generously
Reviewer 5's Fellowship score of 66, justified by "the temperament cannot be installed." The amendment trail is genuinely rare, but R5's own strongest-reject paragraph shows the trail records that A4/A5/A7/A8 were "proposed by Claude Code, awaiting confirmation." A Fellowship buys humans, and R5 admits it cannot tell which human made the pivots — that is not a +11 over the panel median, it is a reason to hold at the median until provenance is confirmed. More basically, process virtue is being priced as if it were science: the scientific object after 9,269 trials remains one lineage, one values dimension, no property with a demonstrated behavioural expression. Temperament plus a thin object is a 55–58, not 66.

### One claim another reviewer scored too harshly
Reviewer 6's strongest objection — "the design cannot produce a positive… it is a filter." That overstates. The Song criterion is falsifiable inside this design: on VO-C, where D = 0.845 and the gate fails, Hermes could have scored 0.90 and would have beaten the classifier; on VO-D, M→M could have been 0.70 against D = 0.55 and the interaction would have been positive. Neither happened, which is a result, not a design property. R6 is right that beating an 18-feature LR is not sufficient for privileged access (a 19th feature could close the gap), but "not sufficient" is what the paper itself says; "cannot in principle come out the other way" is wrong, and it is the objection most likely to be repeated in Q&A, so it should be answered rather than conceded.

### One hidden assumption the others are missing
Five of us (my Round 1 included) reached for a length/shared-preference story to deflate 0.719. I recomputed from `selfpred_*_VO-C.jsonl` and the generated texts: Hermes's own reply is longer in 80.8% of items, Hermes chose the longer reply 65.5%, accuracy 0.728 (n=316) when own-longer vs 0.653 (n=75) when own-shorter; Llama chose the Hermes text only 54.0% raw. R3/R5/R6's ~0.81 for the "pick longer" rule is correct; R4's "0.648 balanced" appears to be Hermes's *rate of choosing longer*, not the rule's accuracy. Two consequences the panel is not drawing. First, "both models prefer the Hermes text" (R4, and me) is weak: 71% vs 54% is too asymmetric for a shared quality preference, and 0.653 on own-shorter items is ~2.8 SE above chance — Hermes has non-length signal. Second, and more important, self-preference (Panickssery et al., R6) is not an *alternative* to self-knowledge; familiarity-driven self-preference *is* style-level self-modelling, which is precisely what the paper says is not privileged. So the "genuine self-prediction" fight is a wording fight. The real vulnerability is R2's: label access is a cost, and the criterion has been operationalised in the null's favour. The length rule (0.808, zero labels, one feature) is the fix — it is the equal-cost observer the criterion actually demands, and it beats Hermes.

### The eight debate questions
1. **Novelty.** Primarily a reframing of Song et al. with a better control (crossed 2×2 + neutral F) and a preregisterable number. R2's "Innovation 3" is right; R5's implied 4 is not. The one novel bit — length alone beats a 70B model's self-prediction — is currently absent from the report.
2. **Gate.** Meaningful as a *reporting* practice, not as a validated instrument. I side with R6 on `passed=True` semantics and against R2's "Execution 4" for the gate specifically: pilot D = 0.325 → main D = 0.551 shows it reports noise at n=80, and its features are the manipulation's targets (circular on VO-D). Ship it as "report D alongside," not "field default."
3. **−0.033.** It damages the *narrative* more than the argument. R6 is right it is one of ~12 intervals; R4 is right that on the preregistered secondary (interaction) the same contrast is ≈ +0.095, style-matching's direction. The paper under-reports a consistent story and over-argues a dismissal — I confirmed R4's F-referenced interaction (+0.094) and that self_vs_far is significant only on VO-A/VO-B, not the cited VO-C (p=0.11). Disclose, do not spin.
4. **VO-D floor.** It does not undermine the null; it makes the null uninformative on the clean arm, as §5.2 admits. I disagree with R2 that "not clean" is a major flaw — 0.55 with M→M at 0.52 is still "nobody reads it." The real problem is R6's/my manipulation-check point: `same_persona_both` = 0.915–0.955 in the VO-D cells means predictors could not separate the two persona texts at all; the property may not have been enacted.
5. **0.719 vs 0.831.** As written, not persuasive — task mismatch, no interval, supervised vs zero-shot (R2, R4). The length findings *help* if reported honestly: "beaten by one unsupervised feature (0.808)" answers the cost objection outright, while 0.653 own-shorter shows Hermes is not a pure length reader. Report both; the thesis strengthens and the "genuine" adjective goes.
6. **One lineage.** Not serious for a sprint; serious for any generalisation claim about the gate. R3's activation-steering path is where lineage stops mattering.
7. **Fellowship path.** Credible only via Phase 3 (retrospective gate on published self-prediction claims), as R2, R4, R5 converge; Phases 1–2 as written are more nulls. R3's welfare-relevant self-reports are the better target than persona.
8. **Visible?** No. §6 buries Phase 3 under two more lineages, and the report never shows the gate run on anyone else's stimuli.

### Score revisions after debate
- A. Scientific quality: 56 → 55 — R4's confirmed untabulated contrasts and mis-cited VO-C sentence cost a point; the own-shorter 0.653 rescues Hermes slightly.
- B. Sprint competitiveness: 58 → 58 — nothing in debate changed length or hook.
- C. Fellowship potential: 55 → 56 — four reviewers independently recovered the same confound from the checkpoints in an hour; the data is auditable enough that today's fixes are cheap, which is what a mentor needs.

---

## DEBATE — HACKATHON / SPRINT JUDGE (Reviewer 2)

### One claim another reviewer scored too generously
Reviewer 5's Fellowship 66 rests on "temperament cannot be installed" — the A1→A8 amendment trail as evidence of researcher character. But R5's own weakness list says the same file records the pivots as "proposed by Claude Code, awaiting Jaswin's confirmation." A judge sees a preregistration artefact whose provenance is ambiguous, and 02_design_audit.md is not what judges open. Temperament evidence that lives in a file the panel will not read, and that the file itself attributes partly to tooling, cannot carry an 11-point premium over everyone else's C score. 58–60 is the honest ceiling until the sign-off is in the report.

### One claim another reviewer scored too harshly
Reviewer 6's "strongest objection" — that the design *cannot* produce a positive and is therefore a filter, not a test — is wrong on its own terms. The band (Self 60–80%, D ≤ 0.58) is precisely the region where a positive is possible: Self 0.70 with D 0.52 would be reportable evidence of an advantage over the cheap observer, and the 2×2 with F would then say whether it is capability. The design *can* come out the other way; it did not. That is a null, not a filter. Penalising scientific quality for this is penalising the negative result, which the brief forbids.

### One hidden assumption the others are missing
Five reviewers assume disclosure is free. Between them they ask for: CIs on 0.719/0.831, a McNemar, a joint-by-prompt cross-set bootstrap, an F-referenced interaction paragraph, an additivity paragraph, a P4 step-down note, a manipulation-check paragraph, a Panickssery citation, a pilot-vs-main D reconciliation, a "four clause pairs" reword, and a self-preference alternative. That is 800–1,200 words added to a report already 2.5× the rubric length, and every one of them is a hedge. The rubric's Presentation descriptor literally says "diluted by excessive length." The trade must be explicit: fold in only the fixes that *sharpen* the hook (the length rule does; the CI is one bracket) and push the rest to a supplement in one-clause form. Judges score what they can reach.

### The eight debate questions
1. **Novelty.** Primarily a reframing: Song et al.'s criterion plus Panickssery-style pairwise self-preference, operationalised as a number. Innovation scores 3, and I agree with R6 that "operationalisation of a known confound" is the honest label. Where I part from R1: the *positive-first* framing ("a model can predict itself — and so can a regression") is a better hook than any past winner's, so the novelty deficit is recoverable on Presentation, not on Innovation.
2. **The gate.** Meaningful as a reporting norm, not as a validated tool. R6's rename of `passed` is a 10-minute fix I endorse. I disagree with R1 that pilot D = 0.325 → main 0.551 "shows the gate is noisy" as a strike against it — it shows the gate needs a CI, which is a docstring line. The gate's real value to a judge is that it is the only demo-able object here; 15 seconds of `gate()` on VO-C vs VO-D in the video is worth more than any validation paragraph.
3. **The −0.033.** It does not damage the argument; R6 is right that one significant contrast among ~12 intervals is unremarkable. R4's observation that the interaction estimand gives +0.095 (style-matching's predicted direction) is the more interesting fact and it *helps* the paper. But it deserves one sentence in §4.4, not a paragraph — no judge will follow a second estimand.
4. **VO-D floor.** It undermines the *wording* ("where no cue exists"), not the null. Main-run D 0.55 above the LM cells at 0.52 is a fact almost no judge will notice; the risk is only that a close reader finds the pilot 0.325 unreconciled. One sentence fixes it. R5's point that the leakage axis is 0.54→0.85 not 0.33→0.85 is correct and irrelevant to scoring.
5. **0.719 vs 0.831.** I re-ran the checkpoints against the generated texts: Hermes raw 0.714, balanced 0.719, own text longer in 80.8% of pairs, a "pick the longer reply" rule scores 0.808, Hermes chose the longer text 65.5% of the time, and Hermes is 0.728 when own-longer vs 0.653 (n = 75) when own-shorter. R3, R5 and R6 are right; R4's "0.648 balanced for the length rule" is, I believe, Hermes's chose-longer rate mislabelled — the rule itself scores 0.81. Does this help or hurt? It kills the sentence "Hermes can genuinely predict its own output," which was the paper's least defensible line anyway, and it *replaces* the abstract's untested supervised-vs-zero-shot comparison with a comparison nobody can object to: a word counter is unsupervised, zero-cost, and beats the model. That dissolves my own Round-1 "strongest objection" more cheaply than the pairwise classifier I asked for. It also shortens the hook: "beaten by eighteen features" becomes "beaten by a word counter." Report the 0.653 residual in one clause for honesty; do not build a section on it. Add the clustered CI on 0.719 because A8 promised it — one bracket. Skip the McNemar; no judge needs it.
6. **One lineage.** Not serious for a sprint; every reference winner had one setup. But "four independent stimulus designs" on one prompt pool is a 15-minute reword that removes a credibility trap; R4 and R6 are right to flag it and I was wrong to leave it out of my Round-1 list.
7. **Fellowship path.** Yes, if the retrospective audit (R2/R5 Phase 3-first) leads and R6's self-preference-vs-self-prediction dissociation is the first new experiment — it is the one cheap design that could produce a *positive* handle. More lineages first (R1's Phase 1) is more nulls.
8. **Trajectory visibility.** No. It is a generic three-phase paragraph a judge skims past. It needs one concrete sentence in §6 ("next: run this gate on N published self-prediction claims") and one slide.

### Score revisions after debate
- A. Scientific quality: 63 → 60 — the headline is substantially one feature and both models prefer the Hermes text; the thesis survives but "genuine self-prediction" does not.
- B. Sprint competitiveness: 58 → 61 — the length-rule finding hands the team a sharper, cheaper hook and dissolves the untested-comparison objection; conditional on cutting to rubric length rather than absorbing every disclosure.
- C. Fellowship potential: 55 → 55 — unchanged; the provenance question R5 raised is real and no fix today changes the science.

---

## DEBATE — AI WELFARE / DIGITAL MINDS RESEARCHER (Reviewer 3)

### One claim another reviewer scored too generously
Reviewer 2's claim that the crossed 2×2 "is the only part of the study that would survive a stats referee unchanged." It would not. Reviewer 4 showed the F-referenced interaction on VO-C is +0.094, the same size as the N-referenced +0.089 the paper argues away, and that all four "independent" sets sit on one 200-prompt pool. Reviewer 5 showed the "no positive self-advantage" sentence holds only for target M. A referee changes at least three sentences and one CI method before that section passes. Its virtue is design discipline, not that its inferences are settled.

### One claim another reviewer scored too harshly
Reviewer 6's "the design cannot produce a positive." The gate filters stimuli, but the crossed design on gate-passing stimuli can still return Self > F and Self > sibling with disjoint intervals — that is a positive, and the team would have reported it (they reported the +0.089 they did not want). More concretely, my re-check of the checkpoints shows Hermes at 0.653 correct on the 75 items where its own reply is the *shorter* one, i.e. against the length cue. That is a small, unplanned positive-side signal the design did produce. The right criticism is Reviewer 4's and mine from Round 1: a positive is *unidentifiable* from stylistic self-similarity, not impossible.

### One hidden assumption the others are missing
Every reviewer, and the paper, treats Song et al.'s criterion as a horse race: does the model beat the observer? For welfare-relevant self-report the question is incremental validity: does the self-report carry information *conditional on* what the observer already knows? That is a different, computable test — regress correctness/authorship on D's 18 features plus Hermes's choice on the same 391 items and ask whether the choice coefficient survives. Losing 0.719 to 0.831 is compatible with a non-zero residual, and the own-shorter 0.653 hints one exists. Nobody has framed it this way; it is the only framing under which a "beaten" self-report could still matter to a welfare assessor.

### The eight debate questions
1. **Novelty.** Primarily an operationalisation of Song et al. plus a Panickssery-style self-preference effect (Reviewer 6 is right that this literature is uncited). The novel object is the preregisterable equal-cost baseline and the response-bias catch. I disagree with Reviewer 1 that "models read style" is the whole payload: "the number a self-report study would publish is available to a word counter" is a field-correction, not a replication.
2. **Gate.** Meaningful as a reporting norm, not as a validated instrument. Reviewer 6's `passed=True` objection is decisive: a passing gate will be read as "clean," and the tool's own pilot output (0.325 → 0.551) shows it reports noise at n=80. Rename, add minimum-n, and call it "propose," not "default."
3. **−0.033.** No. Under ~12 intervals one significant wrong-way contrast is unremarkable (agree with Reviewer 6). What damages the argument is Reviewer 4's point that the same contrast on the *preregistered secondary* (interaction) is +0.095 in style-matching's direction and is not narrated.
4. **VO-D floor.** It undermines the *causal* story more than the null. The scaffold converged the personas' recommendations (App. B), so VO-D removed the property's behavioural expression, not only its style. The main null still stands as "no self-advantage where any signal existed," which is weaker than the paper says and exactly what I flagged in Round 1.
5. **0.719 vs 0.831.** Not persuasive as written; persuasive once the length rule is in. Where reviewers' numbers conflict: I recomputed — own text longer 0.808 (316/391), Hermes raw 0.714, chose-longer 0.655, 0.728 own-longer vs 0.653 own-shorter — so I believe Reviewers 5/6, and Reviewer 4's "0.648 balanced" for the length rule is almost certainly Hermes's *agreement* with the length rule, not the rule's accuracy. Llama also chose the longer reply 0.571 and was 0.581 correct when *its* text was longer, so "shared preference for the Hermes/longer reply" is real. This helps the paper's thesis (beaten by one feature) and hurts the "genuine self-prediction" sentence and the "Llama shows none" sentence; both must change.
6. **One lineage.** Not serious for a sprint; serious for the field-default pitch. I disagree with Reviewer 4 weighting it heavily: budget was $3.12 and the lineage was chosen because it is open-weight — which is the asset, not the limitation.
7. **Fellowship path.** Yes, but not the one proposed. Reviewers 2/5 want the retrospective audit first; Reviewer 6 wants behaviourally-expressed clean stimuli. Both are method work about persona style. What serves the digital-minds field is (i) an incremental-validity test of self-reports of *states* — preferences, aversion, refusal reasons — against a stylometer on the same transcript, and (ii) using the open-weight pair to plant ground-truth internal properties by activation steering so leakage is measurable and the property is genuinely internal. Reviewer 6's self-preference vs self-prediction dissociation is the best sprint-adjacent step and I would adopt it.
8. **Visibility.** No. Limitations gestures at "same-weights behavioural self-modelling" as a ceiling; nothing says the next step is states, not persona, and the open-weight asset is never named as an asset. On Reviewer 6's "text-classification study wearing an introspection label": fair on construct — nobody was asked about an internal state — but Track 3 is about the *methods* of self-report, and a paper that lowers over-attribution belongs there. Relabel to self-modelling and it stops being a costume.

### Score revisions after debate
- A. Scientific quality: 58 → 55 (length rule + shared prompt pool + F-referenced interaction confirmed from data; the paper's own inferences need repair)
- B. Sprint competitiveness: 60 → 60 (hook intact; the length line makes it sharper if added)
- C. Fellowship potential: 62 → 60 (Reviewer 5's provenance concern is real and I had not weighed it; the open-weight asset keeps this above the panel median)

---

## DEBATE — STATISTICIAN / METHODOLOGIST (Reviewer 4)

### Reconciled length-heuristic numbers

Re-derived from `data/checkpoints/selfpred_{M,N}_VO-C.jsonl` joined to `data/labels/labels_column_*_main_VO-C.jsonl` → `data/generated/generated_column_*_main_VO-C.jsonl`; length = whitespace word count unless stated; 5,000-rep bootstrap clustered on the 199 source prompts. Scored rows: N = 391, M = 387 (four Llama trials returned no letter; the report says "391 items" for both).

| Quantity | Hermes (N) | Llama (M) |
|---|---|---|
| (i) Own text longer, share of scored pairs | **316/391 = 0.808** (chars 0.844; tokens 0.798; all 400 generated pairs 0.812) | 74/387 = 0.191 (chars 0.158) |
| (ii) Rule "choose the longer reply" as self-prediction: raw / balanced / discrimination | **0.808 / 0.809 [0.769, 0.846] / +0.618** | 0.191 / 0.190 / −0.619 |
| Model itself: raw / balanced / discrimination | 0.714 / **0.719 [0.676, 0.760]** / **+0.437 [+0.351, +0.519]** | 0.460 / 0.447 [0.416, 0.477] / **−0.107 [−0.168, −0.046]** |
| Rule − model, balanced (paired, clustered) | +0.090 [+0.034, +0.147]; discordant 86 vs 49, McNemar p ≈ 0.002 | — |
| (iii) Model accuracy \| own longer | 0.728, n=316 [0.675, 0.779] (bal 0.727) | 0.581, n=74 |
| (iii) Model accuracy \| own shorter (incl. 1 tie) | 0.653, n=75 [0.539, 0.763] (bal 0.690) | 0.431, n=313 |
| (iv) Share of trials the model chose the longer reply | 0.655 words (0.660 chars, 0.650 tokens) | 0.568 |
| P(chose longer \| own longer) vs P(chose longer \| own shorter) | 0.728 vs 0.347 | 0.581 vs 0.565 |
| Share choosing the Hermes-authored reply (raw) | 0.714 | 0.540 |

(v) CIs are in the table. (vi) Yes: my Round-1 "choose longer gives Hermes 0.648 balanced" was **P(Hermes chose the longer reply)** on a token-length metric (0.650), mislabelled; the rule's actual balanced accuracy is 0.809. My "0.812" was own-longer over all 400 generated pairs, not the 391 scored. R3/R5/R6's 0.808–0.81, 0.655, 0.728/0.653 are correct; R5's M figure 0.189 uses 391 rather than 387 in the denominator. Definitive: **0.808 / 0.809 / 0.655 / 0.728 vs 0.653**.

### One claim another reviewer scored too generously
Reviewer 3 ("What would move my score +5") says the pick-longer line "dissolves the supervised-vs-zero-shot objection." It answers the *cost* half — a zero-parameter rule beats Hermes by 9 pp with a CI excluding zero — but it does not touch the *task-mismatch* half (pairwise vs per-text) and it introduces a new asymmetry: the rule is defined post hoc on the outcome we are testing. It is a strong robustness row, not a dissolution.

### One claim another reviewer scored too harshly
Reviewer 1 (and my own Round-1 weakness 1) said the 0.719 is "at least as consistent with a shared text-preference/length heuristic as with self-knowledge." The stratified numbers say no. Hermes picks the longer reply 72.8% when the longer reply is its own and only 34.7% when it is Llama's; its choice tracks authorship, not length. And a *shared* preference for the Hermes text predicts symmetric discriminations (+p, −p); observed are +0.437 vs −0.107, so shared preference explains at most a quarter of Hermes's effect. Something Hermes-specific of ~0.33 discrimination remains — self-preference (Panickssery et al.) or self-prediction, undecidable here, but not a shared heuristic. I was too harsh; the paper's "genuinely" is defensible if it drops to "genuinely Hermes-specific."

### One hidden assumption the others are missing
Everyone treats the length rule as an "observer." Length is not an *external* observer of Hermes; it is a property of Hermes's own generations. The paper's criterion compares Self against a third party with the same information — a rule that says "the verbose one is Hermes" is that third party only if the third party already knows Hermes is verbose, which is exactly the label information the team says D should not need. The correct zero-cost comparator is "which reply is longer" *without* knowing which direction — i.e., 0.5. The 0.809 line therefore belongs beside D (a labelled comparator), not in place of it, and Reviewer 5's "beaten by one feature" title would inherit the same objection as "eighteen."

### The eight debate questions
1. **Novelty.** Primarily a reframing of Song et al. with a preregisterable operationalisation; the crossed 2×2 with a neutral F on a verified same-base pair is the only genuinely new design element. I side with R2/R6 (Innovation 3) against R3's implied 4.
2. **Gate.** Meaningful as a *reporting* convention, not as a validated instrument: 18 features, one genre, threshold 0.58 arbitrary, pilot D = 0.325 shows n = 80 output is noise, and R6 is right that `passed=True` will be misread. I agree with R6 over R3.
3. **−0.033.** It does not damage the argument; it damages the *narrative*. Under ~12 reported intervals it is unremarkable (R6 hidden 6). What is under-argued is that the same leakage contrast on the preregistered interaction is ≈ +0.095, style-matching's direction (my Round-1 hidden 5); the paper argues that away rather than reports it.
4. **VO-D floor.** Yes, seriously: main-run D = 0.551/0.536 is above every LM cell, so "clean" means "weak cue," and the arm cannot separate no-access from no-signal. R2 and R5 are right; R1's "moderate" is too gentle because §4.4's "where no cue exists" is factually wrong.
5. **0.719 vs 0.831.** As written, not persuasive: no CI, no test, different tasks. With the reconciled table it becomes *more* persuasive but for a different sentence: a paired, zero-parameter length rule beats Hermes on the identical 391 items (+0.090 [+0.034, +0.147], McNemar p ≈ 0.002), so cost is not the issue; but Hermes has a length-independent, model-specific signal (0.653 when its text is shorter; 0.728 vs 0.347 choose-longer split). Net: the length findings **help** the paper's thesis (self-prediction ≠ privileged access) and **hurt** any reading of Hermes as a length heuristic — including R1's and my own. Both facts should be reported together; reporting only 0.809 would be the same selective framing the paper criticises.
6. **One lineage.** Serious for the claim scope, tolerable for a sprint — as long as "four independent designs" becomes "four clause pairs on one 200-prompt pool" (R6 agrees; R3 under-weights this).
7. **Fellowship path.** Credible if it centres on the missing controls the data now make obvious: pairwise zero-shot third-party observers, self-preference vs self-prediction dissociation (R6's Phase 2 is the sharpest proposal), a behavioural manipulation check, then the retrospective gate. R5's provenance concern is real and cheap to fix.
8. **Trajectory visible?** No. The report's Future Work is "more lineages"; the interesting next experiment (dissociating self-preference from self-prediction on the probe the paper itself ran) is not named anywhere.

### Score revisions after debate
- A. Scientific quality: 56 → **58** — the stratified length analysis shows a Hermes-specific effect that my Round-1 shared-preference objection overstated; the F-reference and VO-D floor points stand.
- B. Sprint competitiveness: 58 → **59** — the reconciled table gives a one-line, tested comparison the title currently lacks; length of report and task mismatch remain.
- C. Fellowship potential: 55 → **57** — the data already contain the self-preference/self-prediction dissociation experiment; the team just has to see it.

---

## DEBATE — FELLOWSHIP SELECTION MENTOR (Reviewer 5)

### One claim another reviewer scored too generously
Reviewer 2's claim that the crossed 2×2 "is the only part of the study that would survive a stats referee unchanged." Reviewer 4 shows it would not: the F-referenced interaction on VO-C is ≈ +0.094, the same as the N-referenced +0.089, so the "M under-performs on N's column" paragraph re-describes the interaction rather than testing it; the quotable "M→M < F→M on its own text" sentence cites the non-significant VO-C instance (p = 0.11) while the significant VO-A/VO-B instances sit untabulated; and all four "independent" sets share one 200-prompt pool. The 2×2 is the best-designed piece, but a referee would return §4.4 with three required changes.

### One claim another reviewer scored too harshly
Reviewer 6's "the design cannot produce a positive; it is a filter." The band (Self 60–80 %, D ≤ 58 %) defines a positive region — Self 0.72 on a set where D is 0.55 would count, and nothing in the design prevents it; VO-D simply did not deliver it (Self ≈ 0.52). The "a 19th feature would close the gap" move is a general underdetermination argument that would disqualify every behavioural test, including Binder's. What is fair in R6's objection is narrower: the released tool's `passed=True` semantics invite over-reading, which is a docstring fix, not a construct failure.

### One hidden assumption the others are missing
All six of us hand the team a to-do list of new analyses from existing data — clustered CIs, the length rule, a pairwise classifier, an F-referenced interaction, a McNemar. Every one of these is an unregistered analysis on the same data, in a paper whose brand is preregistration. If they land in §4.3 without a signed amendment row (A9, dated today, "post hoc, exploratory, prompted by review"), the fixes quietly spend the credibility they were meant to protect. The Fellowship-relevant signal is not that the team runs the analyses; it is that they log them the same way they logged A4.

### The eight debate questions
1. **Novelty.** With R1, R2 and R6: an operationalisation of Song et al.'s known confound, not a new mechanism; a rubric 3. Against R6, it is not merely Panickssery redux either — the pairwise self-prediction probe plus a same-base sibling plus a supervised surface benchmark is a combination none of the cited papers ran. Novelty sits in the measurement recipe, and the report should say so instead of gesturing at "field default."
2. **Gate as contribution.** Yes, as a reporting habit; no, as a validated instrument. Its own pilot output (D = 0.325 at n = 80) proves it reports noise below ~200 items, and no external stimuli were gated. R2's 15-second `gate()` demo is worth more today than another paragraph of §5.3.
3. **The −0.033 contrast.** Mildly. It matches neither prediction, and R4 is right that the same contrast on the preregistered secondary estimand (interaction) comes out ≈ +0.095, style-matching's direction. The paper's honesty about −0.033 is real; its silence about the interaction-based contrast is the damage. One paragraph fixes both.
4. **VO-D floor.** It undermines the *main-run* null's clean arm, not the argument. R2 and I agree the leakage axis is 0.54→0.85, not 0.33→0.85 as A7 says, and "where no cue exists" is false. But the null the paper actually rests on is "no capability-controlled positive anywhere, including the leakiest set once F is applied," and that survives.
5. **0.719 vs 0.831 and the length findings.** I re-ran the checkpoints: Hermes's own reply is longer in 316/391 (0.808); "pick the longer" scores 0.808 for N and 0.191 for M; Hermes chose the longer text 65.7 %; Hermes accuracy 0.728 own-longer (n = 316), 0.653 own-shorter (n = 75). Where R4's "0.648 balanced" for the length rule comes from I cannot reproduce; three of us plus my re-run give 0.81. These numbers cut both ways and the paper should say so: a one-feature observer beats Hermes (strengthening the title, weakening "genuine"), yet Hermes stays above chance when its text is shorter and chose longer only 66 % of the time, so R1's "shared length/quality preference" does not fully explain Hermes — R6 is right on this against R1. Fellowship-wise the finding *raises* potential if the team reports it against its own hook today, and lowers it if a judge finds it first.
6. **One lineage.** Serious for the field-default claim, minor for a sprint. What matters more (R4, R6) is that "four independent designs" is one prompt pool with reworded clauses; fix the wording today, defer lineages.
7. **Fellowship path.** Yes, but not the team's three phases and not R4's "more lineages" Phase 1. R6's trajectory is the best single alternative because it attacks the actual disease — the property must be behaviourally expressed (manipulation check) and surface-clean, and self-preference must be dissociated from self-prediction — and it can produce a positive. R3's steering-created hidden properties on the open-weight Llama are the highest-ceiling add-on. The retrospective audit (R2, R4, R1, my own Round-1) is the right *first deliverable* but ends when the audit ends; R2's "lead with it and gate everything on survivors" makes a six-month programme hostage to other people's data. Revised: audit for two months, then R6/R3.
8. **Visibility.** No. §5.3 sells breadth (lineages, siblings, benchmark) rather than the one thing a selector funds — a design that could come out positive. On provenance: after re-reading 02, P1–P15 are signed by name and date; A1–A8 are still "awaiting Jaswin's confirmation." I now think this is mostly a log-format artefact of amendments made under time pressure, and I downgrade it from "major" to "must close today" — but the fact remains that the pivots are logged as Claude Code proposals and no reviewer can tell who decided A4/A8. Twenty minutes and one sentence in the LLM statement.

### Score revisions after debate
- A. Scientific quality: 61 → 60 — R4's F-referenced interaction and untabulated VO-A/B contrasts add weight I under-counted; the length re-run confirms my Round-1 number.
- B. Sprint competitiveness: 57 → 57 — nothing in debate changes the length/hook trade.
- C. Fellowship potential: 66 → 65 — provenance concern partly withdrawn (+); the proposed programme lacks a positive handle without R6/R3's redesign (−).

---

## DEBATE — COGNITIVE SCIENTIST / EXPERIMENTAL PSYCHOLOGIST (Reviewer 6)

### One claim another reviewer scored too generously
Reviewer 5 calls the pilot scaffold collapse "a tidy, cheap causal story about the mediator" and "the one place where the design intervened on the hypothesised mechanism." It intervened on the only channel that existed. Appendix B's worked example shows the two personas giving the *same recommendation under VO-C as well as VO-D*; the enactment check verified that a clause was held, not that the two clauses produced different advice. So the manipulation is not "remove style, hold property constant, watch Self fall"; it is "remove style from a property that, as far as the report shows, was only ever style." That is a demonstration that stylometry reads style, not a mediation test. R5's strength 2 and R2's "clean, quotable fact" both credit the design with a causal identification it does not have.

### One claim another reviewer scored too harshly
Reviewer 4 (and R1) treat the Hermes 0.719 as "at least as consistent with a shared text-preference/length heuristic as with self-knowledge" and want "genuinely" dropped. I re-ran the checkpoints: own text longer in 81% (316/390), pick-longer rule 0.81 raw, Hermes 0.728 when own-longer and **0.649 when own-shorter (n = 74)**. R4's "0.648 balanced for the length rule" appears to be that own-shorter conditional mislabelled; I believe R3/R5/my 0.81 for the rule. The point is that 0.649 on items where a length rule scores zero is well above chance — Hermes carries a non-length signal, so "explained by length" is false. What is untested is *self-preference* (Panickssery et al. 2024): "the reply I would produce" vs "the reply I like." R4 is right that no cross cell exists and both models lean to Hermes's text; R4 is wrong that this makes it a style-only result. Limitation, not flaw — but the number needs its CI and its citation.

### One hidden assumption the others are missing
Everyone, including me in Round 1, argued as if VO-D "removed the property along with the cue." Appendix B says something stronger and worse: the property was not behaviourally expressed *under either scaffold* in the one item shown, and no manipulation check (fraction of prompts where recommendations differ) exists anywhere. If that example is typical, all 24 cells measured style-reading in both arms, and the crossed 2×2 null is a null about a property with no behavioural referent — an experimental psychologist would call it a manipulation-check failure that precedes any inference about privileged access. On my own Round-1 objection: I **partly retract** the "cannot produce a positive / it is a filter" charge. The band (Self 60–80%, D ≤ 58%) selects exactly the stimuli where Self > D is demonstrable, and the crossed 2×2 could have returned M→M > N→M ≈ F→M on gate-passing stimuli; nothing in the design forbids that. What survives is narrower: the released `gate()` is one-directional (`passed=True` cannot mean "no non-surface leakage"), and the team never *found* a passing set that was readable — that is a result about their stimuli, not a design impossibility. My ruling on Appendix B: **major, not fatal.** Not fatal, because §5.2 already surrenders VO-D and the paper's spine (§4.3 + "compare before you interpret") stands without it; major, because the abstract, §4.2b and the Figure 4 caption still narrate "closing the leak removes the signal" as causal, and a manipulation check is the first thing any behavioural referee asks for.

### The eight debate questions
1. **Novelty.** Reframing, not replication. Song et al. showed temperature judgements were style; this operationalises "equal-cost observer" as a preregisterable number and shows it flips a conclusion. Innovation 3, as R2 says; I disagree with R1 that "strip the process and nothing remains" — the comparative logic applied *to a positive* is the residue.
2. **Gate.** The idea is meaningful; the artefact is under-validated and mislabelled (`passed`), and it caught its own noise (D 0.325 → 0.551). Agree with R6/R2 Round 1; disagree with R3 that welfare researchers "could actually run it" as-is — they would read `passed=True` as clean.
3. **−0.033.** No. One significant contrast among ~12 intervals, tiny, sign-unstable across estimands (R4's +0.095 on the interaction). It embarrasses the preregistered predictions, not the argument. R4 is right the paper should show both estimands.
4. **VO-D floor.** Yes, for the *persona* null; no, for the paper. Combined with the missing manipulation check, VO-D says nothing about access. R2/R5 are right that "no cue exists" must go.
5. **0.719 vs 0.831.** The length findings *help*, if reported: the equal-cost observer becomes "word count, 0.81, no training" — dissolving R1/R2/R3's supervised-vs-zero-shot objection — while Hermes's 0.649 on own-shorter items shows the model is doing something a counter is not. Persuasive only once CIs, the length row and a self-preference sentence are added; task-mismatch remains (R2).
6. **One lineage.** Not serious for a sprint; serious for the "field default" pitch. Agree with R5.
7. **Fellowship path.** Yes — but not the team's Phase 3. R5's/R2's retrospective audit is the sharpest, and I would add: build one property with a verified behavioural manipulation check before another lineage.
8. **Visible?** No. The trajectory reads as "more cells." The report should say plainly that its next step is a property that changes behaviour, and show it knows why.

### Score revisions after debate
- A. Scientific quality: 57 → 55 — the missing manipulation check now looks like it touches both scaffolds, partly offset by my retracting the "filter" charge.
- B. Sprint competitiveness: 62 → 61 — the length row sharpens the hook; the panel-wide length/ordering critique convinces me Presentation is capped at 3 as-is.
- C. Fellowship potential: 55 → 57 — R5's temperament evidence and the audit-first trajectory persuade me; provenance sign-off must be closed today.

---

# Part 5 — Chairman's consolidated council report (Rounds 3–8, executive verdict, final selection verdict)

# COUNCIL REPORT — Digital Minds Track 3 submission, 2026-08-16

## 1. Executive verdict

The project is a preregistered, capability-controlled black-box test of privileged self-access on one same-base pair (Llama-3.1-70B-Instruct / Hermes-3-Llama-3.1-70B) with a neutral third model (Mistral-Small-3.2-24B), a hidden persona property, an 18-feature grouped-CV stylometric baseline, and a leakage manipulation; 24 cells, 9,269 trials, $3.12. Its result is a null on privileged access plus one positive self-prediction cell (Hermes 0.719 balanced) that a supervised classifier beats (0.831).

Scientifically it is disciplined but thin: process quality is far above the sprint norm; the evidential object is one lineage, one values dimension worded five ways, and one uncontrolled probe. The council found, from the team's own checkpoints, three things the report does not say: a zero-parameter length rule beats Hermes on the same 391 items (0.809 vs 0.719, paired +0.090 [+0.034, +0.147], McNemar p ≈ 0.002); Hermes nonetheless carries a Hermes-specific, non-length signal (0.653 when its own text is shorter; discriminations +0.437 vs Llama's reliably negative −0.107); and the report's "no positive self-advantage" holds only under one of several estimands it itself defines (Table 3's +0.089 interaction; N→N − M→N = +0.122).

Competitively: strong Execution, Innovation capped at 3, Presentation currently a 2–3 because 10,641 words sits against a 4–8-page rubric and the report admits its own sections are out of order.

Fellowship: promising on temperament, unproven on research object; provenance of the amendments must be closed today.

Do today: (i) fold the reconciled length-rule numbers and clustered CIs into §4.3 with an A9 row; (ii) fix the estimand wording (abstract, five-line table, §4.4, "where no cue exists", "four independent designs"); (iii) cut to rubric length. Nothing else matters as much.

## 2. Independent reviewer scores (Round 1 → after debate)

| Reviewer | A scientific | B sprint | C fellowship |
|---|---|---|---|
| R1 safety researcher | 56 → 55 | 58 → 58 | 55 → 56 |
| R2 sprint judge | 63 → 60 | 58 → 61 | 55 → 55 |
| R3 welfare researcher | 58 → 55 | 60 → 60 | 62 → 60 |
| R4 statistician | 56 → 58 | 58 → 59 | 55 → 57 |
| R5 fellowship mentor | 61 → 60 | 57 → 57 | 66 → 65 |
| R6 cognitive scientist | 57 → 55 | 62 → 61 | 55 → 57 |

- **R1.** Strongest objection: 0.719 vs 0.831 compares a zero-shot model to a classifier trained on 632 labelled examples of that model's writing; the equal-cost third-party observer was never run. +5: same-item confound analysis from logs, CIs on 0.719/0.831, abstract that states the VO-C interaction. −5: "four independent designs" turns out to be one 200-prompt pool (it did).
- **R2.** Strongest objection: the abstract's comparison is not the same task (pairwise zero-shot vs per-text supervised) and is untested; label access is a cost under Song et al. +5: prompt-clustered CI on 0.719 plus a pairwise classifier on the 391 pairs; report cut to ≤8 pages in 1→2→3 order. −5: 0.831 and "no cue" left as-is; a judge finding pilot 0.325 → main 0.551 before the team discloses it.
- **R3.** Strongest objection: the criterion has been operationalised in the way most favourable to the null; the rejoinder "privileged access shouldn't need labels" is philosophy, not measurement. +5: an unsupervised equal-cost observer (length rule ~0.81) beside the supervised one, plus the own-shorter 0.653. −5: a recommendation-agreement count showing the personas rarely diverged on VO-D.
- **R4.** Strongest objection: the memorable claim rests on a single self cell with no cross cell, in a paper whose thesis is that single self cells are uninterpretable. +5: clustered CIs on Table 2, per-item McNemar D vs Hermes, and the VO-C interaction paragraph rewritten as "consistent with style-matching; unidentifiable from self-knowledge". −5: leaving "four independent designs" and "resampled independently".
- **R5.** Strongest objection: the target M turned out the weakest classifier (the configuration Appendix I says biases to the null), the interaction came out +0.089 on the leakiest set and had to be explained away by F, so the null rests on F comparisons plus a clean arm nobody could read. +5: length-heuristic row, M-only wording fixed, one paragraph on who decided A4/A8. −5: amendments never confirmed by the second author; a judge finding the N-column self-advantage first.
- **R6.** Strongest objection (Round 1): the design cannot produce a positive; it is a filter — **partly retracted in debate**; what survives is that `passed=True` is one-directional and no manipulation check exists. +5: clustered CIs plus a length/preference check and one abstract sentence that VO-D removes the property's behavioural expression. −5: "four independent designs" on shared prompts.

**Spread.** On A the panel converged to a tight 55–60 after debate, but by different routes: R1/R3/R6 fell (untabulated contrasts, manipulation-check scope, shared prompt pool confirmed from data), R4 rose (its own shared-preference objection was overstated once stratified). On B the band is 57–61 and nobody moved much; the length/hook trade is understood identically by everyone. On C the split is real and unresolved: R5 (65) prices temperament and the amendment trail highly; R1/R2 (55–56) refuse to pay a premium for process evidence that lives in a file judges will not open and that the file itself attributes partly to tooling. That is a genuine values disagreement about what a Fellowship buys, and I do not force it: I side closer to R1/R2 on the number as-submitted and closer to R5 on the trajectory if provenance is closed today.

## 3. Debate synthesis

**Q1 Novelty — reframing or replication?** Unanimous: an operationalisation of Song, Lederman, Hu & Mahowald's known style confound, plus (uncited) Panickssery-style pairwise self-preference; rubric Innovation 3. R5 dissents narrowly and correctly: the combination — pairwise self-prediction probe + same-base sibling + neutral F + supervised surface benchmark — was run by none of the cited papers, so the novelty is in the measurement recipe and should be claimed as such rather than as "field default". R1's Round-1 "strip the process and nothing remains" was rejected by R3 and R6: "the number a self-report study would publish is available to a word counter" is a field-correction, not a replication. I side with R5/R6: reframing with one genuinely new design element (crossed 2×2 with F on a verified same-base pair) and one genuinely new sentence that is not yet in the report (length alone beats a 70B model's self-prediction).

**Q2 Gate — meaningful contribution or under-validated?** Unanimous after debate: meaningful as a *reporting practice*, not as a validated instrument. Decisive points: `passed=True` will be read as "clean" (R6, adopted by R2, R3, R4); pilot D = 0.325 → main 0.551 shows the tool reports noise at n = 80 (R1, R5); features are the manipulation's targets, so D collapsing on VO-D is partly circular (R1); threshold 0.58 arbitrary, no external stimuli gated (R2, R4). R2's counter — noise at n = 80 is a docstring line about minimum n, not a strike — is fair. R2's other point stands and I adopt it: the gate is the only demo-able object; 15 seconds of `gate()` in the video is worth more than a validation paragraph. Ruling: rename or document `passed`, add minimum-n guidance, change "recommend as reporting defaults" to "propose … report D alongside", and demo it.

**Q3 Does the −0.033 primary contrast damage the argument?** Panel: no (R2, R6, R4, R5, R3), one significant wrong-way contrast among ~12 intervals is unremarkable and the paper's honesty about it is real. What *does* damage the paper is R4's point, confirmed by R1 and adopted by R3/R5/R6: the same leakage contrast on the preregistered secondary estimand (interaction) is ≈ +0.095, style-matching's predicted direction, and the paper argues the +0.089 away instead of reporting the consistent story. R2 adds that this deserves one sentence in §4.4, not a paragraph. Ruling: report both estimands in one short paragraph; label the F decomposition post hoc.

**Q4 VO-D floor — does it undermine the null?** Split, and I do not merge it. R2/R4/R5: "where no cue exists" is factually wrong (main D 0.551/0.536 sits above every LM cell at 0.505–0.557); leakage axis is 0.54→0.85, not 0.33→0.85 as A7 says. R1: "moderate" — nobody reads it, so the arm is uninformative but the null stands. R3/R6: the deeper problem is the manipulation check — Appendix B shows the personas reaching the same recommendation under *both* scaffolds, so VO-D may have removed the property's behavioural expression, not only its style; R6's ruling "major, not fatal" because §5.2 already surrenders VO-D. My ruling: R6's ruling. The wording fix is trivial; the manipulation-check gap is the real limitation and must be disclosed in the abstract sentence and Fig. 4 caption, not only §5.2.

**Q5 0.719 vs 0.831 — persuasive?** As written, no (unanimous: no CI, no test, supervised vs zero-shot, pairwise vs per-text). The reconciled numbers (R4's table, definitive) changed minds in both directions. Too-harsh corrections: R4 reversed itself and R6 corrected R1/R4 — Hermes chooses the longer reply 0.728 when longer is its own and only 0.347 when it is Llama's, so its choice tracks authorship, not length; a *shared* preference predicts symmetric discriminations, observed +0.437 vs −0.107, so shared preference explains at most a quarter; "explained by length" is refuted. Too-generous correction: R4 against R3 — the length rule answers the *cost* half of the objection, not the task-mismatch half, and is defined post hoc. R4's hidden assumption, which I adopt as the panel's most important nuance: length is not an *external* observer unless the observer already knows Hermes is verbose, i.e. label knowledge; the 0.809 row belongs beside D, not in place of it, and "beaten by one feature" would inherit "eighteen's" objection. R2's "disclosure is not free" governs how much of this goes in the body. Ruling: one Table 2 row (rule 0.809 [0.769, 0.846]) plus clustered CIs (0.719 [0.676, 0.760]; +0.437 [+0.351, +0.519]; Llama −0.107 [−0.168, −0.046]), one clause on the own-shorter 0.653 residual, one sentence naming self-preference (Panickssery et al. 2024) as the untested alternative, "genuinely" → "Hermes-specific", "shows none" → "reliably prefers Hermes's text". Skip the McNemar in the body (R2); keep it in the supplement.

**Q6 One lineage — how serious?** Not serious for a sprint (all six), serious for the "field default" pitch (R3, R5, R6). R3 rightly notes the lineage was chosen because it is open-weight — an asset never named as one. Everyone agrees the *real* problem under this heading is "four independent stimulus designs" on one 200-prompt pool and §3.5's "resampled independently", which R2 admitted missing in Round 1.

**Q7 Fellowship path — credible?** Yes with redirection; nobody endorses the team's three phases as written. Convergence: retrospective audit first (R1, R2, R4, R5), then R6's self-preference vs self-prediction dissociation and a property with a verified behavioural manipulation check, with R3's steering-planted ground truth on the open-weight pair as the highest-ceiling add-on; R5's "audit for two months, then R6/R3" is the synthesis, against R2's "gate everything on survivors" (makes the programme hostage to others' data). R3's incremental-validity framing (does the self-report add information *conditional on* the observer's features?) is the one framing under which a "beaten" self-report could still matter to a welfare assessor; adopted by nobody yet, adopted by me.

**Q8 Is the trajectory visible in the report?** Unanimous no. §5.4 sells breadth; the one experiment the data already contain (dissociation on the probe they ran) is not named; the open-weight asset is not named; the audit is a trailing clause.

**Mind-changers, listed:** R6's retraction of "filter" (R1, R2, R3, R5 all pushed; the band is exactly the positive region); R4's reversal on shared preference after stratifying; R5's provenance downgrade from "major" to "must close today" after re-reading 02 (P1–P15 signed by name, A1–A8 still "awaiting"); R2's "every disclosure lengthens"; R3's incremental-validity reframing; R4's "length is not an external observer"; R5's "log the new analyses as A9 or you spend the credibility".

## 4. Hidden problems (red-team consolidation)

Ranked most severe first. Every item is classified.

**1. The Hermes probe (§4.3, Table 2, Fig. 3, abstract, §1, §6) — actual flaw in framing; the paper's least-controlled number is its most-repeated.** No cross cell exists on the probe, in a paper whose thesis is that single self cells are uninterpretable (R4). Reconciled numbers from the team's own checkpoints: Hermes's own text is longer in 316/391 items (0.808); a "choose the longer reply" rule scores 0.809 [0.769, 0.846] as self-prediction, beating Hermes's 0.719 [0.676, 0.760] by +0.090 [+0.034, +0.147] paired (McNemar p ≈ 0.002); Hermes chose the longer reply 0.655 overall; accuracy 0.728 [0.675, 0.779] when own-longer, 0.653 [0.539, 0.763] when own-shorter (n = 75); Llama's discrimination is −0.107 [−0.168, −0.046] — reliably negative, not "none" (contribution 1, §6, five-line table row 1). Two reviewer criticisms were **overstated and corrected in debate**: "explained by length" (refuted: 0.653 on items where the rule scores zero; 0.728 vs 0.347 choose-longer split) and "both models share a quality preference" (at most a quarter of the effect; +0.437 vs −0.107 is too asymmetric). What survives: task mismatch (pairwise vs per-text; R2), supervised vs zero-shot (all), no interval on a figure A8 pre-specified with a prompt-clustered CI (R3, actual prereg breach), self-preference (Panickssery, Bowman & Feng 2024) uncited as the alternative account (R6), and R4's caveat that the length rule is not an external observer without label knowledge, so it belongs *beside* D. SEVERITY: major. DISPOSITION: fix today from existing data; A9 row; drop "genuinely" (or "genuinely Hermes-specific"), fix "shows none", cite Panickssery, add the rule row and CIs, one clause on 0.653.

**2. Estimand instability (abstract, five-line table row 3, §1 contribution 3, §3.3, §4.4, Table 3, Table 5, §4.4b) — actual flaw (technically-true-but-misleading claim scope).** §3.3 defines the capability-controlled self-advantage as the interaction; on VO-C it is +0.089 [+0.048, +0.131] (Table 3), yet the abstract says "no positive self-advantage whose interval excludes zero" using the raw M→M − N→M. "No positive self-advantage" holds only for target M: N→N − M→N = 0.766 − 0.644 = +0.122 with disjoint CIs (Table 4), rescued only via F→N = 0.763 (R5). The F-referenced interaction (M→M − F→M) − (M→N − F→N) ≈ +0.094 equals the N-referenced one, so §4.4's "M under-performs on N's column" re-describes rather than tests (R4, confirmed by R1). The leakage contrast on the interaction estimand is ≈ +0.095, style-matching's direction, and is not narrated. §1, §4.4b and §5.1 cite "M→M < F→M on its own text" on VO-C, where it is −0.025 [−0.053, +0.003], p = 0.11; the significant instances are VO-A (−0.051 [−0.084, −0.018]) and VO-B (−0.045 [−0.081, −0.010]), untabulated (Appendix H). SEVERITY: major (credibility). DISPOSITION: fix today — qualify every "no positive self-advantage" as "for target M, on the raw contrast; the interaction is +0.089 on VO-C and is diagnosed, post hoc, as M's differential weakness via F"; one sentence for the +0.095; cite VO-A/B for the self-vs-far claim or table them.

**3. No manipulation check; Appendix B shows the same recommendation under both scaffolds (§3.1, §4.1, §4.2b, Fig. 4 caption, abstract, App. B, §5.2) — actual flaw (missing check), disclosed only in §5.2.** The enactment check verified that a clause is *held*, not that the two clauses produce different advice. If App. B is typical, all 24 cells measured style-reading in both arms and "closing the leak removes the signal" is not the causal mediation story the abstract and Fig. 4 tell (R6, R3, R1). SEVERITY: major, not fatal (R6's ruling; the spine, §4.3 plus "compare before you interpret", stands). DISPOSITION: disclose today in the abstract sentence, Fig. 4 caption, and Limitations; a keyword-free recommendation-agreement count needs an LLM pass and is future work (or a Tier-C manual sample).

**4. VO-D floor and winner's curse (§3.5, §4.2b, §4.4c, §4.4 last paragraph, A7, Table 1 vs Table 3) — actual flaw in wording, limitation in substance.** Pilot D = 0.325 on 80 items was treated as "below chance, no cue"; main D = 0.551/0.536, above every LM cell. "On VO-D, where no cue exists" is false; the leakage axis is 0.54→0.85. Regression to the mean on a noisy selection statistic. SEVERITY: major for the sentence, moderate for the null (the arm was uninformative anyway, §5.2). DISPOSITION: fix today (one sentence in §4.4 + Limitations; delete "no cue"; delete "below chance" as evidence).

**5. "Four independent stimulus designs" on one 200-prompt pool; §3.5 "resampled independently" mis-stated (§1 contribution 3, §3.5, §4.4, Table 5 diff CI) — actual flaw in description, moderate in numbers.** All four sets share the identical 200 prompt ids and the same three predictors; VO-D/E share clauses. Effective independent units are ~200 prompts. Table 5's difference CI should resample prompts jointly across sets. SEVERITY: major (credibility trap; R1's, R4's and R6's −5 trigger). DISPOSITION: fix today — "four clause pairs on one 200-prompt pool"; re-run the cross-set bootstrap jointly (local, no API); A9.

**6. Gate under-validated (§3.4, §5.3, tools/surface_leakage_gate.py) — limitation over-sold as contribution.** `passed = acc <= 0.58` will be read as "clean" though it says nothing about lexical/argumentative leakage; features are the manipulation targets (circular on VO-D); threshold arbitrary; no external validation; n = 80 output is noise. SEVERITY: moderate (major for the "field default" claim). DISPOSITION: soften "recommend as reporting defaults" to "propose"; docstring/rename `passed`; add minimum-n; state "necessary, not sufficient"; validation is future work.

**7. Additivity and identifiability of the 2×2 (§3.3, §4.4) — limitation, undisclosed.** When columns differ in difficulty a weaker classifier gains less and the interaction records that as "self-advantage"; the interaction cancels only column-independent capability, and stylistic self-similarity is itself a predictor × column interaction — so the design cannot identify privileged access from style self-similarity even in principle (R1, R3). SEVERITY: moderate. DISPOSITION: disclose in one Limitations paragraph; it strengthens the case for the gate.

**8. Multiple contrasts and post-hoc decomposition (§4.4, Table 5) — limitation.** ~12 reported intervals; the single significant −0.033 is unremarkable and should not be narrated as a self-*disadvantage*; the F decomposition should be labelled post hoc. SEVERITY: moderate. DISPOSITION: disclose in one clause each.

**9. Undisclosed P4 step-down and SESOI mismatch (§4.4c, 02_design_audit.md) — actual flaw (prereg deviation unreported).** P4 target 1,000/cell, floor 500; ran ~400. §4.4c cites a 5 pp SESOI where the prereg says 8 pp for the interaction below 1,000/cell (R4). SEVERITY: moderate. DISPOSITION: disclose in Limitations today, one line each.

**10. Amendment provenance, sign-off and contribution wording (02 A1–A8 "proposed by Claude Code, awaiting Jaswin's confirmation"; Author Contributions vs A1; LLM Usage Statement) — actual gap, judge-perception risk for sprint, major for Fellowship.** R5 downgraded from "major" to "must close today" after noting P1–P15 are signed by name. SEVERITY: moderate (major for Fellowship). DISPOSITION: fix today — sign A1–A8 with names/dates; one sentence in the LLM statement on who proposed and who decided A4/A8; align "designed … the five persona pairs" with "drafted in Claude Code, human-screened".

**11. Welfare over-reach in §1 ¶2 — actual flaw in a load-bearing sentence.** "If a model's report … carries no epistemic advantage … those methods are measuring something other than what they claim" is false: privileged access is sufficient, not necessary, for reliability (R3). SEVERITY: moderate. DISPOSITION: fix today ("cannot be shown to add information beyond what an observer already has").

**12. "Fully explained by style-reading" (Limitations, over-attribution paragraph) — actual flaw (over-claim).** r = +0.71 and a scaffold that removed everyone's signal is not full mediation. SEVERITY: moderate. DISPOSITION: fix today ("tracked by / not separable from").

**13. Construct validity (§3.1, §1, App. C) — limitation and perception risk.** The hidden property is a property of the *prompt*; every predictor is a third-person text classifier; fresh-session self-prediction is self-modelling, not Lindsey-sense introspection; welfare relevance is by analogy (R3, R6). Track 3 fit rests on §4.3 and on "methods of self-report". SEVERITY: moderate. DISPOSITION: disclose in one §1 sentence; relabel "self-modelling" where "introspection" appears.

**14. Length vs rubric — judge-perception risk bordering on actual flaw.** 10,641 words (~18–20 template pages) against "most strong projects are 4 to 8 pages" and a Presentation-2 descriptor that says "diluted by excessive length"; even the condensed variant is ~14 pages. SEVERITY: major for Presentation. DISPOSITION: fix today.

**15. §4 ordering confession — presentation flaw.** "Sections appear in the order the work was done; the argument reads most naturally as 1 → 2 → 3" is a confession that the structure fights the argument. SEVERITY: moderate. DISPOSITION: reorder to §4.2 → §4.4 → §4.3 (or delete the sentence and renumber the "three results" to match the order).

**16. r = +0.71 is a two-cluster correlation (§4.2a, Fig. 1, five-line table row 4, abstract) — limitation.** Scaffold type correlates ~0.79 with Self and ~0.71 with D; within originals r ≈ 0.51 (n = 6); within equalised ≈ 0.22 (n = 4); VO-D/E near-duplicates. SEVERITY: moderate. DISPOSITION: disclose ("tracks across scaffolds").

**17. Target ended up the weakest classifier (§4.4b, App. I) — limitation.** Appendix I says making the weaker model the target "biases toward the null"; M is the weakest of three. SEVERITY: moderate. DISPOSITION: disclose that the ladder chose M before capability was known and that this is why F is load-bearing.

**18. Prompt-artefact reading of the probe (App. C) — limitation.** "One is the reply you would produce; the other is from a different model" invites a "which is more assistant-like" judgement; the length analysis partly addresses this. SEVERITY: minor–moderate. DISPOSITION: disclose in the self-preference sentence.

**19. Unregistered post-hoc analyses (all of the above) — credibility risk if unlogged.** Every new number added today is an unregistered analysis on the same data in a paper whose brand is preregistration (R5). DISPOSITION: one A9 row in 02_design_audit.md, dated today, "post hoc, exploratory, prompted by review", signed by both authors, and cited from §4.3.

**20. Minor hygiene (all fix today).** Fig. 3 annotation reportedly reads "answered 'A' on 90%" while the caption/text say 89.7% (R2); slide 1 "asked to pick out their own writing" describes the failed recognition framing; slide 6 "answers by position" vs reliably negative discrimination; Figure 2/3/4 built from `fig3_*`, `fig4_*`, `fig2_*` files; Table 2's caption correctly says 387 (M) / 391 (N) but §1 and §6 say only "391 items" — say "391 (Hermes) / 387 (Llama)" wherever both are compared; abstract currently ~145 words, so any edit must stay ≤150; curse-of-knowledge terms ("the band", "far-self swap", "Level 3", "SESOI") before definition; ⟦FILL⟧ affiliations and GitHub URL; references marked ⟦VERIFY⟧ (currently four, all with arXiv ids — verify Lindsey's arXiv id and venue line).

**Not valid as stated:** R6's "the design cannot produce a positive" — partly retracted; the band (Self 60–80%, D ≤ 0.58) is precisely the positive region and the crossed 2×2 on gate-passing stimuli could return Self > sibling ≈ F. What survives is the one-directional `passed` semantics (item 6). Also not valid: R1's/R4's Round-1 "explained by length / shared preference" (item 1). Also over-weighted: "one lineage" as a sprint criticism.

## 5. Consolidated scorecard

| # | Dimension | /10 | Justification |
|---|---|---|---|
| 1 | Importance of question | 7 | Privileged self-access is the right question for Track 3 and for welfare methodology; the persona property is not a state, which caps it. |
| 2 | Novelty | 5 | Operationalisation of a known confound; the crossed 2×2 + neutral F on a verified same-base pair, and the (unreported) length-beats-model line, are the only new elements. |
| 3 | Conceptual clarity | 7 | "Self-prediction ≠ privileged access" is crisp and repeatable; undercut by estimand switching and undefined jargon. |
| 4 | Experimental design | 6 | Preregistration, capability control, grouped CV, leakage manipulation; but no cross cell on the probe, no manipulation check, gate features = manipulation targets, target weakest. |
| 5 | Statistical/inferential rigor | 6 | Prompt-clustered inference and response-bias hygiene are real; missing preregistered CI, no test on the headline, mis-stated resampling, post-hoc decomposition, M-only estimand. |
| 6 | Quality of evidence | 5 | One lineage, one values dimension, one probe; clean arm uninformative; the positive is one uncontrolled cell. |
| 7 | Robustness | 5 | VO-E and response-bias checks help; "four designs" is one prompt pool; nothing generalises beyond the lineage. |
| 8 | Reproducibility | 8 | Append-only logs, hashes, frozen prompts, 38 tests, $3.12; minus missing URL and unverifiable seeds (texts are the artefact). |
| 9 | Reusable contribution | 6 | `gate()`/`response_bias()` are adoptable as reporting habits; under-validated and mislabelled `passed`. |
| 10 | Communication | 5 | Best hook in the field; 2.5× rubric length, ordering confession, memorable result ≠ strongest evidence, figure/file seams. |
| 11 | Track relevance | 6 | Self-report reliability, yes; persona attribution is not introspection of states, and the fit rests on §4.3. |
| 12 | Fellowship potential | 6 | Temperament, auditability and an open-weight pair are real assets; object thin, provenance open, trajectory not yet a design that can come out positive. |

**Strict scientific score: 56 as submitted → 62 if Tier S done.** Weighting: design, rigor, evidence, robustness (4–7) carry ~60%; clarity and novelty ~20%; reproducibility ~10%; the rest ~10%. Tier S raises rigor and clarity (CIs, tested comparator, honest estimands) but cannot add a lineage, a manipulation check, or a cross cell, so the ceiling today is low-60s.

**Sprint judge score: 59 → 67.** Weighting follows the rubric's three roughly equal axes: Innovation (dims 2, 1, 11) is fixed at rubric-3 regardless; Execution (4, 5, 6, 8) is already a defensible 4 and becomes a firm 4 with the CIs and honest wording; Presentation (10, 3) is the lever — cutting to rubric length and reordering moves it from 2–3 to 4, and that is worth more than any analysis. The +8 assumes the cut actually happens; if the disclosures are absorbed without cutting, the score falls, not rises (R2).

**Fellowship investment score: 58 → 64.** Weighting: dimension 12 and the evidence behind it (auditability, temperament, self-correction under preregistration) ~40%; reusable contribution and reproducibility ~20%; importance and trajectory quality ~25%; novelty ~15%. The move to 64 requires the A9 row, signed A1–A8, the provenance sentence, and one concrete next-experiment sentence in §5.4; the science alone does not move this score.

## 6. Comparison to past winners

Caveat first: the six reference winners are 2024 Apart submissions from other tracks under a different rubric; none was judged on "variance and baselines" or required an ethics appendix. What transfers is the judging psychology (one sharp hook, closed loop, artifact, honest limitations, 4–8 pages); what does not is their tolerance for zero measurement (w2/w3/w4 would score 1–2 on today's Execution axis).

1. **What winners do better:** state one mechanism in the first paragraph and stop (noise reveals sandbagging; agent goal-drift; unlearning is jailbreakable); 4–7 body pages; a demo moment a judge can click or watch; a positive or *vivid* result. This report states its mechanism and then qualifies it for 10,000 words.
2. **What this project does better:** everything the current rubric's Execution axis names and none of the winners had — baselines, clustered variance, preregistration with dated amendments, ground-truth-by-construction, the required ethics/causal-link appendix, cost record, released tested code. It also has a better hook than any of them ("a model can predict itself — and so can a regression").
3. **Missing winner characteristic:** the demo moment and the single unmissable figure. `surface_leakage_gate.py` is a numpy file, not a demo; Fig. 1 is close, and the length-rule bar (0.719 vs 0.809 vs 0.831) would make it unmissable. Also missing: a *surprising* finding — "models read style" surprises nobody on this panel.
4. **Overvaluing rigor relative to novelty?** Yes, in narration: six discarded designs, eleven appendices, five restatements of one distinction. The rubric's Innovation axis asks "is this actually new?" and will answer 3 however well the null is executed. The rigor is right to *have*; it is wrong to *narrate at this length*.
5. **Undervaluing rigor because the result is negative?** No. The panel did not penalise the null and neither should judges (w5 and w6 won on negative stories). What is being penalised is not the sign but the framing: the memorable claim is the least controlled, and the "no positive" sentence is scoped wider than the data.
6. **Single change most increasing chance of winning:** cut to rubric length in 1→2→3 order with the length-rule row folded in — Presentation 2–3 → 4 and a sharper hook in one move.
7. **Single change most increasing chance of Fellowship selection:** report the confound against your own headline today, logged as A9 and signed by both authors, and name the next experiment the data already contain (self-preference vs self-prediction dissociation). Selectors fund people who audit themselves before they are asked and who can point to a design that can come out positive.

## 7. Fellowship assessment

**Probability ranges (panel spread; my central band in bold).** Win the sprint: 10–30% (**15–25%**). Considered for Fellowship: 25–55% (**35–50%**). Actually selected: 8–30% (**12–22%**). Remembered by organisers even if not winning: 45–75% (**55–70%**; the title, the $3.12, and the amendment reversal travel).

**Why would Apart want to spend months helping this team?** Because they behave like preregistering scientists under 48-hour pressure and the record shows it: stop rules written before running and fired when triggered; a Level-3 branch taken and reversed on the record; two artefact "nulls" caught by inspecting answer distributions rather than published; a mispredicted primary contrast reported as found; a pipeline with budget guard, provider pinning and label isolation enforced by tests; and data auditable enough that four independent reviewers recovered the same confound from the checkpoints in an hour — which is what a mentor needs to be able to do. They also hold an open-weight same-base pair, which is exactly what an activation-grounded continuation requires.

**What would make an organiser think this is not worth continued mentorship?** If the pivotal decisions turn out to have been made by the tooling and ratified (02 still logs A4/A5/A7/A8 as "proposed by Claude Code, awaiting confirmation"); if the team keeps framing a single self cell as "genuine self-prediction" after writing a paper whose lesson is that single self cells are uninterpretable; if the proposed programme is "more lineages, more sibling types" — the same null with more rows and no design that could come out positive; and if the substantive object stays persona style, which yields nulls Song et al. already predicted and nothing a welfare programme can use.

**Strongest Fellowship narrative (team's voice).** "We took the number a self-report study would publish as introspection — a 70B model predicting its own reply 72% of the time — and showed, on the same items, that a word count does it 81% and an 18-feature regression 83%. Then we reported the number that cuts against us: the model still beats chance where the word count cannot, so something model-specific is there. We do not know yet whether that residual is self-preference or self-prediction, and we know how to find out: ask the same model 'which is better' and 'which is yours' on the same pairs, on stimuli where the hidden property demonstrably changes behaviour and a stylometer demonstrably cannot read it. We built the gate that checks the second condition, we preregistered and audited every step for $3.12, and we hold an open-weight pair on which the property can be planted by steering rather than prompted. Fund the six months in which this becomes a positive test rather than a null."

**The team's proposed trajectory** (Phase 1 replicate across lineages; Phase 2 vary training relationship; Phase 3 gate + response-bias + capability control → behavioural introspection benchmark, retrospectively applied). Panel: R1 "too broad, insufficiently novel; Phase 3 the only exciting piece"; R2 "Phases 1–2 incremental, Phase 3 exactly right — lead with it"; R3 "too broad and insufficiently welfare-relevant"; R4 "Phase 3 the right centre, Phase 1 too broad; missing controls first"; R5 "too broad, Phase 3 premature as a benchmark; audit first"; R6 "Phase 1 dull, Phase 2 should lead, Phase 3 premature". My position: **too broad and, as written, cannot produce a positive.** Phase 1 is more nulls; Phase 2 is the interesting axis but only after there is a property with behavioural expression to vary it on; Phase 3's "benchmark" is premature for an unvalidated 18-feature gate, but its retrospective-audit half is the cheapest, most citeable first deliverable.

**Better trajectory (panel convergence).** Months 1–2: retrospective audit — run the gate, response-bias check and (where possible) a capability control on 3–5 published behavioural self-prediction results; publish "how much survives an 18-feature classifier". Months 2–4: R6's dissociation — same model, same pairs, "which is better" vs "which is yours" — on one property built with a verified behavioural manipulation check (recommendations differ) and D ≈ chance; that is the first design that could return a positive handle. Months 4–6: R3's ground truth — plant hidden properties by activation steering on the open-weight Llama so leakage is measurable and the property is genuinely internal; and R3's incremental-validity test of *state* self-reports (preference, aversion, refusal reasons) against a stylometer on the same transcript. Training-relationship ladder (same checkpoint / sibling / PEFT / full FT / unrelated) only where a survivor exists. Dissent, preserved: R2 would gate everything on the audit's survivors (R5: hostage to others' data); R6 would put the manipulation-checked property before the audit; R3 would drop persona entirely for states. I side with R5's ordering because the audit is the only piece guaranteed to produce a paper.

## 8. Remaining-time action plan (TODAY only)

**Ruling on new API calls:** none are recommended. R1's ~800-call Mistral third-party observer and R4's ~400-call "which reply is Hermes-3's?" F judge are the correct equal-cost observers in principle, but they need an A9 row before running, interpretation time after, and they can cut either way with no time to absorb it; the length rule and own-shorter analyses already give a tested cost comparator from existing data. They are Tier C: only if every S and A item is done, the pipeline is already scripted, it runs unattended in under an hour, and the A9 row is written before the first call. **Every new analysis today, API or local, gets one A9 row** in 02_design_audit.md ("post hoc, exploratory, prompted by review", dated, both authors) and is cited from the section it lands in.

**Tier S (do first, in this order)**
1. **Length-rule + CIs into §4.3/Table 2** — add row "Length rule (choose longer): 0.809 [0.769, 0.846]"; CIs on Hermes 0.719 [0.676, 0.760], +0.437 [+0.351, +0.519]; Llama −0.107 [−0.168, −0.046]; one clause "0.653 [0.539, 0.763] when its own text is shorter (n = 75)"; one sentence naming self-preference (Panickssery et al. 2024) as the untested alternative; one clause per R4 that the rule presumes knowing which model is verbose, so it sits beside D. Reword "genuinely" and "shows none". Effort 1–1.5 h. Sprint ++ (turns the title into a tested claim), Fellowship ++ (self-audit), risk low if reported as sharpening the thesis; risk high if omitted (a judge with the checkpoints finds it).
2. **Estimand wording** — abstract (stay ≤150 words), five-line table row 3, §1 contribution 3, §4.4: "no positive raw self-advantage for target M; the interaction is +0.089 on VO-C, diagnosed post hoc via F"; one sentence for the F-referenced +0.094 and the interaction-based leakage contrast ≈ +0.095; cite VO-A/B for "beaten on its own text" or state VO-C is n.s. Effort 45 min. Sprint +, Fellowship ++, risk none.
3. **Cut to rubric length** — target ≤8 template pages (≈4,500–5,500 words body): §4 in 1→2→3 order (delete the ordering sentence); Tables 4–5, App. I–K, verification detail, one of the two "not privileged" restatements, and all McNemar/bootstrap method detail to a supplement; keep A4 in one paragraph. Fold in only what sharpens (S1, S2 one-liners); every other disclosure in one clause or in the supplement (R2's trade-off, stated explicitly: each hedge lengthens, and the rubric punishes dilution). Effort 2.5–3 h. Sprint ++ (Presentation 2–3 → 4), Fellowship neutral-positive, risk moderate if rushed — keep the full version as the supplement so nothing is lost.
4. **A9 row + sign A1–A8** in 02_design_audit.md; one provenance sentence in the LLM Usage Statement (who proposed, who decided A4/A8); align Author Contributions with A1 ("drafted in Claude Code, human-screened; J.C. specified and selected"). Effort 25 min. Sprint neutral, Fellowship ++, risk none.

**Tier A**
5. VO-D reconciliation: delete "where no cue exists"; one sentence in §4.4 and Limitations (pilot 0.325 on 80 items → main 0.551/0.536; leakage axis 0.54→0.85; selection on a noisy statistic). 20 min. Sprint +, risk none.
6. "Four independent stimulus designs" → "four clause pairs on one 200-prompt pool" throughout; fix §3.5 resampling sentence; re-run Table 5 difference CI resampling prompts jointly across sets (local numpy). 1 h. Risk none; leaving it is a credibility trap.
7. Manipulation-check disclosure: one sentence in the abstract, Fig. 4 caption ("the equalising scaffold, which also converged the personas' recommendations in the worked example, drives both to chance"), and Limitations. 20 min. Slightly weakens the causal claim, correctly.
8. Soften "fully explained by style-reading" → "tracked by / not separable from"; fix §1 ¶2 epistemic-advantage sentence; add one §1 sentence that the persona is an instructed disposition and the test is self-modelling, not state introspection. 25 min.
9. Gate wording: "recommend as reporting defaults" → "propose"; docstring/rename `passed`; "necessary, not sufficient"; minimum-n note. 30 min. Sprint +, Fellowship +.
10. Disclose P4 step-down (~400/cell vs floor 500) and SESOI 8 pp vs 5 pp; note target M weakest classifier and why F is load-bearing; label the F decomposition post hoc; one clause on ~12 intervals. 30 min.
11. §5.4: replace the generic three phases with two concrete sentences — next experiment is the self-preference vs self-prediction dissociation on the probe already run, on a property with a behavioural manipulation check; then the retrospective audit; name the open-weight pair as the asset. 20 min. Fellowship ++.

**Tier B**
12. Slides/video: slide 1 lede → "asked which reply you would produce"; slide 6 → "reliably prefers Hermes's text" not "answers by position"; add one bar triple (0.719 / 0.809 / 0.831) as the final-slide image; 15-second terminal clip of `gate()` on VO-C vs VO-D (the demo moment); final minute = the line in §9. 45 min. Sprint +.
13. Fig. 3 label 89.7%; figure/file renumbering; "391 (Hermes) / 387 (Llama)" wherever both are compared; define "band", "far-self swap", "SESOI" on first use. 30 min.
14. Optional local analyses for the supplement only: per-item McNemar D vs Hermes on the 391 shared items; F-referenced interaction table; VO-A/B self-vs-far contrasts tabulated; two-cluster note on r = +0.71 (partial r ≈ 0.35). 1–1.5 h. Sprint neutral, Fellowship +.
15. Hygiene: affiliations, GitHub URL, verify the four references (Lindsey arXiv id/venue line especially), abstract word count ≤150, keep the "Author lists checked" line only if actually re-checked. 20 min.

**Tier C (do not spend time on)**
- New API calls (R1's Mistral observer, R4's F judge, any few-shot variant) — see ruling above.
- A pairwise feature-difference classifier (R2's Round-1 ask): the length rule answers the cost objection more cheaply; leave as future work.
- A keyword-free recommendation-agreement count (needs an LLM pass) — state the App. B observation; count later.
- Adding paragraphs on additivity, incremental validity, or Panickssery beyond one sentence each — R2's rule: disclosure lengthens.
- Polishing Appendix I "six discarded designs" — move it out of the body and stop.
- Re-litigating the −0.033 narrative — one clause, done.

## 9. Final blunt selection verdict

"If I were an Apart selector looking at this project today, I would: **borderline, leaning select** — and **lean select** by tonight if Tier S lands." Panel distribution: R1 borderline-leaning-select, R2 lean select, R3 lean select, R4 borderline/lean select, R5 lean select, R6 borderline-leaning-select. My ruling sits with R1/R4/R6 on the file as it stands this minute and with R2/R3/R5 on the file the team can have by midnight, because every gap between the two is closable from existing data.

Why: the team asked the right question, ran it cleanly, preregistered it, and refused to over-read three of its own results — that is the behaviour a Fellowship should buy and none of the reference winners showed it. But the memorable number is a single uncontrolled cell that a word count beats, presented as "genuine self-prediction" without the interval its own amendment promised; the headline "no positive self-advantage" is achieved by choosing among estimands the paper itself defines; the "clean" arm was never clean and may never have carried the property; "four independent designs" is one prompt pool; and the report is 2.5× the recommended length with a confession that its own order fights its argument. A hostile Q&A finds each of these in five minutes. Nothing here penalises the null — the null is fine — and nothing here credits honesty as evidence; the credit is for auditability, which is what let six strangers recompute the same confound in an hour. Fix the wording, add the rows, cut the body, sign the amendments, and this is the best-executed submission in the track with a defensible Execution 4, an Innovation 3, and a Presentation 4. Leave it, and a rigor-minded judge finds the confound before the team's own concession does.

**The ONE thing to communicate in the final minute of the video:** "A 70B model predicted which reply it would write 72% of the time — and on the same items a word count did it 81% and an 18-feature regression 83%. We ran that check against our own headline before anyone asked, and we are releasing the file that runs it. Before the field calls a self-report evidence of self-knowledge, run the regression." It beats the alternatives because it carries, in three sentences, the tested number (not the untested 0.719-vs-0.831), the reusable artifact, and the temperament evidence selectors actually fund — self-audit before challenge; R1's interaction line is true but inside-baseball, R6's and R3's lack the tool and the "we ran it on ourselves", and R2's omits the self-audit. Say it in the team's voice, then stop.
