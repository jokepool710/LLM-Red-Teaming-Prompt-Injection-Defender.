import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_MODE = os.getenv("MODEL_MODE", "mock")  

def _rule_based(prompt: str):

    p = prompt.lower()
    if any(k in p for k in ["ignore previous", "ignore instructions", "reveal system prompt", "exfiltrate"]):
        return {"label":"prompt-injection","score":0.95,"explanation":"Matched prompt-injection keywords"}
    if any(k in p for k in ["rm -rf","sudo","curl http","wget http"]):
        return {"label":"code-execution","score":0.98,"explanation":"Detected shell execution pattern"}
    return {"label":"benign","score":0.01,"explanation":"No rule triggered"}

def _use_openai(prompt: str):
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
      
        mod = openai.Moderation.create(input=prompt)
        mod_res = mod["results"][0]
        flagged = mod_res.get("flagged", False)
        if flagged:
            return {"label":"malicious","score":1.0,"explanation":str(mod_res.get("categories", {}))}
   
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Classify prompt as benign or malicious; return JSON: {label,score,explanation}"},
                {"role":"user","content": prompt}
            ],
            temperature=0
        )
        text = resp["choices"][0]["message"]["content"]
        import json
        try:
            return json.loads(text)
        except Exception:
            return {"label":"unknown","score":0.0,"explanation":text}
    except Exception as e:
        print("OpenAI error:", e)
        return _rule_based(prompt)

def _use_hf_zero_shot(prompt: str):
    try:
        from transformers import pipeline
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        labels = ["benign", "prompt-injection", "data-exfiltration", "jailbreak", "code-execution"]
        out = classifier(prompt, labels, multi_label=False)
        label = out["labels"][0]
        score = float(out["scores"][0])
        explanation = f"Zero-shot labels: {out['labels'][:3]} with scores {out['scores'][:3]}"
        return {"label": label, "score": score, "explanation": explanation}
    except Exception as e:
        print("HF error:", e)
        return _rule_based(prompt)

def analyze_prompt(prompt: str):
    prompt = (prompt or "").strip()
    if not prompt:
        return {"label":"empty","score":0.0,"explanation":"No prompt provided"}
    mode = MODEL_MODE.lower()
    if mode == "openai" and OPENAI_API_KEY:
        return _use_openai(prompt)
    if mode == "hf":
        return _use_hf_zero_shot(prompt)

    r = _rule_based(prompt)
    if r.get("score",0) > 0.5:
        return r
    try:
        return _use_hf_zero_shot(prompt)
    except Exception:
        return r
