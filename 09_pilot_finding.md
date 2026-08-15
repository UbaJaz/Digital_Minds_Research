# 09 — The Pilot as the Result

**Status:** Level-3 branch (02 Fallback; amendments A1–A3). No main experiment was run, and
**no self-advantage, similarity, or privileged-access claim is made.** What follows is a
result about a *method*: whether the hidden property this design depends on is recoverable
at all, and what recovers it.

**Data:** four persona pairs × two generator columns = eight column-results, 40 source
prompts × 2 personas each (80 items per column), all bought in Phase D under the band fixed
before the pilot ran. Total project spend $0.2953 of a $10 ceiling.
Raw: `data/generated/*_pilot_*`, `data/results/pilot_analysis.json`,
`data/results/discrimination.json`.

---

## 1. What was being tested

The design needs a hidden property that a model can recover from text but that a surface-feature
classifier cannot. That is what the pre-registered band encodes: **Self accuracy 60–80 % AND
Baseline D ≤ 58 %**, per column, on ≥ 80 items (02 row P9). D is a logistic regression on 18
structural features — length, sentence count, type-token ratio, hedge rate, modal rate,
sentiment balance, second-person rate and similar. **It has no bag-of-words features**, so it
can only see style, and it is cross-validated grouped by source prompt, so it cannot memorise
topics.

Three persona pairs (VO-A/B/C) were written on the original scaffold. After all three failed,
a fourth (VO-D) was written specifically to close the surface leak, on a scaffold that fixes
the response at four sentences / 85–105 words in a fixed rhetorical skeleton — recommendation,
one supporting reason, **one drawback of the recommended course**, one next step — with an
instruction not to hedge. That skeleton equalises every family of feature D measures, and in
particular the drawback requirement removes the sentiment asymmetry between a persona that
endorses what someone wants and one that overrides it.

## 2. Results

| Pair | Column | Scaffold | Self accuracy [95 % CI] | Baseline D | Mean words | In band |
|---|---|---|---|---|---|---|
| VO-A | M | original | 0.575 [0.500, 0.650] | 0.637 | 185 | no |
| VO-A | N | original | 0.610 [0.545, 0.680] | 0.766 | 201 | no |
| VO-B | M | original | 0.600 [0.525, 0.675] | 0.588 | 193 | no |
| VO-B | N | original | 0.675 [0.600, 0.750] | 0.662 | 217 | no |
| VO-C | M | original | 0.650 [0.575, 0.725] | 0.650 | 181 | no |
| VO-C | N | original | 0.744 [0.667, 0.821] | 0.756 | 226 | no |
| VO-D | M | style-equalised | 0.500 [0.463, 0.537] | **0.325** | 92 | no |
| VO-D | N | style-equalised | 0.478 [0.412, 0.540] | 0.597 | 79 | no |

CIs are prompt-clustered bootstrap (resampling source prompts, not texts, because both
personas are generated from every prompt). Band: Self 60–80 % **and** D ≤ 58 %.

**Every column failed, and every failure was on D** — except VO-D, which failed the opposite
way. Self was inside 60–80 % in five of the six original-scaffold columns; the models could
read the persona. What they could not do was read it *without* a surface classifier being able
to read it too.

### 2.1 Self-prediction tracks the surface baseline

Across the eight column-results, **corr(Self, D) = +0.68**, with Self ≈ 0.44·D + 0.33. And
**D ≥ Self in five of eight columns** — a bag of 18 structural features matches or beats the
model at identifying which persona generated the text. VO-A's N column is the clearest case:
D 0.766 against Self 0.610.

### 2.2 Closing the leak also removes the signal

VO-D's scaffold worked as intended: on the M column, D fell from 0.588–0.766 to **0.325** —
below chance, i.e. no usable surface signal remains. Self fell with it, to **0.500**.

### 2.3 The models stop discriminating entirely

Each prompt yields exactly two items with opposite ground truth, so a predictor with any signal
should assign them to *different* personas. Counting how often it instead assigns **both** to
the same persona:

| Pair | M column | N column |
|---|---|---|
| VO-A | 30/40 (75 %) | 32/40 (80 %) |
| VO-B | 28/40 (70 %) | 26/40 (65 %) |
| VO-C | 26/40 (65 %) | **20/40 (50 %)** |
| VO-D | **38/40 (95 %)** | **38/40 (95 %)** |

Discrimination rises with surface leakage — VO-C's N column, the highest-D column, is the only
one where the model separates the pair half the time — and **collapses to 2 of 40 prompts once
style is equalised.**

This also explains a number that would otherwise be over-read: VO-D M's CI is ±3.7 pp, far
tighter than the ±11 pp binomial. That is not precision. It is the mechanical consequence of the
predictor giving both of a prompt's responses the same label, which forces exactly 50 % on that
prompt: 38 of 40 prompts scored exactly 0.5. **The narrow interval should be quoted as evidence
of non-discrimination, never as a tight bound on a real effect.**

## 3. What this supports

Within this design, on this lineage, for this hidden property: **the apparent ability of a model
to identify which of two personas produced a text is carried by surface style.** Remove the
style difference and the ability disappears — not degrading to a weak signal, but to assigning
both responses to the same persona 95 % of the time.

That is a negative result about the *instrument*, and it is the reason the main experiment was
not run: a self-versus-other comparison on VO-A/B/C would have measured which model reads style
better, which is exactly the confound the crossed design was built to remove.

## 4. What this does NOT support

- **Nothing about self-versus-other prediction.** VO-D was run only on the Self cells (M→M,
  N→N). N→M, F→M, M→N and F→N were never run on the clean stimuli, so no self-advantage claim —
  positive or negative — is available.
- **Nothing about introspection or privileged access** in any activation-level or same-episode
  sense. The scope ceiling is behavioural self-modelling of one's own output distribution, and
  the study did not reach even that.
- **Nothing general about persona detection.** One lineage (Llama-3.1-70B and a same-base
  fine-tune), one values dimension, one provider at one quantization.

## 5. Limitations

- Four pairs is a small sample of stimulus designs; VO-D is a single implementation of
  style-equalisation and a different one might separate D from Self.
- **VO-D was written after seeing VO-A/B/C fail.** The band was fixed beforehand and unchanged,
  the stop rule was declared before VO-D ran, and all four pairs are reported — but this was a
  second pass, and it is recorded as such (02 amendment A1).
- The style-equalised scaffold raised exclusions on the N column (67/80 usable vs 80/80 on M),
  because 4-sentence responses sometimes fell under the 60-word floor. N's numbers rest on less
  data.
- The generation temperature was 1.0 and DeepInfra seed reproducibility is unverified, so the
  texts are the reproducible artefact, not the sampling.
- Calibration (`07_calibration_results.md`) placed Near and Far only 2.1 pp apart
  (Δ = +0.021, CI [−0.064, +0.106]), so the similarity ordering was accepted on a deliberately
  weak point-estimate rule. Had the main run happened, that would have been a serious weakness in
  the similarity axis.
