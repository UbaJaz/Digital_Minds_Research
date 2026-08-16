# FINAL ARTIFACT AUDIT

> **Superseded in part (2026-08-16, later the same day).** A second, end-to-end packaging pass ran
> after this audit was written. It added the judge-facing submission report, retired the condensed
> report, and cleaned the public repository. **Where this file and
> [`FINAL_REPO_AUDIT.md`](FINAL_REPO_AUDIT.md) disagree, `FINAL_REPO_AUDIT.md` is current.**
> Specifically: the "short list" in §1 below is superseded (`submission_report.md` →
> `Submission_Report.docx`/`.pdf` replaces the condensed pair); the regeneration commands in §4 are
> superseded by `scripts/build_submission.py`; §5's "no PDF" ruling is superseded, since a PDF is
> now built as the page-count check; and the backups, competition material and planning documents
> listed as retained have been moved out of the public repository. This file is kept because it is
> the record of what the artifacts looked like at that point.

**Date: 2026-08-16.** Produced during the final packaging pass, after amendments A1 and A3–A9 were
confirmed by **Jaswin Chinthala** and **Ubayd Hattas**.

**Why this file exists.** Every derived deliverable in this repository was built *before* the
2026-08-16 forensic review (A9) and therefore carried none of its corrections. A stale copy that
still reads "four independent stimulus designs", or still shows `⟦FILL: affiliation⟧`, is worse than
no copy at all — **if a stale file is what gets submitted, the corrections do not exist for the
reader.** This audit names, for every artifact, whether it is final and whether it is safe to submit.

**Nothing scientific changed in this pass.** No raw data file, checkpoint, result JSON, figure, or
line of experimental code was touched. No API call was made. The only numeric change anywhere in
`10_report.md` is the addition of section cross-references (`§3.5`, `§3.6`) — verified by comparing
every decimal in the report before and after.

---

## 1. Submission artifacts — the short list

**If you submit exactly these five, you have submitted the current work:**

| # | Artifact | Role |
|---|---|---|
| 1 | **`10_report.md`** → **`10_Report.docx`** | The full report. The authoritative scientific document. |
| 2 | **`10_report_condensed.md`** → **`10_Report_condensed.docx`** | The condensed report — identical minus Appendices A–K. Use where a page limit applies. |
| 3 | **`Digital_Minds_Track3_Slides.pptx`** | The six-slide deck, for presenting or editing. |
| 4 | **`presentation.html`** | The same six slides as a self-contained web page. |
| 5 | **`11_video_script.md`** | The five-minute two-speaker script. |

Plus the repository itself: <https://github.com/UbaJaz/Digital_Minds_Research>, whose front door is
`README.md`.

---

## 2. Full audit

