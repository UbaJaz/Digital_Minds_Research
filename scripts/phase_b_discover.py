"""Phase B, step 1-2: pull the OpenRouter model list and walk the lineage ladder.

No metered calls. GET /models is free; this script only reads it, saves the raw JSON,
and searches by NAME for pairs matching the council's lineage tiers. It asserts nothing
about availability — every candidate it prints is a hypothesis to be tested by an actual
call in phase_b_verify.py.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from selfpred import config
from selfpred.client import OpenRouterClient, price_book_from_models_payload

OUT = config.RAW_DIR / "openrouter_models.json"


def main() -> None:
    with OpenRouterClient("verification") as client:
        payload = client.get_models()
    OUT.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    models = payload.get("data", [])
    print(f"models listed: {len(models)}  -> {OUT}")

    book = price_book_from_models_payload(payload)
    print(f"priced models: {len(book.prompt)}")

    by_author: dict[str, list[dict]] = defaultdict(list)
    for m in models:
        by_author[m["id"].split("/")[0]].append(m)

    def show(label: str, pattern: str, limit: int = 40) -> None:
        rx = re.compile(pattern, re.I)
        hits = [m for m in models if rx.search(m["id"]) or rx.search(m.get("name", ""))]
        print(f"\n=== {label} :: /{pattern}/ :: {len(hits)} hits ===")
        for m in hits[:limit]:
            p_in = book.prompt.get(m["id"])
            p_out = book.completion.get(m["id"])
            price = f"${p_in:.3f}/${p_out:.3f} per Mtok" if p_in is not None else "price?"
            print(f"  {m['id']:<58} {price:<28} ctx={m.get('context_length')}")

    # --- Tier (i): open-weight base, official Instruct + same-base community fine-tune ---
    show("tier-i llama-70b class", r"llama-3(\.\d)?[.-]?\d*-?70b")
    show("tier-i qwen-72b class", r"qwen[-_]?2\.5[-_]?72b")
    show("tier-i qwen-other-large", r"qwen.*(32b|72b)")
    show("tier-i mistral-large/small", r"mistral.*(large|small|nemo)")
    show("tier-i known finetuners", r"(nousresearch|hermes|dolphin|airoboros|openchat|tulu|wizard|eva|magnum|anubis|lumimaid|midnight)")

    # --- Tier (ii): dated snapshots of one closed model ---
    show("tier-ii dated snapshots", r"-20\d{2}[-_]?\d{2}[-_]?\d{2}|-\d{4}$|:\d{8}")

    # --- Tier (iii): same-family adjacent tier ---
    show("tier-iii gpt family", r"^openai/gpt")
    show("tier-iii gemini family", r"^google/gemini")
    show("tier-iii claude family", r"^anthropic/claude")

    # --- Far-Self candidates: cheap, different lineage ---
    show("far-self: deepseek", r"^deepseek/")
    show("far-self: mistral", r"^mistralai/")
    show("far-self: cohere", r"^cohere/")

    print("\nauthors with >=3 models:")
    for a, ms in sorted(by_author.items(), key=lambda kv: -len(kv[1]))[:25]:
        print(f"  {a:<24} {len(ms)}")


if __name__ == "__main__":
    main()
