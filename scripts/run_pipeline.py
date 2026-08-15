"""End-to-end, resumable pipeline: Phase C -> Phase D gate -> freeze commit -> Phase E -> analysis.

Every stage is idempotent: API work is checkpointed per item, stage completion is recorded in
data/generated/pipeline_state.json, and re-running the script continues where it stopped.
All research rules come from 02_design_audit.md (locked 2026-08-15); nothing here decides.

Usage:  .venv/Scripts/python scripts/run_pipeline.py [--until C|D|FREEZE|E|ANALYSIS]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from selfpred import config
from selfpred.analysis import (interaction_bootstrap, interaction_bootstrap_joint, paired_bootstrap_diff)
from selfpred.analysis.score import accuracy_ci, load_column, score_cell
from selfpred.baseline import fit_baseline_cv
from selfpred.calibration import analyze as cal_analyze, freeze_items, run_predictor
from selfpred.client import _spend_in_log, price_book_from_models_payload
from selfpred.personas import PersonaPair, SourcePrompt, generate_column
from selfpred.predict.run import GeneratedItem, run_cell

ROOT = config.REPO_ROOT
STATE = config.GENERATED_DIR / "pipeline_state.json"
RESULTS = config.DATA_DIR / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
LOG = config.GENERATED_DIR / "pipeline.log"


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save_state(**kw) -> None:
    s = state(); s.update(kw)
    STATE.write_text(json.dumps(s, indent=2), encoding="utf-8")


def price_book():
    return price_book_from_models_payload(json.loads((config.RAW_DIR / "openrouter_models.json").read_text(encoding="utf-8")))


def append_02(text: str) -> None:
    p = ROOT / "02_design_audit.md"
    s = p.read_text(encoding="utf-8")
    marker = "_(none yet — anything changed after the freeze commit is listed here with date and reason)_"
    if marker in s:
        s = s.replace(marker, text)
    else:
        s = s.replace("### Amendments after lock\n", "### Amendments after lock\n" + text + "\n", 1)
    p.write_text(s, encoding="utf-8")


def spend() -> float:
    return sum(_spend_in_log(p) for p in config.RAW_DIR.glob("*.jsonl"))


def load_prompts(name: str) -> list[SourcePrompt]:
    d = json.loads((ROOT / "data/stimuli/main" / name).read_text(encoding="utf-8"))
    return [SourcePrompt(x["prompt_id"], x["text"]) for x in d]


def candidate_pairs() -> list[PersonaPair]:
    d = json.loads((ROOT / "data/stimuli/personas/candidates.json").read_text(encoding="utf-8"))
    return [PersonaPair(c["key_a"], c["key_b"], c["clauses"], c["pair_id"], c.get("scaffold"))
            for c in d["candidates"]]


def effective_far():
    """Apply a persisted Far swap (Phase C outcome) before anything uses config.MODELS['F']."""
    marker = config.GENERATED_DIR / "far_swap.json"
    if marker.exists():
        config.MODELS["F"] = config.FAR_SWAP
    return config.MODELS["F"]


# ======================================================================================
# Phase C — calibration
# ======================================================================================

def stage_c() -> None:
    if state().get("C_done"):
        log("C already done"); effective_far(); return
    book = price_book()
    items = freeze_items()
    log(f"C: {len(items)} calibration items frozen")
    effective_far()
    ans = {r: run_predictor(role=r, items=items, price_book=book) for r in ("M", "N", "F")}
    res = cal_analyze(ans["M"], ans["N"], ans["F"])
    swapped = False
    if not res.near_gt_far_point:
        log("C: A_near <= A_far -> pre-declared Far swap to DeepSeek and re-run F")
        (config.GENERATED_DIR / "far_swap.json").write_text(json.dumps({"swapped_at": time.time()}), encoding="utf-8")
        effective_far()
        ans["F"] = run_predictor(role="F", items=items, price_book=book, run_tag="_swap")
        res = cal_analyze(ans["M"], ans["N"], ans["F"])
        swapped = True
    (RESULTS / "calibration.json").write_text(json.dumps(asdict(res) | {"far_model": config.MODELS['F'].model_id, "swapped": swapped}, indent=2), encoding="utf-8")
    doc = f"""# 07 — Calibration Probe Results (Phase 1C)

**Rule (02 row P8):** 50 frozen paraphrase-preference items; Agreement(X, Target); accept Near > Far if the point estimate A_near > A_far; CI reported.

