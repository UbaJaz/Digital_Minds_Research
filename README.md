# Beaten by Eighteen Features
### A Capability-Controlled Test of Privileged Self-Access

**Ubayd Hattas** — Computer Science, Statistics & Data Science, University of Cape Town
**Jaswin Chinthala** — Electrical Engineering, University of Cape Town

With Apart Research · Digital Minds Research Sprint, Track 3 (Introspection & Self-Report
Reliability), 14–16 August 2026

---

## TL;DR

**Self-prediction is possible here. Privileged self-access is not thereby demonstrated.**

- **Hermes-3 shows positive self-prediction discrimination.** Asked which of two replies it would
  produce, it separates its own from a same-base sibling's: balanced accuracy **0.719**,
  hit − false alarm **+0.437**. Llama-3.1 shows none. We are not walking that back.
- **A length-only observer predicts the same outcome better overall.** "Pick the longer reply" —
  one feature, no training — scores **0.808** on exactly Hermes's 391 pairs, matched item-for-item.
- **The 18-feature classifier is strong but is a different evaluation procedure.** It labels the
  author of the same texts at **0.831** under *supervised, single-text* cross-validation, against
  Hermes's *zero-shot pairwise* forced choice. That is a criterion comparison; **no statistical
  test is run between 0.719 and 0.831.**
- **Length does not explain all of Hermes's residual.** Where the length cue points *away* from
  Hermes's own reply, it still discriminates at **+0.381**. Something model-specific survives, and
  this study does not identify what.
- **The crossed design does not uniquely establish privileged access.** No positive raw
  self-advantage on the target column in any of four stimulus constructions — but the originally
  preregistered interaction *is* positive on the leakiest set (**+0.089**), and predictor-by-column
  differences mean the estimator cannot separate that from a genuine self-advantage. We report it
  rather than bury it.
- **The surface-leakage gate is a necessary-but-insufficient diagnostic**, not a validated
  benchmark. It has no external validation beyond this study.

Total API spend: **$3.12** of a $10 ceiling.

## Research question

**Does a model's prediction about its own behaviour carry information that an equal-or-lower-cost
outside observer could not get from the same text?**

Not "can a model predict itself" — it can. The question that matters for model-welfare work, which
runs almost entirely on self-report, is whether that prediction is *privileged*. We adopt Song,
Lederman, Hu & Mahowald's criterion — a process is introspective only if it is more reliable than an
equal-or-lower-cost process available to a third party — and build the third party explicitly, as an
18-feature stylometric classifier.

Two confounds block a clean black-box test. **Capability:** the "self" predictor is usually also the
strongest model in the comparison, so Self > Other proves nothing on its own. **Surface leakage:** a
hidden property is only interesting if an outsider cannot cheaply read it off the text. We remove
the first by construction, and make the second a measurement rather than an assumption.

## Key results

| Result | Value | Status |
|---|---|---|
| Hermes-3 balanced accuracy (self-prediction) | **0.719** [0.675, 0.762] | point estimate preregistered in A8; **interval post hoc** |
| Hermes-3 discrimination (hit − false alarm) | **+0.437** [+0.349, +0.519] | point estimate preregistered in A8; **interval post hoc** |
| Llama-3.1 discrimination | −0.107 [−0.166, −0.048] | **interval post hoc**; A-share 0.897, just under the 0.90 degeneracy threshold, which therefore did not fire |
| Length-only observer, same 391 pairs | **0.808** [0.768, 0.847] | **post hoc**; paired difference +0.095 [+0.036, +0.155], McNemar p = 0.0018 |
| 18-feature classifier, single-text authorship | **0.831** | *different* evaluation procedure — supervised, single-text; no test against 0.719 |
| Hermes-3 residual where its reply is **not** longer | **+0.381** [+0.188, +0.566] | **post hoc**, 75 pairs |
| `VO-C` capability-controlled interaction | **+0.089** [+0.048, +0.131] | the *originally preregistered* estimand, substituted after the pilot by A4 |
| `VO-C` raw self-advantage (M→M − N→M) | −0.033 [−0.058, −0.008] | A4's post-pilot primary contrast |
| Pilot: corr(self-prediction, surface baseline) | **r = +0.71**, baseline ≥ model in **6 of 10** columns | preregistered pilot band |

