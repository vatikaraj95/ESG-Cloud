# Q1 – GreenDesk ESG Assistant (Dialogflow CX)

Text chatbot that lets staff report a sustainability incident and routes it to an urgent or standard pathway.
Built in Dialogflow CX (Conversational Agents console), region `australia-southeast1`, 11 October 2026.

| Component | Built |
|---|---|
| Entity types | `@incident_type` (5 values with synonyms), `@yes_no` |
| Intents | report_incident (12 phrases), talk_to_human (8), recycling_guidance (8), check_status (7) |
| Form (Collect Incident Details) | incident_type, location (`@sys.any`), people_at_risk |
| Branching | `$page.params.status = "FINAL" AND $session.params.people_at_risk = "Yes"` → Urgent Escalation; `"No"` → Standard Ticket |
| Fallback | `sys.no-match-default` on Start Page and Collect Incident Details |
| Endpoints | Urgent Escalation, Standard Ticket, human handover → End Session |

## Tests (all passed)

| Test | Screenshot |
|---|---|
| Urgent path (water leak, "Yes") | `Q1_test_urgent.png` |
| Standard path (contaminated recycling, "no") | `Q1_test_standard.png` |
| Fallback ("cat") | `Q1_test_fallback.png` |
| Human handover | `Q1_test_human.png` |
| Bug found: silent bot after "yes" – entity stored "Yes", condition checked "yes"; fixed | `Q1_debug_panel_yes.png` |
