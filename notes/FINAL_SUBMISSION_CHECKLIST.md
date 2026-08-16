# FINAL SUBMISSION CHECKLIST

**Date: 2026-08-16.** Rewritten at the end of the final end-to-end packaging pass. `[x]` means
*checked in this pass by inspecting or running the thing*, not "believed to be true".

Companion documents: [`FINAL_REPO_AUDIT.md`](FINAL_REPO_AUDIT.md) (what was kept, removed and why)
and [`PUBLIC_REPO_MANIFEST.md`](PUBLIC_REPO_MANIFEST.md) (what the public repository contains).

---

## Report

- [x] `submission_report.md` exists — the judge-facing report, 4,232 words.
- [x] `Submission_Report.docx` builds from it (`scripts/build_submission.py`), 3 figures embedded,
      no placeholder text, no leaked `{width=…}` attribute markup.
- [x] `Submission_Report.pdf` builds and renders to **8 pages** — at the hard maximum, verified by
      counting pages in the PDF, not estimated. A4, 18/20/16 mm margins, 11 pt Calibri, 1.28 line height:
      ordinary manuscript settings. The build **fails** rather than shipping a 9th page.
- [x] Three core figures are **in the body**, not banished to an appendix: surface leakage (Fig. 1),
      the crossed design (Fig. 2), self-prediction vs the external observer (Fig. 3).
- [x] Both results tables fit on one page each; captions sit with their exhibits; no clipping.
- [x] Abstract is 162 words.
- [x] The **full technical report is retained** as `10_report.md` → `10_Report.docx`, rebuilt from
      the current source, appendices A–K intact, 4 figures embedded.
- [x] `submission_report.md` contains **no decimal that is not also in `10_report.md`** — enforced
      by the build, which fails on an invented number.
- [x] References: only the four cited works, unchanged and not re-verified (they were verified
      2026-08-16 and no inconsistency required correction).
- [x] Authors correct and complete on every artifact: **Ubayd Hattas** (Computer Science, Statistics
      & Data Science, University of Cape Town) and **Jaswin Chinthala** (Electrical Engineering,
      University of Cape Town). No initials anywhere.
- [x] Author Contributions present in both reports, complementary and truthful, with `VO-D`/`VO-E`
      attributed at project level rather than to an individual.

## Provenance

- [x] **A1 confirmed** — Jaswin Chinthala and Ubayd Hattas, 2026-08-16.
- [x] **A2** — bug fix, no research sign-off requested; listed for completeness.
- [x] **A3 confirmed** — and recorded as a decision taken and then reversed the same day by A4.
- [x] **A4 confirmed** — and **remains, in the record, a post-pilot substitution of the primary
      reported estimand**, with the stimulus sets selected on their Baseline-D values.
- [x] **A5 confirmed.**
- [x] **A6 confirmed** — the two recognition framings remain "elicitation failure, not measurement".
- [x] **A7 confirmed** — with the A9 §2.2 scope correction: four constructions on **one shared
      200-prompt pool**.
- [x] **A8 confirmed** — and **remains the amendment that introduced the self-prediction probe**,
      so the headline positive result rests on an amendment, not the frozen design.
- [x] **A9 filed and confirmed** — post hoc throughout; changes no result; full record in
      `A9_post_hoc_audit.md`.
- [x] **Nothing reads as awaiting confirmation.** Each original status line is preserved *verbatim*
      and now carries the prefix "as originally recorded …; superseded by the Confirmation below".
      The superseded first confirmation note is likewise marked as superseded, not deleted.
- [x] **Confirmation is not preregistration** — stated in `02`, `10_report.md`,
      `submission_report.md` and `README.md`.
- [x] Post-hoc analyses labelled post hoc wherever they appear: the §4.3 / §5 intervals, the
      length-only rule, the paired McNemar comparison and the own-not-longer residual.
- [x] **Two provenance items remain open and are disclosed as open, not reconstructed:** who
      screened the `VO-D`/`VO-E` clause pairs and when, and the reason for the sample-size
      step-down.

## Presentation

- [x] The existing approved **six-slide** deck was kept as the visual and structural baseline. No
      competing second deck was created; no seventh slide.
- [x] Palette, typography, spacing, layout language and chart treatment preserved unchanged.
- [x] The only content change: slide 4's heading now reads "No self-advantage on the target column —
      and one positive interaction", so the headline no longer over-generalises the raw contrast and
      no longer reads as if the capability control found nothing.
