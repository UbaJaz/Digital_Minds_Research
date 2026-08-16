# FINAL REPOSITORY AUDIT

**Date: 2026-08-16.** Produced during the final end-to-end packaging pass, after amendments A1 and
A3–A9 were confirmed by **Jaswin Chinthala** and **Ubayd Hattas**.

**What this pass did.** It created the judge-facing submission report, aligned the existing
six-slide deck and the video script to it, and cleaned the public repository. **No raw data,
checkpoint, result JSON, figure, experimental result or line of experimental code was changed, and
no API call was made.** `scripts/make_figures.py` was re-run as a check and reproduced all four
figures **byte-identically**; `data/results/` is unchanged under `git status`.

**What "REMOVE" means here.** Nothing was destroyed. Every removed file was **moved out of the
public repository** to `../Digital_Minds_private_archive/` (a sibling directory of the repo, not a
subdirectory, so it cannot be committed). Tracked files therefore show as deletions in
`git status`; the authors' commit is what actually removes them from the public repository, and the
previous commit `e75205d` retains them in history.

Classification key: **A** public research artifact · **B** public reproducibility artifact ·
**C** final submission artifact · **D** source / build tool · **E** private or competition working
material · **F** stale generated copy · **G** duplicate · **H** unknown, author review.

---

## 1. Kept — final submission artifacts (C)

| Path | Classification | Action | Reason | Canonical copy |
|---|---|---|---|---|
| `submission_report.md` | C | **KEEP (new)** | The judge-facing submission report; 8 rendered pages, three core figures. | itself |
| `Submission_Report.docx` | C | **KEEP (new)** | Word build of the above. Derived — never hand-edit. | `submission_report.md` |
| `Submission_Report.pdf` | C | **KEEP (new)** | Print build, and the artifact the page-count check is measured on. Derived. | `submission_report.md` |
| `10_report.md` | A, C | **KEEP** | The full technical record. Unchanged in substance by this pass. | itself |
| `10_Report.docx` | C | **KEEP (rebuilt)** | Word build of the full report, rebuilt from the current source. | `10_report.md` |
| `Digital_Minds_Track3_Slides.pptx` | C | **KEEP (rebuilt)** | The approved six-slide deck. Only slide 4's heading changed, to qualify the self-advantage claim. | `scripts/build_pptx.py` |
| `presentation.html` | C | **KEEP (rebuilt)** | Same six slides, self-contained HTML. | `scripts/build_slides.py` |
| `11_video_script.md` | C | **KEEP (updated)** | Five-minute two-speaker script; one line qualified, word count corrected. | itself |
| `README.md` | A, C | **KEEP (rewritten)** | Repository front door. Restructured; stale claims removed. | itself |

## 2. Kept — provenance and research record (A)

| Path | Classification | Action | Reason | Canonical copy |
|---|---|---|---|---|
| `02_design_audit.md` | A | **KEEP (updated)** | The preregistration. P1–P15 confirmed 2026-08-15; A1–A9 confirmed 2026-08-16. This pass only marked each original status line as superseded by its confirmation — no original text edited or removed. | itself |
| `notes/A9_post_hoc_audit.md` | A | **KEEP** | The final A9 record: the post-hoc forensic review, with the definitions needed to reproduce every figure it cites. | itself |
| `notes/A9_DRAFT.md` | A | **KEEP** | A pointer stub, so two copies of A9 cannot circulate. Cites the two preserved drafts below. | — |
| `notes/A9_DRAFT.pre-final.bak.md` | A | **KEEP** | The **unsigned** A9 draft, preserved byte-for-byte and explicitly cited by the stub. Untracked, so this is its only copy. **Provenance, not clutter.** | itself |
| `notes/A9_DRAFT.pre-fix-pass-3.bak.md` | A | **KEEP** | Earlier A9 draft, cited by the stub. Same reasoning. | itself |
| `notes/AUTHOR_CONFIRMATION_REQUIRED.md` | A | **KEEP** | The confirmation register, including the two provenance items that remain open. | itself |
| `notes/AUTHOR_CONFIRMATION_REQUIRED.pre-final.bak.md` | A | **KEEP** | The register as it stood *before* the confirmations — the evidence that they were added, not backdated. | itself |
| `notes/council-transcript-2026-08-15.md` | A | **KEEP** | The adversarial review that produced the crossed design. Cited by `03`. | itself |
| `notes/council-transcript-2026-08-16-hostile-review.md` | A | **KEEP** | The forensic review behind A9. Cited by the A9 entry in `02`. | itself |
| `notes/message.txt`, `notes/message (1).txt`, `notes/message_claude.txt` | A | **KEEP** | Planning-chat transcripts, but **cited by name as inputs in `03_design_review_and_implementation_plan.md` §sources**. Removing them would break a research record. Checked: no credentials. | itself |
| `01_literature_grounding.md`, `03`–`09` `.md` | A | **KEEP** | Phase records. Superseded by `10_report.md` narratively; still the primary evidence for their own numbers. | themselves |
| `05_status_and_plan.md` | A | **KEEP** | Mid-sprint status record. Historical, but part of the numbered phase series. | itself |
| `Track3_Strategy_Doc_Research_Focused.docx` | **H** | **KEEP — author review** | Pre-project planning, and describes a design that was superseded. **But it is named as "the source-of-truth document" in `02_design_audit.md` §Purpose and read as a source in `03`.** Deleting it breaks a preregistration reference. Kept on the "if uncertain, do not delete" rule; whether a superseded strategy doc belongs in the public repo is an author call. | itself |
| `notes/FINAL_ARTIFACT_AUDIT.md` | A | **KEEP (superseded in part)** | The 2026-08-16 artifact audit. Its artifact rulings still hold except where this file supersedes them; a banner has been added. | itself |