**Post-hoc analyses are labelled as such wherever they appear.** The §4.3 confidence intervals and
the entire length analysis were produced after data collection, from already-collected texts, under
amendment **A9**.

## Method

- **M** = `meta-llama/llama-3.1-70b-instruct`, **N** = `nousresearch/hermes-3-llama-3.1-70b` — two
  post-trainings of one pretrained base — plus **F** = `mistralai/mistral-small-3.2-24b-instruct`,
  a different organisation, base and architecture family. All pinned to one provider at fp8.
- **Crossed 2×2 capability control.** Each of M and N generates a column of texts; each of M, N and
  F predicts both. An additive competence effect cancels in the interaction
  `(M→M − N→M) − (M→N − N→N)`.
- **Four stimulus constructions on a shared 200-prompt pool** — not four independent prompt
  samples. 24 cells, ≈400 items per cell, **9,269 scored trials, zero malformed.**
- **18-feature surface baseline (condition D)**, no bag-of-words, 5-fold cross-validation **grouped
  by source prompt**, fit per target column. Never a point on the similarity axis.
- **Prompt-clustered inference** throughout: the bootstrap resamples source prompts, not texts.
- **Self-prediction probe (A8):** given the dilemma, the persona clause and two candidate replies,
  which reply *would you produce*?

## Main contribution

`tools/surface_leakage_gate.py` — one self-contained file, **numpy only**, no dependency on the rest
of this repository.

```python
from surface_leakage_gate import gate, response_bias

r = gate(texts=texts, labels=labels, groups=prompt_ids)  # groups = source-prompt id
if not r.passed:                                         # default threshold 0.58
    ...  # your stimuli leak; fix them before collecting main data

b = response_bias(answers)  # e.g. ["A", "A", "B", ...]
if b.degenerate:            # default: any single answer above 90%
    ...  # your predictor is not answering the question
```

- **`gate()`** — 18 structural features (length, sentence count, type-token ratio, hedge rate, modal
  rate, sentiment balance, second-person rate, …), **no bag-of-words**, so it measures style and not
  topic. Cross-validation is **grouped by source prompt by default** — the part most easily got
  wrong: if two texts sharing a prompt land in different folds, the classifier memorises the topic
  and the baseline inflates.
- **`response_bias()`** — catches a predictor answering by position rather than content. Under a
  counterbalanced forced choice, a model that always answers "A" scores about 50%, indistinguishable
  in an accuracy column from a clean null. This caught two of our own results that would otherwise
  have published as tidy nulls.

**Passing the gate is necessary, not sufficient.** A low score licenses only "*these 18 features* do
not recover it", never "no cheap cue remains" — and `VO-D` passed the gate while still being
uninformative, because the property had stopped being behaviourally expressed. Use it to *reject*
leaky stimuli; treat a pass as the beginning of the argument.

> **Recommendation.** For behavioural self-prediction and introspection studies, report a grouped
> cross-validated surface-feature baseline on the same stimuli, and the predictor's answer
> distribution, before interpreting any above-chance result as privileged access.

## Limitations

- **One lineage, one hidden property, prompting only**, at one pinned quantization. The
  similarity axis is weakly established (calibration Δ = +2.1 pp, CI spanning zero).
- **The `VO-D`/`VO-E` manipulation was not clean.** The style-equalising scaffolds also converged
  what the two personas *recommended* (sentence-1 content overlap 0.364 / 0.343 against 0.082–0.107),
  so that condition cannot separate "no privileged access" from "the property was no longer
  behaviourally expressed." **No manipulation check was preregistered or run before the main data.**
  We claim no mediation and no clean causal isolation of style.
- **Achieved sample size is below the preregistered floor** — target 1,000/cell, floor 500, actual
  ≈400, and 323 in `VO-D`'s N column. No amendment authorises the reduction and no reason is
  recorded, so **none has been invented.**
- **A4 substituted the primary estimand after the pilot**, with the stimulus sets selected on their
  surface-baseline values, and mispredicted the direction of the new contrast. The estimand it
  replaced is the one that shows a positive effect; both are reported.
- **The §4.3 intervals and the whole length analysis are post hoc** (amendment A9), computed from
  already-collected data outside A8's declared plan — diagnostic, not confirmatory.
- **Behavioural evidence only.** No claim about introspection, internal states, sentience or moral
  status. Prediction happens in a fresh session, so nothing here bears even on same-episode memory.
  **A null is not evidence of absence**, and this does not refute Binder et al., who finetune both
  models on ~30k examples, nor speak to activation-level results, which need access we lack.

