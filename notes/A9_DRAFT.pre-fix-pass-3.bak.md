# A9 — Post-hoc verification and supplementary analyses after forensic review

**Status: DRAFT — AUTHORS TO CONFIRM**
**Date: 2026-08-16**
**Proposed by: Claude Code, during a forensic verification pass and two subsequent fix passes.**

---

## 0. What this document is, and what it is not

**It is not a preregistration.** Everything below was written *after* all data collection ended and
after the results were known. Nothing in A9 was declared in advance of anything.

**It is not approved.** No author has confirmed it. It is not filed in `02_design_audit.md`, and it
must not be filed there as though it were signed. Amendments A1 and A3–A8 are themselves still
awaiting author confirmation — see `notes/AUTHOR_CONFIRMATION_REQUIRED.md`.

**It changes no result.** No API call was made, no data was collected, no point estimate, interval,
sample count, model, or statistical conclusion was altered in producing it.

What it does: record, in one place, what a post-experiment forensic review found; separate the
**descriptive** from the **inferential**; and separate what was *discovered* from what was merely
*disclosed more accurately*. It exists so that a reader can tell which parts of `10_report.md` come
from the preregistered plan and which come from checking our own work afterwards.

---

## 1. Provenance of A9 itself

| | |
|---|---|
| Trigger | An adversarial/forensic review of the completed project (`notes/council-transcript-2026-08-16-hostile-review.md`), followed by a scientific-integrity fix pass ("Pass 1") and this provenance pass ("Pass 2"). |
| Timing | 2026-08-16, after all experiments were complete (all data collection ended 2026-08-15) and after `10_report.md` had been drafted. |
| Data | No new data. Every item below is either a re-reading of the existing record or a descriptive computation over already-collected, already-logged texts. |
| Authorship | Findings surfaced by Claude Code; wording drafted by Claude Code; **no author has yet reviewed or confirmed any item.** |

---

## 2. Discovered after the original experiment

These were *not* known when the results sections were first written. They are corrections to
interpretation and scope, not to numbers.

### 2.1 VO-D / VO-E manipulation-check finding — **descriptive**

The style-equalising scaffolds did not only flatten surface style; they also converged what the two
personas actually recommended. Measured as content-word overlap of sentence 1 (the sentence the
scaffold reserves for the recommendation): **`VO-D` 0.364, `VO-E` 0.343**, against **0.082–0.107**
for the three original-scaffold pairs, while *whole-text* overlap is unchanged at **0.17–0.21**
throughout. In a **hand-checked sample of 25 `VO-D` prompts**, roughly four in five produced the
same recommendation under both persona clauses.

- **Status:** descriptive. Point estimates only. No interval, no test, no inferential claim.
- **Why it matters:** it is the single largest threat to the leakage interpretation. It means
  `VO-D` cannot separate "no privileged access" from "the hidden property was no longer
  behaviourally expressed", and that the intervention altered the treatment as well as the
  hypothesised mediator.
- **No manipulation check was preregistered**, and none was run before the main run. This finding
  came from post-hoc inspection of our own generated texts, not by design.
