"""selfpred — pipeline for the Track 3 self-prediction sprint.

`02_design_audit.md` is the authoritative research design. This package is deliberately
parameterised rather than opinionated: which cells run, which models fill roles M/N/F,
and what n is are all read from `config.py`, and `config.py` leaves them unset until the
design document says otherwise.
"""

__all__ = ["config", "client", "checkpoint"]
