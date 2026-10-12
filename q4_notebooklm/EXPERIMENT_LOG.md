# Q4 Experiment Log – NotebookLM evaluation

**Date run:** 12 October 2026 · **Tool:** Google NotebookLM (free access)
**Scenario:** A business student preparing a briefing on Australia's mandatory climate reporting rules.

## Sources loaded (3)

| Source | Type | Link |
|---|---|---|
| AASB S2 Climate-related Disclosures (Sep 2024) | PDF upload | [standards.aasb.gov.au](https://standards.aasb.gov.au/sites/default/files/2025-01/AASBS2_09-24.pdf) |
| ASIC Regulatory Guide 280 Sustainability Reporting (31 Mar 2025) | PDF upload | [asic.gov.au](https://download.asic.gov.au/media/j4rhwyiz/rg280-published-31-march-2025.pdf) |
| Hamilton Locke: "ASIC Regulatory Guide 280 – what it means in practice" | Web page | [hamiltonlocke.com.au](https://hamiltonlocke.com.au/asic-regulatory-guide-280-what-it-means-for-sustainability-reporting-in-practice/) |

## Tests and results

Accuracy was checked by the author against the source documents (AASB S2 paragraphs were checked directly in the PDF).

| # | Feature | Prompt / setting | Result | Accuracy | Verdict |
|---|---|---|---|---|---|
| 1 | Auto notebook overview | Automatic on upload | Correct one-paragraph summary of the three sources | Accurate | Useful orientation |
| 2 | Chat Q&A with citations | "Which companies must report under AASB S2, and from when? Answer in 3 bullet points." | Groups 1–3, start dates 1 Jan 2025 / 1 Jul 2026 / 1 Jul 2027, size thresholds; citations 1, 4, 5, 9 | **Correct** | Strong; ignored "3 bullets" format (added intro + follow-up) |
| 3 | Chat Q&A with citations | "What is the 'modified liability' period and which disclosures does it cover?" | 3-year protection (FY starting 1 Jan 2025–31 Dec 2027) for Scope 3, scenario analysis, transition plans; 1-year for forward-looking statements; exclusions listed | **Correct**, well structured | Strongest output |
| 4 | Hallucination probe | "What were Woolworths' Scope 3 emissions in its 2025 AASB S2 report?" (not in sources) | Stated the sources do not contain this; offered related cited facts; offered web search | **No hallucination** | Passed; web-search offer is a risk (unvetted sources) |
| 5 | Mind Map | Topic: who must report, AASB S2 requirements, modified liability | 3 branches, 4 levels, 40+ nodes | Mostly accurate; **merged 1-year and 3-year protection periods** under "first three years" | Good for revision; loses precision |
| 6 | Flashcards | Thresholds, dates, modified liability | 24 cards; card 1: legal commencement 31 Dec 2024 (para Aus37.2) | **Correct** (verified in PDF) | Accurate but prioritises a technicality over the application date |
| 7 | Report → Document (Study Guide) | Focus: AASB S2 + RG 280, four pillars, Scope 1–3, modified liability | 11-page guide with quiz, answer key, glossary, paragraph refs (B18, B40, AusB22.1) | Facts checked were correct | **Ignored RG 280, the law-firm source and modified liability entirely**; export showed raw LaTeX (`$\text{CO}_2\text{e}$`), broken tables, mis-numbered list |
| 8 | Audio Overview (Deep Dive, "Short") | Focus: who reports, when, modified liability | 5 min 44 s two-host discussion | Mostly accurate; called the protection immunity from "civil penalty proceedings" (chat said private litigation – tools disagree); speculated Group 1 are "guinea pigs" (not in sources) | Engaging and accessible; no citations; ignored "Short" |

## Cross-feature findings

- **Grounding works best in chat**, where every claim has a clickable citation. Generated artefacts (mind map, audio, study guide) lose citations and precision.
- **Omission is harder to spot than error.** The study guide looked complete but silently dropped two of three sources.
- **Instruction-following is partial:** format and length requests (3 bullets, "Short") were ignored.
- **Different features gave different answers** to the same question (liability scope), so students must check against sources.
- **Usage limits:** the free tier's AI usage bar was about half used after two Studio outputs.

## Files

- [`outputs/notebooklm_study_guide.pdf`](outputs/notebooklm_study_guide.pdf) – exported study guide
- [`outputs/audio_overview.m4a`](outputs/audio_overview.m4a) – Audio Overview
- [`outputs/audio_overview_transcript_machine.txt`](outputs/audio_overview_transcript_machine.txt) – rough offline machine transcript (PocketSphinx), used to analyse the audio
- [`screenshots/`](screenshots/) – every test above
