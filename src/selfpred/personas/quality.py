"""Label-blind generation quality rules (02 row P11, locked 2026-08-15).

Applied mechanically to the *text only*, before any label is joined, so exclusion cannot
depend on the hidden persona. The rules are the ones exercised in the enactment smoke test.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

REFUSAL = re.compile(r"\b(i can'?t|i cannot|i'?m not able|i am not able|as an ai)\b", re.I)
ECHO = re.compile(r"\b(instruction|persona|as instructed|the principle|i was told)\b", re.I)
FORMAT = re.compile(r"^(#|- |\* |\d+\.)", re.M)
#: Persona-clause vocabulary; if a generation *names the principle* with these it is excluded.
#: Kept deliberately narrow: only the tokens the clause pairs were written to avoid.
NAMES_PRINCIPLE = re.compile(r"\b(autonomy|welfare)\b", re.I)
MIN_WORDS = 60


@dataclass(frozen=True)
class QualityVerdict:
    usable: bool
    reasons: tuple[str, ...]
    soft_flags: tuple[str, ...]
    n_words: int


def assess(text: str, finish_reason: str | None = None) -> QualityVerdict:
    words = len(text.split())
    hard: list[str] = []
    soft: list[str] = []
    if not text.strip() or words < MIN_WORDS:
        hard.append(f"short({words}w)")
    if REFUSAL.search(text) and words < 90:
        hard.append("refusal")
    if ECHO.search(text):
        hard.append("echo")
    if FORMAT.search(text):
        hard.append("format")
    if NAMES_PRINCIPLE.search(text):
        hard.append("names-principle")
    if finish_reason == "length":
        soft.append("truncated")
    return QualityVerdict(usable=not hard, reasons=tuple(hard), soft_flags=tuple(soft), n_words=words)
