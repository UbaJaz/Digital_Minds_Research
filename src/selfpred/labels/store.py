"""Ground-truth records, stored apart from everything a predictor can reach.

One record per generated item: which persona clause produced it, which source prompt it
came from, and the generation parameters needed to reproduce it. Files live in
`data/labels/`, which `predict/` never reads.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

from .. import config


@dataclass
class LabelRecord:
    item_id: str
    source_prompt_id: str
    target_column: str        # which model generated this text (role letter)
    persona_key: str          # THE hidden property. Never leaves this package.
    generation_temperature: float
    generation_seed: int | None
    model_returned: str | None
    provider_returned: str | None


def _path(target_column: str) -> Path:
    return config.LABELS_DIR / f"labels_column_{target_column}.jsonl"


def write_label(rec: LabelRecord) -> None:
    path = _path(rec.target_column)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")


def load_labels(target_column: str) -> dict[str, LabelRecord]:
    path = _path(target_column)
    if not path.exists():
        return {}
    out: dict[str, LabelRecord] = {}
    for rec in _iter(path):
        out[rec.item_id] = rec
    return out


def _iter(path: Path) -> Iterator[LabelRecord]:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield LabelRecord(**json.loads(line))