- [x] Slide 6 is Future Work, ending on "Can behavioural self-prediction ever provide evidence
      unavailable to an external observer?" — **no request for the Fellowship anywhere.**
- [x] All six slides rendered and inspected: no overflow, no clipping, no collisions. Verified
      geometrically in the `.pptx` (zero shapes outside the slide bounds; smallest run 9.5 pt) and
      visually in the HTML at 16:9.
- [x] `presentation.html` and the `.pptx` are two renderings of one source and were rebuilt
      together, so they cannot disagree.
- [x] No stale claims, no incorrect figures, correct names, affiliations and GitHub URL on slide 1.

## Video

- [x] `11_video_script.md`: **773 spoken words — 4:50 at 160 wpm**, inside the five-minute limit.
- [x] Speakers balanced: Ubayd 369 (48%), Jaswin 404 (52%).
- [x] Covers all major evidence: 0.719 / 0.808 / 0.831 / +0.381 / +0.089, r = +0.71, 6/10.
- [x] Covers the caveats out loud: the `VO-D` convergence caveat, "we can't claim it" on the
      interaction, "post hoc", "a different evaluation procedure".
- [x] Covers Future Work as the three-stage trajectory, and ends on the required closing line.
- [x] No Fellowship request.

## Repository

- [x] `README.md` final and restructured: TL;DR, research question, key-results table with post-hoc
      status per row, method, contribution, limitations, future work, structure, reproduction,
      artifacts, authors, citation.
- [x] Competition material removed from the public repo (judging criteria, past winners, organisers'
      template, previous hackathon deck) — moved to `../Digital_Minds_private_archive/`, not deleted.
- [x] Duplicates and stale generated copies cleaned: the condensed report pair and its two builders,
      ten per-pass `.bak` snapshots, one stale `.docx.bak`. The three `.bak` files that are the only
      copy of **cited** provenance were deliberately kept.
- [x] **No secrets.** `.env` is git-ignored and has never been committed; no credential appears in
      any tracked file. See the one rotation action in `FINAL_REPO_AUDIT.md` §8.
- [x] Source, data, results and tests retained in full. **38 tests pass.**
- [x] Canonical artifacts regenerated from current sources: both `.docx`, the `.pdf`, the `.pptx`
      and `presentation.html`. `make_figures.py` re-run as a check — all four figures byte-identical,
      `data/results/` unchanged.
- [x] `.gitignore` extended for Office lock files (`~$*`), `.claude/*.lock` and the transient render
      scratch file, without hiding any research artifact.

## Cross-artifact consistency

Checked across `submission_report.md`, `10_report.md`, the deck, the video script and `README.md`:

- [x] 0.719 · 0.808 · 0.831 · +0.437 · +0.381 · +0.089 · −0.033 · r = +0.71 · 6/10 · 9,269 · $3.12
- [x] The `VO-D` caveat (behavioural convergence, not a clean isolation of style) appears in all five.
- [x] The sample-size deviation appears in all five, with no invented reason.
- [x] Post-hoc status stated wherever the §4.3 / §5 numbers appear.
- [x] Future Work is the same three-stage trajectory everywhere.
- [x] The methodological contribution is described as a **necessary-but-insufficient** diagnostic
      everywhere — never as a validated benchmark.
- [x] Authors, affiliations and the GitHub URL identical everywhere.

## Still open by design — not blockers

1. The `VO-D`/`VO-E` screening date and screener (`AUTHOR_CONFIRMATION_REQUIRED.md` §2.2).
2. The reason for the sample-size step-down (§2.3). **Must not be reconstructed.**
3. No committed script for the ad-hoc manipulation-check overlap figures or the post-hoc length
   analysis (`A9_post_hoc_audit.md` §5.1). Both are labelled in-text as computed ad hoc, and the
   definitions needed to reproduce them are recorded.
4. `Track3_Strategy_Doc_Research_Focused.docx` and the three `notes/message*.txt` chats are kept
   because `02` and `03` cite them by name. Whether they belong in a public repository is an author
   call — see `FINAL_REPO_AUDIT.md` §6.

## The authors do the last step

Nothing in this pass was committed or pushed. Review the tree, then commit and push yourselves.
