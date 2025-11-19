import os
import asyncio
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Backend & model selection
LLM_BACKEND = os.getenv("LLM_BACKEND", "openai")  # "openai" or "ollama"
LLM_MODEL = os.getenv("LLM_MODEL")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

# This adapter supports multiple LLM backends (OpenAI, Ollama, etc.)
# Keep this module simple so you can swap providers easily.

async def generate_attack_tree_text_openai(prompt: str, timeout: Optional[int] = 30) -> str:
    """
    Call OpenAI LLM and return raw text. Minimal retries included.
    """
    from openai import AsyncOpenAI

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    # Use ChatCompletion API (OpenAI v1.0+ format)
    for attempt in range(2):
        try:
            resp = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.2
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 1:
                raise
            await asyncio.sleep(0.8)


async def generate_attack_tree_text_ollama(prompt: str, timeout: Optional[int] = 30) -> str:
    """
    Call Ollama LLM and return raw text. Minimal retries included.
    """
    from openai import AsyncOpenAI

    # Ollama uses OpenAI-compatible API
    client = AsyncOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama"  # Ollama doesn't require a real API key
    )

    # Use ChatCompletion API (OpenAI-compatible format)
    for attempt in range(2):
        try:
            resp = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.2
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 1:
                raise
            await asyncio.sleep(0.8)


async def generate_attack_tree_text(prompt: str, timeout: Optional[int] = 30) -> str:
    """
    Call LLM and return raw text. Routes to the appropriate backend.
    """
    backend = LLM_BACKEND.lower()

    if backend == "ollama":
        return await generate_attack_tree_text_ollama(prompt, timeout)
    elif backend == "openai":
        return await generate_attack_tree_text_openai(prompt, timeout)
    else:
        raise RuntimeError(f"Unsupported LLM_BACKEND: {backend}. Use 'openai' or 'ollama'")