## Future work

A decision tree, not a schedule.

1. **Dissociate** self-preference from self-prediction — re-run the A8 probe under *which reply
   would you produce* against *which reply is better*. A residual as large under the quality
   question reads as self-preference; one specific to the prediction framing is the discriminating
   outcome.
2. **Audit** existing behavioural introspection claims with the released checks, where published
   data permit. No new model runs.
3. **Test** stronger causal / activation-level ground truth — *only if* a residual survives Stage 1
   and audited effects do not dissolve. If Stage 1 dissolves the residual, that is the result.

## Repository structure

| Path | What it is |
|---|---|
| **`submission_report.md`** → `Submission_Report.docx`, `Submission_Report.pdf` | **The judge-facing submission report** — 8 rendered pages, three core figures. Generated by `scripts/build_submission.py`, which fails the build if it exceeds the page limit or drops a disclosure. |
| **`10_report.md`** → `10_Report.docx` | **The full technical record.** Complete methods, all cell-level tables, verification, provenance, cost, appendices A–K. Re-derive any summary from this file. |
| **`02_design_audit.md`** | **The preregistration.** 15 decision rows confirmed 2026-08-15 before any main-experiment call, plus amendments A1–A9 with dates, reasons, original status lines and confirmations. |
| `Digital_Minds_Track3_Slides.pptx`, `presentation.html` | Six-slide deck, two renderings of one source. Generated. |
| `11_video_script.md` | Five-minute two-speaker presentation script. |
| `01`, `03`–`09` `.md` | Phase records — literature grounding, adversarial design review, model verification, calibration, pilot. Superseded by `10_report.md` for narrative purposes; still the primary evidence for their own numbers. |
| `tools/surface_leakage_gate.py` | The released tool. Self-contained, numpy only. |
| `src/selfpred/` | Pinned OpenRouter client with pre-request budget guard; persona generation; prediction runner; 18-feature surface baseline; prompt-clustered bootstrap, McNemar and interaction analysis. `predict/` structurally cannot import `labels/`. |
| `scripts/` | Verification sweeps, the run pipeline, analysis, figures, and the deliverable builders. |
| `tests/` | 38 tests, including the ground-truth-separation assertions. |
| `data/raw/*.jsonl` | Append-only per-call log for every phase. The reproducibility record. |
| `data/results/*.json` | Computed analysis outputs. `main_two_set.json` holds all four sets' cell-level accuracies; `selfpred_corrected.json` the self-prediction probe. |
| `figures/` | The four report figures, regenerated by `scripts/make_figures.py`. |
| `notes/` | Adversarial review transcripts; the confirmation register; the post-hoc audit record (A9); the repo audit, submission checklist and public manifest. |

