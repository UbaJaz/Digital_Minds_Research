# 03 — Design Review and Implementation Plan

## Purpose

This document records an independent review of the project as it stood on 2026-08-15 (after Phase 1A/1B, before any code), and turns that review into (a) a set of decisions for the team/council to make and (b) a concrete implementation plan for whoever builds the pipeline.

It reads `01_literature_grounding.md`, `02_design_audit.md`, the source-of-truth strategy docx, and the three pasted planning chats (`message.txt`, `message (1).txt`, `message_claude.txt`).

**Status of this document:** review + proposal. Nothing here is locked. Where a recommendation would change a decision that `02_design_audit.md` marks as locked, that is flagged explicitly — the research design remains authoritative until the team updates `02` deliberately.

> **Post-council addendum (2026-08-15, after `notes/council-transcript-2026-08-15.md`).** The council reviewed Sections 2, 3.1, 3.2, 3.4 and 5. Two recommendations in this document are **superseded** and must not be implemented as written:
> - §2.4 "Fix B now, Fix A as stretch" → overturned unanimously. **Fix A (crossed 2×2) is the primary pre-registered design**, with Fix B's tier-matched same-lineage pair as the model-selection rule inside it, and the M-row design (M→M, N→M, F→M) as the pre-registered fallback. Run the M-row cells first so the fallback is always complete.
> - §2.3 "make the weaker model the Target" → dropped (biases toward the null; fatal for an equivalence claim).
>
> Additions the council made that are now part of the plan: Fallback rewritten as a 3-level ladder (the old collapse reintroduced the confound); Baseline D fit per target column; both personas generated from every source prompt and bootstrap resampled by prompt; n = 500/cell target, 300 floor, SESOI 5 pp (simple) / 8 pp (interaction); values-ordering persona, generator identity withheld from predictors; joint band Self 60–80 % AND D ≤ 58 % per column on ≥ 80 items; provider pinning is a validity condition; project budget guard $7.50 with n stepping 500→400→300; Locked #1 reworded (N→N is a control cell, not a new predictor). Paste-ready `02` wording is in transcript Part 4 "Decisions for 02_design_audit.md". Section 6 below is to be read with these changes applied; `02_design_audit.md` remains authoritative once updated.

**How to use this document:**
1. Section 1 — overall assessment (context only).
2. Section 2 — the main methodological problem and two candidate fixes. **This is the primary question for the council.**
3. Section 3 — secondary points, each with a concrete proposal.
4. Section 4 — repo hygiene (no council needed; just do it).
5. Section 5 — questions for the council, stated crisply.
6. Section 6 — implementation plan for the builder, gated on Section 5 answers.
7. Section 7 — hard constraints the builder must respect regardless of council outcome.

---

## 1. Overall Assessment

**Strengths (keep these):**
- Literature grounding cleanly separates "what the paper established" from "what we are extrapolating."
- Design already fixed the obvious reviewer attacks: three-point regression → pairwise comparisons; assumed similarity → measured similarity; baseline D kept off the similarity axis; same-weights vs. same-episode distinction moved to the abstract; fallback predetermined.
- Discipline about not coding before the design is locked is correct in spirit.

**Weaknesses (addressed below):**
- One unaddressed confound (Section 2) that a hostile reviewer would go to first.
- The design is likely underpowered for the effect sizes that are plausible in a prompting-only setting (3.1).
- The $10 budget is being treated as the binding constraint; it isn't — wall-clock time and zero code are (3.2).
- The move to OpenRouter as the sole provider changes the reproducibility requirements and makes the existing verification checklists partly obsolete (3.3).
- Minor repo hygiene issues, one of which is a live secret-leak risk (Section 4).

---

## 2. Main Problem — Self vs. Near-Self Is Confounded With Capability

### 2.1 The problem

Every candidate configuration in `message.txt` places the **most capable / most expensive model as the Target** and a smaller, cheaper model as Near-Self:

