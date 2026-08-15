"""Condition D — the surface-feature baseline.

D is a leakage check, never a point on the similarity axis (`02_design_audit.md`, locked).
It is fit **per target column** with k-fold cross-validation: a surface-solvable column
would void the self-advantage claim for that column, so one pooled D would hide exactly
the failure D exists to catch.
"""

from .surface import SURFACE_FEATURES, fit_baseline_cv, featurize

__all__ = ["SURFACE_FEATURES", "fit_baseline_cv", "featurize"]
