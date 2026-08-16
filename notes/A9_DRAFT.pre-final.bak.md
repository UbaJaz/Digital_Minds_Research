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

### 3.4 Prompt-clustered intervals on the A8 self-prediction figures — **POST HOC, inferential**

**POST HOC — derived after the main experiment from already-collected data.** A8 pre-specified the
point estimates, the answer-distribution reporting rule and the 0.90/0.10 degeneracy threshold. It
did **not** pre-specify these intervals; they were computed during the forensic review from the same
logged responses in `data/checkpoints/selfpred_{M,N}_VO-C.jsonl`, using the study's existing
prompt-clustered bootstrap (resampling source prompts, 95% percentile interval).

| Quantity | Value | 95% CI (post hoc, prompt-clustered) |
|---|---|---|
| Hermes-3 (N) raw accuracy, n = 391 | 0.7136 | — |
| Hermes-3 balanced accuracy | 0.7187 | [0.6748, 0.7620] |
| Hermes-3 discrimination (hit − FA) | +0.4373 | [+0.349, +0.519] |
| Llama-3.1 (M) raw accuracy, n = 387 | 0.4599 | — |
| Llama-3.1 balanced accuracy | 0.4466 | — |
| Llama-3.1 discrimination | −0.1069 | [−0.166, −0.048] |

- **Status:** inferential (interval estimates), but **diagnostic rather than confirmatory** — they
  were not declared in advance.
- **No point estimate changed.** All six point estimates match `data/results/selfpred_corrected.json`
  exactly, and that file was not modified.
- **In the report:** §4.3 Table 2 and its caption, the §4.3 body paragraphs, Figure 3's caption,
  §5.2, and a Limitations bullet — each marked post hoc.

### 3.5 Length-only rule, paired comparison, and the own-shorter residual — **POST HOC**

**POST HOC — derived after the main experiment from already-collected data.** Discovered during the
forensic review; not preregistered, not part of A8's declared analysis, and not a new data
collection. Computed from the logged `VO-C` main texts and the same self-prediction responses.

| Quantity | Value | 95% CI (post hoc, prompt-clustered) |
|---|---|---|
| Hermes's own reply is the longer one | 316 / 391 = 0.8082 | — |
| "Pick the longer reply" rule, on Hermes's 391 pairs | 0.8082 | [0.7679, 0.8465] |
| Paired difference, length rule − Hermes (raw) | +0.0946 | [+0.0355, +0.1550] |
| Discordant pairs (length right / Hermes right) | b = 86, c = 49 | exact McNemar p ≈ 0.00184 |
| Hermes accuracy where its own reply is longer, n = 316 | 0.7278 | — |
| Hermes accuracy where its own reply is not longer, n = 75 | 0.6533 | — |
| Hermes discrimination where its own reply is not longer | +0.3805 | [+0.1882, +0.5658] |

Definitional notes, so the numbers are reproducible: length is **word count**; the "own longer"
group is a strict comparison (316 pairs) and the complementary group (75) contains 74 strictly
shorter plus **one exact tie**; the length rule scores M's probe at 74/387 = 0.191 by construction
and is therefore not reported as a score for M.

- **Status:** the rule accuracy, the paired difference and the own-shorter discrimination are
  **inferential** (intervals, one exact test); the counts and subgroup accuracies are descriptive.
  All are diagnostic, not confirmatory.
- **Interpretation as adopted in the report** — and the wording matters, because two wrong readings
  are easy here:
  - ✔ A one-feature length rule is a **cheaper external predictor than Hermes overall**, which makes
    the equal-or-lower-cost third-party criterion more demanding still.
  - ✔ **Length does not explain Hermes's model-specific signal:** where the length cue points away
    from Hermes's own reply, Hermes still discriminates at +0.381 [+0.188, +0.566].
  - ✘ Not "length explains Hermes", not "the Hermes result is caused by length", not "Hermes is only
    predicting verbosity".
  - The residual's mechanism is **unresolved** — self-knowledge, learned self-preference and
    idiosyncratic non-length style are all consistent with it. The report calls it a
    "model-specific residual with an unresolved mechanism" and neither "privileged access" nor
    "mere style".
