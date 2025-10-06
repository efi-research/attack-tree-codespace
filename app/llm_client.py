import os
import asyncio
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# This adapter uses OpenAI python client as an example. Replace as needed.
# Keep this module simple so you can swap providers (Anthropic, Cohere, local LLM, etc.)

async def generate_attack_tree_text(prompt: str, timeout: Optional[int] = 30) -> str:
    """
    Call LLM and return raw text. Minimal retries included.
    """
    import openai

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    openai.api_key = OPENAI_API_KEY

    # Use ChatCompletion API as an example. Adjust to your provider & credentials.
    for attempt in range(2):
        try:
            resp = openai.ChatCompletion.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.2
            )
            # Basic compatibility: some clients return different shapes
            content = resp.choices[0].message.content if hasattr(resp.choices[0], 'message') else resp.choices[0].text
            return content
        except Exception as e:
            if attempt == 1:
                raise
            await asyncio.sleep(0.8)
