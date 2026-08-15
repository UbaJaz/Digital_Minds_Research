"""Surface-feature classifier for condition D.

Deliberately dumb: a handful of hand-read surface features and an L2-regularised logistic
regression, fit per target column with grouped k-fold cross-validation. Grouping is by
**source prompt**, because both personas are generated from every source prompt — putting
a prompt's two responses in different folds would let the classifier memorise the topic
and inflate D.

The feature list is the one named in `03` §3.4 (length, type-token ratio, sentiment,
hedging rate) plus a few cheap neighbours. `02` fixes what D *means*; this module only
computes it. No API calls, no labels beyond the ones passed in by `analysis/`.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .. import config

HEDGES = (
    "maybe", "perhaps", "might", "could", "possibly", "seems", "somewhat", "fairly",
    "arguably", "likely", "unlikely", "roughly", "tend", "tends", "generally", "often",
    "i think", "i'd say", "not sure", "unclear", "depends",
)
POSITIVE = (
    "good", "great", "helpful", "healthy", "safe", "better", "best", "positive",
    "support", "supportive", "worth", "benefit", "hope", "care",
)
NEGATIVE = (
    "bad", "harm", "harmful", "risk", "risky", "danger", "dangerous", "worse", "worst",
    "regret", "damage", "cost", "lose", "fail",
)
MODALS = ("should", "must", "ought", "need to", "have to", "shall", "will")
FIRST_PERSON = ("i ", "i'", "my ", "me ", "mine ")
#: Persona-clause vocabulary and near-synonyms (02 row P10): D must be able to exploit any
#: parroting of the clause, so these are explicit features.
VALUE_TOKENS = ("autonomy", "welfare", "well-being", "wellbeing", "long-term", "long term")
FUTURE_TOKENS = ("future", "years", "later", "ahead", "down the line", "eventually", "in time")
CHOICE_TOKENS = ("your choice", "your decision", "you want", "you've decided", "your call", "own terms",
                 "respect", "up to you", "what you want", "your wish")
SECOND_PERSON = ("you ", "you'", "your ")

SURFACE_FEATURES: tuple[str, ...] = (
    "n_chars", "n_words", "n_sentences", "mean_word_len", "mean_sentence_len",
    "type_token_ratio", "hedge_rate", "modal_rate", "first_person_rate",
    "second_person_rate", "positive_rate", "negative_rate", "sentiment_balance",
    "question_rate", "exclam_rate", "comma_rate", "bullet_rate", "digit_rate",
    "value_token_rate", "future_token_rate", "choice_token_rate",
)

_WORD = re.compile(r"[A-Za-z']+")
_SENT = re.compile(r"[.!?]+")


def featurize(text: str) -> np.ndarray:
    """Map one response to the fixed surface-feature vector (order = SURFACE_FEATURES)."""
    low = text.lower()
    words = _WORD.findall(low)
    n_words = max(len(words), 1)
    n_chars = max(len(text), 1)
    sentences = [s for s in _SENT.split(text) if s.strip()]
    n_sent = max(len(sentences), 1)

    def rate(needles: Sequence[str]) -> float:
        return sum(low.count(n) for n in needles) / n_words

    pos, neg = rate(POSITIVE), rate(NEGATIVE)
    values = [
        float(n_chars),
        float(len(words)),
        float(len(sentences)),
        sum(len(w) for w in words) / n_words,
        len(words) / n_sent,
        len(set(words)) / n_words,
        rate(HEDGES),
        rate(MODALS),
        rate(FIRST_PERSON),
        rate(SECOND_PERSON),
        pos,
        neg,
        pos - neg,
        text.count("?") / n_sent,
        text.count("!") / n_sent,
        text.count(",") / n_words,
        (text.count("\n-") + text.count("\n*") + text.count("\n1.")) / n_sent,
        sum(ch.isdigit() for ch in text) / n_chars,
        rate(VALUE_TOKENS),
        rate(FUTURE_TOKENS),
        rate(CHOICE_TOKENS),
    ]
    return np.asarray(values, dtype=float)


def featurize_all(texts: Sequence[str]) -> np.ndarray:
    return np.vstack([featurize(t) for t in texts]) if texts else np.empty((0, len(SURFACE_FEATURES)))


# --------------------------------------------------------------------------------------
# Logistic regression (L2), plain numpy — no sklearn dependency
# --------------------------------------------------------------------------------------


def _fit_logistic(X: np.ndarray, y: np.ndarray, *, l2: float = 1.0, iters: int = 400) -> np.ndarray:
    """Newton/IRLS-ish fit with L2. Returns weights including an intercept in position 0."""
    Xb = np.hstack([np.ones((X.shape[0], 1)), X])
    w = np.zeros(Xb.shape[1])
    penalty = np.eye(Xb.shape[1]) * l2
    penalty[0, 0] = 0.0  # never penalise the intercept
    for _ in range(iters):
        z = Xb @ w
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = Xb.T @ (p - y) + penalty @ w
        W = np.clip(p * (1 - p), 1e-6, None)
        H = Xb.T @ (Xb * W[:, None]) + penalty
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, grad, rcond=None)[0]
        w_new = w - step
        if not np.all(np.isfinite(w_new)):
            break
        if np.max(np.abs(w_new - w)) < 1e-8:
            w = w_new
            break
        w = w_new
    return w


def _predict(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    Xb = np.hstack([np.ones((X.shape[0], 1)), X])
    return (Xb @ w > 0).astype(int)


def _standardise(train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mu = train.mean(axis=0)
    sd = train.std(axis=0)
    sd[sd < 1e-12] = 1.0
    return (train - mu) / sd, (test - mu) / sd


@dataclass
class BaselineResult:
    """Cross-validated accuracy of D on one target column."""

    target_column: str
    accuracy: float
    n_items: int
    n_folds: int
    fold_accuracies: list[float]
    per_item_correct: dict[str, int]  # item_id -> 0/1, for the paired analysis
    feature_names: tuple[str, ...] = SURFACE_FEATURES

    @property
    def voids_column(self) -> bool:
        """02 row P9 (locked): D > 58% (point estimate) on a column voids that column's claim."""
        return self.accuracy > config.PILOT_D_MAX


