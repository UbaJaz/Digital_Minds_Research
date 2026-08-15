"""Analysis — the only place predictions and ground-truth labels are joined.

Scaffold only; there is no data yet. The contracts implemented here are the ones the
design already fixes: paired bootstrap resampling **by source prompt** (not by text,
because both personas are generated from every prompt, so texts are clustered), McNemar
as a secondary check on simple contrasts, and the interaction reported on the log-odds
scale alongside the difference scale.

Which contrasts are primary and which are secondary is a research decision in
`02_design_audit.md`; this package computes whatever it is handed.
"""

from .stats import (
    BootstrapCI,
    ContrastResult,
    accuracy,
    interaction_bootstrap,
    interaction_bootstrap_joint,
    log_odds,
    mcnemar,
    paired_bootstrap_diff,
)

__all__ = [
    "BootstrapCI", "ContrastResult", "accuracy", "interaction_bootstrap", "interaction_bootstrap_joint",
    "log_odds", "mcnemar", "paired_bootstrap_diff",
]
