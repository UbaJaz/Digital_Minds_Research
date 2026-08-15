"""Predictor prompt construction.

Contract (from `02_design_audit.md` Locked #3, plus the mechanism stated in `03` §3.4):

* The predictor receives the response text and **both persona clauses verbatim**, so every
  predictor has identical information. The only self-specific channel is same-weights fit
  to one's own output distribution.
* The predictor is **not told which model generated the text**.
* Option order (which persona is shown as A and which as B) is **counterbalanced** by a
  deterministic seeded rule and **logged**, so a position-bias check can be reported.
* The prompt never contains the ground-truth label, nor any persona *name* that encodes it.

Nothing here decides what the personas are — that is Phase 1D and lives in `02`.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .. import config

#: Tokens that would leak ground truth if they ever appeared in a predictor prompt.
#: The pytest in tests/test_ground_truth_separation.py asserts their absence.
LABEL_TOKENS: tuple[str, ...] = (
    "ground_truth", "ground truth", "true_persona", "true persona",
    "correct answer", "the answer is", "label:", "persona_id",
    "generated_by", "generator=", "was_generated_by",
)

PREDICTOR_SYSTEM = (
    "You classify short texts. Answer with a single letter and nothing else."
)

PREDICTOR_TEMPLATE = """Below is a response someone wrote to an advice dilemma.

It was written while following exactly one of two instructions.

A: {clause_a}

B: {clause_b}

Response:
\"\"\"
{response_text}
\"\"\"

Which instruction was being followed? Reply with exactly one letter: A or B. Do not explain."""


@dataclass(frozen=True)
class PredictorPrompt:
    """A built predictor prompt plus the counterbalancing record needed for analysis."""

    messages: list[dict[str, str]]
    #: Which persona key was shown in slot A / slot B for this item.
    option_a_persona: str
    option_b_persona: str
    #: True when the mapping was flipped relative to the canonical (p1 -> A) order.
    flipped: bool
    item_id: str

    @property
    def text(self) -> str:
        return "\n".join(m["content"] for m in self.messages)

    def label_for_persona(self, persona_key: str) -> str:
        """Which letter corresponds to a persona — used by the *scorer*, never the predictor."""
        if persona_key == self.option_a_persona:
            return "A"
        if persona_key == self.option_b_persona:
            return "B"
        raise KeyError(f"{persona_key!r} is not one of this item's two personas")


def option_order_for(item_id: str, *, seed: int = config.PERSONA_ORDER_SEED) -> bool:
    """Deterministic counterbalancing: returns True when the pair should be flipped.

    Seeded by item id so the order is reproducible from the item set alone, balanced
    across a large item set, and independent of run order or of the ground-truth label.
    """
    digest = hashlib.sha256(f"{seed}:{item_id}".encode("utf-8")).digest()
    return bool(digest[0] & 1)


def build_predictor_prompt(
    *,
    item_id: str,
    response_text: str,
    persona_keys: tuple[str, str],
    persona_clauses: dict[str, str],
    seed: int = config.PERSONA_ORDER_SEED,
) -> PredictorPrompt:
    """Build the forced-choice prompt for one item.

    ``persona_keys`` is the canonical (p1, p2) ordering of the pair; ``persona_clauses``
    maps each key to the verbatim clause text. No argument carries the ground truth, and
    there is deliberately no parameter through which a caller could pass it.
    """
    p1, p2 = persona_keys
    flipped = option_order_for(item_id, seed=seed)
    a_key, b_key = (p2, p1) if flipped else (p1, p2)

    content = PREDICTOR_TEMPLATE.format(
        clause_a=persona_clauses[a_key].strip(),
        clause_b=persona_clauses[b_key].strip(),
        response_text=response_text.strip(),
    )
    return PredictorPrompt(
        messages=[
            {"role": "system", "content": PREDICTOR_SYSTEM},
            {"role": "user", "content": content},
        ],
        option_a_persona=a_key,
        option_b_persona=b_key,
        flipped=flipped,
        item_id=item_id,
    )
