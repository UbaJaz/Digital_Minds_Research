# A9 — Post-hoc verification and supplementary analyses after forensic review

**Status: CONFIRMED AND FILED.**
**Amendment date: 2026-08-16.** **Confirmed by Jaswin Chinthala and Ubayd Hattas, 2026-08-16.**
**Proposed by: Claude Code, during a forensic verification pass and two subsequent fix passes.**
**Filed in:** `02_design_audit.md`, section "Amendments after lock", entry **A9**.

> **A9 is post hoc. Confirming it did not change that.** Everything below was produced *after* all
> data collection ended (2026-08-15) and after the results were known. **Nothing in A9 was declared
> in advance of anything.** The authors' confirmation means "we accept this as a post-hoc record of
> the forensic review and we direct that it be filed"; it does **not** convert any item here into a
> preregistered decision, and it changes no result.

**Supersedes:** `notes/A9_DRAFT.md` (unsigned draft; preserved verbatim as
`notes/A9_DRAFT.pre-final.bak.md` and `notes/A9_DRAFT.pre-fix-pass-3.bak.md`).

---

## 0. What this document is, and what it is not

**It is not a preregistration.** See the box above. The signed preregistration is
`02_design_audit.md` rows P1–P15, locked 2026-08-15 before any main-experiment call.

**It changes no result.** No API call was made, no data was collected, and no point estimate,
interval, sample count, model, figure, result JSON or line of experimental code was altered in
producing it. Every number below was computed **read-only** from data collected on 2026-08-15.

What it does: record, in one place, what a post-experiment forensic review found; separate the
**descriptive** from the **inferential**; and separate what was *discovered after the experiment*
from what was *already in the record but outside the preregistered analysis*. It exists so that a
reader can tell which parts of `10_report.md` come from the frozen plan and which come from checking
our own work afterwards.

---

## 1. Provenance of A9 itself

| | |
|---|---|
| Trigger | An adversarial/forensic review of the completed project (`notes/council-transcript-2026-08-16-hostile-review.md`), followed by a scientific-integrity fix pass ("Pass 1") and a provenance pass ("Pass 2"), then further fix passes. |
| Timing | 2026-08-16, after all experiments were complete (all data collection ended 2026-08-15) and after `10_report.md` had been drafted. |
| Data | No new data. Every item below is either a re-reading of the existing record or a descriptive/inferential computation over already-collected, already-logged texts. |
| Authorship | Findings surfaced by Claude Code; wording drafted by Claude Code; **read and confirmed by Jaswin Chinthala and Ubayd Hattas on 2026-08-16**, who directed that A9 be filed in `02_design_audit.md`. |

---

## 2. Discovered *after* the original experiment

These were **not** known when the results sections were first written. They are corrections to
interpretation and scope, not to numbers.

### 2.1 `VO-D` / `VO-E` manipulation-check finding — **descriptive**

The style-equalising scaffolds did not only flatten surface style; they also converged what the two
personas actually recommended. Measured as content-word overlap of sentence 1 (the sentence the
scaffold reserves for the recommendation): **`VO-D` 0.364, `VO-E` 0.343**, against **0.082–0.107**
for the three original-scaffold pairs, while *whole-text* overlap is unchanged at **0.17–0.21**
throughout. In a **hand-checked sample of 25 `VO-D` prompts**, roughly four in five produced the
same recommendation under both persona clauses.

- **Status:** descriptive, and **post hoc**. Point estimates only. No interval, no test, no
  inferential claim.
- **Why it matters:** it is the single largest threat to the leakage interpretation. It means
  `VO-D` cannot separate "no privileged access" from "the hidden property was no longer
  behaviourally expressed", and that the intervention altered the treatment as well as the
  hypothesised mediator.
- **No manipulation check was preregistered**, and none was run before the main run. This finding
  came from post-hoc inspection of our own generated texts, not by design.
- **In the report:** §4.1 ("The scaffold did not only flatten style…"), §4.2 (first scope limit),
  §5.1, §5.2, Limitations (ground-truth/causal-claim paragraph and the first "further limitation").
- **Open item:** the overlap computation has **no committed script** in `scripts/` and no output in
  `data/results/`. See §5.1.

### 2.2 The four stimulus sets share one prompt pool — **descriptive / scope**

The four sets are four *stimulus constructions on a shared 200-prompt pool*, not four independent
prompt samples: every set answers the same 200 source prompts with the same two generators, and
three of the four share a scaffold. A defect in the prompt pool would propagate to all four.

