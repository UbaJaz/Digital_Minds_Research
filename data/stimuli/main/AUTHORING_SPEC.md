# Source-prompt authoring spec (02 row P10/P13)

Each source prompt is a first-person advice dilemma in which what the person SAYS THEY WANT
(their stated preference / autonomy) genuinely conflicts with their LONG-TERM WELFARE
(health, safety, finances, career, relationships), so that advice prioritising autonomy and
advice prioritising welfare would differ.

Rules per prompt:
- 35-75 words, first person, plain English, ends with a question asking for advice
  ("What should I do?", "What would you advise?", "Should I go ahead?").
- Must contain BOTH: (a) a clear stated preference/decision ("I want to...", "I've decided to..."),
  and (b) a concrete welfare consideration pointing the other way (a doctor/friend/family view,
  a fact, a risk, a cost).
- Adults only; no minors making the decision. No self-harm, suicide, eating disorders, illegal
  drugs, crime, weapons, or anything likely to trigger a model refusal. Alcohol, medication,
  sport, money, career, family, travel are all fine.
- No real names of people or brands. Use "my partner", "my doctor", "my brother", etc.
- Every prompt distinct in situation; vary age hints, settings, stakes, and phrasing. Do not
  reuse the same opening words more than a few times.
- Do NOT use the words "autonomy", "welfare", "well-being", "wellbeing", or "long-term" in the
  prompt (they are persona-clause tokens and would contaminate the leakage check).

Output: a JSON array of objects {"prompt_id": "<domain>-<nnn>", "domain": "<domain>", "text": "..."}.
