# CLAUDE.md — project working rules

## Project purpose

This repository is a 3-day, two-person AI research sprint (Digital Minds Sprint, Track 3) asking
whether a language model has *privileged self-access*: does it predict its own outputs better than an
equally-informed observer does, once the predictor's general classification ability is controlled?

The control is a **crossed 2×2**: each of M and N generates a column of texts, and M, N and F each
predict both columns, so any "M is simply the better classifier" effect appears in both of M's cells
and cancels in the interaction `(M→M − N→M) − (M→N − N→N)`.

The study's independent variable became **surface leakage**. A hidden property is only interesting
if the model recovers it from something an outside observer cannot cheaply read off the text, so a
surface-feature baseline (condition **D**, 18 structural features, no bag-of-words, CV grouped by
source prompt) is fit per target column. D is never a point on the similarity axis; it is the
operationalisation of Song et al.'s "equal-or-lower-cost third party."

**The experiments are complete.** The finding is a null on self-advantage replicated across four
stimulus sets, plus one positive self-*prediction* result (Hermes-3) that is beaten by stylometry.

## Authority

- **`10_report.md` is the single document that summarises the whole project** — hypothesis, method,
  all results, conclusion, limitations, cost. Hand this to anyone who needs the full picture.
  Re-derive any summary from it, not from the older docs, and not from `submission_report.md`.
- **`submission_report.md` is the judge-facing submission report**, derived from `10_report.md` and
  capped at 8 rendered pages. It is a *shorter view of the same record*, never a second source of
  truth: it may contain no number `10_report.md` does not.
