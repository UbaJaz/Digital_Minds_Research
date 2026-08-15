"""Phase B, step 3: per-candidate endpoints — providers, quantization, per-provider price.

No metered calls. For each PAIR, reports whether ONE provider serves BOTH members at a
stated quantization; that is the pinning requirement, and per the council it is a validity
condition rather than a nicety (M-as-generator and M-as-Self-predictor must hit identical
weights).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from selfpred import config
from selfpred.client import OpenRouterClient

CANDIDATES = [
    # tier (i): open-weight base + same-base community fine-tune, same parameter size
    "meta-llama/llama-3.1-70b-instruct",
    "nousresearch/hermes-3-llama-3.1-70b",
    "meta-llama/llama-3.3-70b-instruct",
    "nousresearch/hermes-4-70b",
    "qwen/qwen-2.5-72b-instruct",
    "anthracite-org/magnum-v4-72b",
    # tier (ii): dated snapshots of one closed model
    "openai/gpt-4o-2024-08-06",
    "openai/gpt-4o-2024-11-20",
    # tier (iii): same-family adjacent tier
    "openai/gpt-5.6-terra",
    "openai/gpt-5.6-luna",
    "google/gemini-3.7-flash",
    "google/gemini-3.5-flash-lite",
    # far-self candidates: different lineage
    "deepseek/deepseek-chat-v3-0324",
    "mistralai/mistral-small-3.2-24b-instruct",
]

PAIRS = [
    ("meta-llama/llama-3.1-70b-instruct", "nousresearch/hermes-3-llama-3.1-70b", "i"),
    ("meta-llama/llama-3.3-70b-instruct", "nousresearch/hermes-4-70b", "i"),
    ("qwen/qwen-2.5-72b-instruct", "anthracite-org/magnum-v4-72b", "i"),
    ("openai/gpt-4o-2024-08-06", "openai/gpt-4o-2024-11-20", "ii"),
    ("openai/gpt-5.6-terra", "openai/gpt-5.6-luna", "iii"),
    ("google/gemini-3.7-flash", "google/gemini-3.5-flash-lite", "iii"),
]

OUT = config.RAW_DIR / "openrouter_endpoints.json"


def main() -> None:
    collected: dict[str, dict] = {}
    with OpenRouterClient("verification") as client:
        for mid in CANDIDATES:
            try:
                collected[mid] = client.get_endpoints(mid)
            except Exception as exc:  # noqa: BLE001 - message is already redacted
                collected[mid] = {"error": str(exc)}
    OUT.write_text(json.dumps(collected, indent=1), encoding="utf-8")

    providers_of: dict[str, dict[str, dict]] = {}
    for mid, payload in collected.items():
        data = (payload or {}).get("data") or {}
        eps = data.get("endpoints") or []
        if "error" in payload:
            print(f"\n### {mid}\n  ERROR: {str(payload['error'])[:160]}")
            providers_of[mid] = {}
            continue
        print(f"\n### {mid}   ({len(eps)} endpoints)")
        pm: dict[str, dict] = {}
        for e in eps:
            name = e.get("provider_name") or e.get("name") or "?"
            quant = e.get("quantization")
            pricing = e.get("pricing") or {}
            try:
                p_in = float(pricing.get("prompt", 0)) * 1e6
                p_out = float(pricing.get("completion", 0)) * 1e6
            except (TypeError, ValueError):
                p_in = p_out = float("nan")
            pm[name] = {"quantization": quant, "price_in": p_in, "price_out": p_out,
                        "context": e.get("context_length"), "status": e.get("status")}
            print(f"   {name:<26} quant={str(quant):<10} ${p_in:.3f}/${p_out:.3f}  ctx={e.get('context_length')}")
        providers_of[mid] = pm

    print("\n\n=========== PAIR PINNING ===========")
    for a, b, tier in PAIRS:
        shared = sorted(set(providers_of.get(a, {})) & set(providers_of.get(b, {})))
        print(f"\ntier ({tier})  {a}  ||  {b}")
        if not shared:
            print("   NO SHARED PROVIDER -> cannot pin both members. Pinning FAIL.")
            continue
        for p in shared:
            qa = providers_of[a][p]["quantization"]
            qb = providers_of[b][p]["quantization"]
            same = "same-quant" if qa == qb else "QUANT MISMATCH"
            print(f"   {p:<26} quant {str(qa):<8} / {str(qb):<8}  [{same}]")


if __name__ == "__main__":
    main()
