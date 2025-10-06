from fastapi import FastAPI, HTTPException, Response, Query
from pydantic import BaseModel
from app.llm_client import generate_attack_tree_text
from app.prompt_utils import build_prompt, extract_first_json
from app.tree_types import AttackTree
import json
from app.renderer import render_graph
from typing import Optional

app = FastAPI(title="Attack Tree Generator")

class ScenarioIn(BaseModel):
    title: str
    description: str

@app.post("/generate")
async def generate(s: ScenarioIn):
    prompt = build_prompt(s.title, s.description)
    raw = await generate_attack_tree_text(prompt)
    # Try to parse JSON, with a fallback extraction
    try:
        tree_text = extract_first_json(raw)
        tree_json = json.loads(tree_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM output: {e}")

    # Validate structure with pydantic
    try:
        tree = AttackTree(**tree_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    return tree.dict()

@app.post("/render")
async def render(tree: AttackTree, format: Optional[str] = Query("png", regex="^(png|svg)$")):
    try:
        out = render_graph(tree, fmt=format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Render failed: {e}")

    media_type = "image/png" if format == "png" else "image/svg+xml"
    return Response(content=out, media_type=media_type)
