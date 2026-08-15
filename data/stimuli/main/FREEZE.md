# Source-prompt freeze

Frozen 2026-08-15 before any generation call on these prompts.
- Authored per AUTHORING_SPEC.md: health/money/career/lifestyle by Claude Code subagents, relationships by the main Claude Code session; screened mechanically (35-75 words, ends with '?', banned tokens absent, Jaccard<0.6 near-duplicate check) and spot-read.
- Split with seed 20260815: **pilot = 40 prompts** (8 per domain; used only for the Phase D screen/pilot and excluded from the main set); **main = 500 prompts** (-> 1000 items per target column, 02 row P4 target).
- The 10 smoke-test dilemmas (data/stimuli/smoke) are excluded from both.
- prompts_pilot.json sha256 `8e5fc263b03138da2336013b20efece84fd5b907b8b21bd9e4e3d36e3f135d78`
- prompts_main.json sha256 `925f1ae26d7119d9b6b4842df83b1ba226b211ff39d56fc81271ced3663a5640`
- Domain counts (main): {"career": 105, "health": 106, "lifestyle": 105, "money": 107, "relationships": 77}
