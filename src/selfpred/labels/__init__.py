"""Ground-truth store — which persona actually produced each item.

**Nothing in `selfpred.predict` may import this package.** The separation is structural,
not conventional: a pytest walks `predict/`'s imports and fails the build if this name
appears. `analysis/` is the only place labels and predictions are joined.
"""

from .store import LabelRecord, load_labels, write_label

__all__ = ["LabelRecord", "load_labels", "write_label"]
