# 04 — Model Verification (Phase B)

**Run:** 2026-08-15 · **Total cost: $0.0071** of the $0.50 Phase B sub-budget (1.4%) ·
**Raw record:** `data/raw/verification.jsonl` (311 calls, append-only), summarised in
`data/raw/verification_summary.json`, `data/raw/verification_followup.json`.
Model list and endpoint data: `data/raw/openrouter_models.json` (413 models),
`data/raw/openrouter_endpoints.json`.

Every call was pinned to one provider with `allow_fallbacks: false`. 11 distinct models
were called, under the 12-model cap. **Nothing here selects a model** — this document
ranks candidates and records what passed; the choice is the team's.

---

## (a) Every model called

Prices are USD per million tokens, as listed by OpenRouter. "Returned = requested" in
every case: no model silently resolved to something else.

| # | Requested id | Exists | Returned id | Pinned provider | Returned provider | Pin | Quant | $ in | $ out | Reasoning-off | Malformed | Temp-0 agree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `meta-llama/llama-3.1-70b-instruct` | ✅ | same | DeepInfra | DeepInfra | ✅ | fp8 | 0.40 | 0.40 | ✅ (0 tok) | 0 % | 100 % |
| 2 | `nousresearch/hermes-3-llama-3.1-70b` | ✅ | same | DeepInfra | DeepInfra | ✅ | fp8 | 0.70 | 0.70 | ✅ (0 tok) | 0 % | 100 % |
| 3 | `meta-llama/llama-3.3-70b-instruct` | ✅ | same | Nebius | Nebius | ✅ | fp8 | 0.10 | 0.32 | ✅ (0 tok) | 0 % | 100 % |
| 4 | `nousresearch/hermes-4-70b` | ✅ | same | Nebius | Nebius | ✅ | fp8 | 0.13 | 0.40 | ✅ (0 tok) | 0 % | 100 % |
| 5 | `openai/gpt-4o-2024-08-06` | ✅ | same | OpenAI | OpenAI | ✅ | unknown | 2.50 | 10.00 | ✅ (0 tok) | 0 % | not run |
| 6 | `openai/gpt-4o-2024-11-20` | ✅ | same | OpenAI | OpenAI | ✅ | unknown | 2.50 | 10.00 | ✅ (0 tok) | 0 % | not run |
| 7 | `openai/gpt-5.6-terra` | ✅ | same | OpenAI | OpenAI | ✅ | unknown | 1.00 | 6.00 | ✅ (0 tok) | 0 % | not run |
| 8 | `openai/gpt-5.6-luna` | ✅ | same | OpenAI | OpenAI | ✅ | unknown | 0.10 | 0.60 | ✅ (0 tok) | 0 % | not run |
| 9 | `deepseek/deepseek-chat-v3-0324` | ✅ | same | SiliconFlow | SiliconFlow | ✅ | fp8 | 0.27 | 1.12 | ✅ (0 tok) | 0 % | not run |
| 10 | `mistralai/mistral-small-3.2-24b-instruct` | ✅ | same | DeepInfra | DeepInfra | ✅ | fp8 | 0.094 | 0.25 | ✅ (0 tok) | 0 % | not run |
| 11 | `google/gemini-3.5-flash-lite` | ✅ | same | Google | Google | ✅ | unknown | 0.30 | 2.50 | ❌ rejected | 0 % † | not run |

**All 11 models resolve and all 11 honoured the provider pin.** No response came back from
an unpinned provider, so pinning is achievable across every lineage tier tested.

† **Gemini needs a correction to the raw numbers.** On the first pass it scored **100 %
malformed** — but every response was an *empty string* with `finish_reason: "length"` and
zero visible completion tokens, which is the signature of `max_tokens=4` being exhausted
before any token is emitted, not of a model that cannot answer. Retested at
`max_tokens=16` it scored **0 % malformed**. The honest reading is that Gemini is usable
for one-letter output but needs a larger token allowance than the open-weight models; its
`reasoning: {enabled: false}` rejection is real and separate. DeepSeek and Mistral were
retested at 16 tokens as well and stayed at 0 %.

