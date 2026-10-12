# Q3 - LLM-based ESG message triage experiment
# Run in Google Colab with a T4 GPU (Runtime > Change runtime type > T4 GPU).
# Each "# %% Cell" block below was one Colab cell. Run them in order.
# Tested: 12 October 2026, transformers (latest Colab build), Qwen/Qwen2.5-1.5B-Instruct, facebook/bart-large-mnli.

# %% Cell 1 - setup
# !pip install -q transformers accelerate
import torch
print("GPU ready:", torch.cuda.is_available())

# %% Cell 2 - test messages + rule-based baseline
import pandas as pd, json, re

messages = [
    "There is a water leak in Building C that has been running all morning.",
    "The recycling bins are contaminated again and no one seems to be checking them.",
    "The air conditioning is running overnight in an empty office.",
    "I want to report that one of our suppliers may not meet our sustainability policy.",
    "The accessible entrance near the main building has been blocked for two days.",
    "Someone spilled chemicals near the loading dock and a worker says they feel dizzy.",
    "Not urgent, but the lights in meeting room 4 keep getting left on after hours.",
]

rules = {
    "water_leak": ["leak", "pipe", "flood", "drip"],
    "waste_contamination": ["recycl", "bin", "contaminat", "rubbish"],
    "energy_waste": ["air conditioning", "aircon", "lights", "heater", "energy"],
    "supplier_compliance": ["supplier", "procurement", "vendor"],
    "accessibility_barrier": ["accessible", "ramp", "wheelchair", "lift"],
    "hazardous_spill": ["spill", "chemical", "hazard"],
}
teams = {
    "water_leak": "Facilities", "waste_contamination": "Waste & Sustainability",
    "energy_waste": "Energy Management", "supplier_compliance": "Procurement",
    "accessibility_barrier": "Facilities + Diversity & Inclusion",
    "hazardous_spill": "Health & Safety", "unknown": "Human review",
}
urgent_words = ["leak", "blocked", "spill", "dizzy", "injur", "unsafe"]

def rule_classify(msg):
    m = msg.lower()
    cat = next((c for c, kws in rules.items() if any(k in m for k in kws)), "unknown")
    urgency = "HIGH" if any(w in m for w in urgent_words) else "MEDIUM"
    return {"issue_category": cat, "urgency": urgency, "recommended_team": teams[cat]}

rule_df = pd.DataFrame([{"message": m, **rule_classify(m)} for m in messages])
rule_df

# %% Cell 3 - Hugging Face zero-shot baseline
from transformers import pipeline

zs = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

cat_labels = {
    "water leak": "water_leak",
    "recycling or waste contamination": "waste_contamination",
    "energy waste": "energy_waste",
    "supplier sustainability compliance": "supplier_compliance",
    "accessibility barrier": "accessibility_barrier",
    "hazardous chemical spill": "hazardous_spill",
}
urg_labels = {"critical emergency": "CRITICAL", "high urgency": "HIGH",
              "medium urgency": "MEDIUM", "low urgency": "LOW"}

rows = []
for m in messages:
    c = zs(m, list(cat_labels.keys()))
    u = zs(m, list(urg_labels.keys()))
    rows.append({"message": m,
                 "issue_category": cat_labels[c["labels"][0]],
                 "category_confidence": round(c["scores"][0], 2),
                 "urgency": urg_labels[u["labels"][0]],
                 "urgency_confidence": round(u["scores"][0], 2)})
zs_df = pd.DataFrame(rows)
zs_df

# %% Cell 4 - load the LLM and the two prompts
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(model_id)
llm = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float16, device_map="cuda")

ORIGINAL = open("prompts/original_prompt.txt").read()   # or paste the text inline
REVISED = open("prompts/revised_prompt.txt").read()
# NOTE: when pasting REVISED inline, double the JSON braces ({{ }}) so .format() works.

# %% Cell 5 - ask() helper
# Fixed version: newer transformers returns a dict from apply_chat_template,
# so return_dict=True is needed (the first version failed with KeyError: 'shape').
def ask(template, msg):
    prompt = template.replace("{message}", msg)
    chat = [{"role": "user", "content": prompt}]
    enc = tok.apply_chat_template(chat, add_generation_prompt=True,
                                  return_tensors="pt", return_dict=True).to("cuda")
    out = llm.generate(**enc, max_new_tokens=300, do_sample=False)   # greedy = repeatable
    text = tok.decode(out[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
    found = re.search(r"\{.*\}", text, re.S)
    try:
        parsed = json.loads(found.group(0)) if found else None
    except Exception:
        parsed = None
    return text, parsed

# %% Cell 6 - run both prompts on all messages and compare
def flatten(p):
    if isinstance(p, dict) and isinstance(p.get("issues"), list) and p["issues"]:
        return p["issues"][0]
    if isinstance(p, list) and p:
        return p[0]
    return p if isinstance(p, dict) else {}

results = []
for i, m in enumerate(messages):
    for name, tpl in [("original", ORIGINAL), ("revised", REVISED)]:
        raw, parsed = ask(tpl, m)
        p = flatten(parsed)
        results.append({"msg_id": i, "prompt": name, "valid_json": parsed is not None,
                        "issue_category": p.get("issue_category"), "urgency": p.get("urgency"),
                        "recommended_team": p.get("recommended_team"),
                        "needs_human_review": p.get("needs_human_review"),
                        "raw_output": raw})

llm_df = pd.DataFrame(results)
orig = llm_df[llm_df.prompt == "original"].reset_index(drop=True)
rev = llm_df[llm_df.prompt == "revised"].reset_index(drop=True)

comparison = pd.DataFrame({
    "message": [m[:45] + "..." for m in messages],
    "rules_urgency": rule_df["urgency"],
    "zeroshot_urgency": zs_df["urgency"],
    "llm_original_urgency": orig["urgency"],
    "llm_revised_urgency": rev["urgency"],
    "llm_original_category": orig["issue_category"],
    "llm_revised_category": rev["issue_category"],
    "revised_human_review": rev["needs_human_review"],
})
comparison

# %% Cell 7 - print sample JSON and save evidence
for i in [0, 4, 5]:
    print(f"\n=== Message {i}: {messages[i]}")
    print(rev.loc[i, "raw_output"])

llm_df.to_csv("results/q3_llm_outputs.csv", index=False)
comparison.to_csv("results/q3_comparison.csv", index=False)
rule_df.to_csv("results/q3_rule_baseline.csv", index=False)
zs_df.to_csv("results/q3_zero_shot.csv", index=False)
