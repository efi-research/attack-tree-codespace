# SSE Streaming Implementation

This document describes the Server-Sent Events (SSE) streaming implementation for the Attack Tree Generator.

## Overview

The application now uses SSE streaming to provide real-time feedback during LLM-based attack tree generation. This eliminates timeout issues and provides users with immediate visual feedback as tokens are generated.

## Architecture

### Backend Components

#### 1. LLM Client (`app/llm_client.py`)

**New Streaming Functions:**
- `generate_attack_tree_stream_openai(prompt)` - Streams tokens from OpenAI API
- `generate_attack_tree_stream_ollama(prompt)` - Streams tokens from Ollama API
- `generate_attack_tree_stream(prompt)` - Routes to appropriate backend

All streaming functions are async generators that yield tokens as they arrive from the LLM.

#### 2. API Endpoint (`app/main.py`)

**Modified Endpoint:** `POST /generate`
- Returns `StreamingResponse` with `media_type="text/event-stream"`
- Streams events in SSE format: `data: {JSON}\n\n`
- Event types:
  - `start` - Generation has started
  - `token` - Individual token from LLM (contains `content` field)
  - `done` - Generation complete (contains `tree` field with full JSON)
  - `error` - Error occurred (contains `message` field)

### Frontend Components

#### 1. JavaScript Client (`static/app.js`)

**Modified Function:** `generateAttackTree(title, description)`
- Uses `fetch()` with `response.body.getReader()` for streaming
- Processes SSE events as they arrive
- Updates streaming preview in real-time
- Resolves promise when `done` event received

#### 2. UI Components (`static/index.html` + `static/styles.css`)

**New UI Elements:**
- Streaming preview box showing live LLM output
- Blinking cursor animation for active generation
- Auto-scroll to latest content
- Dark theme code display

## Event Flow

```
1. User submits form
   ↓
2. Frontend calls POST /generate
   ↓
3. Backend sends 'start' event
   ↓
4. Backend streams 'token' events as LLM generates
   ↓
5. Frontend displays tokens in streaming preview
   ↓
6. Backend accumulates tokens and parses JSON
   ↓
7. Backend sends 'done' event with complete tree
   ↓
8. Frontend renders D3 visualization
```

## Testing

### Integration Tests

Run the full test suite:
```bash
python -m pytest tests/ -v
```

All tests have been updated to work with SSE streaming responses.

### Manual Testing

1. Configure your LLM backend in `.env`:
   ```bash
   # For OpenAI
   LLM_BACKEND=openai
   LLM_MODEL=gpt-4o-mini
   OPENAI_API_KEY=your_key_here

   # OR for Ollama
   LLM_BACKEND=ollama
   LLM_MODEL=llama2
   OLLAMA_BASE_URL=http://localhost:11434/v1
   ```

2. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Open browser to http://localhost:8000

4. Enter a scenario and click "Generate Attack Tree"

5. Watch the streaming preview show tokens in real-time

## Benefits

✅ **No Timeouts** - SSE keeps connection alive indefinitely
✅ **Real-time Feedback** - Users see generation progress immediately
✅ **Better UX** - Reduces perceived wait time
✅ **Simple Protocol** - Native browser support, no extra libraries
✅ **Works with Both Backends** - OpenAI and Ollama both support streaming

## SSE Format Example

```
data: {"type": "start", "message": "Starting generation..."}\n\n
data: {"type": "token", "content": "{\n"}\n\n
data: {"type": "token", "content": "  \"goal\":"}\n\n
data: {"type": "token", "content": " \"Compromise"}\n\n
...
data: {"type": "done", "tree": {...complete tree JSON...}}\n\n
```

## Configuration

Both streaming backends are configured with:
- **Timeout:** 300 seconds (5 minutes) to handle slow models
- **Max Tokens:** 2000 to accommodate complex attack trees
- **Temperature:** 0.2 for more deterministic outputs

## Troubleshooting

**Issue:** "Failed to parse LLM output: No JSON object found" after 60 seconds
**Solution:** This was caused by the default 60-second timeout. Now fixed with 300-second timeout in both OpenAI and Ollama clients.

**Issue:** Streaming not working
**Solution:** Check that CORS is properly configured and proxy buffering is disabled

**Issue:** Tokens not displaying
**Solution:** Open browser console and check for JavaScript errors in SSE parsing

**Issue:** Empty streaming preview
**Solution:** Verify LLM is actually returning tokens (check backend logs)

**Issue:** Ollama models timing out
**Solution:** Ensure timeout is set to 300 seconds in the AsyncOpenAI client configuration

## Future Improvements

- Add progress percentage indicator
- Implement retry logic for connection failures
- Add streaming cancellation support
- Optimize token batching for better performance