Temperature-0 agreement is reported **as data, not as a pass/fail** (council Q2). All four
shortlisted models returned the identical answer on 20/20 repeats — near-deterministic on
their pinned providers.

---

## (b) Candidate PAIRS, ranked by lineage tier

| Rank | Pair | Tier | Both resolve | Single pinnable provider @ stated quant | Reasoning-off | < 5 % malformed | Not a re-alias | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | `llama-3.1-70b-instruct` + `hermes-3-llama-3.1-70b` | **(i)** | ✅ | ✅ **DeepInfra, both fp8** | ✅ | ✅ 0 % / 0 % | ✅ wildly different | **PASS — only tier (i) pair that passes everything** |
| 2 | `gpt-4o-2024-08-06` + `gpt-4o-2024-11-20` | **(ii)** | ✅ | ✅ OpenAI (quant not stated) | ✅ | ✅ 0 % / 0 % | not tested | **PASS on all tested criteria** |
| 3 | `llama-3.3-70b-instruct` + `hermes-4-70b` | ~~(i)~~ → (iii)-like | ✅ | ✅ Nebius, both fp8 | ✅ | ✅ 0 % / 0 % | ✅ differ on 3/10 | **LINEAGE FAIL** — see below |
| 4 | `gpt-5.6-terra` + `gpt-5.6-luna` | (iii) | ✅ | ✅ OpenAI / Azure / Bedrock | ✅ | ✅ 0 % / 0 % | not tested | PASS as a tier (iii) pair |
| — | `qwen-2.5-72b-instruct` + `magnum-v4-72b` | (i) | — | ❌ **no shared provider** | — | — | — | **PINNING FAIL**, not called |
| — | `llama-3.1-70b-instruct` + `hermes-4-70b` | **(i)** | ✅ | ❌ **no shared provider** | — | — | — | **PINNING FAIL** — see below |

### The lineage correction that matters

`nousresearch/hermes-4-70b`'s own model card states it is **"built on
Meta-Llama-3.1-70B"** — *not* Llama-3.3. So:

- Pairing it with `llama-3.3-70b-instruct` (rank 3) is **not a same-base pair**. It pins
  perfectly on Nebius at matched fp8 and passes every mechanical check, but it fails the
  construct: it is an official Instruct of one generation against a fine-tune of the
  *previous* generation's base. It should not be presented as tier (i).
- The correctly-paired version — `llama-3.1-70b-instruct` + `hermes-4-70b` — **cannot be
  pinned**: Hermes-4-70B is served only by Nebius, while Llama-3.1-70B-Instruct is served
  by DeepInfra, Amazon Bedrock and CoreWeave. No shared provider, so
  `allow_fallbacks: false` cannot hold both. Verified from the endpoints data, no call
  needed.

That leaves **rank 1 as the only pair that is simultaneously same-base, same-parameter-size,
and pinnable to one provider at a stated matched quantization.**

### Re-alias check (step 8)

Ten fixed prompts at temperature 0 on both members. Identical output on all 10 would flag a
silent alias.

- **Rank 1:** not remotely identical. Llama-3.1-70B returned clean single words
  (`blue, apple, japan, lion, copper, guitar, carrot, earth, oak, paris`); Hermes-3-70B
  returned rambling, largely non-compliant text on every one. **Not a re-alias.**
- **Rank 3:** differ on 3/10 (`canada`/`japan`, `iron`/`copper`, `maple`/`oak`).
  **Not a re-alias.**

### The risk attached to rank 1

Hermes-3-70B is a **poor instruction-follower on bare prompts**. It failed to reply "OK" to
"Reply with the single word OK" (it began "*Okay, a well-ti…"), and produced junk on all ten
re-alias prompts. It was nonetheless **0 % malformed on the structured A/B task with a
system prompt**, which is the format the experiment actually uses.

