# Attack Tree Generator

Generate visual attack trees from security scenarios using AI. This application uses LLMs to automatically create structured attack trees and renders them as interactive visualizations using D3.js.

## Features

- 🤖 **AI-Powered Generation**: Uses OpenAI GPT models to generate attack trees from natural language descriptions
- 🎨 **Frontend Rendering**: Renders attack trees as SVG visualizations using D3.js directly in the browser
- 💾 **Multiple Export Formats**: Download as PNG or SVG
- 🌐 **Web Interface**: User-friendly browser-based UI for easy interaction
- 📊 **JSON Export**: Download attack tree data in JSON format for further analysis
- ⚡ **Instant Visualization**: See your attack tree immediately after generation with no server round-trip
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Option 1: GitHub Codespaces (Recommended)
1. Open this repository in GitHub Codespaces
2. The devcontainer will auto-install all dependencies
3. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`
4. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```
5. Open your browser to `http://localhost:8080`

### Option 2: Local Installation
1. Install Python 3.11+:
   ```bash
   # macOS
   brew install python

   # Ubuntu/Debian
   sudo apt-get install python3 python3-pip
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

5. Open `http://localhost:8080` in your browser

## Using the Web Interface

1. **Enter Scenario Details**:
   - Provide a title for your attack scenario
   - Describe the scenario in detail (e.g., "An attacker wants to compromise a web application...")

2. **Generate Attack Tree**:
   - Click "Generate Attack Tree"
   - Wait for AI to analyze and create the tree structure

3. **View Results**:
   - See the interactive visual representation of the attack tree (rendered with D3.js)
   - Toggle between SVG and PNG format buttons
   - Expand JSON data to see the raw structure

4. **Download**:
   - Click "Download Image" to save as PNG or SVG (based on selected format)
   - Click "Download JSON" to save the attack tree data for further analysis

**Pro Tip**: Press `Ctrl+Shift+S` to auto-fill sample data for testing!

## API Endpoints

### Web Interface
- `GET /` - Serves the web interface

### API Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)

### Generate Attack Tree
- `POST /generate`
- **Body**: `{"title": "string", "description": "string"}`
- **Returns**: JSON attack tree structure

**Note**: Tree rendering is now performed entirely in the frontend using D3.js. The attack tree JSON returned by `/generate` is visualized directly in the browser.

## Example CURL Commands

Generate an attack tree:
```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ransomware Attack",
    "description": "Encrypt corporate files and demand payment for decryption key"
  }'
```

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app and endpoints
│   ├── tree_types.py        # Pydantic models
│   ├── llm_client.py        # OpenAI integration
│   └── prompt_utils.py      # Prompt engineering
├── static/
│   ├── index.html           # Web interface
│   ├── styles.css           # Styling
│   └── app.js               # Frontend logic with D3.js rendering
├── tests/
│   ├── test_parser.py       # Unit tests
│   └── test_integration.py  # Integration tests
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

Edit `.env` to configure:

```bash
# Required
OPENAI_API_KEY=your-api-key-here

# Optional
OPENAI_ORG_ID=your-org-id
LLM_MODEL=gpt-4o-mini  # or gpt-4, gpt-3.5-turbo
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run only integration tests:
```bash
pytest tests/test_integration.py -v
```

## Development

The application supports hot-reload during development. Any changes to Python files will automatically restart the server.

For frontend development, simply edit files in `static/` and refresh your browser.

## Troubleshooting

### "OpenAI API key not configured" error
- **Solution**: Make sure you've created a `.env` file with your `OPENAI_API_KEY`

### Port 8080 already in use
- **Solution**: Change the port number:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```

### Visualization not appearing
- **Solution**: Make sure JavaScript is enabled in your browser. The visualization is rendered client-side using D3.js.

## License

GNU General Public License v3.0

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Future Enhancements

- [ ] Support for multiple LLM providers (Anthropic, local models)
- [ ] Export to additional formats (PDF, DOT)
- [ ] Interactive tree editing
- [ ] Attack path probability calculations
- [ ] Defense strategy recommendations
- [ ] Multi-language support