| Quantity | Value | 95 % bootstrap CI |
|---|---|---|
| Items with all three answers | {res.n_items} | — |
| A_near (Hermes-3 vs Llama-3.1) | {res.a_near:.3f} | [{res.a_near_ci[0]:.3f}, {res.a_near_ci[1]:.3f}] |
| A_far ({config.MODELS['F'].model_id} vs Llama-3.1) | {res.a_far:.3f} | [{res.a_far_ci[0]:.3f}, {res.a_far_ci[1]:.3f}] |
| Δ = A_near − A_far | {res.delta:+.3f} | [{res.delta_ci[0]:+.3f}, {res.delta_ci[1]:+.3f}] |
| Target's share of "A" answers (position bias) | {res.target_a_share:.2f} | — |
| Malformed (target/near/far) | {res.n_malformed} | — |

**Outcome:** {'Near > Far on the point estimate — similarity ordering accepted; ASSUMPTION 9 (Far not distilled from Target) not contradicted.' if res.near_gt_far_point else 'Near ≤ Far even after the swap — the similarity ordering is NOT confirmed; report plainly.'}
{'**Far was swapped** to `' + config.MODELS['F'].model_id + '` per the pre-declared rule (logged as amendment A1 in 02).' if swapped else 'No Far swap needed.'}

