"""The budget guard must refuse before the call, and secrets must never surface.

These tests make no network calls.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from selfpred import client as client_mod  # noqa: E402
from selfpred import config  # noqa: E402
from selfpred.client import (  # noqa: E402
    BudgetExceeded,
    BudgetGuard,
    MissingPrice,
    PriceBook,
    redact,
)


# ---------------------------------------------------------------------------------------
# budget guard
# ---------------------------------------------------------------------------------------


def test_guard_refuses_when_phase_budget_would_break(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "RAW_DIR", tmp_path)
    guard = BudgetGuard("verification", phase_budget_usd=0.10)
    guard.check(0.05)                     # fine
    with pytest.raises(BudgetExceeded):
        guard.check(0.20)                 # would break the sub-budget


def test_guard_refuses_when_project_ceiling_would_break(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "RAW_DIR", tmp_path)
    guard = BudgetGuard("verification", phase_budget_usd=100.0)
    with pytest.raises(BudgetExceeded) as exc:
        guard.check(config.PROJECT_CEILING_USD + 0.01)
    assert "CEILING" in str(exc.value)


def test_guard_reconstructs_spend_from_the_log(tmp_path, monkeypatch) -> None:
    """A resumed process must not forget what an earlier process already spent."""
    monkeypatch.setattr(config, "RAW_DIR", tmp_path)
    log = tmp_path / "verification.jsonl"
    log.write_text(
        "\n".join(json.dumps({"cost_usd": 0.04}) for _ in range(5)) + "\n", encoding="utf-8"
    )
    guard = BudgetGuard("verification", phase_budget_usd=0.25)
    assert guard.phase_spent == pytest.approx(0.20)
    with pytest.raises(BudgetExceeded):
        guard.check(0.10)


def test_guard_rejects_unknown_phase_without_explicit_budget(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(config, "RAW_DIR", tmp_path)
    with pytest.raises(BudgetExceeded):
        BudgetGuard("not-a-phase")


def test_pricebook_refuses_to_guess() -> None:
    book = PriceBook()
    with pytest.raises(MissingPrice):
        book.project("some/unlisted-model", est_prompt_tokens=100, max_completion_tokens=4)


def test_pricebook_projection_is_arithmetically_right() -> None:
    book = PriceBook()
    book.add("x/y", 2.0, 12.0)  # USD per Mtok
    got = book.project("x/y", est_prompt_tokens=1_000_000, max_completion_tokens=1_000_000)
    assert got == pytest.approx(14.0)


def test_phase_budgets_fit_under_the_working_guard() -> None:
    total = sum(config.PHASE_BUDGETS_USD.values())
    assert total <= config.WORKING_GUARD_USD, (
        f"per-phase sub-budgets total ${total:.2f}, above the ${config.WORKING_GUARD_USD:.2f} "
        "working guard"
    )
    assert config.WORKING_GUARD_USD < config.PROJECT_CEILING_USD


# ---------------------------------------------------------------------------------------
# secrets
# ---------------------------------------------------------------------------------------


def test_redact_scrubs_openrouter_keys() -> None:
    fake = "sk-or-v1-" + "0123456789abcdef" * 4
    out = redact(f"HTTP 401 for key {fake} on /chat/completions")
    assert fake not in out
    assert "REDACTED" in out


def test_redact_scrubs_authorization_headers() -> None:
    out = redact('{"Authorization": "Bearer sk-or-v1-deadbeefdeadbeef"}')
    assert "deadbeef" not in out


def test_redacted_error_messages_are_scrubbed() -> None:
    fake = "sk-or-v1-" + "f" * 40
    err = client_mod.RedactedError(f"boom {fake}")
    assert fake not in str(err)


def test_dotenv_is_the_only_key_path() -> None:
    """The key is read from the environment loaded by dotenv, never from a call argument."""
    import inspect

    src = inspect.getsource(client_mod.OpenRouterClient.chat)
    assert "api_key" not in src and "OPENROUTER_KEY" not in src


# ---------------------------------------------------------------------------------------
# config sanity — no research decision has been silently made in code
# ---------------------------------------------------------------------------------------


def test_design_matches_02_locked_decisions() -> None:
    """02 'Post-Council Locked Decisions' (locked 2026-08-15): crossed 2x2, all six cells."""
    assert config.ACTIVE_CELLS == config.ALL_CELLS
    assert config.active_cells()[:3] == config.M_ROW


def test_model_roles_match_02_rows_p2_p3() -> None:
    assert config.model("M").model_id == "meta-llama/llama-3.1-70b-instruct"
    assert config.model("N").model_id == "nousresearch/hermes-3-llama-3.1-70b"
    assert config.model("F").model_id == "mistralai/mistral-small-3.2-24b-instruct"
    # Pinning is a validity condition: M and N must sit on one provider at one quantization.
    assert config.model("M").provider == config.model("N").provider == "DeepInfra"
    assert config.model("M").quantization == config.model("N").quantization == "fp8"
    for role in ("M", "N", "F"):
        assert config.model(role).price_prompt_usd_per_mtok is not None


def test_all_six_cells_are_expressible() -> None:
    names = {c.name for c in config.ALL_CELLS}
    assert names == {"M->M", "N->M", "F->M", "M->N", "N->N", "F->N"}
    assert config.CELL_RUN_ORDER[:3] == config.M_ROW  # M-row completes first


def test_n_ladder_steps_down_not_up() -> None:
    assert config.N_PER_CELL_LADDER == (1000, 750, 500)   # 02 row P4
    # A projection that only fits at the floor must return the floor, not the target.
    assert config.step_down_n(lambda n: 0.02 * n) == 500
    assert config.step_down_n(lambda n: 0.001 * n) == 1000