| Artifact | Final/stale | Source | Regenerate? | Safe to submit? | Purpose / final role |
|---|---|---|---|---|---|
| `10_report.md` | **FINAL** | hand-authored | — | **YES** | The report. Single source of truth; everything else derives from it. |
| `10_Report.docx` | **FINAL** (rebuilt 2026-08-16) | `10_report.md` via `scripts/build_docx.py` | done | **YES** | Word copy of the full report. 4 figures embedded, no placeholders. |
| `10_report_condensed.md` | **FINAL** (rebuilt) | `10_report.md` via `scripts/build_condensed.py` | done | **YES** | Condensed report, appendices removed. Build fails if a required disclosure is dropped. |
| `10_Report_condensed.docx` | **FINAL** (rebuilt) | `10_report_condensed.md` via `scripts/build_docx.py` | done | **YES** | Word copy of the condensed report. |
| `Digital_Minds_Track3_Slides.pptx` | **FINAL** (rebuilt, now **6 slides**) | `scripts/build_pptx.py` | done | **YES** | Presentation deck. Replaces the previous 10-slide version. |
| `presentation.html` | **FINAL** (rebuilt, now **6 slides**) | `scripts/build_slides.py` | done | **YES** | Same deck, self-contained HTML (figure embedded as a data URI). |
| `11_video_script.md` | **FINAL** (new) | hand-authored from `10_report.md` | — | **YES** | Five-minute script, two speakers, slide cues. |
| `README.md` | **FINAL** (new) | hand-authored | — | **YES** | Repository front door: question, findings, released tool, reproduction path, structure. |
| `02_design_audit.md` | **FINAL** | hand-authored | — | **YES** | The preregistration. P1–P15 confirmed 2026-08-15; A1–A9 confirmed 2026-08-16 as amendments. |
| `notes/A9_post_hoc_audit.md` | **FINAL** (new) | supersedes `notes/A9_DRAFT.md` | — | **YES** | The post-hoc forensic-review record, filed as amendment A9. |
| `notes/AUTHOR_CONFIRMATION_REQUIRED.md` | **FINAL** | hand-authored | — | **YES** | Confirmation register. Records what was confirmed and the two items still open. |
| `figures/fig1..fig4*.png` | **FINAL** | `scripts/make_figures.py` | not needed — no result changed | **YES** | The four report figures. Unchanged in this pass, by design. |
| `tools/surface_leakage_gate.py` | **FINAL** | hand-authored | — | **YES** | The released tool. Untouched by the review and by this pass. |
| `scripts/build_condensed.py`, `build_docx.py`, `build_slides.py`, `build_pptx.py` | **FINAL** (`build_docx.py` new; the two slide builders rewritten for 6 slides) | hand-authored | — | n/a (code) | The only sanctioned way to produce a derived artifact. Two of them refuse to build if a disclosure is missing or a retracted claim survives. |
| `notes/FINAL_SUBMISSION_CHECKLIST.md` | **FINAL** (new) | hand-authored | — | yes, as context | Item-by-item submission check, with the three still-open items listed rather than hidden. |
| `01`, `03`–`09` `.md` | **CURRENT as phase records** | hand-authored | — | yes, as context | Superseded by `10_report.md` for narrative purposes; still the primary evidence for their own numbers. |
| `notes/A9_DRAFT.md` | **SUPERSEDED → stub** | — | — | no (points to the final) | Now a five-line pointer to `notes/A9_post_hoc_audit.md`, so two copies of A9 cannot circulate. |
| `notes/A9_DRAFT.pre-final.bak.md` | **HISTORICAL** | backup | — | no | The unsigned A9 draft, preserved byte-for-byte. |
| `notes/A9_DRAFT.pre-fix-pass-3.bak.md` | **HISTORICAL** | backup | — | no | Earlier A9 draft. |
| `notes/AUTHOR_CONFIRMATION_REQUIRED.pre-final.bak.md` | **HISTORICAL** | backup | — | no | The register as it stood before the confirmations. |
| `02_design_audit.pre-final.bak.md`, `.pre-fix-pass-2.bak.md` | **HISTORICAL** | backups | — | no | Audit before this pass / before the provenance pass. |
| `10_report.pre-final.bak.md`, `.pre-fix-pass-1..5.bak.md` | **HISTORICAL** | backups | — | no | Report at each fix pass. Retained under the repo's `.bak` convention; **none is a submission file.** |
| `CLAUDE.pre-fix-pass-2.bak.md` | **HISTORICAL** | backup | — | no | Project instructions before the provenance pass. |
| `10_Report.docx.bak` | **STALE** (2026-08-16 08:35) | old build | superseded | **NO** | Pre-review Word build. Kept as a backup only; **do not submit.** |
| `Track3_One_Page_Summary.docx` | **STALE** (2026-08-14) | pre-project planning | no | **NO** | Written before the experiments ran. Describes a study that was not the one performed. |
| `Track3_Strategy_Doc_Research_Focused.docx` | **STALE** (2026-08-14) | pre-project planning | no | **NO** | Same. Historical planning material. |
| `Copy of Digital Minds Research Sprint submission template.docx` | **REFERENCE** | organisers | no | n/a | The organisers' template. Input, not output. |
| `AfriGuard_Presentation/AfriGuard_Hackathon_Summary_V2.pptx` | **REFERENCE** | previous hackathon | no | n/a | Visual reference for the deck's palette and typography. Not part of this project's content. |
| `notes/council-transcript-*.md` | **HISTORICAL** | review transcripts | no | as context | The adversarial reviews that produced the crossed design (15 Aug) and the forensic review behind A9 (16 Aug). |
| `judging criteria/`, `Past Hackathon winners/`, `*.zip` | **REFERENCE** | organisers / prior work | no | n/a | Input material. |
| `~$Digital_Minds_Track3_Slides.pptx` | **REMOVED** | Word/PowerPoint lock file | — | n/a | A lock file had been committed by accident. Deleted; it is not a document. |

