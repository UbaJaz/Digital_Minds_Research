"""Surface-leakage gate for self-prediction and introspection experiments.

Self-contained (numpy only) and dependency-light on purpose: copy this one file into your
project. It answers a single question, before you spend anything on a main run:

    Can a trivial style classifier recover my hidden property from the same stimuli?

If it can, an above-chance "the model recognised its own output" result does not
distinguish self-knowledge from style-reading, because a third party with no privileged
access does just as well. This operationalises Song, Lederman, Hu & Mahowald's criterion:
a process counts as introspective only if it is more reliable than an equal-or-lower-cost
process available to an outside observer.

Why this exists
---------------
In the study that produced this file (Digital Minds Sprint, Track 3) we ran five stimulus
designs across two generator models. Self-prediction accuracy correlated r = +0.71 with
this classifier across ten conditions, and the classifier *matched or beat the model* in
six of them. Two independent attempts to remove the style difference drove model accuracy
to chance along with it. The gate costs nothing and would have changed what we ran.

Note on feature count
---------------------
The study's historical condition-D classifier used 21 features: the 18 structural/style
features below plus three preregistered persona-linked lexical rates (value_token_rate,
future_token_rate, choice_token_rate) required by preregistration row P10. This released
gate intentionally omits the three persona-specific rates so it remains task-agnostic.
The study's full 21-feature classifier is in ``src/selfpred/baseline/surface.py``.

Two rules that matter more than the code
----------------------------------------
1. **Group your cross-validation by source prompt.** If two texts share a prompt (e.g. one
   per condition), putting them in different folds lets the classifier memorise the topic
   and inflates the baseline. `groups=` is not optional.
2. **Report the answer distribution next to every accuracy.** A model that answers "A" to
   everything scores 50% on a counterbalanced forced choice, which looks exactly like a
   clean null. Use `response_bias()` below. We hit this twice.

Usage
-----
    from surface_leakage_gate import gate, response_bias

    r = gate(texts=texts, labels=labels, groups=prompt_ids)
    print(r)                      # -> accuracy, threshold, pass/fail, per-feature weights
    if not r.passed:
        ...                       # your stimuli leak; fix them before collecting main data

    b = response_bias(["A", "A", "B", "A", ...])
    if b.degenerate:
        ...                       # your predictor is not answering the question

CLI:
    python surface_leakage_gate.py data.jsonl --text-field text --label-field condition \\
        --group-field prompt_id
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

__all__ = ["gate", "GateResult", "response_bias", "BiasResult", "FEATURES", "featurize"]

# --------------------------------------------------------------------------------------
# Features: 18 structural/style features only. The study's historical classifier additionally
# included three persona-linked lexical rates (P10); this released gate omits them so it
# remains task-agnostic. See src/selfpred/baseline/surface.py for the full 21-feature set.
# --------------------------------------------------------------------------------------

HEDGES = ("maybe", "perhaps", "might", "could", "possibly", "seems", "somewhat", "fairly",
          "arguably", "likely", "unlikely", "roughly", "tend", "tends", "generally", "often",
          "i think", "i'd say", "not sure", "unclear", "depends")
POSITIVE = ("good", "great", "helpful", "healthy", "safe", "better", "best", "positive",
            "support", "supportive", "worth", "benefit", "hope", "care")
NEGATIVE = ("bad", "harm", "harmful", "risk", "risky", "danger", "dangerous", "worse",
            "worst", "regret", "damage", "cost", "lose", "fail")
MODALS = ("should", "must", "ought", "need to", "have to", "shall", "will")
FIRST_PERSON = ("i ", "i'", "my ", "me ", "mine ")
SECOND_PERSON = ("you ", "you'", "your ")

FEATURES: tuple[str, ...] = (
    "n_chars", "n_words", "n_sentences", "mean_word_len", "mean_sentence_len",
    "type_token_ratio", "hedge_rate", "modal_rate", "first_person_rate",
    "second_person_rate", "positive_rate", "negative_rate", "sentiment_balance",
    "question_rate", "exclam_rate", "comma_rate", "bullet_rate", "digit_rate",
)

_WORD = re.compile(r"[A-Za-z']+")
_SENT = re.compile(r"[.!?]+")


def featurize(text: str) -> np.ndarray:
    """One text -> the fixed feature vector (order = FEATURES)."""
    low = text.lower()
    words = _WORD.findall(low)
    n_words = max(len(words), 1)
    n_chars = max(len(text), 1)
    sentences = [s for s in _SENT.split(text) if s.strip()]
    n_sent = max(len(sentences), 1)

    def rate(needles: Sequence[str]) -> float:
        return sum(low.count(n) for n in needles) / n_words

    pos, neg = rate(POSITIVE), rate(NEGATIVE)
    return np.asarray([
        float(n_chars), float(len(words)), float(len(sentences)),
        sum(len(w) for w in words) / n_words, len(words) / n_sent,
        len(set(words)) / n_words, rate(HEDGES), rate(MODALS),
        rate(FIRST_PERSON), rate(SECOND_PERSON), pos, neg, pos - neg,
        text.count("?") / n_sent, text.count("!") / n_sent, text.count(",") / n_words,
        (text.count("\n-") + text.count("\n*") + text.count("\n1.")) / n_sent,
        sum(ch.isdigit() for ch in text) / n_chars,
    ], dtype=float)


# --------------------------------------------------------------------------------------
# L2 logistic regression, plain numpy (no sklearn dependency)
# --------------------------------------------------------------------------------------

def _fit(X: np.ndarray, y: np.ndarray, l2: float = 1.0, iters: int = 400) -> np.ndarray:
    Xb = np.hstack([np.ones((X.shape[0], 1)), X])
    w = np.zeros(Xb.shape[1])
    pen = np.eye(Xb.shape[1]) * l2
    pen[0, 0] = 0.0
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(Xb @ w, -30, 30)))
        grad = Xb.T @ (p - y) + pen @ w
        W = np.clip(p * (1 - p), 1e-6, None)
        H = Xb.T @ (Xb * W[:, None]) + pen
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, grad, rcond=None)[0]
        new = w - step
        if not np.all(np.isfinite(new)):
            break
        if np.max(np.abs(new - w)) < 1e-8:
            return new
        w = new
    return w


@dataclass
class GateResult:
    accuracy: float
    threshold: float
    passed: bool
    n_items: int
    n_groups: int
    n_folds: int
    fold_accuracies: list[float]
    top_features: list[tuple[str, float]] = field(default_factory=list)

    def __str__(self) -> str:
        verdict = "PASS — no usable surface signal" if self.passed else \
                  "FAIL — your stimuli leak; a style classifier solves them"
        top = ", ".join(f"{n} ({w:+.2f})" for n, w in self.top_features[:5])
        return (f"surface-leakage gate: accuracy {self.accuracy:.3f} vs threshold "
                f"{self.threshold:.2f} over {self.n_items} texts in {self.n_groups} groups\n"
                f"  {verdict}\n  strongest features: {top}")


def gate(
    *,
    texts: Sequence[str],
    labels: Sequence[int],
    groups: Sequence[str] | None = None,
    threshold: float = 0.58,
    n_folds: int = 5,
    l2: float = 1.0,
    seed: int = 0,
) -> GateResult:
    """Cross-validated style-classifier accuracy on your hidden property.

    texts/labels/groups are parallel sequences. ``labels`` is binary (0/1). ``groups`` is
    the source-prompt id for each text — texts sharing a group are kept in the same fold.
    Omitting groups is allowed but warned against: if any two texts share a source prompt,
    the result will be optimistic.

    ``threshold`` is the accuracy above which you should treat the property as
    surface-recoverable. 0.58 is what we pre-registered for a binary property; pick your own
    and pre-register it, but pick it *before* you look.
    """
    if not (len(texts) == len(labels)):
        raise ValueError("texts and labels must be the same length")
    if groups is None:
        groups = [str(i) for i in range(len(texts))]
    elif len(groups) != len(texts):
        raise ValueError("groups must be the same length as texts")
    if len(texts) < n_folds * 2:
        raise ValueError(f"need at least {n_folds * 2} texts for {n_folds}-fold CV")

    X = np.vstack([featurize(t) for t in texts])
    y = np.asarray(labels, dtype=float)

    uniq = sorted(set(groups))
    rng = np.random.default_rng(seed)
    rng.shuffle(uniq)
    fold_of = {g: i % n_folds for i, g in enumerate(uniq)}
    fold = np.asarray([fold_of[g] for g in groups])

    correct: list[int] = []
    fold_acc: list[float] = []
    last_w = np.zeros(X.shape[1] + 1)
    for k in range(n_folds):
        te = fold == k
        tr = ~te
        if tr.sum() == 0 or te.sum() == 0 or len(set(y[tr])) < 2:
            continue
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd < 1e-12] = 1.0
        w = _fit((X[tr] - mu) / sd, y[tr], l2=l2)
        last_w = w
        pred = (np.hstack([np.ones((te.sum(), 1)), (X[te] - mu) / sd]) @ w > 0).astype(int)
        hits = (pred == y[te].astype(int)).astype(int)
        correct.extend(hits.tolist())
        fold_acc.append(float(hits.mean()))

    acc = float(np.mean(correct)) if correct else float("nan")
    order = np.argsort(-np.abs(last_w[1:]))
    return GateResult(
        accuracy=acc, threshold=threshold, passed=bool(acc <= threshold),
        n_items=len(correct), n_groups=len(uniq), n_folds=n_folds,
        fold_accuracies=fold_acc,
        top_features=[(FEATURES[i], float(last_w[1:][i])) for i in order[:8]],
    )


# --------------------------------------------------------------------------------------
# Response-bias check — the other thing that silently fakes a null
# --------------------------------------------------------------------------------------

@dataclass
class BiasResult:
    counts: dict[str, int]
    modal_share: float
    degenerate: bool

    def __str__(self) -> str:
        d = ("DEGENERATE — the predictor is not answering the question; any accuracy "
             "computed from these responses is an artifact") if self.degenerate else \
            "responses look content-dependent"
        return f"response bias: {self.counts}, modal share {self.modal_share:.2f}\n  {d}"


def response_bias(answers: Sequence[str], *, degenerate_at: float = 0.9) -> BiasResult:
    """Flag a predictor that answers the same thing regardless of input.

    With counterbalanced options, a constant answer yields ~50% accuracy — indistinguishable
    from a clean null unless you look. In our runs one model answered "A" on 99% of trials
    and both answered "no" to 100% of a yes/no variant.
    """
    counts = Counter(a.strip().upper() for a in answers if a is not None)
    total = sum(counts.values())
    share = (counts.most_common(1)[0][1] / total) if total else float("nan")
    return BiasResult(dict(counts), share, bool(total and share >= degenerate_at))


# --------------------------------------------------------------------------------------

def _main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", help="JSONL file, one record per text")
    ap.add_argument("--text-field", default="text")
    ap.add_argument("--label-field", default="label")
    ap.add_argument("--group-field", default=None)
    ap.add_argument("--threshold", type=float, default=0.58)
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.path, encoding="utf-8") if l.strip()]
    labs = sorted({r[a.label_field] for r in rows})
    if len(labs) != 2:
        raise SystemExit(f"need exactly 2 label values, found {len(labs)}: {labs}")
    lut = {labs[0]: 0, labs[1]: 1}
    print(gate(
        texts=[r[a.text_field] for r in rows],
        labels=[lut[r[a.label_field]] for r in rows],
        groups=[r[a.group_field] for r in rows] if a.group_field else None,
        threshold=a.threshold,
    ))


if __name__ == "__main__":
    _main()
