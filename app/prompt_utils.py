from typing import Tuple
import re
import json

PROMPT_SCHEMA = """
You are given a scenario. Output ONLY valid JSON matching the schema:

{{"goal":string, "nodes":[{{"id":string, "text":string, "type":"or"|"and", "children":[ids]}}]}}

Example:
{{"goal":"steal funds","nodes":[{{"id":"n0","text":"compromise payment server","type":"or","children":["n1","n2"]}},{{"id":"n1","text":"exploit CVE-xxxx","children":[]}}]}}

Scenario:
Title: {title}
Description: {description}

Return JSON only.
"""

def build_prompt(title: str, description: str) -> str:
    return PROMPT_SCHEMA.format(title=title.replace('"', '\\"'), description=description.replace('"','\\"'))

def extract_first_json(text: str) -> str:
    """
    Try to extract the first JSON object from LLM output.
    This is a pragmatic fallback for noisy responses.
    """
    # Attempt a direct parse
    text = text.strip()
    try:
        json.loads(text)
        return text
    except Exception:
        pass

    # Find first balanced JSON object using regex recursion (PCRE not available in python),
    # use a pragmatic approach: find first "{" and the matching "}" by counting.
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start:i+1]
                # sanitize common wrapping markdown
                candidate = re.sub(r"^```(?:json)?\n", "", candidate)
                candidate = re.sub(r"\n```$", "", candidate)
                return candidate
    raise ValueError("Could not extract balanced JSON")