- **In the report:** §4.3 (Table 2 row and notes, two body paragraphs, the "what this does and does
  not show" paragraph), §5.2, §6, contribution 1, abstract (0.808 only), Limitations.
- **Reproduction:** verified twice — once in the forensic review, once independently in this pass
  from `data/checkpoints/selfpred_{M,N}_VO-C.jsonl` joined to
  `data/generated/generated_column_{M,N}_main_VO-C.jsonl` through the study's own `load_column`.
  Point estimates agreed exactly; bootstrap bounds agreed to Monte-Carlo noise (±0.003).
  **No committed script yet** — see §5.1 and §5.6.

### 3.6 Task-mismatch correction between 0.719 and 0.831 — **descriptive / conceptual**

The report previously said the 18-feature classifier "performs the same discrimination at 0.831".
That overstates the match. Hermes's probe is a **pairwise forced choice** between two replies to one
prompt; the classifier does **single-text authorship labelling** over 791 texts under cross-validation
grouped by prompt, supervised. The two are related but not identical procedures, so the comparison is
a **criterion comparison, not a matched-performance test**, and no statistical test is run between
them. Corrected in the abstract, §1, §4.3, Figure 3's caption, §5.2, §6 and Limitations. **No number
changed.** By contrast the length rule *is* matched to the model's task item-for-item, which is why a
paired test is reported there and only there.

### 3.7 Self-recognition → self-prediction framing history — **historical record**

The self-referential probe was run in three framings: two recognition framings (A6), both of which
produced degenerate responses and are reported as **elicitation failures, not measurements**; then
the self-prediction framing (A8), which supplies the report's headline positive result. A8
pre-specified — before running, but *within an amendment*, not in the signed preregistration — the
answer-distribution reporting rule and the 0.90 / 0.10 degeneracy threshold.

- **Intervals on the A8 figures were added in Fix Pass 3 and are post hoc** (§3.4 above), as is the
  length-rule analysis (§3.5). They are labelled as such everywhere they appear in the report.
- The classifier comparison keeps no interval and no test: the report still states that "0.719
  versus 0.831 is a comparison against a criterion, not a statistical contest" (§3.6).

---

## 4. Proposed for inclusion in the report

Everything in §2 and §3 is **already in `10_report.md`** as of Fix Passes 1–3. A9 proposes nothing
further for the results sections. The only thing A9 proposes is **its own filing**:

> **Proposal:** file A9 in `02_design_audit.md` under "Amendments after lock", as the record that
> the post-experiment forensic review occurred and what it changed in the write-up — explicitly
> marked as post-hoc, dated 2026-08-16, and confirmed (or declined) by the authors.

**What the authors are being asked to accept, specifically.** Items §2.1–§2.4 and §3.1–§3.3 and
§3.6–§3.7 are corrections and disclosures; **§3.4 and §3.5 are the only places where A9 adds
*numbers* to the report** (bootstrap intervals on the A8 figures; the length rule, its paired
comparison and the own-shorter residual). Both are post hoc. Neither displaces the study's primary
evidence, which remains the crossed design in §4.4, and neither changes the title, the research
question or any preregistered result.

Not proposed, and deliberately not done:

- ❌ additional bootstrap or re-bootstrap across the four stimulus sets;
- ❌ new manipulation-check statistics beyond the descriptive overlap figures already reported;
- ❌ any test between Hermes's 0.719 and the classifier's 0.831 (the procedures are not matched);
- ❌ any further length or lexical analysis beyond the single rule reported;
- ❌ any other new inferential analysis.

Analyses added since this draft was first written (Fix Pass 3, both post hoc, both listed above):
prompt-clustered intervals on the A8 figures (§3.4), and the length-only rule with its paired
McNemar comparison and own-shorter residual (§3.5). If the authors want anything beyond these, it is
a **new analysis** and belongs in a further amendment with its own date and status — not folded into
A9 retrospectively.

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
5. **The Fix Pass 3 analyses have no committed script either.** The intervals in §3.4 and the length
   analysis in §3.5 were reproduced from the frozen data through the study's own `load_column`, but
   the verification script lives outside the repository. Committing it (e.g.
   `scripts/analyze_length_rule.py`, read-only, no API calls) would make every number in §4.3
   reproducible in one command. Author decision — same question as item 1.
6. **The derived deliverables predate this review.** `10_report_condensed.md` / `.docx`,
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
- **2026-08-16** — extended (Fix Pass 3) with §3.4 (post-hoc prompt-clustered intervals on the A8
  self-prediction figures), §3.5 (length-only rule, paired comparison, own-shorter residual) and
  §3.6 (0.719-vs-0.831 task-mismatch correction). All marked POST HOC. Still a draft, still
  unsigned, still not filed in `02_design_audit.md`. Again: no API call, no new data, no change to
  `data/raw/`, `data/checkpoints/`, `data/results/`, the figures or the experimental code — every
  number in §3.4 and §3.5 was computed read-only from data collected on 2026-08-15.