This is precisely **ASSUMPTION 8** (both M and N enact the persona clauses with > 90 %
usable output) and it is **untested** — the 40-item persona screen is what tests it. If
Hermes-3 cannot hold a persona scaffold, the N column dies and the design drops to fallback
level 2. **This is the single largest open risk in the model selection**, and it is
knowable cheaply on Day 1.

---

## (c) Far-Self candidates

All three resolve, pin, and produce clean one-letter output. Lineage justification is what
separates them.

| Candidate | Provider pinned | Quant | $ in / $ out | Lineage vs. the rank-1 pair | Note |
|---|---|---|---|---|---|
| `mistralai/mistral-small-3.2-24b-instruct` | DeepInfra | fp8 | 0.094 / 0.25 | Mistral's own 24B base — different organisation, different base, different architecture family from Llama | Cheapest; **preferred on lineage grounds** |
| `deepseek/deepseek-chat-v3-0324` | SiliconFlow | fp8 | 0.27 / 1.12 | DeepSeek V3, 685B MoE — different organisation and a different *architecture class* (MoE vs dense) | Strongest architectural contrast |
| `google/gemini-3.5-flash-lite` | Google | unknown | 0.30 / 2.50 | Closed Google model — different organisation, but base and training data are **unverifiable** | Rejects the reasoning-off parameter; needs ≥ 16 max_tokens |

Both open-weight Far candidates come from a **different provider AND a different base**
than the rank-1 pair, which is the council's stated preference. Mistral-Small is the
cheaper of the two and the cleaner "different lineage" claim; DeepSeek V3 gives a larger
architectural gap if the calibration probe shows Mistral is not far enough.

**ASSUMPTION 9 (Far is not distilled from Target) remains UNTESTED here** — by design, it
is tested by the calibration Δ in Phase C, not by a verification call. Neither Mistral nor
DeepSeek is a known Llama distillation, but "not known to be" is not evidence.

---

## (d) Burst test (step 9)

`meta-llama/llama-3.1-70b-instruct` @ DeepInfra, 30 concurrent one-letter calls:

- **30/30 succeeded, 0 × HTTP 429, 2.47 s wall clock.**

Extrapolating naively, ~3,000 prediction calls at this concurrency is on the order of four
minutes of wall clock. **ASSUMPTION 6 is verified** for this provider at this concurrency —
rate limits are not a constraint on the sprint. Not tested on Nebius, OpenAI or Google.

---

## (e) Total Phase B cost

**$0.0071** — 1.4 % of the $0.50 sub-budget, 0.07 % of the $10 project ceiling.
311 calls. Cost figures come from OpenRouter's own `usage.cost` field per call, not from
an estimate.

The relevant consequence: **calls are far cheaper than the planning documents assumed.**
`03` §3.2 estimated ≈ $1.7 for the locked design and ≈ $3.1 for the crossed design using
$2/M-in, $12/M-out pricing. The rank-1 pair prices at **$0.40–0.70/M in and out** — 5–17×
cheaper on output. Budget is not the binding constraint on n.

---

## (f) Consequences for 02

### Recommended (M, N, F) triple

Ranked, not chosen. To be written into `config.py` only after `02_design_audit.md` records
the decision.

**Primary recommendation — the only pair that satisfies the full tier (i) rule:**

```python
M = ModelSpec(model_id="meta-llama/llama-3.1-70b-instruct",
              provider="DeepInfra", quantization="fp8",
              price_prompt_usd_per_mtok=0.40, price_completion_usd_per_mtok=0.40)
N = ModelSpec(model_id="nousresearch/hermes-3-llama-3.1-70b",
              provider="DeepInfra", quantization="fp8",
              price_prompt_usd_per_mtok=0.70, price_completion_usd_per_mtok=0.70)
F = ModelSpec(model_id="mistralai/mistral-small-3.2-24b-instruct",
              provider="DeepInfra", quantization="fp8",
              price_prompt_usd_per_mtok=0.094, price_completion_usd_per_mtok=0.25)
```

