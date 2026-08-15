"""Predictor side of the pipeline.

**This package must never import from `selfpred.labels`.** A pytest asserts it. The
ground-truth label of an item is not available here by construction, so no predictor —
including the Self predictor — can receive it even by accident.

Prompts built here are parameterised by (predictor role, target column); nothing in this
package knows or cares which model generated the text, and predictors are not told.
"""

from .prompts import PredictorPrompt, build_predictor_prompt, option_order_for

__all__ = ["PredictorPrompt", "build_predictor_prompt", "option_order_for"]