Spend so far: ${spend():.4f}. Raw: `data/generated/calibration/`, log `data/raw/calibration.jsonl`.
"""
    (ROOT / "07_calibration_results.md").write_text(doc, encoding="utf-8")
    if swapped:
        append_02(f"- **A1 (2026-08-15, Phase C):** Far-Self swapped from Mistral-Small-3.2-24B to `{config.MODELS['F'].model_id}` because A_near ≤ A_far on the calibration probe (pre-declared rule, row P3/P8).\n")
    save_state(C_done=True, C=asdict(res))
    log(f"C done: A_near={res.a_near:.3f} A_far={res.a_far:.3f} delta={res.delta:+.3f}")


# ======================================================================================
# Phase D — pilot (screen ≤3 pairs @ 40 items on M, winner @ 80 items on M and N)
# ======================================================================================

def _pilot_column(col: str, pair: PersonaPair, prompts, run_tag: str, book):
    spec = config.model(col)
    generate_column(column=col, generator_model_id=spec.model_id, generator_provider=spec.provider,
                    prompts=prompts, pair=pair, price_book=book, phase="pilot",
                    labels_dir=config.LABELS_DIR, run_tag=run_tag)
    # Restrict to the prompts this call asked for: without it, a resumed screen would read
    # the 80 items the full pilot has since written and stop being a 40-item screen.
    coldata = load_column(col, run_tag=run_tag, labels_dir=config.LABELS_DIR,
                          prompt_ids={p.prompt_id for p in prompts})
    items = [GeneratedItem(i, coldata.prompt_of[i], col, coldata.texts[i]) for i in coldata.texts]
    run_cell(cell=config.Cell(col, col), items=items, persona_keys=pair.keys, persona_clauses=pair.clauses,
             price_book=book, phase="pilot", run_tag=run_tag)
    sc = score_cell(config.Cell(col, col), coldata, run_tag=run_tag)
    usable_ids = sorted(coldata.usable)
    d = fit_baseline_cv(target_column=col, item_ids=usable_ids, texts=[coldata.texts[i] for i in usable_ids],
                        labels=[int(coldata.labels[i].persona_key == pair.key_b) for i in usable_ids],
                        groups=[coldata.prompt_of[i] for i in usable_ids])
    self_acc = sum(sc.correct.values()) / len(sc.correct) if sc.correct else float("nan")
    return {"column": col, "pair_id": pair.pair_id, "n_generated": len(coldata.texts), "n_usable": len(coldata.usable),
            "quality_reasons": dict(coldata.quality_reasons), "n_scored": len(sc.correct), "n_malformed": sc.n_malformed,
            "self_acc": self_acc, "d_acc": d.accuracy, "a_share": sc.a_share,
            "in_band": (config.PILOT_SELF_BAND[0] <= self_acc <= config.PILOT_SELF_BAND[1]) and d.accuracy <= config.PILOT_D_MAX,
            "provider_ok_for_self": sc.provider_ok_for_self}


def stage_d() -> None:
    if state().get("D_done"):
        log("D already done"); return
    book = price_book()
    pilot_prompts = load_prompts("prompts_pilot.json")
    screen_prompts, all_prompts = pilot_prompts[:20], pilot_prompts
    pairs = candidate_pairs()
    screen = []
    for pair in pairs:
        r = _pilot_column("M", pair, screen_prompts, f"_pilot_{pair.pair_id}", book)
        screen.append(r); log(f"D screen {pair.pair_id}: self={r['self_acc']:.3f} D={r['d_acc']:.3f} usable={r['n_usable']}/{r['n_generated']} in_band={r['in_band']}")
    # Selection rule (row P9): in-band first, then D closest to 50 %, then Self closest to 70 %.
    ranked = sorted(screen, key=lambda r: (not r["in_band"], abs(r["d_acc"] - 0.5), abs(r["self_acc"] - 0.7)))
    full = []
    winner = None; level = 3
    for cand in ranked:                       # ≤3 pairs, in rank order; stop at the first that passes on both columns
        pair = next(p for p in pairs if p.pair_id == cand["pair_id"])
        rm = _pilot_column("M", pair, all_prompts, f"_pilot_{pair.pair_id}", book)
        rn = _pilot_column("N", pair, all_prompts, f"_pilot_{pair.pair_id}", book)
        full.append({"M": rm, "N": rn})
        log(f"D full {pair.pair_id}: M self={rm['self_acc']:.3f} D={rm['d_acc']:.3f} band={rm['in_band']} | N self={rn['self_acc']:.3f} D={rn['d_acc']:.3f} band={rn['in_band']}")
        if rm["in_band"] and rn["in_band"]:
            winner, level = pair, 1; break
        if rm["in_band"] and winner is None:
            winner, level = pair, 2          # tentative level 2; keep looking for a level-1 pair
    out = {"screen": screen, "full": full, "winner": winner.pair_id if winner else None, "level": level}
    (RESULTS / "pilot.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    rows = "\n".join(f"| {r['pair_id']} | {r['n_usable']}/{r['n_generated']} | {r['self_acc']:.3f} | {r['d_acc']:.3f} | {'yes' if r['in_band'] else 'no'} |" for r in screen)
    frows = "\n".join(f"| {f['M']['pair_id']} | M | {f['M']['n_usable']}/{f['M']['n_generated']} | {f['M']['self_acc']:.3f} | {f['M']['d_acc']:.3f} | {'yes' if f['M']['in_band'] else 'no'} |\n| {f['N']['pair_id']} | N | {f['N']['n_usable']}/{f['N']['n_generated']} | {f['N']['self_acc']:.3f} | {f['N']['d_acc']:.3f} | {'yes' if f['N']['in_band'] else 'no'} |" for f in full)
    verdict = {1: "GO — level 1: crossed design (winner in band on M and N).",
               2: "Level 2: winner in band on M only — M-row design; capability confound becomes the headline limitation.",
               3: "Level 3: no pair in band on M — temperature fallback would be next; NOT run in this session (see 02 Fallback)."}[level]
    doc = f"""# 08 — Persona Pilot Results (Phase 1D)

**Band (02 row P9, fixed before the pilot):** per column, ≥ 80 items where possible, Self accuracy 60–80 % AND Baseline D (5-fold CV grouped by prompt, point estimate) ≤ 58 %. Screen ≤ 3 pairs at 40 items on M; winner at 80 items on M and N. Selection: in-band, then D closest to 50 %, then Self closest to 70 %.

## Screen (20 pilot prompts × 2 personas on M)
| Pair | usable | Self acc (M→M) | D acc | in band |
|---|---|---|---|---|
{rows}

## Full pilot (40 pilot prompts × 2 personas)
| Pair | Column | usable | Self acc | D acc | in band |
|---|---|---|---|---|---|
{frows}

## Gate outcome
**{verdict}** Winner: `{out['winner']}`.

