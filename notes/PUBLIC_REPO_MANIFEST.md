# PUBLIC REPOSITORY MANIFEST

**Date: 2026-08-16.** The files and folders intentionally included in the public research
repository <https://github.com/UbaJaz/Digital_Minds_Research>. Anything not listed here is either
git-ignored (see the bottom section) or was moved out of the repository in the final packaging pass
— see [`FINAL_REPO_AUDIT.md`](FINAL_REPO_AUDIT.md) for what went where and why.

Counts below exclude `.git/`, `.venv/`, `__pycache__/` and `.pytest_cache/`.

---

## Root

```
README.md                          repository front door
submission_report.md               the judge-facing submission report (8 pages)
Submission_Report.docx             derived from submission_report.md
Submission_Report.pdf              derived; the page-count check measures this file
10_report.md                       the full technical record
10_Report.docx                     derived from 10_report.md
02_design_audit.md                 the preregistration (P1-P15) + amendments A1-A9
11_video_script.md                 five-minute two-speaker script
presentation.html                  six-slide deck, self-contained
Digital_Minds_Track3_Slides.pptx   the same six slides as PowerPoint
CLAUDE.md                          project working rules
pyproject.toml  requirements.txt   packaging and pinned dependencies
.gitignore
Track3_Strategy_Doc_Research_Focused.docx    superseded strategy doc, cited by 02 and 03
```

## Phase records (`01`, `03`–`09`)

```
01_literature_grounding.md                     Binder / Song / Song / Lindsey grounding
03_design_review_and_implementation_plan.md    the adversarial review that produced the crossed design
04_model_verification.md                       311 verification calls across 11 candidate models
05_status_and_plan.md                          mid-sprint status record
06_hermes_smoke_test.md                        enactment smoke test
07_calibration_results.md                      the 50-item calibration probe
08_pilot_results.md                            the five-pair pilot
09_pilot_finding.md                            the pilot reported as a result (superseded by A4)
```

Superseded by `10_report.md` for narrative purposes; still the primary evidence for their own
numbers.

## `notes/` — provenance, review, packaging

```
A9_post_hoc_audit.md                       THE A9 record: the post-hoc forensic review
A9_DRAFT.md                                pointer stub -> A9_post_hoc_audit.md
A9_DRAFT.pre-final.bak.md                  the unsigned A9 draft, byte-for-byte (cited by the stub)
A9_DRAFT.pre-fix-pass-3.bak.md             earlier A9 draft (cited by the stub)
AUTHOR_CONFIRMATION_REQUIRED.md            confirmation register; the two items still open
AUTHOR_CONFIRMATION_REQUIRED.pre-final.bak.md   the register before the confirmations were added
council-transcript-2026-08-15.md           adversarial design review -> the crossed design
council-transcript-2026-08-16-hostile-review.md  forensic review -> A9
message.txt, message (1).txt, message_claude.txt  planning chats, cited by name in 03
FINAL_ARTIFACT_AUDIT.md                    2026-08-16 artifact audit (partly superseded)
FINAL_REPO_AUDIT.md                        this pass's file-by-file classification
FINAL_SUBMISSION_CHECKLIST.md              item-by-item submission check
PUBLIC_REPO_MANIFEST.md                    this file
```

## `src/selfpred/` — 18 files

```
client.py          pinned OpenRouter client; projects cost BEFORE issuing; the only network code
config.py          M/N/F, active cells, n ladder, PHASE_BUDGETS_USD
checkpoint.py      resumable run checkpoints
labels/            ground-truth store — predict/ structurally cannot import this
predict/           predictor prompts (frozen) and the cell runner
personas/          persona generation and quality screening
baseline/          the 18-feature surface classifier (condition D)
calibration/       the paraphrase-preference probe
analysis/          scoring, prompt-clustered bootstrap, McNemar, interaction
```

## `scripts/` — 13 files

```
run_pipeline.py            the main run (network)
phase_b_*.py               model discovery, endpoints, verification, follow-up (network)
smoke_hermes_enactment.py  the enactment smoke test (network)
analyze_pilot.py           pilot analysis            -> data/results/pilot_analysis.json
analyze_selfpred.py        A8 self-prediction probe  -> data/results/selfpred_corrected.json
check_discrimination.py    within-prompt discrimination rates
check_vod_ci.py            VO-D interval check
make_figures.py            figures/fig1..fig4*.png
build_submission.py        Submission_Report.docx/.pdf + 10_Report.docx, with all guards
build_slides.py            presentation.html
build_pptx.py              Digital_Minds_Track3_Slides.pptx
```

Only the first three groups make network calls, and all of them route through `client.py`.

## `tests/` — 3 files, 38 tests

```
test_ground_truth_separation.py   predict/ cannot import labels/; no label token in any prompt;
                                  persona option order counterbalanced and logged
test_budget_and_secrets.py        the pre-request budget guard; key redaction in tracebacks
test_analysis_and_checkpoint.py   estimators (a pure capability effect must return zero); resume
```

## `tools/`

```
surface_leakage_gate.py   the released tool: gate() and response_bias(), numpy only,
                          no dependency on the rest of this repository
```

## `figures/` — 4 files

```
fig1_self_vs_surface.png       self-prediction vs the surface baseline, ten pilot columns
fig2_leakage_manipulation.png  the leakage manipulation; all six cells, both end sets
fig3_authorship.png            authorship discrimination and the two degenerate framings
fig4_selfprediction.png        the A8 self-prediction probe against the surface classifier
```

## `data/` — tracked

```
data/raw/*.jsonl              append-only per-call log for every phase — THE reproducibility record
data/raw/verification_*.json  the verification sweep summaries
data/results/*.json           computed analysis outputs
data/labels/, data/labels_smoke/   ground truth, stored apart from predictor inputs
data/stimuli/                 frozen stimulus sets with FREEZE.md content hashes
```

`data/results/main_two_set.json` holds all four sets' cell-level accuracies;
`selfpred_corrected.json` holds the A8 probe.

## Deliberately **not** tracked (`.gitignore`)

```
.env, *.key                          secrets — never committed, never printed
data/generated/                      generated corpora and predictions (large)
data/checkpoints/                    resumable run checkpoints (large)
data/raw/openrouter_models.json      raw provider model dump (large)
__pycache__/, .venv/, .pytest_cache/, *.egg-info/, build/, dist/
.DS_Store, Thumbs.db, .idea/, .vscode/
~$*, .claude/*.lock                  Office lock files
_submission_render.html              transient build scratch
```

The generated corpora are excluded for size, not for secrecy: every text in them is reconstructible
from `data/raw/generation.jsonl` and `data/raw/prediction.jsonl`, which are tracked.
