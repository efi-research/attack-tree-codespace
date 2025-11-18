from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from app.llm_client import generate_attack_tree_text
from app.prompt_utils import build_prompt, extract_first_json
from app.tree_types import AttackTree
from app.auth import oauth, get_current_user, require_auth, SECRET_KEY
import json
import os

app = FastAPI(title="Attack Tree Generator")

# Add session middleware (must be added before routes)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

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


# Authentication endpoints
@app.get("/auth/login")
async def login(request: Request):
    """Redirect to Google OAuth login."""
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Handle Google OAuth callback."""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if user_info:
            request.session['user'] = dict(user_info)
        return RedirectResponse(url='/')
    except Exception as e:
        return RedirectResponse(url=f'/?error=auth_failed')


@app.get("/auth/logout")
async def logout(request: Request):
    """Logout the current user."""
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.get("/auth/user")
async def get_user(request: Request):
    """Get current user info."""
    user = get_current_user(request)
    if user:
        return {"authenticated": True, "user": user}
    return {"authenticated": False, "user": None}


class ScenarioIn(BaseModel):
    title: str
    description: str

@app.post("/generate")
async def generate(request: Request, s: ScenarioIn):
    # Require authentication
    user = require_auth(request)

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