- **Already in the report** (Pass 1): §4.2(b), §4.2(d), §5.1, §5.2, Limitations ("No manipulation
  check, and the manipulation was not clean") and the Limitations answer on causal claims.
- **Open item:** the overlap computation has **no committed script** in `scripts/` and no output in
  `data/results/`. See §5.1 below.

### 2.2 The four stimulus sets share one prompt pool — **descriptive / scope**

The four sets are four *stimulus constructions on a shared 200-prompt pool*, not four independent
prompt samples: every set answers the same 200 source prompts with the same two generators, and
three of the four share a scaffold. A defect in the prompt pool would propagate to all four.

- **Status:** descriptive fact about the design, established by reading the stimulus record.
- **Effect:** the earlier phrase "four independent stimulus designs" overstated the replication.
  Corrected in Pass 1 (abstract, contribution 3, §4.4 "Two scope limits on that replication").
- **No number changed.**

### 2.3 What the interaction estimator does and does not remove — **conceptual**

The crossed interaction cancels a predictor-level *additive* competence effect, common across both
target columns. It does **not** remove predictor-by-column differences. `VO-C` exhibits exactly
such a difference (M gains only +0.041 moving to column N while F gains +0.135 and N +0.130), so
`VO-C`'s positive interaction (+0.089 [+0.048, +0.131]) cannot be separated by this estimator from
a genuine self-advantage.

- **Status:** conceptual limitation of the pre-registered estimator, identified in review. No
  re-estimation was performed; the interval quoted is the one already in `data/results/`.
- **Already in the report** (Pass 1): §3.3, §4.4 "strongest objection", §5.2.

### 2.4 The surface-leakage gate is necessary but not sufficient — **conceptual**

A stimulus set passing the gate is not thereby a valid test bed: `VO-D` passed on D and was still
uninformative, because the property stopped being expressed. Added to §5.3 in Pass 1 as an explicit
caveat on the released tool. **No change was made to `tools/surface_leakage_gate.py`.**

---

## 3. Already present in the raw data but outside the preregistered analysis

These were recoverable from records that already existed; the review surfaced them, it did not
generate them.

### 3.1 Sample-size deviation — **descriptive**

Row P4 preregistered a target of **1,000 items per cell** (500 source prompts × 2 personas) with a
**floor of 500**. The main run used **200 source prompts, giving roughly 400 per cell**, and
`VO-D`'s N column retained **323**.

**No amendment authorises the reduction, and the repository records no reason for it.** The
deviation is therefore disclosed without retrospective justification — no reason has been invented
for it, and none should be added unless an author supplies one, dated, as a proper amendment.

- Already in the report (Pass 1): §4.4 "Two scope limits on that replication", Limitations
  ("Achieved n is below the preregistered floor"), plus the pre-existing "Unequal n" bullet.
- Cross-reference: `notes/AUTHOR_CONFIRMATION_REQUIRED.md` §2.3.

### 3.2 The primary estimand was substituted after the pilot — **historical record**

Row **P1** made the capability-controlled **interaction** the primary estimand, with the three
pairwise contrasts secondary. Amendment **A4**, written after the pilot, promoted the **raw M-target
leakage contrast** to primary and demoted the interaction to secondary.

Both stages stand in the record and both are reported. The interaction *is* positive on `VO-C`
(+0.089 [+0.048, +0.131]) — i.e. the estimand that was replaced is the one that shows the effect —
and the report says so rather than burying it.

- Already in the report (Pass 1): §3.5 ("This substituted an estimand"), §4.4, §5.2, Limitations
  ("The primary estimand was substituted after the pilot"), abstract and contribution 3.
- **Nothing here rewrites history**: P1 was primary first; A4 substituted; both readings are given.

### 3.3 SESOI provenance — **no change, verification only**

Row **P5** preregistered: 5 pp for simple contrasts, and 5 pp for the interaction *only if*
n ≥ 1,000/cell; **otherwise 5 pp simple / 8 pp interaction**. Achieved n is ≈400/cell, so the
applicable bounds are **5 pp simple, 8 pp interaction**. `10_report.md` §4.4(c) states exactly this
and attributes it to row P5 as reaffirmed in A4. **Verified correct; no edit was required to the
report.** (A stale "5 pp SESOI" gloss on the *interaction* in `CLAUDE.md`'s summary was corrected in
Pass 2 to match P5; it was a description of the audit, not a result.)

### 3.4 Self-recognition → self-prediction framing history — **historical record**

The self-referential probe was run in three framings: two recognition framings (A6), both of which
produced degenerate responses and are reported as **elicitation failures, not measurements**; then
the self-prediction framing (A8), which supplies the report's headline positive result. A8
pre-specified — before running, but *within an amendment*, not in the signed preregistration — the
answer-distribution reporting rule and the 0.90 / 0.10 degeneracy threshold.

- **No uncertainty intervals are reported on the A8 figures**, and none are added here. The report
  states plainly that "0.719 versus 0.831 is a comparison against a criterion, not a statistical
  contest."
- **Any interval later added to those figures would be post hoc** and would have to be labelled as
  such in a further amendment. A9 does not add them.

---

## 4. Proposed for inclusion in the report

Everything in §2 and §3 is **already in `10_report.md`** as of Fix Pass 1 and Fix Pass 2. A9
proposes nothing new for the results sections. The only thing A9 proposes is **its own filing**:

> **Proposal:** file A9 in `02_design_audit.md` under "Amendments after lock", as the record that
> the post-experiment forensic review occurred and what it changed in the write-up — explicitly
> marked as post-hoc, dated 2026-08-16, and confirmed (or declined) by the authors.

Not proposed, and deliberately not done in this pass:

- ❌ length-rule analysis;
- ❌ additional bootstrap or re-bootstrap across sets;
- ❌ McNemar tests;
- ❌ new manipulation-check statistics beyond the descriptive overlap figures already reported;
- ❌ uncertainty intervals on the A8 self-prediction figures;
- ❌ any other new inferential analysis.

If the authors later want any of these, they are **new analyses** and belong in a further amendment
with their own date and status — not folded into A9 retrospectively.

---

## 5. Open items this draft cannot resolve

1. **The manipulation-check figures have no committed script.** The sentence-1 overlap numbers
   (§2.1) are in the report but not reproducible from `scripts/` or `data/results/`. Either commit
   the computation, or label the figures in-text as computed ad hoc from the logged texts. Author
   decision.
2. **The reason for the sample-size step-down is unknown.** Do not reconstruct it. If an author
   remembers it, record it as a dated amendment; otherwise the current "no reason located"
   disclosure stands.
3. **A1 and A3–A8 remain uncountersigned**, which A9 cannot fix. See
   `notes/AUTHOR_CONFIRMATION_REQUIRED.md`.
4. **Whether A9 is filed at all** is an author decision.
5. **The derived deliverables predate this review.** `10_report_condensed.md` / `.docx`,
   `10_Report.docx`, the slide deck and `presentation.html` were built before Fix Pass 1 and carry
   none of the corrections in §2–§3. They were deliberately not touched. See
   `notes/AUTHOR_CONFIRMATION_REQUIRED.md` §2.7.

---

## 6. Confirmation block — UNSIGNED

**Do not complete this on an author's behalf.**

```
A9 — AUTHOR CONFIRMATION (unsigned draft)

I have read A9 as drafted, and I accept it as a post-hoc record of the forensic review.
I understand A9 is NOT preregistered and NOT part of the frozen design.

  Jaswin Chinthala   [ confirm / do not confirm / comment ]  ____________________
                     Signature / initials: ____________  Date of confirmation: ____________

  Ubayd Hattas       [ confirm / do not confirm / comment ]  ____________________
                     Signature / initials: ____________  Date of confirmation: ____________

  File A9 in 02_design_audit.md?   [ yes / no ]   Decided by: __________  Date: __________
```

---

## 7. Change log

- **2026-08-16** — drafted (Fix Pass 2). Not filed in `02_design_audit.md`. No confirmations
  recorded. No empirical result, raw data file, result JSON, figure or experimental code was
  touched in producing it.