| Config | Target | Near-Self | Approx. price gap |
|---|---|---|---|
| 1 | GPT-5.6 Terra | GPT-5.6 Luna | ~10× |
| 2 | Gemini 3.6 Flash | Gemini 3.5 Flash-Lite | ~5× |
| 3 | Claude Sonnet 5 | Claude Haiku 4.5 | ~2–3× |

The Self condition is therefore "the big model classifies its own outputs" and the Near-Self condition is "a small model classifies the big model's outputs." If Self > Near-Self, two explanations are indistinguishable:

1. **Same weights** → the model is unusually well-fit to its own output distribution (the hypothesis under test, H_privileged).
2. **Capability** → the Target is simply a better text classifier than Near-Self, and would beat Near-Self at classifying *anyone's* outputs.

Nothing in the current design separates these. The calibration probe does not help: it measures *agreement* on subjective judgments (similarity), not *classification ability*. The strategy doc's own §2.4 logic — "a proxy, not a measurement" — applies here in full.

Note this cuts both ways: if Self ≈ Near-Self, a real same-weights effect could be masked by the Near-Self model being worse at the task in general — but the confound is asymmetric in the direction that matters, because in all three configs any positive Self result is contaminated.

### 2.2 Fix A — Crossed (2×2) design

Each predictor predicts outputs from *each* target. With Target M and Near-Self N:

| | predicts M's outputs | predicts N's outputs |
|---|---|---|
| **M predicts** | M→M (self) | M→N (cross) |
| **N predicts** | N→M (cross) | N→N (self) |

Self-advantage becomes the interaction: `(M→M − N→M) − (M→N − N→N)`. Any "M is just smarter" effect appears equally in M→M and M→N and cancels. This is structurally what Binder et al. and Song et al. do.

Far-Self F is added as a predictor on both targets (F→M, F→N), giving a 2 targets × 3 predictors = 6-cell design. Full 3×3 (F also as a target) is a stretch, not required.

- **Pros:** the strongest control; directly answers the confound; the same-weights hypothesis is tested twice (M→M and N→N).
- **Cons:** changes the locked design in `02` ("one target model", "three pre-registered pairwise comparisons"). Requires restating the pre-registered comparisons as interaction contrasts. Two targets are used as a *control*, not pooled to manufacture regression points — but this must be argued explicitly because `02` forbids pooling. Doubles generation and prediction call counts (still well under budget — see 3.2). Requires persona pair to be feasible for both M and N, so the pilot must run on both.
- **Analysis:** item-level paired bootstrap on the interaction; also report the four cell accuracies with CIs and the two simple contrasts (M→M vs N→M; N→N vs M→N).

### 2.3 Fix B — Tier-matched Near-Self

Keep the design in `02` exactly as locked, but choose a Near-Self that is the **same lineage at the same capability tier**, so capability is held roughly constant and only "same weights vs. sibling weights" varies. Candidate types (availability on OpenRouter is **unverified** — must be checked by an actual API call before selection):

- Two dated snapshots of the same closed model (e.g. `<model>-2026-03-xx` vs `<model>-2026-06-xx`).
- Open-weight base with two different post-trainings (e.g. `Llama-3.x-70B-Instruct` vs a community fine-tune of the same base such as a Hermes/Nous variant; or `Qwen2.5-72B-Instruct` vs a fine-tune of it).
- Same family, same size, adjacent generation.

These correspond to Song, Hu & Mahowald's "same-seed / base-instruct variant" feature-similarity categories, which is a much more literal "near-self" than "same company, different size."

If a tier gap is unavoidable, make the **Target the weaker model** so any self-advantage found is conservative (the self model won *despite* being the weaker classifier).

- **Pros:** preserves every locked decision in `02`; cheapest; simplest analysis; no change to pre-registered comparisons.
- **Cons:** capability is *approximately* matched, not controlled — a reviewer can still ask "how do you know they're equally good at this task?" A partial answer: report each model's accuracy on the calibration probe or on a small labelled classification sanity set. Also depends on OpenRouter actually offering a suitable pair.

### 2.4 Reviewer's recommendation (for the council to accept, modify, or reject)