## 3. Kept — code, data, tests (B, D)

| Path | Classification | Action | Reason | Canonical copy |
|---|---|---|---|---|
| `src/selfpred/` | B, D | **KEEP** | Pinned client with pre-request budget guard, generation, prediction, surface baseline, bootstrap/McNemar/interaction. Untouched by this pass. | itself |
| `tools/surface_leakage_gate.py` | A, B | **KEEP** | The released tool. Untouched. | itself |
| `tests/` | B | **KEEP** | 38 tests, including ground-truth separation. All pass. | itself |
| `data/raw/*.jsonl`, `data/results/*.json`, `data/labels/`, `data/stimuli/` | B | **KEEP** | The reproducibility record and the analysis outputs. Unchanged. | themselves |
| `data/generated/`, `data/checkpoints/`, `data/raw/openrouter_models.json` | B | **KEEP, gitignored** | Large generated corpora and resumable checkpoints. Present locally, deliberately not tracked. | themselves |
| `figures/fig1..fig4*.png` | A, B | **KEEP** | The four report figures. Re-generated as a check and byte-identical. | `scripts/make_figures.py` |
| `scripts/make_figures.py`, `analyze_pilot.py`, `analyze_selfpred.py`, `check_*.py`, `phase_b_*.py`, `run_pipeline.py`, `smoke_hermes_enactment.py` | D | **KEEP** | Analysis, verification and run tooling. Untouched. | themselves |
| `scripts/build_slides.py`, `scripts/build_pptx.py` | D | **KEEP (updated)** | The two deck builders. One heading string changed in each. | themselves |
| `scripts/build_submission.py` | D | **KEEP (new)** | The single sanctioned builder for the Word/PDF deliverables. Guards placeholders, required disclosures, invented numbers and the 8-page limit. | itself |
| `pyproject.toml`, `requirements.txt`, `.gitignore` | D | **KEEP** (`.gitignore` extended) | Now also ignores Office lock files (`~$*`), `.claude/*.lock` and the transient render scratch file. | themselves |
| `CLAUDE.md` | D | **KEEP (updated)** | Project working rules, refreshed for the new deliverable set and two stale claims corrected. | itself |

## 4. Removed — private / competition working material (E)

All moved to `../Digital_Minds_private_archive/competition/`.

| Path | Classification | Action | Reason | Canonical copy |
|---|---|---|---|---|
| `judging criteria/` (6 screenshots) | E | **REMOVE → archive** | Competition judging criteria. Not research, not reproducibility, not provenance. Referenced by no code or document. | archive |
| `judging criteria.zip` | E, G | **REMOVE → archive** | Zip of the above. | archive |
| `Past Hackathon winners/` (6 PDFs) | E | **REMOVE → archive** | Previous hackathon winner submissions — other people's work, kept as competition reference. Not ours to publish. | archive |
| `Past Hackathon winners.zip` | E, G | **REMOVE → archive** | Zip of the above. | archive |
| `Copy of Digital Minds Research Sprint submission template.docx` | E | **REMOVE → archive** | The organisers' template. Input, not output. | archive |
| `AfriGuard_Presentation/AfriGuard_Hackathon_Summary_V2.pptx` | E | **REMOVE → archive** | Previous hackathon presentation, kept as a palette/typography reference. The deck builders only cite it in a comment; there is no file dependency. | archive |
| `Track3_One_Page_Summary.docx` | E, F | **REMOVE → archive** | Pre-project planning (2026-08-14) describing a study that was not the one performed. Referenced by nothing except the artifact audit. | archive |

