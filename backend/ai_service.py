import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Lazy imports for faster startup
def _use_openai(prompt: str):
    import openai
    openai.api_key = OPENAI_API_KEY
    # Try moderation first (safer), else use completion for richer explanation
    try:
        mod = openai.Moderation.create(input=prompt)
        mod_res = mod["results"][0]
        flagged = mod_res.get("flagged", False)
        categories = mod_res.get("categories", {})
        score = 1.0 if flagged else 0.0
        explanation = f"Moderation flags: {categories}"
        label = "malicious" if flagged else "benign"
        return {"label": label, "score": score, "explanation": explanation}
    except Exception:
        # fallback to instruction-based classification
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role":"system","content":"You are an assistant that classifies prompts as benign or malicious (prompt-injection, data-exfiltration, jailbreak, or code-execution). Return JSON only with keys label, score, explanation."},
                {"role":"user","content": f"Classify and explain this prompt:\n\n{prompt}"}
            ],
            temperature=0
        )
        text = resp["choices"][0]["message"]["content"]
        import json
        try:
            return json.loads(text)
        except Exception:
            return {"label":"unknown","score":0.0,"explanation":text}

def _use_hf_zero_shot(prompt: str):
    from transformers import pipeline
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    labels = ["benign", "prompt-injection", "data-exfiltration", "jailbreak", "code-execution"]
    out = classifier(prompt, labels, multi_label=False)
    # out: {labels: [...], scores: [...]}
    label = out["labels"][0]
    score = float(out["scores"][0])
    explanation = f"Zero-shot labels: {out['labels'][:3]} with scores {out['scores'][:3]}"
    # map HF labels to normalized ones
    if label == "benign":
        mapped = "benign"
    else:
        mapped = label
    return {"label": mapped, "score": score, "explanation": explanation}

def analyze_prompt(prompt: str):
    """
    Returns dict: {label, score, explanation}
    """
    prompt = (prompt or "").strip()
    if not prompt:
        return {"label":"empty", "score":0.0, "explanation":"No prompt provided"}
    if OPENAI_API_KEY:
        try:
            return _use_openai(prompt)
        except Exception as e:
            # fallback to HF if OpenAI call fails
            print("OpenAI error:", e)
            return _use_hf_zero_shot(prompt)
    else:
        return _use_hf_zero_shot(prompt)