Spend so far: ${spend():.4f}. Raw: `data/generated/*_pilot_*`, log `data/raw/pilot.jsonl`. Pilot prompts are excluded from the main set.
"""
    (ROOT / "08_pilot_results.md").write_text(doc, encoding="utf-8")
    append_02(f"- **Pilot gate (2026-08-15, Phase D):** {verdict} Winning pair `{out['winner']}` (see `08_pilot_results.md`).\n")
    save_state(D_done=True, D=out)
    log(f"D done: level {level}, winner {out['winner']}")


# ======================================================================================
# Freeze commit (row P15)
# ======================================================================================

def stage_freeze() -> None:
    if state().get("FREEZE_done"):
        log("FREEZE already done"); return
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    msg = ("Preregistration freeze: locked 02, stimuli, calibration + pilot results, pipeline\n\n"
           "02_design_audit.md Post-Council Locked Decisions confirmed 2026-08-15; stimuli hashes in data/stimuli/*/FREEZE.md.\n\n"
           "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>")
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=ROOT, check=True)
    h = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    append_02(f"- **Freeze commit (2026-08-15):** `{h}` — this document, the stimuli and the pipeline as they stood before the main run.\n")
    save_state(FREEZE_done=True, freeze_commit=h)
    log(f"FREEZE commit {h}")


# ======================================================================================
# Phase E — main run
# ======================================================================================

def stage_e() -> None:
    if state().get("E_done"):
        log("E already done"); return
    st = state()
    level = st["D"]["level"]; winner_id = st["D"]["winner"]
    if level == 3 or winner_id is None:
        log("E: pilot level 3 — main run not started (fallback level 3 requires the temperature design; stop here)."); return
    pair = next(p for p in candidate_pairs() if p.pair_id == winner_id)
    book = price_book()
    prompts = load_prompts("prompts_main.json")
    columns = ("M", "N") if level == 1 else ("M",)
    cells = config.ALL_CELLS if level == 1 else config.M_ROW
    effective_far()
    for col in columns:
        spec = config.model(col)
        log(f"E: generating column {col} ({len(prompts)}×2 items) on {spec.model_id}")
        generate_column(column=col, generator_model_id=spec.model_id, generator_provider=spec.provider,
                        prompts=prompts, pair=pair, price_book=book, phase="generation")
    for cell in cells:
        coldata = load_column(cell.target)
        items = [GeneratedItem(i, coldata.prompt_of[i], cell.target, coldata.texts[i]) for i in coldata.texts]
        log(f"E: predicting cell {cell.name} ({len(items)} items)")
        run_cell(cell=cell, items=items, persona_keys=pair.keys, persona_clauses=pair.clauses,
                 price_book=book, phase="prediction")
    save_state(E_done=True, E={"level": level, "pair": winner_id, "columns": columns, "cells": [c.name for c in cells]})
    log(f"E done. Spend ${spend():.4f}")


# ======================================================================================
# Analysis
# ======================================================================================

def stage_analysis() -> None:
    st = state()
    if not st.get("E_done"):
        log("ANALYSIS: E not done"); return
    level = st["E"]["level"]; pair = next(p for p in candidate_pairs() if p.pair_id == st["E"]["pair"])
    columns = st["E"]["columns"]; cells = [c for c in config.ALL_CELLS if c.name in st["E"]["cells"]]
    effective_far()
    cols = {c: load_column(c) for c in columns}
    scores = {cell.name: score_cell(cell, cols[cell.target]) for cell in cells}
    prompt_of = {}
    for c in cols.values():
        prompt_of.update(c.prompt_of)
    n_per_cell = min(len(s.correct) for s in scores.values())
    sesoi_simple = config.SESOI_SIMPLE_PP / 100
    sesoi_inter = (config.SESOI_INTERACTION_PP_AT_TARGET_N if n_per_cell >= config.N_PER_CELL_LADDER[0] else config.SESOI_INTERACTION_PP_BELOW_TARGET_N) / 100

    out: dict = {"level": level, "pair": pair.pair_id, "n_per_cell_min": n_per_cell, "cells": {}, "contrasts": {}, "baseline": {}, "spend_usd": spend()}
    lines = [f"# 09 — Main Results", "",
             f"**Design run:** {'crossed 2×2 (level 1)' if level == 1 else 'M-row only (level 2)'} · persona pair `{pair.pair_id}` · "
             f"M = `{config.MODELS['M'].model_id}`, N = `{config.MODELS['N'].model_id}`, F = `{config.MODELS['F'].model_id}` (all pinned; see 04) · "
             f"n per cell (scored) min {n_per_cell} · SESOI simple {config.SESOI_SIMPLE_PP:.0f} pp, interaction {sesoi_inter*100:.0f} pp · total spend ${spend():.4f} of $10.", ""]

    # cells
    lines += ["## Cell accuracies (prompt-clustered 95 % CI)", "", "| Cell | n scored | malformed | excluded (quality) | accuracy | 95 % CI | share 'A' | acc flipped / unflipped | self-cell provider match |", "|---|---|---|---|---|---|---|---|---|"]
    for cell in cells:
        s = scores[cell.name]
        acc, lo, hi = accuracy_ci(s.correct, prompt_of)
        out["cells"][cell.name] = {"n": len(s.correct), "malformed": s.n_malformed, "excluded": s.n_excluded_quality, "acc": acc, "ci": [lo, hi], "a_share": s.a_share,
                                   "flipped_acc": s.flipped_acc, "unflipped_acc": s.unflipped_acc, "provider_ok_for_self": s.provider_ok_for_self}
        lines.append(f"| {cell.name} | {len(s.correct)} | {s.n_malformed} | {s.n_excluded_quality} | {acc:.3f} | [{lo:.3f}, {hi:.3f}] | {s.a_share:.2f} | "
                     f"{'' if s.flipped_acc is None else f'{s.flipped_acc:.3f}'} / {'' if s.unflipped_acc is None else f'{s.unflipped_acc:.3f}'} | "
                     f"{'—' if s.provider_ok_for_self is None else ('✅' if s.provider_ok_for_self else '❌')} |")
    lines.append("")

    def contrast_row(name, res, sesoi):
        eq = res.diff.bounded_below(sesoi)
        out["contrasts"][name] = {"diff": res.diff.point, "ci": [res.diff.lo, res.diff.hi], "log_odds": None if res.log_odds is None else [res.log_odds.point, res.log_odds.lo, res.log_odds.hi],
                                  "mcnemar_p": res.mcnemar_p, "n_items": res.n_items, "n_prompts": res.n_prompts, "excludes_zero": res.diff.excludes_zero, "equivalence_within_sesoi": eq, "sesoi": sesoi}
        lo_txt = "" if res.log_odds is None else f"{res.log_odds.point:+.3f} [{res.log_odds.lo:+.3f}, {res.log_odds.hi:+.3f}]"
        mc = "" if res.mcnemar_p is None else f"{res.mcnemar_p:.3g}"
        return f"| {name} | {res.n_items} / {res.n_prompts} | {res.diff.point*100:+.1f} pp | [{res.diff.lo*100:+.1f}, {res.diff.hi*100:+.1f}] | {lo_txt} | {mc} | {'yes' if res.diff.excludes_zero else 'no'} | {'yes' if eq else 'no'} (±{sesoi*100:.0f} pp) |"

    lines += ["## Pre-registered contrasts (paired bootstrap by source prompt, 10,000 resamples)", "",
              "| Contrast | items / prompts | difference | 95 % CI | log-odds [CI] | McNemar p | CI excludes 0 | equivalence (CI within ±SESOI) |", "|---|---|---|---|---|---|---|---|"]
    c = {k: v.correct for k, v in scores.items()}
    if level == 1:
        joint = interaction_bootstrap_joint(m_on_m=c["M->M"], n_on_m=c["N->M"], m_on_n=c["M->N"], n_on_n=c["N->N"], prompt_of=prompt_of)
        indep = interaction_bootstrap(m_on_m=c["M->M"], n_on_m=c["N->M"], m_on_n=c["M->N"], n_on_n=c["N->N"], prompt_of=prompt_of)
        lines.append(contrast_row("PRIMARY: (M→M − N→M) − (M→N − N→N), joint prompt resampling (row P7)", joint, sesoi_inter))
        lines.append(contrast_row("  same, independent per-column resampling (sensitivity)", indep, sesoi_inter))
    lines.append(contrast_row("S1: M→M − N→M (Self vs Near, M's outputs)", paired_bootstrap_diff(c["M->M"], c["N->M"], prompt_of, name="S1"), sesoi_simple))
    lines.append(contrast_row("S2: N→M − F→M (Near vs Far, M's outputs)", paired_bootstrap_diff(c["N->M"], c["F->M"], prompt_of, name="S2"), sesoi_simple))
    lines.append(contrast_row("S3: M→M − F→M (Self vs Far, M's outputs)", paired_bootstrap_diff(c["M->M"], c["F->M"], prompt_of, name="S3"), sesoi_simple))
    if level == 1:
        lines.append(contrast_row("S4: N→N − M→N (Self vs Near, N's outputs)", paired_bootstrap_diff(c["N->N"], c["M->N"], prompt_of, name="S4"), sesoi_simple))
        lines.append(contrast_row("S5: F→M − F→N (Far capability check; different item sets, unpaired)", _unpaired(c["F->M"], c["F->N"], prompt_of), sesoi_simple))
    lines.append("")

    # baseline D per column
    lines += ["## Condition D — surface baseline per target column (5-fold CV grouped by prompt; never on the similarity axis)", "", "| Column | n | D accuracy | > 58 % voids column? |", "|---|---|---|---|"]
    for col, cd in cols.items():
        ids = sorted(cd.usable)
        d = fit_baseline_cv(target_column=col, item_ids=ids, texts=[cd.texts[i] for i in ids],
                            labels=[int(cd.labels[i].persona_key == pair.key_b) for i in ids], groups=[cd.prompt_of[i] for i in ids])
        out["baseline"][col] = {"n": d.n_items, "acc": d.accuracy, "voids": d.voids_column}
        lines.append(f"| {col} | {d.n_items} | {d.accuracy:.3f} | {'YES — self-advantage claim on this column is void' if d.voids_column else 'no'} |")
    lines.append("")

    # quality / exclusions
    lines += ["## Generation quality (label-blind rules, row P11)", ""]
    for col, cd in cols.items():
        lines.append(f"- Column {col}: {len(cd.texts)} generated, {len(cd.usable)} usable ({len(cd.usable)/max(len(cd.texts),1):.1%}); exclusion reasons {dict(cd.quality_reasons) or '—'}; generator returned `{cd.generator_model}` @ `{cd.generator_provider}`.")
    lines.append("")
    cal = json.loads((RESULTS / "calibration.json").read_text(encoding="utf-8"))
    lines += ["## Measured similarity (Phase C, see 07)", "", f"A_near = {cal['a_near']:.3f}, A_far = {cal['a_far']:.3f}, Δ = {cal['delta']:+.3f} [{cal['delta_ci'][0]:+.3f}, {cal['delta_ci'][1]:+.3f}] on {cal['n_items']} items; Far = `{cal['far_model']}`{' (swapped)' if cal.get('swapped') else ''}.", ""]
    lines += ["## Scope reminder", "", "Any self-advantage here is **same-weights behavioural self-modelling** — never same-episode memory, never activation-level introspection. A null is reported as an equivalence bound, not as 'not significant'.", ""]
    (ROOT / "09_main_results.md").write_text("\n".join(lines), encoding="utf-8")
    (RESULTS / "main_results.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    save_state(ANALYSIS_done=True)
    log("ANALYSIS done -> 09_main_results.md")


def _unpaired(a, b, prompt_of):
    """F->M vs F->N are on different item sets: independent prompt-clustered bootstrap of the difference."""
    import numpy as np
    from selfpred.analysis.stats import BootstrapCI, ContrastResult, _prompt_index, _resample_positions
    ia = sorted(a); ib = sorted(b)
    va = np.asarray([a[i] for i in ia], float); vb = np.asarray([b[i] for i in ib], float)
    pa, bpa = _prompt_index(ia, prompt_of); pb, bpb = _prompt_index(ib, prompt_of)
    rng = np.random.default_rng(config.BOOTSTRAP_SEED); d = np.empty(10_000)
    for k in range(10_000):
        d[k] = va[_resample_positions(pa, bpa, rng)].mean() - vb[_resample_positions(pb, bpb, rng)].mean()
    return ContrastResult(name="S5", diff=BootstrapCI(float(va.mean() - vb.mean()), float(np.quantile(d, .025)), float(np.quantile(d, .975)), n_boot=10_000),
                          log_odds=None, mcnemar_p=None, n_items=len(ia) + len(ib), n_prompts=len(pa) + len(pb))


# ======================================================================================
# Phase E2 — the crossed design on TWO stimulus sets (02 amendment A4)
# ======================================================================================
#
# The pilot produced one leaky pair (VO-C, D = 0.650 on M) and one clean pair
# (VO-D, D = 0.325 on M). Running the full crossed 2x2 on both turns surface leakage into a
# manipulated variable: style-matching predicts a self-advantage on VO-C that disappears on
# VO-D; privileged access predicts it survives on VO-D. Main prompts are disjoint from the
# pilot prompts, so the stimulus sets were selected on data these cells do not reuse.

E2_PAIRS = ("VO-C", "VO-D")


def stage_e2(pair_ids: tuple[str, ...] = E2_PAIRS, n_prompts: int = 200) -> None:
    done = list(state().get("E2_done", []))
    book = price_book()
    prompts = load_prompts("prompts_main.json")[:n_prompts]
    effective_far()
    log(f"E2: {len(prompts)} main prompts x 2 personas per column; pairs {pair_ids}")
    for pid in pair_ids:
        if pid in done:
            log(f"E2: {pid} already done"); continue
        pair = next(p for p in candidate_pairs() if p.pair_id == pid)
        tag = f"_main_{pid}"
        for col in ("M", "N"):
            spec = config.model(col)
            log(f"E2 {pid}: generating column {col} ({len(prompts)}x2) on {spec.model_id}")
            generate_column(column=col, generator_model_id=spec.model_id,
                            generator_provider=spec.provider, prompts=prompts, pair=pair,
                            price_book=book, phase="generation",
                            labels_dir=config.LABELS_DIR, run_tag=tag)
        for cell in config.ALL_CELLS:
            cd = load_column(cell.target, run_tag=tag, labels_dir=config.LABELS_DIR)
            items = [GeneratedItem(i, cd.prompt_of[i], cell.target, cd.texts[i]) for i in cd.texts]
            log(f"E2 {pid}: predicting {cell.name} ({len(items)} items)")
            run_cell(cell=cell, items=items, persona_keys=pair.keys, persona_clauses=pair.clauses,
                     price_book=book, phase="prediction", run_tag=tag)
        done.append(pid)
        save_state(E2_done=done)
        log(f"E2 {pid} done. Spend ${spend():.4f}")


def _discrimination(pair_id: str, cell_name: str) -> float | None:
    """Share of prompts where the predictor gave BOTH responses the same persona label."""
    path = config.GENERATED_DIR / f"predictions_{cell_name.replace('->', '_to_')}_main_{pair_id}.jsonl"
    if not path.exists():
        return None
    by: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if not r.get("chosen_letter"):
            continue
        pred = r["option_a_persona"] if r["chosen_letter"] == "A" else r["option_b_persona"]
        by.setdefault(r["source_prompt_id"], []).append(pred)
    pairs = [v for v in by.values() if len(v) == 2]
    return (sum(1 for v in pairs if v[0] == v[1]) / len(pairs)) if pairs else None


def stage_analysis2(pair_ids: tuple[str, ...] = E2_PAIRS) -> None:
    """Pre-specified analysis from 02 amendment A4. Reports every cell of both sets."""
    out: dict = {"pairs": {}}
    per_set_selfadv: dict[str, dict] = {}
    for pid in pair_ids:
        pair = next(p for p in candidate_pairs() if p.pair_id == pid)
        tag = f"_main_{pid}"
        cols = {c: load_column(c, run_tag=tag, labels_dir=config.LABELS_DIR) for c in ("M", "N")}
        prompt_of = {**cols["M"].prompt_of, **cols["N"].prompt_of}
        scores, cells = {}, {}
        for cell in config.ALL_CELLS:
            sc = score_cell(cell, cols[cell.target], run_tag=tag)
            scores[cell.name] = sc.correct
            acc, lo, hi = accuracy_ci(sc.correct, cols[cell.target].prompt_of)
            cells[cell.name] = {
                "acc": acc, "lo": lo, "hi": hi, "n": len(sc.correct),
                "n_malformed": sc.n_malformed, "a_share": sc.a_share,
                "provider_ok_for_self": sc.provider_ok_for_self,
                "same_persona_both": _discrimination(pid, cell.name),
            }
            log(f"  {pid} {cell.name}: {acc:.3f} [{lo:.3f},{hi:.3f}] n={len(sc.correct)}")
        d_per_col = {}
        for c in ("M", "N"):
            cd = cols[c]; usable = sorted(cd.usable)
            d = fit_baseline_cv(target_column=c, item_ids=usable,
                                texts=[cd.texts[i] for i in usable],
                                labels=[int(cd.labels[i].persona_key == pair.key_b) for i in usable],
                                groups=[cd.prompt_of[i] for i in usable])
            d_per_col[c] = d.accuracy
            log(f"  {pid} baseline D column {c}: {d.accuracy:.3f}")
        self_adv = paired_bootstrap_diff(scores["M->M"], scores["N->M"], prompt_of,
                                         name=f"{pid}: M->M - N->M")
        inter = interaction_bootstrap_joint(m_on_m=scores["M->M"], n_on_m=scores["N->M"],
                                            m_on_n=scores["M->N"], n_on_n=scores["N->N"],
                                            prompt_of=prompt_of)
        near_far = paired_bootstrap_diff(scores["N->M"], scores["F->M"], prompt_of,
                                         name=f"{pid}: N->M - F->M")
        self_far = paired_bootstrap_diff(scores["M->M"], scores["F->M"], prompt_of,
                                         name=f"{pid}: M->M - F->M")
        out["pairs"][pid] = {
            "cells": cells, "baseline_d": d_per_col,
            "self_vs_near": _ci(self_adv), "interaction": _ci(inter),
            "near_vs_far": _ci(near_far), "self_vs_far": _ci(self_far),
        }
        per_set_selfadv[pid] = {"scores": scores, "prompt_of": prompt_of}
        log(f"  {pid} self-adv (M->M - N->M) = {self_adv.diff}; interaction = {inter.diff}")

    # ---- PRIMARY: leakage contrast across the two stimulus sets -----------------------
    if len(pair_ids) == 2:
        a, b = pair_ids
        out["primary_leakage_contrast"] = _cross_set_selfadv(per_set_selfadv[a], per_set_selfadv[b], a, b)
        log(f"  PRIMARY leakage contrast ({a} - {b}): {out['primary_leakage_contrast']}")
    (RESULTS / "main_two_set.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    save_state(ANALYSIS2_done=True)
    log("ANALYSIS2 done -> data/results/main_two_set.json")


def _ci(res) -> dict:
    return {"point": res.diff.point, "lo": res.diff.lo, "hi": res.diff.hi,
            "n_items": res.n_items, "n_prompts": res.n_prompts,
            "mcnemar_p": res.mcnemar_p,
            "log_odds": None if res.log_odds is None else
                        {"point": res.log_odds.point, "lo": res.log_odds.lo, "hi": res.log_odds.hi}}


def _cross_set_selfadv(set_a: dict, set_b: dict, name_a: str, name_b: str) -> dict:
    """[(M->M - N->M) in set A] - [(M->M - N->M) in set B], sets resampled independently."""
    import numpy as np
    from selfpred.analysis.stats import _prompt_index, _resample_positions

    def prep(s):
        shared = sorted(set(s["scores"]["M->M"]) & set(s["scores"]["N->M"]))
        mm = np.asarray([s["scores"]["M->M"][i] for i in shared], float)
        nm = np.asarray([s["scores"]["N->M"][i] for i in shared], float)
        prompts, by = _prompt_index(shared, s["prompt_of"])
        return mm, nm, prompts, by

    mma, nma, pa, bya = prep(set_a)
    mmb, nmb, pb, byb = prep(set_b)
    rng = np.random.default_rng(config.BOOTSTRAP_SEED)
    boot = np.empty(10_000)
    for k in range(10_000):
        ia = _resample_positions(pa, bya, rng)
        ib = _resample_positions(pb, byb, rng)
        boot[k] = (mma[ia].mean() - nma[ia].mean()) - (mmb[ib].mean() - nmb[ib].mean())
    point = float((mma.mean() - nma.mean()) - (mmb.mean() - nmb.mean()))
    lo, hi = np.quantile(boot, [0.025, 0.975])
    return {"name": f"self-advantage({name_a}) - self-advantage({name_b})",
            "point": point, "lo": float(lo), "hi": float(hi),
            "self_adv_a": float(mma.mean() - nma.mean()),
            "self_adv_b": float(mmb.mean() - nmb.mean())}


STAGES = [("C", stage_c), ("D", stage_d), ("FREEZE", stage_freeze), ("E", stage_e),
          ("ANALYSIS", stage_analysis), ("E2", stage_e2), ("ANALYSIS2", stage_analysis2)]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--until", default="ANALYSIS")
    ap.add_argument("--only", default="", help="comma-separated stage names to run alone")
    ap.add_argument("--e2-prompts", type=int, default=200)
    a = ap.parse_args()
    only = [s.strip() for s in a.only.split(",") if s.strip()]
    for name, fn in STAGES:
        if only and name not in only:
            continue
        log(f"=== stage {name} ===")
        fn(n_prompts=a.e2_prompts) if name == "E2" else fn()
        if not only and name == a.until:
            break
    log(f"pipeline finished through {a.until}; total spend ${spend():.4f}")
