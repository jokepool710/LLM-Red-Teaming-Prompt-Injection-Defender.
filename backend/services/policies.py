import re
from typing import Tuple

def rule_no_system_prompt_exfiltration(prompt: str) -> Tuple[str,str]:
    if re.search(r"system prompt|hidden prompt|system instruction", prompt, re.I):
        return ("REVIEW", "possible-system-prompt-exfiltration")
    return ("NONE","")

def rule_shell_exec_block(prompt: str) -> Tuple[str,str]:
    if re.search(r"(rm\s+-rf|sudo|curl\s+http|wget\s+http|nc\s+)", prompt, re.I):
        return ("BLOCK", "shell-exec-risk")
    return ("NONE","")

RULES = [rule_no_system_prompt_exfiltration, rule_shell_exec_block]

def evaluate(prompt: str):
    for r in RULES:
        action, reason = r(prompt)
        if action == "BLOCK":
            return ("BLOCK", reason)
    for r in RULES:
        action, reason = r(prompt)
        if action == "REVIEW":
            return ("REVIEW", reason)
    return ("NONE", "")
