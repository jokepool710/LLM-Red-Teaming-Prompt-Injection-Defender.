
import re
_email_re = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_api_key_re = re.compile(r"(?i)(api[_-]?key|secret)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9\-_]{16,100})")

def redact_output(text: str) -> str:
    text = _email_re.sub("[REDACTED_EMAIL]", text)
    text = _api_key_re.sub(r"\1: [REDACTED_KEY]", text)
    text = re.sub(r"([A-Za-z0-9]{20,})", "[REDACTED_TOKEN]", text)
    return text