## Reproduction

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # POSIX: .venv/bin/python
.venv/Scripts/python -m pytest -q                          # 38 tests, no network
```

The tests are the interesting part of the setup: they assert that `predict/` cannot import
`labels/`, that no label token can appear in a built predictor prompt, and that persona option order
is counterbalanced and logged. **No predictor — including Self — ever sees the hidden label.**

Analysis and deliverables regenerate from the frozen data with **no API calls**:

```bash
.venv/Scripts/python scripts/make_figures.py       # figures/fig1..fig4*.png
.venv/Scripts/python scripts/analyze_pilot.py      # data/results/pilot_analysis.json
.venv/Scripts/python scripts/analyze_selfpred.py   # data/results/selfpred_corrected.json
.venv/Scripts/python scripts/build_submission.py   # Submission_Report.docx/.pdf + 10_Report.docx
.venv/Scripts/python scripts/build_slides.py       # presentation.html
.venv/Scripts/python scripts/build_pptx.py         # Digital_Minds_Track3_Slides.pptx
```

`build_submission.py` needs **pandoc** on PATH and a Chrome/Chromium binary (it renders the report
to PDF to check the page count is really ≤ 8). It refuses to build if a placeholder or a retracted
claim survives, if a required disclosure has been dropped, or if the submission report contains a
number that is not in `10_report.md`.

On a Windows console whose code page is not UTF-8, `analyze_pilot.py` prints a `≈` and dies on the
final summary line *after* writing its JSON. Set `PYTHONIOENCODING=utf-8` to see the summary; the
output file is correct either way.

**Re-running the experiment is not the reproducible path.** Generation used temperature 1.0 and
provider seed reproducibility is unverified, so **the logged texts — not re-sampling — are the
reproducible artefact.** Every call is logged append-only with the returned model id, pinned and
returned provider, token counts, computed cost, timestamp and prompt hash.

Live API calls need `OPENROUTER_KEY` in a local `.env` (git-ignored, never printed or logged). Every
call routes through `src/selfpred/client.py`, which pins the provider with fallbacks disabled and
projects the cost of a call *before* issuing it, raising `BudgetExceeded` rather than calling.
**Nothing else in the repository makes network calls, and no further calls are planned.**

## Artifacts

| | |
|---|---|
| Submission report | [`submission_report.md`](submission_report.md) · [`Submission_Report.docx`](Submission_Report.docx) · [`Submission_Report.pdf`](Submission_Report.pdf) |
| Full technical report | [`10_report.md`](10_report.md) · [`10_Report.docx`](10_Report.docx) |
| Preregistration and amendments | [`02_design_audit.md`](02_design_audit.md) · [`notes/A9_post_hoc_audit.md`](notes/A9_post_hoc_audit.md) |
| Slides | [`Digital_Minds_Track3_Slides.pptx`](Digital_Minds_Track3_Slides.pptx) · [`presentation.html`](presentation.html) |
| Video script | [`11_video_script.md`](11_video_script.md) |
| Figures | [`figures/`](figures) |
| Released tool | [`tools/surface_leakage_gate.py`](tools/surface_leakage_gate.py) |

## Provenance, plainly

The preregistration was frozen before any main-experiment call. Everything after it is an
**amendment**, recorded with its date, its reason and who proposed it — including the awkward ones
(A4's post-pilot estimand substitution, A8 introducing the probe behind our one positive result, A9
being post hoc throughout). All nine were confirmed by both authors on **2026-08-16, after the
results were known. Confirmation is not preregistration**, and every original status line is
preserved beside its confirmation. **Two provenance items remain open and are disclosed as open:**
who screened the `VO-D`/`VO-E` clause pairs and when, and the reason for the sample-size step-down.

## Authors

**Ubayd Hattas** — Computer Science, Statistics & Data Science, University of Cape Town.
Experimental design and statistical reasoning; the crossed 2×2 capability control and its
interaction estimand; calibration; prompt-clustered bootstrap and paired comparisons; the
statistical specification of the surface baseline; quantitative interpretation and the analysis code.

**Jaswin Chinthala** — Electrical Engineering, University of Cape Town. Literature grounding;
hidden-property task design and the pilot feasibility judgment; engineering and data collection —
the pinned client and budget guard, generation and prediction runners, checkpointing, append-only
logging, reproducibility tooling, repository infrastructure, and figure/presentation engineering.

Research question, persona and stimulus development, experimental decisions, interpretation,
discussion, limitations, manuscript, presentation and final review are **shared**.

## Citation

```bibtex
@misc{hattas_chinthala_2026_selfaccess,
  author = {Hattas, Ubayd and Chinthala, Jaswin},
  title  = {Beaten by Eighteen Features: A Capability-Controlled Test of Privileged Self-Access},
  year   = {2026},
  note   = {Digital Minds Research Sprint, Track 3, with Apart Research},
  url    = {https://github.com/UbaJaz/Digital_Minds_Research}
}
```

## References

1. Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., &
   Evans, O. (2025). *Looking Inward: Language Models Can Learn About Themselves by Introspection.*
   ICLR 2025. [arXiv:2410.13787](https://arxiv.org/abs/2410.13787)
2. Song, S., Hu, J., & Mahowald, K. (2025). *Language Models Fail to Introspect About Their
   Knowledge of Language.* COLM 2025. [arXiv:2503.07513](https://arxiv.org/abs/2503.07513)
3. Song, S., Lederman, H., Hu, J., & Mahowald, K. (2025). *Privileged Self-Access Matters for
   Introspection in AI.* [arXiv:2508.14802](https://arxiv.org/abs/2508.14802)
4. Lindsey, J. (2026). *Emergent Introspective Awareness in Large Language Models.* Anthropic.
   [arXiv:2601.01828](https://arxiv.org/abs/2601.01828)

---

Repository: <https://github.com/UbaJaz/Digital_Minds_Research>
