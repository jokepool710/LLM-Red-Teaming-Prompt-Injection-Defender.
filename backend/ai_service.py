def analyze_prompt(text: str) -> str:
    if any(word in text.lower() for word in ["attack", "exploit", "bypass"]):
        return "⚠️ Potentially malicious or prompt-injection detected"
    return "✅ Clean prompt"
