from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm_client import generate_attack_tree_text
from app.prompt_utils import build_prompt, extract_first_json
from app.tree_types import AttackTree
import json
import os

app = FastAPI(title="Attack Tree Generator")

# Add CORS middleware for API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Serve the frontend."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Attack Tree Generator API", "docs": "/docs"}

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

    return tree.model_dump()
