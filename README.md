# Assessment 3 – RPA, AI and Cloud-Enabled ESG Analytics

Evidence repository for Assessment 3 (La Trobe University, Semester 2 2026).
Author: Vatika

| Folder | Contents |
|---|---|
| [`q1_dialogflow_chatbot/`](q1_dialogflow_chatbot/) | GreenDesk ESG Assistant: build summary, test transcripts, screenshots |
| [`q3_llm_triage/`](q3_llm_triage/) | LLM triage experiment: Colab code, original and revised prompts, raw CSV outputs, [experiment log](q3_llm_triage/EXPERIMENT_LOG.md) |
| [`q4_notebooklm/`](q4_notebooklm/) | NotebookLM evaluation: [experiment log](q4_notebooklm/EXPERIMENT_LOG.md), study guide, audio overview and transcript, screenshots |

**Q1 demonstration video:** [Watch the video on Microsoft Stream](https://latrobeuni-my.sharepoint.com/:v:/g/personal/22884063_students_ltu_edu_au/IQBVy0OzSy2iQIGthHeS78-UAc_8YGKst8aOBRFUZiYgqaU?e=Kh16zs)

## Reproducing Q3

1. Open Google Colab, set **Runtime → Change runtime type → T4 GPU**.
2. Upload the `prompts/` folder, then run the cells in [`q3_esg_triage_colab.py`](q3_llm_triage/q3_esg_triage_colab.py) in order.
3. Greedy decoding (`do_sample=False`) is used, so outputs should repeat closely on the same model version.

## Generative AI use

Category: **AI Exploration**. Claude (Anthropic) was used to guide the Dialogflow build, write the Colab code and prompts, and draft analysis. All tools were run and all screenshots captured by the author; the AI outputs evaluated in Q3 and Q4 are recorded unedited.
