"""Resumable run checkpoints.

An aborted run — a pinned provider going away mid-run, a budget guard raise, a laptop
closing — must not force re-calling items that already completed. Every runner wraps its
work list in a :class:`Checkpoint`: completed item keys are appended to a JSONL sidecar as
they finish, and :meth:`pending` filters them out on restart.

The checkpoint stores *keys and results*, never prompts-with-secrets and never labels.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

from . import config


@dataclass
class Checkpoint:
    """Append-only completed-item record for one run.

    ``run_id`` should identify the phase and cell, e.g. ``"predict_M->N"``, so two cells
    never share a checkpoint file.
    """

    run_id: str
    path: Path | None = None

    def __post_init__(self) -> None:
        if self.path is None:
            safe = self.run_id.replace("->", "_to_").replace("/", "_")
            self.path = config.CHECKPOINT_DIR / f"{safe}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    # -- state --------------------------------------------------------------------
    def completed_keys(self) -> set[str]:
        if not self.path.exists():
            return set()
        keys: set[str] = set()
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    keys.add(json.loads(line)["key"])
                except (json.JSONDecodeError, KeyError):
                    continue
        return keys

    def records(self) -> Iterator[dict[str, Any]]:
        if not self.path.exists():
            return iter(())
        def _gen() -> Iterator[dict[str, Any]]:
            with self.path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            continue
        return _gen()

    # -- use ----------------------------------------------------------------------
    def pending(self, keys: Iterable[str]) -> list[str]:
        done = self.completed_keys()
        return [k for k in keys if k not in done]

    def mark(self, key: str, result: dict[str, Any] | None = None) -> None:
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"key": key, "result": result or {}}, ensure_ascii=False) + "\n")

    @property
    def n_done(self) -> int:
        return len(self.completed_keys())