Do **Fix B as the primary change** (it preserves the locked design and costs nothing), and **add the reverse cell (N→N and M→N) as a pre-registered stretch** if the pilot shows the persona task is feasible on N as well as M. That gives the crossed control if time allows, without betting the sprint on a design change. If the council prefers Fix A outright, `02_design_audit.md` must be updated to reflect the new pre-registered contrasts *before* any main-experiment code runs.

---

## 3. Secondary Points

### 3.1 Statistical power — expect a "clean null," design the write-up for it

At n = 300 per condition and accuracy near 65%:
- SE of one condition's accuracy ≈ √(0.65·0.35/300) ≈ 2.8 pp
- SE of a difference between two independent conditions ≈ 3.9 pp → 95% CI ≈ ±7.6 pp
- Item-level pairing (all predictors see identical items) reduces this somewhat, but not below ~±5–6 pp.

Binder et al.'s finetuned self-advantage was on the order of +15–17 pp on simple tasks; a prompting-only effect, if any, is almost certainly smaller. The most likely outcome is a CI that includes zero. That is a legitimate, publishable-at-workshop-level result *if the design is clean* — which is exactly why Section 2 matters: a null under a confounded design is uninformative, a null under a controlled design is the contribution.

**Proposals:**
- Keep 300/condition as the floor, not the target; go higher (400–500) if the budget check in 3.2 allows, since calls are cheap.
- Pre-register the analysis as **paired**: item-level bootstrap on accuracy differences, plus McNemar's test as a secondary check. `message (1).txt` already flags this for the calibration probe; apply it to the main experiment too.
- Pre-register the smallest effect size of interest (e.g. 5 pp) so a null can be stated as "we can rule out effects larger than X," not just "not significant."

### 3.2 Budget vs. time — $10 is not the binding constraint

Order-of-magnitude estimate (verify with actual token counts before locking):

| Stage | Calls | Tokens (in / out per call) | Cost @ $2/M in, $12/M out |
|---|---|---|---|
| Verification | ~10 | 50 / 5 | ≈ $0.00 |
| Calibration, 50 items × 3 models | 150 | 300 / 2 | ≈ $0.09 |
| Persona generation, 300 items × 1 target | 300 | 200 / 150 | ≈ $0.66 |
| Predictions, 3 LLM conditions × 300 | 900 | 500 / 2 | ≈ $0.92 |
| **Locked design total** | | | **≈ $1.7** |
| Crossed design (2 targets, 6 cells) | 600 gen + 1,800 pred | as above | ≈ $3.1 |
| Pilot + retries + malformed outputs | | | ≈ $0.5–1.0 |

Even the crossed design at the most expensive candidate pricing fits under $10 with headroom. Cheaper models (Luna-class, Flash-Lite-class, open-weight) cut this by 5–10×.

**The actual constraint is two people, three days, and no code yet.** Five planning docs and three "do not implement yet" instructions were right up to this point; past it, they become the risk. **Proposal:** time-box — calibration probe running and a 20-trial persona pilot done by end of Day 1, or the interpretation/writing time the strategy doc rightly protects gets squeezed anyway.

Still implement the hard budget guard in code (`PROJECT_BUDGET_USD = 10.00`, per-phase sub-budgets, refuse to call when exceeded) — cheap insurance, and it produces the cost record for the write-up.

### 3.3 OpenRouter changes the reproducibility story

The verification checklists in `message.txt` assume direct OpenAI / Google consoles. The project now has one provider: OpenRouter. Consequences:

- **Model availability must be checked against OpenRouter's model list**, not the vendors' pages. The candidate IDs (`gpt-5.6-terra`, `gemini-3.6-flash`, etc.) may or may not exist there under those names.
- **Pin the backend provider.** OpenRouter routes a given model ID to multiple hosting providers; open-weight models in particular may be served at different quantizations. Use `provider: { order: [...], allow_fallbacks: false }` and record the `provider` and exact `model` fields returned in every response. Without this, "the same model" can silently differ between runs.
- **Reasoning must be off** (or `effort: none` / equivalent) for the one-letter predictor calls; confirm the parameter name OpenRouter accepts per model and confirm no hidden reasoning tokens are billed.
- **Temperature 0 for predictors**, but note that persona *generation* needs non-zero temperature to produce varied outputs — record the seed/temperature per generated item.
- **Log everything per call:** request params, returned model ID, provider, token counts, cost, timestamp, and a hash of the prompt. This *is* the reproducibility record; start it in the first verification call.
- Verification calls cost cents; they have been deferred long enough. Do them.

