# Attack Tree Generator (Codespaces Starter)

Minimal prototype to generate attack trees from a scenario description using an LLM,
and render them as images using Graphviz.

## Quick start (Codespaces)
1. Create a new GitHub repo and paste these files.
2. Open in GitHub Codespaces (the devcontainer auto-installs dependencies).
3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` (or configure your LLM).
4. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
