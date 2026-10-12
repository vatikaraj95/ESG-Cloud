# Q3 Experiment Log – LLM triage of ESG operational messages

**Date run:** 12 October 2026 · **Environment:** Google Colab, T4 GPU
**Models:** `Qwen/Qwen2.5-1.5B-Instruct` (open-source LLM, greedy decoding, 300 max tokens) · `facebook/bart-large-mnli` (Hugging Face zero-shot baseline) · keyword rule baseline
**Code:** [`q3_esg_triage_colab.py`](q3_esg_triage_colab.py) · **Prompts:** [`prompts/`](prompts/) · **Raw outputs:** [`results/`](results/)

## Test set

Seven messages: the five sample messages from the brief plus two added edge cases.

| # | Message | Expected urgency (analyst judgement) |
|---|---|---|
| 0 | Water leak in Building C running all morning | HIGH |
| 1 | Recycling bins contaminated again | MEDIUM |
| 2 | Air conditioning running overnight in empty office | MEDIUM |
| 3 | Supplier may not meet sustainability policy | MEDIUM |
| 4 | Accessible entrance blocked for two days | HIGH |
| 5 | **Edge case:** chemical spill, worker feels dizzy | CRITICAL |
| 6 | **Edge case:** "Not urgent", lights left on after hours | LOW |

## Results

| # | Rules | Zero-shot (confidence) | LLM original prompt | LLM revised prompt | Revised category |
|---|---|---|---|---|---|
| 0 | HIGH | HIGH (0.41) | HIGH | CRITICAL | water_leak |
| 1 | MEDIUM | MEDIUM (0.38) | HIGH | MEDIUM | waste_contamination |
| 2 | MEDIUM | MEDIUM (0.44) | HIGH | LOW | energy_waste |
| 3 | MEDIUM | HIGH (0.40) | HIGH | CRITICAL | supplier_compliance |
| 4 | HIGH | MEDIUM (0.40) | HIGH | HIGH | accessibility_barrier |
| 5 | HIGH | MEDIUM (0.40) | HIGH | **CRITICAL** | hazardous_spill |
| 6 | MEDIUM | LOW (0.94) | LOW | LOW | energy_waste |

### Scorecard

| Method | Category correct | Urgency matches expected | Caught the CRITICAL safety case |
|---|---|---|---|
| Keyword rules | 7/7 | 5/7 | No (cannot output CRITICAL) |
| Zero-shot (BART-MNLI) | 7/7 | 4/7 | No (MEDIUM) |
| LLM, original prompt | 0/7 usable (free-text labels: "Infrastructure", "Operational", "Security"…) | 3/7 (6 of 7 = HIGH) | No (HIGH) |
| LLM, revised prompt | 7/7 | 4/7 | **Yes** |

The rule baseline scores well on urgency only because its keywords were written with these seven messages in view; it would not generalise.

## Observations

1. **Original prompt is not routable.** No fixed category list, so the model invented categories that do not map to a team, and it rated almost everything HIGH.
2. **Revised prompt fixed categorisation and caught the emergency**, but **over-escalated** messages 0 and 3 to CRITICAL and **under-rated** message 2 (LOW).
3. **Hallucination despite instructions.** Message 0: escalation reason "Water leakage poses a significant health and safety hazard" – not in the message. Message 4: summary says "blocked **ramp**" – the message said "entrance".
4. **Overconfidence.** Self-reported `confidence: 1` on message 0, which was mis-rated. `data_sensitivity_risk` was HIGH on messages containing no personal or health data.
5. **Human-review flag over-triggered:** 6 of 7 marked `needs_human_review: true`, including the "not urgent" message, which would overload reviewers.
6. **Zero-shot urgency is near chance:** confidence ≈ 0.40 across four labels; categories were strong (0.63–0.97).

## Debugging notes

- Colab runtime reset after ~30 min idle → `NameError: torch` → fixed with Runtime > Run all.
- `KeyError: 'shape'` – newer transformers returns a dict from `apply_chat_template`; fixed with `return_dict=True` (see Cell 5).

## Screenshots

See [`screenshots/`](screenshots/): rule baseline, zero-shot table, comparison table, revised prompt code, JSON outputs.
