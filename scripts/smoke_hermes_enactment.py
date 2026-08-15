"""Hermes-3 enactment smoke test — see 06_hermes_smoke_test.md for the pre-declared criteria.

Two stages, both through the budgeted, pinned client:
  1. generation: 10 draft dilemmas x 2 draft personas x {Llama-3.1-70B, Hermes-3-70B}  (40 calls)
  2. prediction: both models predict all 40 items with the REAL predictor prompt       (80 calls)

Outputs
  data/generated/generated_column_{M,N}_smoke.jsonl   (text, no label)
  data/labels_smoke/labels_column_{M,N}_smoke.jsonl   (label, separate dir; NOT data/labels/)
  data/generated/predictions_*_smoke.jsonl            (letters, no label)
  06_hermes_smoke_test.md                             (results appended: usability + malformed only)

**No accuracy is computed anywhere in this script.** Predictions and labels are never joined.
The persona keys are used only to build the (label-free) predictor prompt, exactly as run_cell does.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from selfpred import config
from selfpred.client import OpenRouterClient, PriceBook, price_book_from_models_payload
from selfpred.personas import PersonaPair, SourcePrompt, generate_column
from selfpred.predict.run import GeneratedItem, run_cell

PHASE = "smoke"
RUN_TAG = "_smoke"
STIM = config.REPO_ROOT / "data" / "stimuli" / "smoke"
LABELS_SMOKE_DIR = config.DATA_DIR / "labels_smoke"
REPORT = config.REPO_ROOT / "06_hermes_smoke_test.md"

# Verified in 04_model_verification.md. Held locally: config.MODELS stays unset until 02 decides.
SPECS = {
    "M": config.ModelSpec(model_id="meta-llama/llama-3.1-70b-instruct", provider="DeepInfra",
                          quantization="fp8", price_prompt_usd_per_mtok=0.40, price_completion_usd_per_mtok=0.40),
    "N": config.ModelSpec(model_id="nousresearch/hermes-3-llama-3.1-70b", provider="DeepInfra",
                          quantization="fp8", price_prompt_usd_per_mtok=0.70, price_completion_usd_per_mtok=0.70),
}

REFUSAL = re.compile(r"\b(i can'?t|i cannot|i'?m not able|i am not able|as an ai)\b", re.I)
ECHO = re.compile(r"\b(instruction|persona|as instructed|the principle|i was told)\b", re.I)
FORMAT = re.compile(r"^(#|- |\* |\d+\.)", re.M)
SOFT = re.compile(r"\b(autonomy|welfare|wellbeing|well-being)\b", re.I)


def usability(text: str, finish_reason: str | None) -> tuple[bool, list[str], list[str]]:
    hard, soft = [], []
    words = len(text.split())
    if not text.strip() or words < 60:
        hard.append(f"short({words}w)")
    if REFUSAL.search(text) and words < 90:
        hard.append("refusal")
    if ECHO.search(text):
        hard.append("echo")
    if FORMAT.search(text):
        hard.append("format")
    if SOFT.search(text):
        soft.append("names-value")
    if finish_reason == "length":
        soft.append("truncated")
    return (not hard), hard, soft


def main() -> None:
    models_json = config.RAW_DIR / "openrouter_models.json"
    book: PriceBook = price_book_from_models_payload(json.loads(models_json.read_text(encoding="utf-8")))
    for s in SPECS.values():   # make sure the guard can project for both
        book.project(s.model_id, est_prompt_tokens=10, max_completion_tokens=1)

    dil = json.loads((STIM / "dilemmas.json").read_text(encoding="utf-8"))
    per = json.loads((STIM / "personas_draft.json").read_text(encoding="utf-8"))
    prompts = [SourcePrompt(d["prompt_id"], d["text"]) for d in dil]
    pair = PersonaPair(key_a=per["key_a"], key_b=per["key_b"], clauses=per["clauses"], pair_id=per["pair_id"])

    lines: list[str] = ["", "## Results (appended by scripts/smoke_hermes_enactment.py)", ""]

    # ---- stage 1: generation --------------------------------------------------------
    gen: dict[str, list] = {}
    for col in ("M", "N"):
        spec = SPECS[col]
        recs = generate_column(
            column=col, generator_model_id=spec.model_id, generator_provider=spec.provider,
            prompts=prompts, pair=pair, price_book=book, phase=PHASE,
            labels_dir=LABELS_SMOKE_DIR, run_tag=RUN_TAG,
        )
        # resumed runs return only new items; reload the full column from disk
        path = config.GENERATED_DIR / f"generated_column_{col}{RUN_TAG}.jsonl"
        gen[col] = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

    lines.append("### Stage 1 — generation usability (pre-declared rules in the section above)")
    lines.append("")
    lines.append("| Column / generator | n | usable | rate | hard-fail reasons | soft flags | finish=length | mean words | PASS (>=90%) |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    gen_pass: dict[str, bool] = {}
    for col in ("M", "N"):
        rows = gen[col]
        hard_c, soft_c = Counter(), Counter()
        usable = 0
        wc = []
        for r in rows:
            ok, hard, soft = usability(r["response_text"], r.get("finish_reason"))
            usable += ok
            hard_c.update(hard); soft_c.update(soft)
            wc.append(len(r["response_text"].split()))
        n = len(rows)
        rate = usable / n if n else float("nan")
        gen_pass[col] = rate >= 0.90
        trunc = sum(1 for r in rows if r.get("finish_reason") == "length")
        lines.append(
            f"| {col} / `{SPECS[col].model_id}` | {n} | {usable} | {rate:.0%} | "
            f"{dict(hard_c) or '—'} | {dict(soft_c) or '—'} | {trunc} | {sum(wc)/max(n,1):.0f} | "
            f"{'PASS' if gen_pass[col] else 'FAIL'} |"
        )
    lines.append("")

    # ---- stage 2: prediction with the real template, both predictors on both columns --
    items = {
        col: [GeneratedItem(r["item_id"], r["source_prompt_id"], r["target_column"], r["response_text"]) for r in gen[col]]
        for col in ("M", "N")
    }
    lines.append("### Stage 2 — prediction malformed rate on the real predictor prompt")
    lines.append("")
    lines.append("| Cell | items | malformed | rate | PASS (<5%) |")
    lines.append("|---|---|---|---|---|")
    pred_malformed: dict[str, int] = {}
    pred_n: dict[str, int] = {}
    for predictor in ("M", "N"):
        for col in ("M", "N"):
            cell = config.Cell(predictor, col)
            recs = run_cell(
                cell=cell, items=items[col], persona_keys=pair.keys, persona_clauses=pair.clauses,
                price_book=book, phase=PHASE, predictor_spec=SPECS[predictor], run_tag=RUN_TAG,
            )
            path = config.GENERATED_DIR / f"predictions_{cell.name.replace('->', '_to_')}{RUN_TAG}.jsonl"
            allrecs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
            mal = sum(1 for r in allrecs if r["malformed"])
            pred_malformed[predictor] = pred_malformed.get(predictor, 0) + mal
            pred_n[predictor] = pred_n.get(predictor, 0) + len(allrecs)
            lines.append(f"| {cell.name} | {len(allrecs)} | {mal} | {mal/max(len(allrecs),1):.0%} | — |")
    for predictor in ("M", "N"):
        n, mal = pred_n[predictor], pred_malformed[predictor]
        lines.append(f"| **predictor {predictor} total** | {n} | {mal} | {mal/max(n,1):.0%} | {'PASS' if mal/max(n,1) < 0.05 else 'FAIL'} |")
    lines.append("")

    # ---- cost -------------------------------------------------------------------------
    from selfpred.client import _spend_in_log
    spent = _spend_in_log(config.RAW_DIR / f"{PHASE}.jsonl")
    lines.append(f"**Smoke phase spend:** ${spent:.4f} (sub-budget $0.08). Log: `data/raw/smoke.jsonl`.")
    lines.append("")
    lines.append("**Sealed:** `data/generated/predictions_*_smoke.jsonl` and `data/labels_smoke/` were never joined; no accuracy exists.")
    lines.append("")
    verdict = (
        "Hermes PASSES both stages -> tier-(i) pair viable for the crossed design."
        if gen_pass["N"] and pred_malformed["N"] / max(pred_n["N"], 1) < 0.05
        else "Hermes FAILS generation, passes prediction -> N column not buildable; ladder level 2 is live (sign-off #13)."
        if (not gen_pass["N"]) and pred_malformed["N"] / max(pred_n["N"], 1) < 0.05
        else "Hermes FAILS prediction -> tier-(i) pair not viable as specified; tier-(ii) fallback pair (sign-off)."
    )
    lines.append(f"**Consequence (per the pre-declared table):** {verdict}")
    lines.append("")
    with REPORT.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