### 3.4 Persona hidden property — state the mechanism plainly

Every predictor must be *told* the two candidate personas to make a forced choice, so all predictors receive identical information. The only self-specific channel is therefore "I know how *I* would enact persona X" — a same-weights fit to own output distribution. That is exactly the hypothesis in `02`, and it should be written that plainly in the pilot design and the abstract.

Design constraints for the persona pair (for Phase 1D):
- Differ in a semantic/dispositional property (e.g. risk-tolerance, epistemic caution, values ordering), not in register, length, or vocabulary — otherwise baseline D solves it and the similarity axis is moot.
- Same system-prompt scaffold, same length, same format instructions; only the persona clause differs.
- Pilot feasibility band (currently proposed 55–75% for Self; **not locked**) must be fixed before the pilot runs, and the pilot must run on Near-Self too if Fix A is adopted.
- Baseline D: a simple classifier on surface features (length, type-token ratio, sentiment, hedging-word rate) trained with cross-validation on the same items — reported separately, never on the similarity axis.

### 3.5 Calibration probe — small additions

- 50 items preferred over 30 (cost is negligible); freeze the item set and A/B randomisation before any model sees it.
- Analyse as paired against Target's labels; report `A_near`, `A_far`, `Δ`, each with bootstrap CI. Do not lock the "10 pp + non-overlapping CIs" rule; a paired bootstrap CI on Δ excluding zero is the cleaner criterion.
- Also report each model's own consistency (re-run a subset at temperature 0 to check determinism on OpenRouter's backend).

---

## 4. Repo Hygiene (do it; no decision needed)

| Item | Current state | Action |
|---|---|---|
| Secret-leak risk | `.env` holds `OPENROUTER_KEY`; **no `.gitignore` exists** | Add `.gitignore` covering `.env`, `__pycache__/`, `.venv/`, `data/raw/` if large, `*.pyc` |
| Pasted chat logs | `message.txt`, `message (1).txt`, `message_claude.txt` at repo root, untracked | Move to `notes/` (or fold the useful content — model configs, calibration design, budget table — into a `04_model_selection.md`); keep the numbered `NN_*.md` series as the research record |
| Tooling | No `requirements.txt` / `pyproject.toml`, no venv, no `src/` | Create as part of implementation (Section 6) |
| `CLAUDE.md` | One line about the OpenRouter key | Extend with: project purpose, "research design in `02` is authoritative — do not change without updating the doc", budget guard rule, never print secrets |
| Source of truth | `Track3_Strategy_Doc_Research_Focused.docx` is binary and undiffable | Optional: export a `.md` copy alongside so changes are reviewable; keep the docx as the original |

Track3_Strategy_Doc_Research_Focused.docx was a pre-project planning document and is not part of the public repository; see the final design audit and report for the executed study.

---

## 5. Questions for the Council

Answer these in order; later ones depend on earlier ones.

