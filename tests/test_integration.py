import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.tree_types import AttackTree, Node
import json


async def mock_stream_generator(text):
    """Helper to create async generator for mocking streaming."""
    for char in text:
        yield char


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_llm_response():
    """Mock LLM response with valid attack tree JSON."""
    return json.dumps({
        "goal": "Compromise Web Application",
        "nodes": [
            {
                "id": "n1",
                "text": "Exploit SQL Injection",
                "type": "or",
                "children": ["n2", "n3"],
                "probability": 0.7,
                "cost": 100.0
            },
            {
                "id": "n2",
                "text": "Exploit login form",
                "type": "and",
                "children": [],
                "probability": 0.5,
                "cost": 50.0
            },
            {
                "id": "n3",
                "text": "Exploit search endpoint",
                "type": "and",
                "children": [],
                "probability": 0.3,
                "cost": 75.0
            }
        ]
    })


@pytest.fixture
def mock_llm_response_wrapped():
    """Mock LLM response wrapped in markdown code block."""
    return """Here is the attack tree:
```json
{
    "goal": "Steal User Credentials",
    "nodes": [
        {
            "id": "n1",
            "text": "Phishing Attack",
            "type": "or",
            "children": []
        }
    ]
}
```
This shows the attack path."""


class TestGenerateEndpoint:
    """Integration tests for /generate endpoint."""

    @patch("app.main.generate_attack_tree_stream")
    def test_generate_success(self, mock_llm_stream, client, mock_llm_response):
        """Test successful attack tree generation with streaming."""
        mock_llm_stream.return_value = mock_stream_generator(mock_llm_response)

        response = client.post(
            "/generate",
            json={
                "title": "Web Application Attack",
                "description": "Attacker wants to compromise a web application"
            }
        )

        assert response.status_code == 200

        # Parse the SSE stream to get the final result
        content = response.text
        lines = content.split('\n')

        # Find the 'done' event with the tree data
        tree_data = None
        for line in lines:
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data.get('type') == 'done':
                    tree_data = data['tree']
                    break

        assert tree_data is not None
        assert tree_data["goal"] == "Compromise Web Application"
        assert len(tree_data["nodes"]) == 3
        assert tree_data["nodes"][0]["id"] == "n1"
        assert tree_data["nodes"][0]["probability"] == 0.7

    @patch("app.main.generate_attack_tree_stream")
    def test_generate_with_markdown_wrapped_json(self, mock_llm_stream, client, mock_llm_response_wrapped):
        """Test generation with LLM response wrapped in markdown."""
        mock_llm_stream.return_value = mock_stream_generator(mock_llm_response_wrapped)

        response = client.post(
            "/generate",
            json={
                "title": "Phishing Campaign",
                "description": "Social engineering attack"
            }
        )

        assert response.status_code == 200

        # Parse the SSE stream to get the final result
        content = response.text
        lines = content.split('\n')

        tree_data = None
        for line in lines:
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data.get('type') == 'done':
                    tree_data = data['tree']
                    break

        assert tree_data is not None
        assert tree_data["goal"] == "Steal User Credentials"
        assert len(tree_data["nodes"]) == 1

    def test_generate_missing_title(self, client):
        """Test generation with missing title field."""
        response = client.post(
            "/generate",
            json={"description": "Some description"}
        )

        assert response.status_code == 422  # Validation error

    def test_generate_missing_description(self, client):
        """Test generation with missing description field."""
        response = client.post(
            "/generate",
            json={"title": "Some title"}
        )

        assert response.status_code == 422  # Validation error

    def test_generate_empty_payload(self, client):
        """Test generation with empty payload."""
        response = client.post("/generate", json={})

        assert response.status_code == 422

    @patch("app.main.generate_attack_tree_stream")
    def test_generate_invalid_json_response(self, mock_llm_stream, client):
        """Test handling of invalid JSON from LLM."""
        mock_llm_stream.return_value = mock_stream_generator("This is not valid JSON at all")

        response = client.post(
            "/generate",
            json={
                "title": "Test",
                "description": "Test description"
            }
        )

        assert response.status_code == 200

        # Parse the SSE stream to check for error event
        content = response.text
        lines = content.split('\n')

        error_found = False
        for line in lines:
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data.get('type') == 'error':
                    error_found = True
                    assert "Failed to parse LLM output" in data['message']
                    break

        assert error_found

    @patch("app.main.generate_attack_tree_stream")
    def test_generate_invalid_schema(self, mock_llm_stream, client):
        """Test handling of JSON that doesn't match AttackTree schema."""
        invalid_json = json.dumps({
            "goal": "Test",
            "nodes": [
                {
                    "id": "n1",
                    # Missing required 'text' field
                    "type": "or",
                    "children": []
                }
            ]
        })
        mock_llm_stream.return_value = mock_stream_generator(invalid_json)

        response = client.post(
            "/generate",
            json={
                "title": "Test",
                "description": "Test description"
            }
        )

        assert response.status_code == 200

        # Parse the SSE stream to check for error event
        content = response.text
        lines = content.split('\n')

        error_found = False
        for line in lines:
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data.get('type') == 'error':
                    error_found = True
                    assert "Validation error" in data['message']
                    break

        assert error_found


class TestAppHealth:
    """Basic app health tests."""

    def test_health_check_app_startup(self, client):
        """Test that the app starts and responds."""
        # FastAPI has OpenAPI docs at /docs
        response = client.get("/docs")
        assert response.status_code == 200

    @patch("app.main.generate_attack_tree_stream")
    def test_full_workflow_generate(self, mock_llm_stream, client, mock_llm_response):
        """Test complete workflow: generate attack tree with streaming."""
        mock_llm_stream.return_value = mock_stream_generator(mock_llm_response)

        # Generate attack tree
        gen_response = client.post(
            "/generate",
            json={
                "title": "Complete Attack Scenario",
                "description": "Multi-stage attack on infrastructure"
            }
        )

        assert gen_response.status_code == 200

        # Parse the SSE stream to get the final result
        content = gen_response.text
        lines = content.split('\n')

        tree_data = None
        for line in lines:
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data.get('type') == 'done':
                    tree_data = data['tree']
                    break

        assert tree_data is not None
        assert tree_data["goal"] == "Compromise Web Application"
        assert len(tree_data["nodes"]) == 3
