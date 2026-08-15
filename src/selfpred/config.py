"""Single source of configuration for the sprint.

Nothing in this file is a research decision. `02_design_audit.md` is the authoritative
research design; this module only holds the knobs the design turns. Where the council's
Part 4 verdict has not yet been applied to `02`, the knob is present and *parameterised*
but left explicitly undecided (see ``CELLS`` and ``ROLES``).

Rules this module exists to enforce:
  * budgets live here and nowhere else;
  * model IDs, provider pins and quantizations are filled in from `04_model_verification.md`
    after Phase B, never guessed;
  * the run pipeline is parameterised by (predictor, target column), so M->M, N->M, F->M,
    M->N, N->N, F->N are all expressible without touching code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
LABELS_DIR = DATA_DIR / "labels"
GENERATED_DIR = DATA_DIR / "generated"
CHECKPOINT_DIR = DATA_DIR / "checkpoints"
NOTES_DIR = REPO_ROOT / "notes"

for _d in (RAW_DIR, LABELS_DIR, GENERATED_DIR, CHECKPOINT_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------------------
# Budget
# --------------------------------------------------------------------------------------

#: Hard project ceiling. The entire experimental budget for the project. Never raise this
#: in code; it is a fact about the available credit, not a preference.
PROJECT_CEILING_USD = 10.00

#: Working guard. If the *projected* total spend exceeds this, `n_per_cell` steps down
#: (500 -> 400 -> 300) rather than the design changing. Council verdict Q3.
WORKING_GUARD_USD = 7.50

#: Per-phase sub-budgets. The client refuses a call whose projected cost would push the
#: phase over its sub-budget, and refuses regardless if the project ceiling would break.
#: These must total <= WORKING_GUARD_USD (a pytest asserts it), leaving the difference
#: between the guard and the ceiling as genuine headroom rather than pre-spent budget.
PHASE_BUDGETS_USD: dict[str, float] = {
    "verification": 0.50,   # Phase B — this run
    "calibration": 0.40,    # Phase C
    "pilot": 1.20,          # Phase D
    "generation": 2.20,     # Phase E, persona generation
    "prediction": 3.10,     # Phase E, prediction cells
    "smoke": 0.08,          # pre-pilot enactment smoke test (05_status_and_plan.md §4.1)
    "scratch": 0.02,        # ad-hoc / debugging
}


# --------------------------------------------------------------------------------------
# Models — filled in from 04_model_verification.md after Phase B
# --------------------------------------------------------------------------------------

Role = Literal["M", "N", "F"]


@dataclass(frozen=True)
class ModelSpec:
    """One model in one role.

    ``model_id``   OpenRouter model slug, exactly as the API returns it.
    ``provider``   The pinned backend provider name. Fallbacks are always disabled;
                   pinning is a *validity* condition, not hygiene — M-as-generator and
                   M-as-Self-predictor must hit the identical provider and quantization
                   or the "same weights" claim is literally false (council Q5).
    ``quantization`` As reported by the endpoints API for that provider. ``None`` means
                   the provider did not state one, which must be recorded as such.
    ``price_prompt_usd_per_mtok`` / ``price_completion_usd_per_mtok``
                   Verified prices used by the budget guard's projection. Guessing these
                   defeats the guard, so they default to ``None`` and the guard raises.
    ``supports_reasoning_off`` Whether the reasoning-disable parameter was accepted with
                   zero reasoning tokens billed (ASSUMPTION 5).
    """

    model_id: str | None = None
    provider: str | None = None
    quantization: str | None = None
    price_prompt_usd_per_mtok: float | None = None
    price_completion_usd_per_mtok: float | None = None
    supports_reasoning_off: bool | None = None
    lineage_note: str = ""

    @property
    def configured(self) -> bool:
        return bool(self.model_id and self.provider)


#: PLACEHOLDERS. Phase B writes the verified triple into `04_model_verification.md`;
#: the team then transcribes it here. Leaving these unset is deliberate — an unset role
#: makes the client raise rather than silently call some default model.
#: Transcribed from 02_design_audit.md "Post-Council Locked Decisions" rows P2/P3 (locked
#: 2026-08-15), values verified in 04_model_verification.md.
MODELS: dict[Role, ModelSpec] = {
    "M": ModelSpec(
        model_id="meta-llama/llama-3.1-70b-instruct", provider="DeepInfra", quantization="fp8",
        price_prompt_usd_per_mtok=0.40, price_completion_usd_per_mtok=0.40, supports_reasoning_off=True,
        lineage_note="Target. Meta's post-training of the Llama-3.1-70B base.",
    ),
    "N": ModelSpec(
        model_id="nousresearch/hermes-3-llama-3.1-70b", provider="DeepInfra", quantization="fp8",
        price_prompt_usd_per_mtok=0.70, price_completion_usd_per_mtok=0.70, supports_reasoning_off=True,
        lineage_note="Near-Self. NousResearch post-training of the same Llama-3.1-70B base (HF card: Base model meta-llama/Llama-3.1-70B).",
    ),
    "F": ModelSpec(
        model_id="mistralai/mistral-small-3.2-24b-instruct", provider="DeepInfra", quantization="fp8",
        price_prompt_usd_per_mtok=0.094, price_completion_usd_per_mtok=0.25, supports_reasoning_off=True,
        lineage_note="Far-Self. Mistral base, different organisation/architecture family. Pre-declared swap: deepseek/deepseek-chat-v3-0324 @ SiliconFlow fp8 if calibration delta fails.",
    ),
}

#: Pre-declared Far-Self swap (02 row P3) — used only if Phase C shows A_near <= A_far.
FAR_SWAP = ModelSpec(
    model_id="deepseek/deepseek-chat-v3-0324", provider="SiliconFlow", quantization="fp8",
    price_prompt_usd_per_mtok=0.27, price_completion_usd_per_mtok=1.12, supports_reasoning_off=True,
    lineage_note="Far-Self swap candidate. DeepSeek V3 MoE.",
)


def model(role: Role) -> ModelSpec:
    spec = MODELS[role]
    if not spec.configured:
        raise RuntimeError(
            f"Role {role!r} is not configured. Fill MODELS[{role!r}] in config.py from "
            f"04_model_verification.md before running any phase that calls it."
        )
    return spec


# --------------------------------------------------------------------------------------
# Cells — the pipeline is parameterised by (predictor, target column)
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Cell:
    """One (predictor, target column) cell, e.g. predictor 'N' on column 'M' == N->M."""

    predictor: Role
    target: Role

    @property
    def name(self) -> str:
        return f"{self.predictor}->{self.target}"

    @property
    def is_self_cell(self) -> bool:
        return self.predictor == self.target


#: Every cell the pipeline can express. Which of these actually RUN is a research
#: decision that belongs to `02_design_audit.md`, not to this file. The council's Part 4
#: proposes the crossed 2x2 as primary with the M-row as fallback, but that proposal has
#: not been applied to `02` yet, so nothing here is selected.
ALL_CELLS: tuple[Cell, ...] = (
    Cell("M", "M"), Cell("N", "M"), Cell("F", "M"),   # M-row  (the current 02 design)
    Cell("M", "N"), Cell("N", "N"), Cell("F", "N"),   # N-column (crossed control)
)

M_ROW: tuple[Cell, ...] = ALL_CELLS[:3]
N_COLUMN: tuple[Cell, ...] = ALL_CELLS[3:]

#: Run order, when a design that includes the N column is eventually locked: the M-row
#: completes first so the pre-registered fallback is always whole (council Q1 / Q4).
CELL_RUN_ORDER: tuple[Cell, ...] = M_ROW + N_COLUMN

#: Locked 2026-08-15 (02 row P1): crossed 2x2 primary -> all six cells, M-row first.
#: The M-row-only fallback (level 2) is expressed by setting this to M_ROW.
ACTIVE_CELLS: tuple[Cell, ...] | None = ALL_CELLS


def active_cells() -> tuple[Cell, ...]:
    if ACTIVE_CELLS is None:
        raise RuntimeError(
            "ACTIVE_CELLS is None: no cell set has been locked. Update "
            "02_design_audit.md first, then set ACTIVE_CELLS here (M_ROW, ALL_CELLS, "
            "or an explicit tuple). Code never picks the design."
        )
    return ACTIVE_CELLS


def target_columns(cells: tuple[Cell, ...] | None = None) -> tuple[Role, ...]:
    """The distinct target columns implied by a cell set.

    Baseline D and the label store are both per-column, so most callers need this.
    """
    cells = cells if cells is not None else active_cells()
    seen: list[Role] = []
    for c in cells:
        if c.target not in seen:
            seen.append(c.target)
    return tuple(seen)


# --------------------------------------------------------------------------------------
# Sample size — with the 500 -> 400 -> 300 step-down hook
# --------------------------------------------------------------------------------------

#: 02 row P4 (locked): 1,000/cell target (500 source prompts x 2 personas), 500/cell floor.
#: Step-down trigger is stimulus supply / wall-clock; cost cannot bind at verified prices.
N_PER_CELL_LADDER: tuple[int, ...] = (1000, 750, 500)
N_SOURCE_PROMPTS_TARGET = N_PER_CELL_LADDER[0] // 2
#: 02 row P5: SESOI 5 pp for every contrast if n >= 1000/cell, else 5 pp simple / 8 pp interaction.
SESOI_SIMPLE_PP = 5.0
SESOI_INTERACTION_PP_AT_TARGET_N = 5.0
SESOI_INTERACTION_PP_BELOW_TARGET_N = 8.0
#: 02 row P9: pilot feasibility band, per column, point estimates, >= 80 items.
PILOT_SELF_BAND = (0.60, 0.80)
PILOT_D_MAX = 0.58
PILOT_MIN_ITEMS = 80
#: 02 row P7: both columns share the same source prompts -> joint prompt resampling.
SHARED_PROMPTS_ACROSS_COLUMNS = True
N_PER_CELL_FLOOR = N_PER_CELL_LADDER[-1]


def step_down_n(projected_total_usd_at: "callable", *, guard_usd: float = WORKING_GUARD_USD) -> int:
    """Pick the largest n on the ladder whose projected total fits under the guard.

    ``projected_total_usd_at`` is a callable ``(n: int) -> float`` supplied by the caller
    once real per-token prices and real token counts are known. This function makes no
    price assumptions of its own; with no verified prices there is nothing to project and
    the caller is expected to raise instead of guessing.

    Returns the floor if even the floor does not fit — stepping below the floor is a
    research decision (fallback ladder), not an arithmetic one.
    """
    for n in N_PER_CELL_LADDER:
        if projected_total_usd_at(n) <= guard_usd:
            return n
    return N_PER_CELL_FLOOR


# --------------------------------------------------------------------------------------
# Sampling / determinism
# --------------------------------------------------------------------------------------

SEED = 20260815              # master seed; per-phase seeds derive from it
CALIBRATION_SEED = SEED + 1  # item order and A/B randomisation
PERSONA_ORDER_SEED = SEED + 2  # persona option counterbalancing in predictor prompts
BOOTSTRAP_SEED = SEED + 3

PREDICTOR_TEMPERATURE = 0.0   # predictors are deterministic-as-possible
GENERATION_TEMPERATURE = 1.0  # 02 row P6 (locked): 1.0, logged per item
MAX_PREDICTION_TOKENS = 4     # one letter, plus slack
GENERATION_MAX_TOKENS = 400   # ~200 words of advice + slack (smoke test saw 1/40 truncations at 320)
REQUEST_TIMEOUT_S = 60.0

#: Malformed one-letter output: one retry with the identical prompt, then log and move on.
#: Exclusion of a still-malformed item is a research rule and lives in `02`, not here.
MALFORMED_RETRIES = 1
MALFORMED_RATE_PASS_THRESHOLD = 0.05  # council Q2 verification criterion

# --------------------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------------------

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_KEY_ENV_VAR = "OPENROUTER_KEY"

#: Optional attribution headers OpenRouter accepts. Never put a secret here.
OPENROUTER_HEADERS = {
    "HTTP-Referer": os.environ.get("SELFPRED_REFERER", "https://github.com/UbaJaz/Digital_Minds_Research"),
    "X-Title": "Digital Minds Sprint Track 3",
}

LOG_PATHS: dict[str, Path] = {
    phase: RAW_DIR / f"{phase}.jsonl" for phase in PHASE_BUDGETS_USD
}
