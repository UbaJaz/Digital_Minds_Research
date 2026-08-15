# CLAUDE.md — project working rules

## Project purpose

This repository is a 3-day, two-person AI research sprint (Digital Minds Sprint, Track 3) testing
whether a language model has a *self-prediction residual*: when a model predicts a hidden property
(which of two value-ordering personas produced a piece of text) of its own output, does it do better
than a tier-matched same-lineage sibling does on that same text — after the predictor's general
classification ability is controlled by a crossed 2x2 design (each of M and N generates a column of
texts, and M, N and F each predict both columns)? The point of the crossed design is that any
"M is simply the better classifier" effect appears in both of M's cells and cancels in the
interaction. A surface-feature baseline (condition D) is fit per target column purely as a
leakage check and is never a point on the similarity axis.

## Authority

**`02_design_audit.md` is the authoritative research design. Change it in the doc first, then the
code — never the reverse.** `03_design_review_and_implementation_plan.md` and
`notes/council-transcript-2026-08-15.md` are review and proposal only: the council's Part 4 verdict
has **not** yet been applied to `02`. Code may be written *parameterised* so that either the crossed
design or the M-row fallback is expressible from config, but code must not encode a research
decision that `02` has not made. If you find yourself wanting to change a hypothesis, a condition,
an n, or an analysis contract, stop and edit `02` first.

## Budget guard

- Project ceiling: **$10.00** (hard; this is the entire experimental budget for the project).
- Working guard: **$7.50** projected total. If the projection from verified per-token prices exceeds
  it, n steps down 500 -> 400 -> 300 rather than the design changing.
- Per-phase sub-budgets live in `src/selfpred/config.py` (`PHASE_BUDGETS_USD`) and nowhere else.
- Every API call goes through `client.py`. The guard projects the cost of a call *before* issuing it
  and raises `BudgetExceeded` rather than calling. Nothing else in the repo may make network calls.

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

## Ground-truth separation

`src/selfpred/predict/` must not import from `src/selfpred/labels/`. A pytest asserts this, asserts
that a built predictor prompt contains no label token, and asserts persona option order is
counterbalanced and logged. No predictor — including Self — ever sees the hidden label.

## Current state (updated 2026-08-15, post-lock)

- `02_design_audit.md` **Post-Council Locked Decisions** rows P1–P15 are all confirmed (2026-08-15). The
  design is: crossed 2×2, M = llama-3.1-70b-instruct, N = hermes-3-llama-3.1-70b, F = mistral-small-3.2-24b
  (DeepSeek-V3 as pre-declared swap), all DeepInfra fp8; 1,000 items/cell target (500 prompts × 2 personas),
  500 floor; SESOI 5 pp; generation temperature 1.0; shared prompts across columns (joint resampling);
  values-ordering personas (3 candidates in `data/stimuli/personas/candidates.json`, chosen by the pilot);
  band Self 60–80 % AND D ≤ 58 %; label-blind exclusions in `personas/quality.py`.
- Stimuli frozen: `data/stimuli/main/` (500 main + 40 pilot prompts, hashes in FREEZE.md),
  `data/stimuli/calibration/items.json`, `data/stimuli/personas/candidates.json`.
- **Pipeline:** `scripts/run_pipeline.py` runs C (calibration) → D (pilot gate) → FREEZE (git commit) →
  E (main run) → ANALYSIS, fully resumable (per-item checkpoints + `data/generated/pipeline_state.json`).
  If a session dies mid-run: `.venv/Scripts/python scripts/run_pipeline.py` continues where it stopped.
  Progress: `data/generated/pipeline.log`. Results: `07_calibration_results.md`, `08_pilot_results.md`,
  `09_main_results.md`, `data/results/*.json`.
- Docs: 03 = review + plan, 04 = model verification, 05 = status/plan audit, 06 = Hermes smoke test.
  The pre-data report template is a template only and must be re-derived from 02 + 09 (its F is stale).

## Current state (updated 2026-08-15, post-pilot)

- **Phase C (calibration) DONE** — `07_calibration_results.md`. A_near 0.660, A_far 0.638,
  Δ = +0.021 [−0.064, +0.106]. Near > Far on the point estimate, so F stays Mistral-Small (no swap).
- **Phase D (pilot) DONE — gate outcome LEVEL 3.** All four persona pairs failed the band on both
  columns (`08_pilot_results.md`). VO-A/B/C failed on Baseline D (0.588–0.766) while Self was in
  band in 5 of 6 columns; VO-D, written on a style-equalising scaffold under amendment A1, closed
  the leak (D 0.325 on M) but took Self to chance (0.500).
- **Phase E (main run) NOT RUN and not to be run** — see 02 amendment A3. There is no validated
  hidden property, so a self-vs-other comparison would only measure who reads style better.
  The temperature rung of the ladder was deliberately not taken (same leakage failure mode).
- **The pilot is the result:** `09_pilot_finding.md`. Self accuracy tracks Baseline D across the
  eight column-results (r = +0.68); D ≥ Self in 5 of 8; equalising style collapses the model's
  within-prompt discrimination to 2/40 prompts. No self-advantage or privileged-access claim.
- Spend $0.2953 of the $10 ceiling. Remaining work: the write-up (re-derive from 02 + 07 + 08 + 09)
  and Jaswin's sign-off on amendments A1–A3.