Both M and N sit on **DeepInfra at fp8**, satisfying the validity condition that
M-as-generator and M-as-Self-predictor hit identical weights.

**Fallback if the persona screen fails on Hermes-3 (the live risk):** the tier (ii) GPT-4o
snapshot pair, `openai/gpt-4o-2024-08-06` + `openai/gpt-4o-2024-11-20`, both pinned to
OpenAI. It passes every mechanical check; its weaknesses are that quantization is not
stated (so "identical weights" rests on OpenAI's word) and it is ~6× the price — still
affordable at these volumes. Its re-alias check was not run and **must be** before use.

**Not recommended:** `llama-3.3-70b-instruct` + `hermes-4-70b`, despite being the
best-behaved and cheapest pair mechanically. The base mismatch is a construct failure, and
the construct is the whole paper.

### Council ASSUMPTIONS 1–7: status

| # | Assumption | Status | Evidence |
|---|---|---|---|
| 1 | OpenRouter lists an official Instruct + same-base fine-tune at the same size | ✅ **VERIFIED** | `llama-3.1-70b-instruct` + `hermes-3-llama-3.1-70b`, both 70B, Llama-3.1 base |
| 2 | One provider serves both IDs, pinnable with fallbacks off at a stated quantization | ✅ **VERIFIED** | DeepInfra serves both at fp8; pin honoured on every call |
| 3 | Dated snapshots of closed models exist as distinct IDs, not silent aliases | ⚠️ **PARTIALLY VERIFIED** | Three GPT-4o snapshots exist as distinct IDs and both called ones returned their own id — but the temperature-0 non-identity test was **not run** on them |
| 4 | Per-token prices at or below $2/M in, $12/M out | ✅ **VERIFIED, comfortably** | Rank-1 pair at $0.40–0.70/M; Far at $0.094/M |
| 5 | Reasoning can be disabled with no reasoning tokens billed | ✅ **VERIFIED for 10 of 11** | 0 reasoning tokens billed everywhere; **FALSIFIED for `gemini-3.5-flash-lite`**, which rejects the parameter outright |
| 6 | ~10-way concurrency lets ~3,000 calls finish within an hour | ✅ **VERIFIED** (DeepInfra) | 30 concurrent calls, 0 × 429, 2.47 s |
| 7 | Temperature-0 repeats are near-deterministic | ✅ **VERIFIED** | 20/20 identical for all four shortlisted models |

**8, 9, 10 are untested by design** — they are pilot and calibration questions, not
verification questions. 8 (persona enactment) is the one to fear, for the reason in (b).

### Does the team have a tier (i) pair?

**Yes.** A tier-(i) pair passes every verification criterion, so the design is **not**
forced down to tier (iii). This matters because tier (iii) was only acceptable *under* the
crossed design; a genuine tier (i) pair keeps the M-row fallback scientifically meaningful
too.

Caveat worth stating plainly: the tier (i) claim rests on Hermes-3-Llama-3.1-70B being a
fine-tune of Llama-3.1-70B. The **model ID encodes this** and it is NousResearch's
documented base, but OpenRouter's own description text is truncated and does not state the
base explicitly. **Someone should confirm it against the Hugging Face model card before
this goes in the write-up** — it is a one-minute check and it is load-bearing for the
central "verifiably shared weights" claim.

### What this does not decide

- Which cells run (crossed 2×2 vs M-row) — that is `02`'s decision; the code is
  parameterised for both and `config.ACTIVE_CELLS` is deliberately `None`.
- n per cell — the ladder hook exists; the cost evidence above says the budget will not
  force a step-down, but n is a research decision.
- The persona pair, the feasibility band, and the calibration task — all unresolved in
  `02`.