1. **Capability confound.** Fix A (crossed design), Fix B (tier-matched Near-Self), or B-now-A-as-stretch (reviewer's recommendation)? What does the answer imply for the locked "one target model" and "three pairwise comparisons" decisions in `02`?
2. **Target model choice under Fix B.** Given OpenRouter as sole provider, which lineage gives the most literal near-self pair (dated snapshots of one closed model vs. two post-trainings of one open-weight base)? What must be verified before choosing?
3. **Power.** Accept 300/condition as floor and raise if cheap? Pre-register a smallest effect of interest — what value?
4. **Time-boxing.** Is "calibration + 20-trial pilot running by end of Day 1" the right gate, given the strategy doc's allocation (~1/5 effort on code)?
5. **OpenRouter reproducibility.** Any objection to pinning provider / disabling fallbacks / logging per-call metadata as mandatory? Anything missing?
6. **Persona design.** Which dispositional dimension is most likely to land in the feasibility band while resisting surface detection?
7. **Anything the review missed.**

---

## 6. Implementation Plan (for the builder)

Gated: **do not start Phase C or later until Section 5 Q1–Q2 are answered and `02_design_audit.md` is updated to reflect them.** Phases A–B can start immediately.

### Phase A — Hygiene and scaffold (no API calls)
1. `.gitignore`; move chat logs to `notes/`; extend `CLAUDE.md`.
2. Python project: `pyproject.toml` or `requirements.txt` (`httpx` or `openai` SDK pointed at OpenRouter, `numpy`, `pandas`, `scipy`, `python-dotenv`), `.venv`.
3. Layout:
   ```
   src/selfpred/
     config.py          # budgets, model IDs, provider pins, seeds — single source of config
     client.py          # OpenRouter wrapper: pinned provider, reasoning off, retry policy,
                        #   per-call JSONL log (model, provider, tokens, cost, prompt hash),
                        #   hard budget guard (raises before the call if over budget)
     calibration/       # items.json (frozen), run.py, analyze.py
     personas/          # persona pair spec, generate.py (ground truth stored separately)
     predict/           # run.py — builds predictor prompts; NEVER sees labels
     baseline/          # surface-feature classifier (condition D)
     analysis/          # paired bootstrap, McNemar, cell accuracies, plots
   data/
     raw/               # JSONL per phase, append-only
     labels/            # ground truth, separate directory, never loaded by predict/
   notes/               # chat logs, scratch
   ```
4. Ground-truth separation enforced structurally: `predict/` imports nothing from `labels/`; a test asserts the predictor prompt contains no label token.

### Phase B — Verification (~10 calls, cents)
1. Pull OpenRouter model list; confirm candidate IDs exist; record exact IDs.
2. One "reply OK" call per candidate; record returned `model` + `provider`.
3. Confirm reasoning-off parameter is accepted and no reasoning tokens are billed.
4. Test the one-letter constrained prompt on each candidate; record malformed-output rate.
5. Write results to `data/raw/verification.jsonl` and a short `04_model_verification.md`.

### Phase C — Calibration probe (Phase 1C in `02`)
1. Generate and freeze 50 forced-choice items (subjective dimension unrelated to persona); freeze A/B randomisation.
2. Run all candidate predictors; paired analysis; report `A_near`, `A_far`, `Δ` with CIs.
3. Decide Target / Near / Far per the pre-declared rule.

### Phase D — Persona pilot (Phase 1D in `02`)
1. Feasibility band fixed and written down first.
2. Generate ~40 items per persona on Target (and Near if Fix A); run Self prediction; run baseline D.
3. GO / FALLBACK decision per `02`.

### Phase E — Freeze and main run
1. Update `02` → preregistration section: conditions, n, contrasts, analysis, effect of interest.
2. Run generation → predictions → baseline; budget guard active; logs append-only.
3. `analysis/` produces cell accuracies, paired bootstrap CIs, McNemar, calibration Δ, cost record.

### Phase F — Write-up
Same-weights vs. same-episode in the first paragraph; calibration result reported next to the main result; D reported separately; interpretation against Binder / Song; limitations including capability matching and OpenRouter routing.

---

## 7. Hard Constraints for the Builder

- The research design in `02_design_audit.md` and the strategy docx is authoritative. Any deviation is made by editing `02` first, then code — never the reverse.
- No experimental API calls until Phase B; no main-experiment calls until Phase E; budget guard is on for every call.
- No predictor, including Self, ever receives the hidden label — enforce in code, not by convention.
- Never print, log, or commit `OPENROUTER_KEY` or any secret.
- Freeze stimuli (calibration items, persona pair, feasibility band) before any model sees them; log the freeze commit hash.
- Every API response's returned model ID and provider are logged; provider fallbacks disabled.
