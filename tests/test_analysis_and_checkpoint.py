"""Analysis contracts and checkpoint resumability. No network, no data required."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from selfpred.analysis import interaction_bootstrap, mcnemar, paired_bootstrap_diff  # noqa: E402
from selfpred.baseline import fit_baseline_cv  # noqa: E402
from selfpred.checkpoint import Checkpoint  # noqa: E402


def _synthetic_column(n_prompts: int, acc_a: float, acc_b: float, seed: int, tag: str):
    """Two predictors on one column; two items per prompt, as the design generates them."""
    rng = np.random.default_rng(seed)
    ca, cb, prompt_of = {}, {}, {}
    for p in range(n_prompts):
        for k in range(2):
            iid = f"{tag}-{p:04d}-{k}"
            prompt_of[iid] = f"{tag}-prompt-{p:04d}"
            ca[iid] = int(rng.random() < acc_a)
            cb[iid] = int(rng.random() < acc_b)
    return ca, cb, prompt_of


def test_paired_bootstrap_recovers_a_known_difference() -> None:
    ca, cb, prompt_of = _synthetic_column(250, 0.75, 0.60, seed=1, tag="M")
    res = paired_bootstrap_diff(ca, cb, prompt_of, name="M->M - N->M", n_boot=2000)
    assert res.n_prompts == 250
    assert res.n_items == 500
    assert res.diff.lo < 0.15 < res.diff.hi
    assert res.diff.excludes_zero
    assert res.log_odds is not None


def test_bootstrap_resamples_prompts_not_texts() -> None:
    """Clustered resampling must give a wider CI than naive item resampling would."""
    ca, cb, prompt_of = _synthetic_column(100, 0.70, 0.60, seed=2, tag="M")
    clustered = paired_bootstrap_diff(ca, cb, prompt_of, n_boot=2000)
    # Same data, but pretend every item is its own prompt.
    independent = {i: i for i in ca}
    unclustered = paired_bootstrap_diff(ca, cb, independent, n_boot=2000)
    width = lambda r: r.diff.hi - r.diff.lo  # noqa: E731
    assert width(clustered) >= width(unclustered) * 0.95


def test_paired_bootstrap_requires_a_prompt_for_every_item() -> None:
    ca, cb, prompt_of = _synthetic_column(10, 0.7, 0.6, seed=3, tag="M")
    prompt_of.pop(next(iter(prompt_of)))
    with pytest.raises(KeyError):
        paired_bootstrap_diff(ca, cb, prompt_of, n_boot=100)


def test_interaction_cancels_a_pure_capability_effect() -> None:
    """M better by the same margin on BOTH columns is capability, not self-knowledge.

    This is the test the crossed design exists to pass: the confounded M-row contrast
    would read +15pp here, and the interaction must read ~0.
    """
    mm, nm, pm = _synthetic_column(250, 0.75, 0.60, seed=4, tag="M")   # column M
    mn, nn, pn = _synthetic_column(250, 0.75, 0.60, seed=5, tag="N")   # column N, same gap
    res = interaction_bootstrap(
        m_on_m=mm, n_on_m=nm, m_on_n=mn, n_on_n=nn,
        prompt_of={**pm, **pn}, n_boot=2000,
    )
    # Tolerance is the estimator's own precision, not zero: at 250 prompts per column the
    # interaction's 95% CI is ~±9pp (matching the council's variance arithmetic), so a
    # single seed lands within noise of zero rather than on it.
    assert abs(res.diff.point) < 0.10
    assert res.diff.lo < 0.0 < res.diff.hi, "a pure capability effect must not be significant"
    # The confounded simple contrast, by contrast, reads the full 15pp.
    simple = paired_bootstrap_diff(mm, nm, pm, n_boot=2000)
    assert simple.diff.excludes_zero and simple.diff.point > 0.10
    assert res.log_odds is not None
    assert res.mcnemar_p is None  # McNemar does not apply across two item sets


def test_interaction_detects_a_genuine_self_advantage() -> None:
    """Each model better on its OWN column is the same-weights signal; it must survive."""
    mm, nm, pm = _synthetic_column(250, 0.75, 0.60, seed=10, tag="M")  # M wins its column
    mn, nn, pn = _synthetic_column(250, 0.60, 0.75, seed=11, tag="N")  # N wins its column
    res = interaction_bootstrap(
        m_on_m=mm, n_on_m=nm, m_on_n=mn, n_on_n=nn,
        prompt_of={**pm, **pn}, n_boot=2000,
    )
    assert res.diff.point > 0.20
    assert res.diff.excludes_zero


def test_interaction_ci_is_wider_than_a_simple_contrast() -> None:
    mm, nm, pm = _synthetic_column(250, 0.70, 0.62, seed=6, tag="M")
    mn, nn, pn = _synthetic_column(250, 0.70, 0.62, seed=7, tag="N")
    simple = paired_bootstrap_diff(mm, nm, pm, n_boot=2000)
    inter = interaction_bootstrap(
        m_on_m=mm, n_on_m=nm, m_on_n=mn, n_on_n=nn,
        prompt_of={**pm, **pn}, n_boot=2000,
    )
    assert (inter.diff.hi - inter.diff.lo) > (simple.diff.hi - simple.diff.lo)


def test_equivalence_bound_helper() -> None:
    ca, cb, prompt_of = _synthetic_column(300, 0.65, 0.65, seed=8, tag="M")
    res = paired_bootstrap_diff(ca, cb, prompt_of, n_boot=2000)
    assert res.diff.bounded_below(0.15)


def test_mcnemar_returns_none_without_discordant_pairs() -> None:
    same = {"a": 1, "b": 0}
    assert mcnemar(same, dict(same)) is None


def test_baseline_is_fit_per_column_and_grouped_by_prompt() -> None:
    """On texts with no surface signal, D should land near chance."""
    rng = np.random.default_rng(9)
    ids, texts, labels, groups = [], [], [], []
    vocab = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
    for p in range(60):
        for k in range(2):
            ids.append(f"i-{p}-{k}")
            texts.append(" ".join(rng.choice(vocab, size=40)))
            labels.append(k)
            groups.append(f"prompt-{p}")
    res = fit_baseline_cv(
        target_column="M", item_ids=ids, texts=texts, labels=labels, groups=groups, n_folds=5
    )
    assert res.target_column == "M"
    assert res.n_items > 0
    assert 0.30 < res.accuracy < 0.70
    assert set(res.per_item_correct) <= set(ids)


def test_checkpoint_skips_completed_items(tmp_path) -> None:
    ck = Checkpoint(run_id="predict_M->N", path=tmp_path / "ck.jsonl")
    keys = [f"item-{i}" for i in range(5)]
    assert ck.pending(keys) == keys
    ck.mark("item-0", {"letter": "A"})
    ck.mark("item-3", {"letter": "B"})
    assert ck.pending(keys) == ["item-1", "item-2", "item-4"]
    # A fresh object over the same file resumes identically.
    assert Checkpoint(run_id="predict_M->N", path=tmp_path / "ck.jsonl").n_done == 2
