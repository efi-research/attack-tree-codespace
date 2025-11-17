# Attack Tree Generator

Generate visual attack trees from security scenarios using AI. This application uses LLMs to automatically create structured attack trees and renders them as interactive visualizations using Graphviz.

## Features

- 🤖 **AI-Powered Generation**: Uses OpenAI GPT models to generate attack trees from natural language descriptions
- 🎨 **Visual Rendering**: Renders attack trees as PNG or SVG images using Graphviz
- 🌐 **Web Interface**: User-friendly browser-based UI for easy interaction
- 📊 **JSON Export**: Download attack tree data in JSON format for further analysis
- 🔄 **Real-time Preview**: See your attack tree visualization immediately after generation
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Option 1: GitHub Codespaces (Recommended)
1. Open this repository in GitHub Codespaces
2. The devcontainer will auto-install all dependencies (Python, Graphviz, etc.)
3. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`
4. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```
5. Open your browser to `http://localhost:8080`

### Option 2: Local Installation
1. Install Python 3.11+ and Graphviz:
   ```bash
   # macOS
   brew install python graphviz

   # Ubuntu/Debian
   sudo apt-get install python3 python3-pip graphviz
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
   - See the visual representation of the attack tree
   - Switch between SVG and PNG formats
   - Expand JSON data to see the raw structure

4. **Download**:
   - Download the image (PNG/SVG)
   - Download the JSON data for further analysis

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

### Render Attack Tree
- `POST /render?format=svg|png`
- **Body**: Attack tree JSON
- **Returns**: Image (SVG or PNG)

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

Render attack tree:
```bash
curl -X POST "http://localhost:8080/render?format=svg" \
  -H "Content-Type: application/json" \
  -d @attack_tree.json \
  -o attack_tree.svg
```

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app and endpoints
│   ├── tree_types.py        # Pydantic models
│   ├── llm_client.py        # OpenAI integration
│   ├── prompt_utils.py      # Prompt engineering
│   └── renderer.py          # Graphviz rendering
├── static/
│   ├── index.html           # Web interface
│   ├── styles.css           # Styling
│   └── app.js               # Frontend logic
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

**Note**: Rendering tests require Graphviz to be installed. They will be skipped if Graphviz is not available.

## Development

The application supports hot-reload during development. Any changes to Python files will automatically restart the server.

For frontend development, simply edit files in `static/` and refresh your browser.

## Troubleshooting

### "Graphviz not found" error
- **Solution**: Install Graphviz system package
  ```bash
  # macOS
  brew install graphviz

  # Ubuntu/Debian
  sudo apt-get install graphviz
  ```

### "OpenAI API key not configured" error
- **Solution**: Make sure you've created a `.env` file with your `OPENAI_API_KEY`

### Port 8080 already in use
- **Solution**: Change the port number:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```

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
