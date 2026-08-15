"""Phase B follow-up: two questions the first pass raised.

1. `google/gemini-3.5-flash-lite` returned an EMPTY string with finish_reason="length" on
   every one-letter call. That is consistent with max_tokens=4 being consumed before any
   visible token is emitted, not with the model being unable to answer. Retest at a larger
   max_tokens to tell "unusable" apart from "misconfigured" — the distinction decides
   whether a Far-Self candidate is really disqualified.

2. Confirm the correctly-paired tier (i) alternative cannot be pinned: hermes-4-70b's card
   states a Llama-3.1-70B base, but it is served only by Nebius while
   llama-3.1-70b-instruct is not. Checked from the saved endpoints JSON, no call needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from selfpred import config
from selfpred.client import OpenRouterClient, price_book_from_models_payload

sys.path.insert(0, str(Path(__file__).resolve().parent))
from phase_b_verify import ONE_LETTER_ITEMS, one_letter_msgs, _cost_so_far  # noqa: E402

RETEST = [
    ("google/gemini-3.5-flash-lite", "Google", False),
    ("deepseek/deepseek-chat-v3-0324", "SiliconFlow", True),
    ("mistralai/mistral-small-3.2-24b-instruct", "DeepInfra", True),
]


def main() -> None:
    payload = json.loads((config.RAW_DIR / "openrouter_models.json").read_text(encoding="utf-8"))
    book = price_book_from_models_payload(payload)
    out: dict[str, dict] = {}

    print("=== 1. one-letter retest at max_tokens=16 (Far-Self candidates) ===")
    with OpenRouterClient("verification", price_book=book) as client:
        for model_id, provider, reasoning_off in RETEST:
            malformed, samples = 0, []
            for i, (a, b) in enumerate(ONE_LETTER_ITEMS):
                label, calls = client.one_letter(
                    model_id=model_id, messages=one_letter_msgs(a, b), provider=provider,
                    max_tokens=16, reasoning_off=reasoning_off, tag=f"followup-16tok-{i}",
                )
                if label is None:
                    malformed += 1
                    samples.append(calls[-1].text[:40])
            rate = malformed / len(ONE_LETTER_ITEMS)
            out[model_id] = {"malformed_rate_at_16_tokens": rate, "samples": samples[:3]}
            print(f"  {model_id:<44} malformed {rate:.0%} "
                  f"{'PASS' if rate < config.MALFORMED_RATE_PASS_THRESHOLD else 'FAIL'}"
                  + (f"  e.g. {samples[:2]}" if samples else ""))

    print("\n=== 2. tier (i) pinning check: llama-3.1-70b + hermes-4-70b (same stated base) ===")
    eps = json.loads((config.RAW_DIR / "openrouter_endpoints.json").read_text(encoding="utf-8"))

    def providers(mid: str) -> set[str]:
        return {
            e.get("provider_name")
            for e in ((eps.get(mid) or {}).get("data") or {}).get("endpoints", [])
        }

    a, b = "meta-llama/llama-3.1-70b-instruct", "nousresearch/hermes-4-70b"
    pa, pb = providers(a), providers(b)
    shared = pa & pb
    print(f"  {a}: {sorted(pa)}")
    print(f"  {b}: {sorted(pb)}")
    print(f"  shared: {sorted(shared) or 'NONE -> cannot pin both members (pinning FAIL)'}")
    out["tier_i_alternative"] = {"pair": [a, b], "shared_providers": sorted(shared)}

    print(f"\ntotal Phase B cost now: ${_cost_so_far():.4f}")
    (config.RAW_DIR / "verification_followup.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
