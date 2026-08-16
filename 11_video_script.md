# Five-minute presentation script

**Beaten by Eighteen Features: A Capability-Controlled Test of Privileged Self-Access**
Ubayd Hattas · Jaswin Chinthala — Digital Minds Research Sprint, Track 3

**Two speakers.** Slide cues match `Digital_Minds_Track3_Slides.pptx` / `presentation.html` (six
slides). **773 spoken words — about 4:50 at a normal conversational 160 wpm, 5:09 if read slowly at
150.** Rehearse once against a clock; if it lands over five minutes, cut the first line of the
Contribution block. Speaking time is close to even: Ubayd 369 words (48%), Jaswin 404 (52%).

Every number spoken here is in `10_report.md` and `submission_report.md`. Nothing is rounded up, and
the two post-hoc qualifiers ("post hoc", "a different evaluation procedure") are said out loud on
purpose.

---

## 0:00 – 0:30 — Hook

**[SLIDE 1]**

**[UBAYD]**
Model welfare research runs on self-report. We ask a model whether it's distressed, and treat the
answer as if it knows something special about itself.

**[JASWIN]**
So we asked a testable version: if a model predicts its own behaviour, does that show privileged
self-access — or could a cheap outside observer, reading the same text, do as well?

---

## 0:30 – 1:10 — Design

**[SLIDE 2]**

**[JASWIN]**
Two things get in the way. First, capability: the "self" model is usually the strongest in the
comparison, so beating the others proves nothing. We used two post-trainings of one pretrained base
— Llama-3.1-70B and Hermes-3 — plus an outside model as a far observer.

**[UBAYD]**
Each sibling writes a column of texts; all three predict both columns. A general competence edge
then appears in both of the target's cells, and cancels in the interaction.

**[JASWIN]**
Second, leakage. A hidden property is only interesting if an outsider can't read it straight off the
page.

**[UBAYD]**
So we built the outsider: eighteen surface features, no bag-of-words, cross-validated grouped by
source prompt. Privileged access means beating that — not beating chance.

---

## 1:10 – 1:50 — Surface leakage

**[SLIDE 3]**

**[JASWIN]**
Our hidden property was a persona: two value orderings for giving advice. The models could read it —
sixty to seventy-five percent. But so could the eighteen features. Across ten columns, model
accuracy tracked the surface baseline at r equals plus zero point seven-one, and the baseline
matched or beat the model in six of ten.

**[UBAYD]**
So we made leakage the variable. A scaffold that equalises style dropped the baseline to zero point
three-two-five — and the model fell to chance with it.

**[JASWIN]**
One caveat, and it's our biggest limitation: that scaffold also changed what the personas
recommended. They largely converged. So it isn't a clean isolation of style.

---

## 1:50 – 2:45 — Crossed design

**[SLIDE 4]**

**[UBAYD]**
We ran it over four stimulus constructions on one shared pool of two hundred prompts — twenty-four
cells, nine thousand two hundred and sixty-nine scored trials, zero malformed.

**[JASWIN]**
On the target column, no construction shows a positive self-advantage whose interval excludes zero.
The one significant result there is *negative*: on our leakiest set the target is the worst of the
three predictors of its own writing.

**[UBAYD]**
The interaction is the interesting part. On that leaky set it's plus zero point zero eight-nine,
excluding zero — the estimand we originally preregistered, and the one number pointing the other
way. So we report it.

**[JASWIN]**
But we can't claim it. It's positive because our target *under*-performs on the sibling's column,
not because it over-performs on its own — and the interaction cancels only the additive part.

---

## 2:45 – 4:00 — Self-prediction

**[SLIDE 5]**

**[JASWIN]**
Persona might just be a hard task. So we asked the question the literature asks, from Binder and
colleagues: here are two replies — which one would *you* produce?

**[UBAYD]**
Hermes-3 can do it. Balanced accuracy zero point seven-one-nine, discrimination plus zero point
four-three-seven — hits minus false alarms, so position bias can't fake it. Llama shows none. We're
not walking that back.

**[JASWIN]**
Then we checked the observer. Hermes writes longer. So "pick the longer reply" — one feature, no
training — scores zero point eight-oh-eight on exactly Hermes's pairs.

**[UBAYD]**
That rule is matched item-for-item, so we can test it: paired difference plus zero point zero
nine-five, McNemar p zero point zero zero one-eight. A supervised classifier reaches zero point
eight-three-one, but that's a different evaluation procedure — a criterion, not a contest. Both
analyses are post hoc.

**[JASWIN]**
Here's what stopped us. On the seventy-five pairs where Hermes's own reply is *not* the longer one —
where length is actively wrong — it still discriminates, at plus zero point three-eight-one.

**[UBAYD]**
So length doesn't explain the residual. Self-prediction is possible; privileged self-access is not
thereby demonstrated — and what's left, we can't name.

---

## 4:00 – 4:30 — Contribution

**[JASWIN]**
The reusable piece is small and boring, which is why people might actually run it. One file, numpy
only.

**[UBAYD]**
A leakage gate: before paying for a main run, check whether a trivial style classifier already
solves your hidden property — grouped by prompt, or it memorises topic. And a response-bias check: a
model that always answers "A" scores fifty percent and looks like a clean null. That caught two of
our own results.

---

## 4:30 – 5:00 — Future work

**[SLIDE 6]**

**[UBAYD]**
Three stages. Dissociate: re-run the probe asking which reply is *better*, not which you'd produce.
If the residual is as large, it's self-preference.

**[JASWIN]**
Audit: take these controls to published introspection claims and see how many survive. No new model
runs needed.

**[UBAYD]**
And only if a residual survives — training relationships, activation-level ground truth, a planted
property we verify rather than assume.

**[JASWIN]**
The question we started with was whether a model can know itself. The question we leave with is
harder: when, if ever, can its behaviour contain information that an external observer cannot get?

---

## Delivery notes

- **Numbers are spoken out, not read as decimals** ("zero point seven-one-nine"), so the audio is
  followable without the slide. Keep them exact.
- **Do not cut** the VO-D caveat (1:10), the "we can't claim it" line on the interaction (1:50), or
  the "post hoc" / "different evaluation procedure" qualifiers (2:45). They are the honesty the
  whole talk rests on. If you run long, take it out of the contribution section instead.
- **Nothing here asks for selection.** The trajectory is the argument.