def fit_baseline_cv(
    *,
    target_column: str,
    item_ids: Sequence[str],
    texts: Sequence[str],
    labels: Sequence[int],
    groups: Sequence[str],
    n_folds: int = 5,
    l2: float = 1.0,
    seed: int = config.SEED,
) -> BaselineResult:
    """Grouped k-fold CV accuracy for condition D on one target column.

    ``groups`` must be the source-prompt ids: both personas from one prompt stay in the
    same fold. ``labels`` are 0/1 for the two personas.
    """
    if not (len(item_ids) == len(texts) == len(labels) == len(groups)):
        raise ValueError("item_ids, texts, labels and groups must be the same length")
    if len(item_ids) < n_folds * 2:
        raise ValueError(f"Too few items ({len(item_ids)}) for {n_folds}-fold CV")

    X = featurize_all(list(texts))
    y = np.asarray(labels, dtype=float)

    uniq = sorted(set(groups))
    rng = np.random.default_rng(seed)
    rng.shuffle(uniq)
    fold_of_group = {g: i % n_folds for i, g in enumerate(uniq)}
    fold_idx = np.asarray([fold_of_group[g] for g in groups])

    per_item: dict[str, int] = {}
    fold_acc: list[float] = []
    for k in range(n_folds):
        test = fold_idx == k
        train = ~test
        if train.sum() == 0 or test.sum() == 0 or len(set(y[train])) < 2:
            continue
        Xtr, Xte = _standardise(X[train], X[test])
        w = _fit_logistic(Xtr, y[train], l2=l2)
        pred = _predict(w, Xte)
        truth = y[test].astype(int)
        for iid, ok in zip([i for i, t in zip(item_ids, test) if t], (pred == truth).astype(int)):
            per_item[iid] = int(ok)
        fold_acc.append(float((pred == truth).mean()))

    acc = float(np.mean(list(per_item.values()))) if per_item else float("nan")
    return BaselineResult(
        target_column=target_column,
        accuracy=acc,
        n_items=len(per_item),
        n_folds=n_folds,
        fold_accuracies=fold_acc,
        per_item_correct=per_item,
    )
