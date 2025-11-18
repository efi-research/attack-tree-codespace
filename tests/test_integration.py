import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.tree_types import AttackTree, Node
import json


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_user():
    """Mock authenticated user data."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "sub": "123456789"
    }


@pytest.fixture
def mock_auth(mock_user):
    """Mock the authentication system to return a test user."""
    with patch("app.auth.get_current_user", return_value=mock_user):
        with patch("app.auth.require_auth", return_value=mock_user):
            yield


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

    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_generate_success(self, mock_llm, client, mock_llm_response, mock_auth):
        """Test successful attack tree generation."""
        mock_llm.return_value = mock_llm_response

        response = client.post(
            "/generate",
            json={
                "title": "Web Application Attack",
                "description": "Attacker wants to compromise a web application"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["goal"] == "Compromise Web Application"
        assert len(data["nodes"]) == 3
        assert data["nodes"][0]["id"] == "n1"
        assert data["nodes"][0]["probability"] == 0.7

    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_generate_with_markdown_wrapped_json(self, mock_llm, client, mock_llm_response_wrapped, mock_auth):
        """Test generation with LLM response wrapped in markdown."""
        mock_llm.return_value = mock_llm_response_wrapped

        response = client.post(
            "/generate",
            json={
                "title": "Phishing Campaign",
                "description": "Social engineering attack"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["goal"] == "Steal User Credentials"
        assert len(data["nodes"]) == 1

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

    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_generate_invalid_json_response(self, mock_llm, client, mock_auth):
        """Test handling of invalid JSON from LLM."""
        mock_llm.return_value = "This is not valid JSON at all"

        response = client.post(
            "/generate",
            json={
                "title": "Test",
                "description": "Test description"
            }
        )

        assert response.status_code == 500
        assert "Failed to parse LLM output" in response.json()["detail"]

    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_generate_invalid_schema(self, mock_llm, client, mock_auth):
        """Test handling of JSON that doesn't match AttackTree schema."""
        mock_llm.return_value = json.dumps({
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

        response = client.post(
            "/generate",
            json={
                "title": "Test",
                "description": "Test description"
            }
        )

        assert response.status_code == 400
        assert "Validation error" in response.json()["detail"]


class TestAuthentication:
    """Tests for authentication and authorization."""

    def test_generate_requires_authentication(self, client):
        """Test that /generate endpoint requires authentication."""
        response = client.post(
            "/generate",
            json={
                "title": "Test Attack",
                "description": "Test description"
            }
        )

        assert response.status_code == 401
        assert "Authentication required" in response.json()["detail"]

    def test_auth_user_endpoint(self, client):
        """Test that /auth/user returns not authenticated without session."""
        response = client.get("/auth/user")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is False
        assert data["user"] is None


class TestAppHealth:
    """Basic app health tests."""

    def test_health_check_app_startup(self, client):
        """Test that the app starts and responds."""
        # FastAPI has OpenAPI docs at /docs
        response = client.get("/docs")
        assert response.status_code == 200

    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_full_workflow_generate(self, mock_llm, client, mock_llm_response, mock_auth):
        """Test complete workflow: generate attack tree."""
        mock_llm.return_value = mock_llm_response

        # Generate attack tree
        gen_response = client.post(
            "/generate",
            json={
                "title": "Complete Attack Scenario",
                "description": "Multi-stage attack on infrastructure"
            }
        )

        assert gen_response.status_code == 200
        tree_data = gen_response.json()
        assert tree_data["goal"] == "Compromise Web Application"
        assert len(tree_data["nodes"]) == 3