## 5. Removed — stale generated copies and duplicates (F, G)

All moved to `../Digital_Minds_private_archive/`.

| Path | Classification | Action | Reason | Canonical copy |
|---|---|---|---|---|
| `10_report_condensed.md` | F, G | **REMOVE → archive** | The condensed report was the previous answer to a page limit. `submission_report.md` replaces it, and keeping both would leave two competing "short reports". Contains nothing not in `10_report.md`. | `10_report.md` |
| `10_Report_condensed.docx` | F, G | **REMOVE → archive** | Word build of the above. | `10_report.md` |
| `scripts/build_condensed.py` | F | **REMOVE → archive** | Built only the retired condensed report. Its disclosure/retraction guards were carried into `scripts/build_submission.py`, which is stricter. | `scripts/build_submission.py` |
| `scripts/build_docx.py` | F, G | **REMOVE → archive** | Superseded: `build_submission.py` builds `10_Report.docx` and both submission-report formats, with the same guards. | `scripts/build_submission.py` |
| `10_report.pre-fix-pass-1..5.bak.md`, `10_report.pre-final.bak.md` | F | **REMOVE → archive** | Per-pass drafting snapshots of a document whose final version is in the repo. Cited by nothing. | `10_report.md` |
| `02_design_audit.pre-fix-pass-2.bak.md`, `02_design_audit.pre-final.bak.md` | F | **REMOVE → archive** | Same. | `02_design_audit.md` |
| `CLAUDE.pre-fix-pass-2.bak.md` | F | **REMOVE → archive** | Same. | `CLAUDE.md` |
| `10_Report.docx.bak` | F | **REMOVE → archive** | Pre-review Word build; carries none of the A9 corrections. Never safe to submit. | `10_Report.docx` |
| `~$Digital_Minds_Track3_Slides.pptx` | F | **REMOVED (deleted earlier)** | A PowerPoint lock file, committed by accident. Not a document. `.gitignore` now excludes `~$*`. | — |

## 6. Unknown / author review (H)

| Path | Why it is flagged |
|---|---|
| `Track3_Strategy_Doc_Research_Focused.docx` | Kept (see §2). It is superseded planning material **and** the document `02_design_audit.md` calls its source of truth. Either keep it, or remove it *and* amend the two references in `02` and `03` — do not do one without the other. |
| `notes/message.txt`, `notes/message (1).txt`, `notes/message_claude.txt` | Kept (see §2). They are pasted planning chats — the kind of material Part 7 would ordinarily strip — but `03_design_review_and_implementation_plan.md` analyses them by name. Removing them silently would leave that record citing files that do not exist. |
| Author order | Every artifact lists **Ubayd Hattas** first, as the repository has throughout. This pass did not reorder it; changing it is an author decision and would have to be made in all seven artifacts at once. |

## 7. Deletion rule, applied

Before any file was moved out: (1) it was grepped for across the whole repository to confirm no code
or document imports or cites it; (2) it was confirmed not to be needed to reproduce a reported
result; (3) it was confirmed not to be the only copy of a piece of provenance — the three `.bak`
files that *are* the only copy of cited provenance were kept for exactly this reason; (4) a
canonical copy was named where the file was a duplicate; (5) the move is recorded in the tables
above. Nothing was deleted outright.

## 8. Secret scan

`.env` exists locally, is matched by `.gitignore`, has **never been committed** (`git log --all
--diff-filter=A -- .env` is empty) and is not tracked. No API key, token or credential appears in
any tracked file; the only key-shaped string in the repository is an obvious dummy inside
`tests/test_budget_and_secrets.py`, which exists to assert that the redactor removes it.

**One action for the authors:** the live `OPENROUTER_KEY` value was read into the terminal during
this pass's secret scan. It was not written to any file and not committed, but it did appear in a
session transcript, so **rotating the key at OpenRouter is the prudent step.** No further API calls
are planned, so rotation costs nothing.
