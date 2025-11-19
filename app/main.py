from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm_client import generate_attack_tree_stream
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


class ScenarioIn(BaseModel):
    """Input model for attack tree generation requests."""
    title: str
    description: str


def create_sse_event(event_type: str, **data) -> str:
    """
    Create a Server-Sent Event formatted string.

    Args:
        event_type: Type of event (start, token, done, error)
        **data: Additional data to include in the event

    Returns:
        Formatted SSE event string
    """
    event_data = {"type": event_type, **data}
    return f"data: {json.dumps(event_data)}\n\n"


@app.get("/")
async def root():
    """Serve the frontend."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Attack Tree Generator API", "docs": "/docs"}

@app.post("/generate")
async def generate(s: ScenarioIn):
    """
    Generate an attack tree using Server-Sent Events (SSE) streaming.

    This endpoint streams the LLM response in real-time, providing:
    - Start event when generation begins
    - Token events as each token is generated
    - Done event with the complete, validated attack tree
    - Error events if parsing or validation fails

    Args:
        s: ScenarioIn object containing title and description

    Returns:
        StreamingResponse with SSE events
    """
    async def event_generator():
        try:
            # Send start event
            yield create_sse_event("start", message="Starting generation...")

            # Build the prompt
            prompt = build_prompt(s.title, s.description)

            # Stream tokens from LLM
            accumulated_text = ""
            async for token in generate_attack_tree_stream(prompt):
                accumulated_text += token
                yield create_sse_event("token", content=token)

            # Parse the complete response
            try:
                tree_text = extract_first_json(accumulated_text)
                tree_json = json.loads(tree_text)
            except Exception as e:
                yield create_sse_event("error", message=f"Failed to parse LLM output: {str(e)}")
                return

            # Validate structure with pydantic
            try:
                tree = AttackTree(**tree_json)
            except Exception as e:
                yield create_sse_event("error", message=f"Validation error: {str(e)}")
                return

            # Send success with complete tree
            yield create_sse_event("done", tree=tree.model_dump())

        except Exception as e:
            # Send error event for any unexpected errors
            yield create_sse_event("error", message=str(e))

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable proxy buffering
        }
    )