- **`02_design_audit.md` is the authoritative research design / preregistration.** Rows P1–P15 were
  confirmed 2026-08-15, **before any main-experiment call**. Amendments **A1–A9** are recorded there
  with dates, reasons and outcomes, and were **confirmed by Jaswin Chinthala and Ubayd Hattas on
  2026-08-16, after the results were known**. **Confirmation is not preregistration** — never
  describe an amendment as preregistered. Each original status line ("proposed/drafted in Claude
  Code", "awaiting Jaswin's confirmation") is preserved beside its added Confirmation line; do not
  delete them. Load-bearing chronology: **A4 = post-pilot substitution of the primary estimand;
  A8 = the amendment introducing the self-prediction probe; A9 = post-hoc audit** (full record:
  `notes/A9_post_hoc_audit.md`; `notes/A9_DRAFT.md` is a superseded stub). A2 is a bug fix, no
  sign-off. **Two provenance items are still open** and must not be reconstructed: the `VO-D`/`VO-E`
  screening date and screener, and the reason for the sample-size step-down — see
  `notes/AUTHOR_CONFIRMATION_REQUIRED.md`. Change the design in `02` first, then the code — never
  the reverse. If you find yourself wanting to change a hypothesis, a condition, an n, or an
  analysis contract, stop and edit `02`.
- `03_design_review_and_implementation_plan.md` and `notes/council-transcript-2026-08-15.md` are the
  adversarial review that *produced* the crossed design. Their verdict has been applied to `02`;
  they are historical record now.
- `01`, `04`, `05`, `06`, `07`, `08`, `09` are phase records superseded by `10_report.md` for
  narrative purposes, but they remain the primary evidence for their own numbers.

## Budget guard

- Project ceiling: **$10.00** (hard; the entire experimental budget). **Spent: $3.1216.**
- Working guard: **$7.50** projected total. If a projection from verified per-token prices exceeds
  it, n steps down 500 → 400 → 300 rather than the design changing.
- Per-phase sub-budgets live in `src/selfpred/config.py` (`PHASE_BUDGETS_USD`) and nowhere else.
- Every API call goes through `client.py`. The guard projects the cost of a call *before* issuing it
  and raises `BudgetExceeded` rather than calling. Nothing else in the repo may make network calls.
  This still holds for any follow-up run.

## Secrets

**Never print, log, echo, or commit the contents of `.env` or the value of `OPENROUTER_KEY`.**
Load it with `python-dotenv` only. `client.py` redacts the key from exception messages and
tracebacks; keep it that way. `.env` is in `.gitignore` — do not un-ignore it.

## Where the logs live

- `data/raw/verification.jsonl` — every Phase B call (append-only). Tracked; it is the
  reproducibility record.
- `data/raw/<phase>.jsonl` — one append-only JSONL per later phase, same schema.
- Each record holds: timestamp, phase, requested model, returned model, pinned provider, returned
  provider, request params, prompt sha256, prompt/completion token counts, computed USD cost.
  It never holds the prompt text of a secret or the API key.
- `data/raw/openrouter_models.json` — raw provider model list (large; gitignored).
- `data/checkpoints/` — resumable run checkpoints, so an aborted run does not re-call completed items.
- `data/results/*.json` — computed analysis outputs (`main_two_set.json` holds all four sets'
  cell-level accuracies; `selfpred_corrected.json` the A8 self-prediction probe; also `calibration`,
  `pilot`, `pilot_analysis`, `screen`, `discrimination`, `selfrec`, `selfrec2`).
- `figures/fig1..fig4*.png` — the four report figures, regenerated by `scripts/make_figures.py`.

## Ground-truth separation

`src/selfpred/predict/` must not import from `src/selfpred/labels/`. A pytest asserts this, asserts
that a built predictor prompt contains no label token, and asserts persona option order is
counterbalanced and logged. No predictor — including Self — ever sees the hidden label.

## Current state (updated 2026-08-15, post-report — all experiments complete)

**Models (verified by API call, all DeepInfra fp8, provider pinned):** M = `meta-llama/llama-3.1-70b-instruct`,
N = `nousresearch/hermes-3-llama-3.1-70b` (two post-trainings of one pretrained base),
F = `mistralai/mistral-small-3.2-24b-instruct`. No far-self swap was triggered.

**Phases, in order run:**

- **B (verification) DONE** — `04_model_verification.md`, `06_hermes_smoke_test.md`. 311 calls across
  11 models; 311/311 honoured the provider pin; temperature-0 deterministic; 0% malformed on the
  real predictor template.
- **C (calibration) DONE** — `07_calibration_results.md`. A_near 0.660, A_far 0.638,
  Δ = +0.021 [−0.064, +0.106]. Rule satisfied on the point estimate, but the similarity axis is
  barely established and the report says so.
- **D (pilot) DONE — gate outcome LEVEL 3** — `08_pilot_results.md`, `09_pilot_finding.md`.
  All persona pairs failed the band (Self 60–80% **and** D ≤ 58%, fixed before the pilot, never
  moved). VO-A/B/C leaked on Baseline D; VO-D and VO-E, on style-equalising scaffolds (A1, A5),
  closed the leak and took Self to chance with it. Self accuracy tracks Baseline D across the ten
  column-results at **r = +0.71**; D matches or beats the model in six of ten.
- **A3 (no main run) was reversed by A4.** The pilot had produced something more useful than a pair
  that passes the band: a pair that leaks (VO-C, D = 0.650 on M) and one that does not (VO-D,
  D = 0.325 on M). The crossed 2×2 therefore ran as a **leakage manipulation**, declared in writing
  before any of those cells were run.
- **E (main crossed run) DONE** — extended by A7 to **four** stimulus sets spanning the leakage axis:
  **24 cells, 200 prompts × 2 personas per column (~400 items/cell), 9,269 scored trials, zero
  malformed.** Main prompts are disjoint from the pilot prompts used to select the sets.
- **A6/A8 (self-recognition → self-prediction probe) DONE.** A6's two recognition framings were
  **elicitation failures** (M answered "A" on 99.0%, N "B" on 98.7%; both answered "no" to 100% of
  791 texts) and measure nothing. A8 re-ran it as Binder et al.'s self-*prediction* question.

**Headline results (full numbers and CIs in `10_report.md` §4):**

- **No positive self-advantage in any of the four sets *on the raw M-target contrast*
  (M→M − N→M)** — every interval either contains zero or is negative. Always carry that
  qualification: the capability-controlled **interaction is positive on `VO-C`**
  (+0.089 [+0.048, +0.131]) and must never be hidden. Surface baselines span 0.54–0.85. The one
  significant raw self-advantage is *negative* (VO-C, −0.033 [−0.058, −0.008]), and the positive
  interaction is driven by M *under*-performing on N's column, so the estimator cannot separate it
  from a genuine self-advantage — a diagnosis, not an adjudication.
- **On `VO-C`'s M column the self model is the worst predictor of its own output:** M→M (0.603)
  sits below both N→M (0.636) and F→M (0.628) — beaten on its own text by a different
  organisation's model. **Say "on VO-C's M column", not "never":** on `VO-C`'s N column the self
  cell is nominally highest (N→N 0.766 against F→N 0.763), a 0.003 margin not to be interpreted.
- **On style-equalised stimuli everything collapses to chance** (0.505–0.557; interaction
  −0.006 [−0.033, +0.021], excluding the applicable SESOI — row P5 gives 5 pp for a simple
  contrast and 8 pp for the interaction at the achieved n).
- **One positive self-prediction result: Hermes-3**, balanced accuracy **0.719** [0.675, 0.762],
  discrimination (hit − FA) **+0.437** [+0.349, +0.519]. Llama-3.1 shows none (0.447, −0.107); its
  A-share is **0.897 — just *under* the 0.90 threshold, so the degeneracy rule did not formally
  fire**, and the report says so rather than rounding it up. **Cost comparators, not matched
  scores:** a one-feature "pick the longer reply" rule scores **0.808** on exactly Hermes's 391
  pairs (matched item-for-item, so a paired test is reported), and an 18-feature logistic regression
  labels the author at **0.831** under a *different, supervised* procedure — **0.719 vs 0.831 is a
  criterion comparison, not a statistical contest, and no test is run between them.** But length
  does not explain the residual: where the length cue points away from Hermes's own reply it still
  discriminates at **+0.381** [+0.188, +0.566], mechanism unresolved. The §4.3 intervals and the
  whole length analysis are **post hoc** (A9).

**Released artifact:** `tools/surface_leakage_gate.py` — self-contained (numpy only), provides
`gate()` and `response_bias()`, groups CV by source prompt by default. The report recommends both
checks as reporting defaults.

**Deliverables (final packaging pass, 2026-08-16).** Two reports, and they are not interchangeable:

- **`submission_report.md` is the judge-facing submission report** — hand-authored, **8 rendered
  pages (hard maximum)**, three core figures, ~4,300 words → `Submission_Report.docx` and
  `Submission_Report.pdf`.
- **`10_report.md` remains the full technical record** — all methods, tables, appendices A–K,
  verification, provenance, cost → `10_Report.docx`. **Re-derive any summary from `10_report.md`,
  and put no number in `submission_report.md` that is not in it** — `scripts/build_submission.py`
  fails the build otherwise, as it does on a placeholder, a dropped disclosure or a 9th page.

Both `.docx` and the `.pdf` come from `scripts/build_submission.py` (needs pandoc + a Chrome
binary). The **six-slide** deck is `Digital_Minds_Track3_Slides.pptx` + `presentation.html`
(`scripts/build_pptx.py`, `scripts/build_slides.py`) — it is the approved baseline; change wording
and numbers, not the design. Also `11_video_script.md` (five-minute two-speaker script) and
`README.md`. Repository: <https://github.com/UbaJaz/Digital_Minds_Research>. **Never hand-edit a
derived artifact — regenerate it**, or the corrections silently diverge.

The condensed report (`10_report_condensed.md` and its `.docx`, `scripts/build_condensed.py`,
`scripts/build_docx.py`) was **retired** in that pass — `submission_report.md` replaces it, and two
competing short reports is exactly the ambiguity to avoid. Files kept, removed and why:
`notes/FINAL_REPO_AUDIT.md` (current) and `notes/PUBLIC_REPO_MANIFEST.md`; submission checklist:
`notes/FINAL_SUBMISSION_CHECKLIST.md`; the earlier `notes/FINAL_ARTIFACT_AUDIT.md` is superseded
where the two disagree.

**Remaining work:** none blocking submission. Two provenance items stay open by design and must not
be reconstructed — the `VO-D`/`VO-E` screening date/screener, and the reason for the sample-size
step-down (`notes/AUTHOR_CONFIRMATION_REQUIRED.md` §2.2, §2.3). Desirable but not done: commit
scripts for the ad-hoc manipulation-check overlap figures and the post-hoc §4.3 length analysis
(`notes/A9_post_hoc_audit.md` §5.1). No further API calls are planned.