---

## 3. Duplicate-final resolution

Where two files could each be mistaken for "the final one", this is the ruling:

| If you see… | The authoritative artifact is… | Because |
|---|---|---|
| `10_Report.docx` **vs** `10_Report.docx.bak` | **`10_Report.docx`** | The `.bak` predates the forensic review and carries none of its corrections. |
| `10_report.md` **vs** any `10_report.pre-*.bak.md` | **`10_report.md`** | The `.bak` files are per-pass snapshots, deliberately frozen. |
| Full report **vs** condensed report | **Both are current; neither supersedes the other.** | Use the condensed one where a page limit applies; the condensed build refuses to run if it drops a disclosure. |
| `notes/A9_post_hoc_audit.md` **vs** `notes/A9_DRAFT.md` | **`A9_post_hoc_audit.md`** | The draft is now a pointer stub. The unsigned draft text survives at `A9_DRAFT.pre-final.bak.md`. |
| Report **vs** `Track3_One_Page_Summary.docx` | **The report.** | The one-pager predates the experiments. |

**No file was deleted in this pass except the accidental PowerPoint lock file.** The repository's
established convention is backup-then-overwrite (`*.pre-fix-pass-N.bak.md`), and that convention was
followed rather than replaced.

---

## 4. Regeneration commands

Every derived artifact rebuilds from the current sources with no API calls:

```bash
.venv/Scripts/python scripts/build_condensed.py    # 10_report_condensed.md   (guards the disclosures)
.venv/Scripts/python scripts/build_docx.py         # both .docx               (needs pandoc)
.venv/Scripts/python scripts/build_slides.py       # presentation.html
.venv/Scripts/python scripts/build_pptx.py         # Digital_Minds_Track3_Slides.pptx
.venv/Scripts/python scripts/make_figures.py       # figures/  (only if a result changes — none did)
```

`build_condensed.py` fails the build if the condensed output drops any required disclosure
(the length rule, the manipulation-check overlaps, the own-not-longer residual, the shared prompt
pool, the estimand substitution, the post-hoc labels, the sample-size floor, the author names, the
affiliations, the repository URL) or if it carries a retracted claim (`four independent stimulus
designs`, `⟦FILL`, `not countersigned`, `A9_DRAFT`). `build_docx.py` refuses to build a Word file
from a source containing any of those. **Never hand-edit a derived artifact** — fix the markdown and
rebuild, or the two silently diverge.

---

## 5. Not produced, and why

- **No PDF.** The project has never had a PDF deliverable, so none was invented here; adding one
  would create a fourth "final report" file to keep in sync. If a PDF is required at submission,
  export `10_Report.docx` (or `10_Report_condensed.docx`) from Word and treat the export as
  disposable — the `.docx` remains the artifact of record.
- **Figures were not regenerated.** No result changed, so re-running `make_figures.py` could only
  introduce a difference where there is none. The four PNGs are the ones the report has always used.
- **The slide figures are the report figures.** They are light-background matplotlib PNGs shown on
  white cards inside a dark deck; that is deliberate, not an oversight — they read as printed
  exhibits. No dark-themed variants were made, because a second set of figures is a second thing to
  keep in sync.
