"""Phase 1D — the persona pair and generation.

**Minimal implementation (generate.py) exists for the enactment smoke test.** The persona pair itself is still The exact persona design is unresolved in
`02_design_audit.md` (Unresolved Decisions row 2), as is the pilot feasibility band
(row 4). The council proposes values-ordering with a joint per-column band, but that
proposal has not been applied to `02`, so nothing is written down here.

What the layout reserves:
  * a persona-pair spec: two clauses on a shared scaffold, identical length and format
    instructions, differing only in the clause; the generation prompt forbids naming the
    value;
  * ``generate.py`` — generates from every source prompt under **both** personas (so the
    topic is balanced by construction and the analysis can pair within prompt), writing
    the text to ``data/generated/`` and the persona key to ``data/labels/`` via
    ``selfpred.labels`` — never to the same file.

Ground truth leaves this package only through ``selfpred.labels``. Nothing in
``selfpred.predict`` may read it.
"""

from .quality import QualityVerdict, assess  # noqa: E402
from .generate import (  # noqa: E402
    GENERATION_SYSTEM_TEMPLATE,
    GeneratedRecord,
    PersonaPair,
    SourcePrompt,
    build_generation_messages,
    generate_column,
    make_item_id,
)

__all__ = [
    "GENERATION_SYSTEM_TEMPLATE", "GeneratedRecord", "PersonaPair", "SourcePrompt",
    "build_generation_messages", "generate_column", "make_item_id", "QualityVerdict", "assess",
]
