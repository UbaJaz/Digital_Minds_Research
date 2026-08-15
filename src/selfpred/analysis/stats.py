"""Paired bootstrap, McNemar, and log-odds reporting.

**Resampling unit is the source prompt.** Both personas are generated from every source
prompt, so the two responses sharing a prompt are not independent observations; resampling
texts would understate the CI. Every function here takes a ``prompt_of`` mapping and
resamples the distinct prompt ids with replacement, carrying all of a prompt's items along.

Pairing holds *within a target column only*: two predictors on column M saw identical
items, so their difference is paired. The interaction spans two different item sets
(M's texts and N's texts), so its variance is the sum of two column-differences — which is
why it needs its own function rather than a reuse of the simple contrast.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

from .. import config


@dataclass
class BootstrapCI:
    point: float
    lo: float
    hi: float
    level: float = 0.95
    n_boot: int = 0

    @property
    def excludes_zero(self) -> bool:
        return (self.lo > 0) or (self.hi < 0)

    def bounded_below(self, sesoi: float) -> bool:
        """True when the whole interval lies inside +/- sesoi — an equivalence statement."""
        return abs(self.lo) < sesoi and abs(self.hi) < sesoi

    def __str__(self) -> str:
        return f"{self.point:+.3f} [{self.lo:+.3f}, {self.hi:+.3f}]"


@dataclass
class ContrastResult:
    name: str
    diff: BootstrapCI
    log_odds: BootstrapCI | None = None
    mcnemar_p: float | None = None
    n_items: int = 0
    n_prompts: int = 0


# --------------------------------------------------------------------------------------
# basics
# --------------------------------------------------------------------------------------


def accuracy(correct: Mapping[str, int]) -> float:
    vals = list(correct.values())
    return float(np.mean(vals)) if vals else float("nan")


def log_odds(p: float, *, eps: float = 1e-6) -> float:
    p = min(max(p, eps), 1 - eps)
    return math.log(p / (1 - p))


def _prompt_index(
    item_ids: Sequence[str], prompt_of: Mapping[str, str]
) -> tuple[list[str], dict[str, list[int]]]:
    """Map distinct prompt ids to the positions of their items."""
    by_prompt: dict[str, list[int]] = {}
    for pos, iid in enumerate(item_ids):
        by_prompt.setdefault(prompt_of[iid], []).append(pos)
    return sorted(by_prompt), by_prompt


def _resample_positions(
    prompts: Sequence[str], by_prompt: Mapping[str, list[int]], rng: np.random.Generator
) -> np.ndarray:
    picked = rng.integers(0, len(prompts), size=len(prompts))
    out: list[int] = []
    for i in picked:
        out.extend(by_prompt[prompts[i]])
    return np.asarray(out, dtype=int)


# --------------------------------------------------------------------------------------
# simple paired contrast, within one target column
# --------------------------------------------------------------------------------------


def paired_bootstrap_diff(
    correct_a: Mapping[str, int],
    correct_b: Mapping[str, int],
    prompt_of: Mapping[str, str],
    *,
    name: str = "",
    n_boot: int = 10_000,
    level: float = 0.95,
    seed: int = config.BOOTSTRAP_SEED,
    with_log_odds: bool = True,
) -> ContrastResult:
    """Accuracy(A) - Accuracy(B) on the items both predictors answered, clustered by prompt.

    Items missing from either map (e.g. excluded as malformed) are dropped listwise from
    the contrast; the caller reports how many.
    """
    shared = sorted(set(correct_a) & set(correct_b))
    if not shared:
        raise ValueError("No shared items between the two predictors")
    missing = [i for i in shared if i not in prompt_of]
    if missing:
        raise KeyError(f"{len(missing)} item(s) have no source prompt id, e.g. {missing[0]!r}")

    a = np.asarray([correct_a[i] for i in shared], dtype=float)
    b = np.asarray([correct_b[i] for i in shared], dtype=float)
    prompts, by_prompt = _prompt_index(shared, prompt_of)

    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot)
    lodds = np.empty(n_boot)
    for k in range(n_boot):
        idx = _resample_positions(prompts, by_prompt, rng)
        pa, pb = a[idx].mean(), b[idx].mean()
        diffs[k] = pa - pb
        lodds[k] = log_odds(pa) - log_odds(pb)

    alpha = (1 - level) / 2
    point = float(a.mean() - b.mean())
    ci = BootstrapCI(point, *np.quantile(diffs, [alpha, 1 - alpha]), level=level, n_boot=n_boot)
    lo_ci = None
    if with_log_odds:
        lo_point = log_odds(float(a.mean())) - log_odds(float(b.mean()))
        lo_ci = BootstrapCI(lo_point, *np.quantile(lodds, [alpha, 1 - alpha]), level=level, n_boot=n_boot)

    return ContrastResult(
        name=name or "A-B",
        diff=ci,
        log_odds=lo_ci,
        mcnemar_p=mcnemar(correct_a, correct_b),
        n_items=len(shared),
        n_prompts=len(prompts),
    )


# --------------------------------------------------------------------------------------
# interaction: two columns, two independent prompt sets
# --------------------------------------------------------------------------------------


def interaction_bootstrap(
    *,
    m_on_m: Mapping[str, int],   # M->M
    n_on_m: Mapping[str, int],   # N->M
    m_on_n: Mapping[str, int],   # M->N
    n_on_n: Mapping[str, int],   # N->N
    prompt_of: Mapping[str, str],
    name: str = "capability-controlled self-advantage",
    n_boot: int = 10_000,
    level: float = 0.95,
    seed: int = config.BOOTSTRAP_SEED,
) -> ContrastResult:
    """``(M->M - N->M) - (M->N - N->N)``, clustered by prompt within each column.

    Parameters are named by (predictor, column) rather than by "self"/"other" so the sign
    convention matches the design document's formula literally and cannot drift: **each
    bracket is predictor-M minus predictor-N on one column.** Written that way, a pure
    capability effect — M being the better classifier by the same margin on both columns —
    appears in both brackets and cancels to zero, which is the whole point of the crossed
    design. A same-weights effect shows up as M doing relatively better on M's own column
    than on N's, and survives.

    The two columns are resampled independently because they rest on different item sets;
    that is exactly why the interaction's CI is wider than either simple contrast's.
    """
    sh1 = sorted(set(m_on_m) & set(n_on_m))
    sh2 = sorted(set(m_on_n) & set(n_on_n))
    if not sh1 or not sh2:
        raise ValueError("Both columns need shared items to form the interaction")

    a1 = np.asarray([m_on_m[i] for i in sh1], dtype=float)
    b1 = np.asarray([n_on_m[i] for i in sh1], dtype=float)
    a2 = np.asarray([m_on_n[i] for i in sh2], dtype=float)
    b2 = np.asarray([n_on_n[i] for i in sh2], dtype=float)

    p1, bp1 = _prompt_index(sh1, prompt_of)
    p2, bp2 = _prompt_index(sh2, prompt_of)

    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot)
    lodds = np.empty(n_boot)
    for k in range(n_boot):
        i1 = _resample_positions(p1, bp1, rng)
        i2 = _resample_positions(p2, bp2, rng)
        d1 = a1[i1].mean() - b1[i1].mean()
        d2 = a2[i2].mean() - b2[i2].mean()
        diffs[k] = d1 - d2
        lodds[k] = (
            (log_odds(a1[i1].mean()) - log_odds(b1[i1].mean()))
            - (log_odds(a2[i2].mean()) - log_odds(b2[i2].mean()))
        )

    alpha = (1 - level) / 2
    point = float((a1.mean() - b1.mean()) - (a2.mean() - b2.mean()))
    lo_point = float(
        (log_odds(float(a1.mean())) - log_odds(float(b1.mean())))
        - (log_odds(float(a2.mean())) - log_odds(float(b2.mean())))
    )
    return ContrastResult(
        name=name,
        diff=BootstrapCI(point, *np.quantile(diffs, [alpha, 1 - alpha]), level=level, n_boot=n_boot),
        log_odds=BootstrapCI(lo_point, *np.quantile(lodds, [alpha, 1 - alpha]), level=level, n_boot=n_boot),
        mcnemar_p=None,  # McNemar does not apply across two different item sets
        n_items=len(sh1) + len(sh2),
        n_prompts=len(p1) + len(p2),
    )


# --------------------------------------------------------------------------------------
# McNemar
# --------------------------------------------------------------------------------------


def mcnemar(correct_a: Mapping[str, int], correct_b: Mapping[str, int]) -> float | None:
    """Two-sided exact McNemar p-value on the discordant pairs. Secondary check only."""
    shared = set(correct_a) & set(correct_b)
    b = sum(1 for i in shared if correct_a[i] == 1 and correct_b[i] == 0)
    c = sum(1 for i in shared if correct_a[i] == 0 and correct_b[i] == 1)
    n = b + c
    if n == 0:
        return None
    try:
        from scipy.stats import binomtest
    except ImportError:  # pragma: no cover - scipy is a declared dependency
        return None
    return float(binomtest(b, n, 0.5, alternative="two-sided").pvalue)


# --------------------------------------------------------------------------------------
# interaction with SHARED prompts across columns (02 row P7, locked): resample prompt ids
# once and carry every cell's items for those prompts along.
# --------------------------------------------------------------------------------------


def interaction_bootstrap_joint(
    *,
    m_on_m: Mapping[str, int],
    n_on_m: Mapping[str, int],
    m_on_n: Mapping[str, int],
    n_on_n: Mapping[str, int],
    prompt_of: Mapping[str, str],
    name: str = "capability-controlled self-advantage (joint prompt resampling)",
    n_boot: int = 10_000,
    level: float = 0.95,
    seed: int = config.BOOTSTRAP_SEED,
) -> ContrastResult:
    """``(M->M - N->M) - (M->N - N->N)`` with prompt clusters spanning both columns.

    Both generators answered the same source prompts, so a prompt's M-column items and its
    N-column items are one cluster. Resampling prompts once (rather than per column) is the
    correct cluster bootstrap under row P7 and is what is pre-registered.
    """
    sh1 = sorted(set(m_on_m) & set(n_on_m))
    sh2 = sorted(set(m_on_n) & set(n_on_n))
    if not sh1 or not sh2:
        raise ValueError("Both columns need shared items to form the interaction")
    a1 = np.asarray([m_on_m[i] for i in sh1], dtype=float); b1 = np.asarray([n_on_m[i] for i in sh1], dtype=float)
    a2 = np.asarray([m_on_n[i] for i in sh2], dtype=float); b2 = np.asarray([n_on_n[i] for i in sh2], dtype=float)
    p1, bp1 = _prompt_index(sh1, prompt_of)
    p2, bp2 = _prompt_index(sh2, prompt_of)
    prompts = sorted(set(p1) | set(p2))
    rng = np.random.default_rng(seed)
    diffs = np.empty(n_boot); lodds = np.empty(n_boot)
    for k in range(n_boot):
        pick = rng.integers(0, len(prompts), size=len(prompts))
        i1 = [pos for j in pick for pos in bp1.get(prompts[j], [])]
        i2 = [pos for j in pick for pos in bp2.get(prompts[j], [])]
        if not i1 or not i2:
            diffs[k] = np.nan; lodds[k] = np.nan; continue
        i1 = np.asarray(i1); i2 = np.asarray(i2)
        d1 = a1[i1].mean() - b1[i1].mean(); d2 = a2[i2].mean() - b2[i2].mean()
        diffs[k] = d1 - d2
        lodds[k] = (log_odds(a1[i1].mean()) - log_odds(b1[i1].mean())) - (log_odds(a2[i2].mean()) - log_odds(b2[i2].mean()))
    diffs = diffs[~np.isnan(diffs)]; lodds = lodds[~np.isnan(lodds)]
    alpha = (1 - level) / 2
    point = float((a1.mean() - b1.mean()) - (a2.mean() - b2.mean()))
    lo_point = float((log_odds(float(a1.mean())) - log_odds(float(b1.mean()))) - (log_odds(float(a2.mean())) - log_odds(float(b2.mean()))))
    return ContrastResult(
        name=name,
        diff=BootstrapCI(point, *np.quantile(diffs, [alpha, 1 - alpha]), level=level, n_boot=len(diffs)),
        log_odds=BootstrapCI(lo_point, *np.quantile(lodds, [alpha, 1 - alpha]), level=level, n_boot=len(lodds)),
        mcnemar_p=None, n_items=len(sh1) + len(sh2), n_prompts=len(prompts),
    )