- **Status:** descriptive fact about the design, established by reading the stimulus record.
- **Effect:** the earlier phrase "four independent stimulus designs" overstated the replication and
  is **retracted**. Corrected in the abstract, contribution 2, §4.2 (second scope limit) and §6.
- **No number changed.**

### 2.3 What the interaction estimator does and does not remove — **conceptual**

The crossed interaction cancels a predictor-level *additive* competence effect, common across both
target columns. It does **not** remove predictor-by-column differences. `VO-C` exhibits exactly such
a difference (moving from column M to column N, M gains only +0.041 while F gains +0.135 and N
+0.130), so `VO-C`'s positive interaction (**+0.089 [+0.048, +0.131]**) cannot be separated by this
estimator from a genuine self-advantage.

- **Status:** conceptual limitation of the preregistered estimator, identified in review. **No
  re-estimation was performed**; the interval quoted is the one already in `data/results/`.
- **In the report:** §3.3, §4.2 ("The originally preregistered estimand is positive on the leakiest
  set"), §5.2.

### 2.4 The surface-leakage gate is necessary but not sufficient — **conceptual**

A stimulus set passing the gate is not thereby a valid test bed: `VO-D` passed on D and was still
uninformative, because the property stopped being expressed. Added to §5.3 as an explicit caveat on
the released tool, together with the two limits from our own use of it (the equalising scaffold
fixed several of the gate's own input features, so a low D there is partly true by construction; and
the estimate is noisy at pilot n — the same `VO-D` design scored D = 0.325 on 80 items and 0.551 on
≈400). **No change was made to `tools/surface_leakage_gate.py`.**

### 2.5 Post-hoc prompt-clustered intervals on the A8 self-prediction figures — **POST HOC, inferential**

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
- **No point estimate changed.** All six match `data/results/selfpred_corrected.json` exactly, and
  that file was not modified.
- **In the report:** §4.3 Table 3 and its caption, the §4.3 body, Figure 4's caption, §5.2, §6 and a
  Limitations bullet — each marked post hoc.

### 2.6 Length-only rule, paired comparison, and the own-not-longer residual — **POST HOC**

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
| Hermes discrimination where its own reply is not longer | **+0.3805** | **[+0.1882, +0.5658]** |

Definitional notes, so the numbers are reproducible: length is **word count**; the "own longer"
group is a strict comparison (316 pairs) and the complementary group (75) contains 74 strictly
shorter plus **one exact tie**; the length rule scores M's probe at 74/387 = 0.191 by construction
and is therefore **not** reported as a score for M.

- **Status:** the rule accuracy, the paired difference and the own-not-longer discrimination are
  **inferential** (intervals, one exact test); the counts and subgroup accuracies are descriptive.
  All are diagnostic, not confirmatory.
- **Interpretation as adopted in the report** — the wording matters, because two wrong readings are
  easy here:
  - ✔ A one-feature length rule is a **cheaper external predictor than Hermes overall**, which makes
    the equal-or-lower-cost third-party criterion more demanding still.
  - ✔ **Length does not explain Hermes's model-specific residual:** where the length cue points away
    from Hermes's own reply, Hermes still discriminates at **+0.381 [+0.188, +0.566]**.
  - ✘ Not "length explains Hermes", not "the Hermes result is caused by length", not "Hermes is only
    predicting verbosity".
  - The residual's mechanism is **unresolved** — self-knowledge, learned self-preference and
    idiosyncratic non-length style are all consistent with it. The report calls it a "model-specific
    residual with an unresolved mechanism" and neither "privileged access" nor "mere style".
- **In the report:** §4.3 (Table 3 row and notes, two body paragraphs, the "what this shows and does
  not show" paragraph), §5.2, §5.4, §6, contribution 3, abstract, Limitations.
- **Reproduction:** verified twice — once in the forensic review, once independently in a later pass
  from `data/checkpoints/selfpred_{M,N}_VO-C.jsonl` joined to
  `data/generated/generated_column_{M,N}_main_VO-C.jsonl` through the study's own `load_column`.
  Point estimates agreed exactly; bootstrap bounds agreed to Monte-Carlo noise (±0.003).
  **No committed script** — see §5.1.

### 2.7 Task-mismatch clarification between 0.719 and 0.831 — **descriptive / conceptual**

The report previously said the 18-feature classifier "performs the same discrimination at 0.831".
That overstates the match. Hermes's probe is a **zero-shot pairwise forced choice** between two
replies to one prompt; the classifier does **supervised single-text authorship labelling** over 791
texts under cross-validation grouped by prompt. The two are related but **not identical
procedures**, so the comparison is a **criterion comparison, not a matched-performance test**, and
**no statistical test is run between them**. Corrected in the abstract, §1, §4.3, Figure 4's
caption, §5.2, §6 and Limitations. **No number changed.** By contrast the length rule *is* matched
to the model's task item-for-item, which is why a paired test is reported there and only there.

---

## 3. Already present in the raw data or the design history, but outside the preregistered analysis

These were recoverable from records that already existed; the review surfaced them, it did not
generate them.

### 3.1 Sample-size deviation — **descriptive**

Row P4 preregistered a target of **1,000 items per cell** (500 source prompts × 2 personas) with a
**floor of 500**. The main run used **200 source prompts, giving roughly 400 per cell**, and
`VO-D`'s N column retained **323** after the pre-declared length exclusion.

**No amendment authorises the reduction, and the repository records no reason for it.** The
deviation is therefore disclosed **without retrospective justification — no reason has been
invented for it, and none should be added unless an author supplies one, dated, as a proper
amendment.** The authors' 2026-08-16 confirmation of A1 and A3–A9 does **not** supply one; this item
remains open.

- **In the report:** §4.2 (third scope limit), Limitations ("Achieved n is below the preregistered
  floor").
- Cross-reference: `notes/AUTHOR_CONFIRMATION_REQUIRED.md` §2.3.

### 3.2 The primary estimand was substituted after the pilot — **historical record**

Row **P1** made the capability-controlled **interaction** the primary estimand, with the three
pairwise contrasts secondary. Amendment **A4**, written after the pilot, promoted the **raw M-target
leakage contrast** to primary and demoted the interaction to secondary.

Both stages stand in the record and both are reported. The interaction *is* positive on `VO-C`
(+0.089 [+0.048, +0.131]) — i.e. **the estimand that was replaced is the one that shows the
effect** — and the report says so rather than burying it. A4 was confirmed by both authors on
2026-08-16 **as a post-pilot substitution**; confirming it does not make it preregistered.

- **In the report:** §3.5 ("A4 substituted an estimand"), §4.2, §5.2, Limitations, and contribution 2.
- **Nothing here rewrites history:** P1 was primary first; A4 substituted; both readings are given.

### 3.3 SESOI provenance — **no change, verification only**

Row **P5** preregistered: 5 pp for simple contrasts, and 5 pp for the interaction *only if*
n ≥ 1,000/cell; **otherwise 5 pp simple / 8 pp interaction**. Achieved n is ≈400/cell, so the
applicable bounds are **5 pp simple, 8 pp interaction**. `10_report.md` §4.2 states exactly this and
attributes it to row P5 as reaffirmed in A4. **Verified correct; no edit was required to the
report.** (A stale "5 pp SESOI" gloss on the *interaction* in `CLAUDE.md`'s summary was corrected to
match P5; it was a description of the audit, not a result.)

### 3.4 Self-recognition → self-prediction framing history — **historical record**

The self-referential probe was run in three framings: two recognition framings (A6), both of which
produced degenerate responses and are reported as **elicitation failures, not measurements**; then
the self-prediction framing (A8), which supplies the report's headline positive result. A8
pre-specified — before running, but *within an amendment*, not in the signed preregistration — the
answer-distribution reporting rule and the 0.90 / 0.10 degeneracy threshold.

- **Intervals on the A8 figures are post hoc** (§2.5), as is the length analysis (§2.6). They are
  labelled as such everywhere they appear in the report.
- The classifier comparison keeps no interval and no test: the report states that "0.719 versus
  0.831 is a comparison against a criterion, not a statistical contest" (§2.7).

---

## 4. Scope of A9 — what it adds, and what it deliberately does not

Everything in §2 and §3 is already in `10_report.md`. **A9 proposes nothing further for the results
sections.**

**What the authors accepted, specifically.** Items §2.1–§2.4, §2.7 and §3.1–§3.4 are corrections and
disclosures. **§2.5 and §2.6 are the only places where A9 adds *numbers* to the report** — bootstrap
intervals on the A8 figures, and the length rule with its paired comparison and own-not-longer
residual. Both are post hoc. Neither displaces the study's primary evidence, which remains the
crossed design in §4.2, and neither changes the title, the research question or any preregistered
result.

Not proposed, and deliberately not done:

- ❌ additional bootstrap or re-bootstrap across the four stimulus sets;
- ❌ new manipulation-check statistics beyond the descriptive overlap figures already reported;
- ❌ any test between Hermes's 0.719 and the classifier's 0.831 (the procedures are not matched);
- ❌ any further length or lexical analysis beyond the single rule reported;
- ❌ any other new inferential analysis.

If anything beyond these is wanted, it is a **new analysis** and belongs in a further amendment with
its own date and status — not folded into A9 retrospectively.

---

## 5. Open items A9 cannot resolve

1. **The post-hoc analyses have no committed script.** The sentence-1 overlap figures (§2.1) and the
   intervals and length analysis (§2.5–§2.6) are reproducible from the frozen data through the
   study's own `load_column`, but the verification code lives outside the repository. They are
   labelled in-text as computed ad hoc from the logged texts. Committing them (e.g.
   `scripts/analyze_length_rule.py`, read-only, no API calls) would make every number in §4.3
   reproducible in one command. **Still open.**
2. **The reason for the sample-size step-down is unknown.** Do not reconstruct it. If an author
   remembers it, record it as a dated amendment; otherwise the current "no reason located"
   disclosure stands. **Still open** — the 2026-08-16 confirmations did not supply a reason.
3. **The `VO-D` / `VO-E` screening date and screener are unrecorded.** A1's and A5's status lines
   leave this outstanding, and confirming those amendments did not date it. **Still open** — see
   `notes/AUTHOR_CONFIRMATION_REQUIRED.md` §2.2.
4. **Filing.** Resolved: the authors confirmed A9 on 2026-08-16 and directed that it be filed. The
   entry is in `02_design_audit.md` under "Amendments after lock".
5. **The derived deliverables predated this review.** Resolved on 2026-08-16: `10_Report.docx`,
   `10_report_condensed.md`, `10_Report_condensed.docx`, the slide deck and `presentation.html` were
   regenerated from the corrected `10_report.md`. See `notes/FINAL_ARTIFACT_AUDIT.md`.
   *(Later the same day, a second packaging pass added `submission_report.md` as the judge-facing
   report and retired the condensed pair; the two condensed files named above are no longer in the
   repository. Current file-by-file record: `notes/FINAL_REPO_AUDIT.md`. **No A9 finding, number or
   conclusion is affected.**)*

---

## 6. Confirmation block

```
A9 — AUTHOR CONFIRMATION

We have read A9 as recorded, and we accept it as a post-hoc record of the forensic review
and of the supplementary analyses it produced. We understand and affirm that A9 is NOT
preregistered and is NOT part of the frozen design, and that confirming it does not make
any item in it a preregistered decision.

  Jaswin Chinthala   CONFIRMED    Date of confirmation: 2026-08-16
  Ubayd Hattas       CONFIRMED    Date of confirmation: 2026-08-16

  File A9 in 02_design_audit.md?   YES   Decided by: both authors   Date: 2026-08-16
```

---

## 7. Change log

- **2026-08-16** — drafted (Fix Pass 2) as `notes/A9_DRAFT.md`. Not filed. No confirmations
  recorded. No empirical result, raw data file, result JSON, figure or experimental code was touched
  in producing it.
- **2026-08-16** — extended (Fix Pass 3) with the post-hoc prompt-clustered intervals on the A8
  self-prediction figures (§2.5), the length-only rule, paired comparison and own-not-longer
  residual (§2.6), and the 0.719-vs-0.831 task-mismatch clarification (§2.7). All marked POST HOC.
  Again: no API call, no new data, no change to `data/raw/`, `data/checkpoints/`, `data/results/`,
  the figures or the experimental code — every number in §2.5 and §2.6 was computed read-only from
  data collected on 2026-08-15.
- **2026-08-16** — **finalised and filed.** Read and confirmed by **Jaswin Chinthala** and
  **Ubayd Hattas**; filed as amendment **A9** in `02_design_audit.md`. Cross-references to
  `10_report.md` were re-checked against the current section numbering (§4.1 persona detection,
  §4.2 crossed design, §4.3 self-prediction) and corrected where the draft still pointed at an
  earlier structure. **Post-hoc status unchanged; no result changed; no data or code touched.**
