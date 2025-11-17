import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.tree_types import AttackTree, Node
import json
import shutil


# Check if Graphviz is available
def graphviz_available():
    """Check if Graphviz dot command is available."""
    return shutil.which("dot") is not None


# Skip marker for tests requiring Graphviz
requires_graphviz = pytest.mark.skipif(
    not graphviz_available(),
    reason="Graphviz not installed (required for rendering tests)"
)


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


@pytest.fixture
def valid_attack_tree():
    """Create a valid attack tree for testing."""
    return AttackTree(
        goal="Test Attack Goal",
        nodes=[
            Node(
                id="n1",
                text="Initial Access",
                type="or",
                children=["n2"],
                probability=0.8,
                cost=200.0
            ),
            Node(
                id="n2",
                text="Lateral Movement",
                type="and",
                children=[],
                probability=0.6,
                cost=150.0
            )
        ]
    )


class TestGenerateEndpoint:
    """Integration tests for /generate endpoint."""

    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_generate_success(self, mock_llm, client, mock_llm_response):
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
    def test_generate_with_markdown_wrapped_json(self, mock_llm, client, mock_llm_response_wrapped):
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
    def test_generate_invalid_json_response(self, mock_llm, client):
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
    def test_generate_invalid_schema(self, mock_llm, client):
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


class TestRenderEndpoint:
    """Integration tests for /render endpoint."""

    @requires_graphviz
    def test_render_png_success(self, client, valid_attack_tree):
        """Test successful PNG rendering."""
        response = client.post(
            "/render?format=png",
            json=valid_attack_tree.model_dump()
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 0

    @requires_graphviz
    def test_render_svg_success(self, client, valid_attack_tree):
        """Test successful SVG rendering."""
        response = client.post(
            "/render?format=svg",
            json=valid_attack_tree.model_dump()
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/svg+xml"
        assert len(response.content) > 0
        # SVG should contain XML
        assert b"<svg" in response.content or b"<?xml" in response.content

    @requires_graphviz
    def test_render_default_format(self, client, valid_attack_tree):
        """Test rendering with default format (png)."""
        response = client.post(
            "/render",
            json=valid_attack_tree.model_dump()
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_render_invalid_format(self, client, valid_attack_tree):
        """Test rendering with invalid format parameter."""
        response = client.post(
            "/render?format=pdf",
            json=valid_attack_tree.model_dump()
        )

        assert response.status_code == 422  # Validation error

    def test_render_invalid_tree_structure(self, client):
        """Test rendering with invalid tree structure."""
        response = client.post(
            "/render",
            json={
                "goal": "Test",
                "nodes": [
                    {
                        "id": "n1",
                        # Missing required 'text' field
                        "children": []
                    }
                ]
            }
        )

        assert response.status_code == 422

    @requires_graphviz
    def test_render_empty_nodes(self, client):
        """Test rendering tree with no nodes."""
        response = client.post(
            "/render",
            json={
                "goal": "Empty Tree",
                "nodes": []
            }
        )

        assert response.status_code == 200
        assert len(response.content) > 0

    @requires_graphviz
    def test_render_with_metrics(self, client):
        """Test rendering tree with probability and cost metrics."""
        tree_with_metrics = AttackTree(
            goal="Attack with Metrics",
            nodes=[
                Node(
                    id="n1",
                    text="Node with metrics",
                    probability=0.95,
                    cost=500.0,
                    children=[]
                )
            ]
        )

        response = client.post(
            "/render?format=svg",
            json=tree_with_metrics.model_dump()
        )

        assert response.status_code == 200
        # Check that metrics appear in SVG output
        content = response.content.decode('utf-8')
        assert "P=0.95" in content
        assert "C=500" in content


class TestEndToEndWorkflow:
    """End-to-end integration tests."""

    @requires_graphviz
    @patch("app.main.generate_attack_tree_text", new_callable=AsyncMock)
    def test_full_workflow_generate_and_render(self, mock_llm, client, mock_llm_response):
        """Test complete workflow: generate tree then render it."""
        mock_llm.return_value = mock_llm_response

        # Step 1: Generate attack tree
        gen_response = client.post(
            "/generate",
            json={
                "title": "Complete Attack Scenario",
                "description": "Multi-stage attack on infrastructure"
            }
        )

        assert gen_response.status_code == 200
        tree_data = gen_response.json()

        # Step 2: Render the generated tree as PNG
        render_response_png = client.post(
            "/render?format=png",
            json=tree_data
        )

        assert render_response_png.status_code == 200
        assert render_response_png.headers["content-type"] == "image/png"
        assert len(render_response_png.content) > 0

        # Step 3: Render the same tree as SVG
        render_response_svg = client.post(
            "/render?format=svg",
            json=tree_data
        )

        assert render_response_svg.status_code == 200
        assert render_response_svg.headers["content-type"] == "image/svg+xml"
        assert len(render_response_svg.content) > 0

    def test_health_check_app_startup(self, client):
        """Test that the app starts and responds."""
        # FastAPI has OpenAPI docs at /docs
        response = client.get("/docs")
        assert response.status_code == 200


class TestDataValidation:
    """Tests for data validation and edge cases."""

    @requires_graphviz
    def test_node_with_circular_reference(self, client):
        """Test handling of circular references in node children."""
        response = client.post(
            "/render",
            json={
                "goal": "Circular Test",
                "nodes": [
                    {
                        "id": "n1",
                        "text": "Node 1",
                        "children": ["n2"]
                    },
                    {
                        "id": "n2",
                        "text": "Node 2",
                        "children": ["n1"]  # Circular reference
                    }
                ]
            }
        )

        # Should still render (Graphviz will handle it)
        assert response.status_code == 200

    @requires_graphviz
    def test_node_referencing_nonexistent_child(self, client):
        """Test node referencing a child that doesn't exist."""
        response = client.post(
            "/render",
            json={
                "goal": "Missing Child Test",
                "nodes": [
                    {
                        "id": "n1",
                        "text": "Node 1",
                        "children": ["n999"]  # Non-existent child
                    }
                ]
            }
        )

        # Should still render (Graphviz will create the edge)
        assert response.status_code == 200

    @requires_graphviz
    def test_large_attack_tree(self, client):
        """Test rendering a large attack tree with many nodes."""
        large_tree = AttackTree(
            goal="Large Attack Tree",
            nodes=[
                Node(
                    id=f"n{i}",
                    text=f"Attack step {i}",
                    children=[f"n{i+1}"] if i < 49 else [],
                    probability=0.5,
                    cost=100.0 * i
                )
                for i in range(50)
            ]
        )

        response = client.post(
            "/render?format=svg",
            json=large_tree.model_dump()
        )

        assert response.status_code == 200
        assert len(response.content) > 0

    @requires_graphviz
    def test_special_characters_in_text(self, client):
        """Test nodes with special characters in text."""
        tree = AttackTree(
            goal='Test "quotes" & <tags>',
            nodes=[
                Node(
                    id="n1",
                    text="Node with 'quotes' and \"double quotes\"",
                    children=[]
                ),
                Node(
                    id="n2",
                    text="Node with <html> & special chars: @#$%",
                    children=[]
                )
            ]
        )

        response = client.post(
            "/render?format=svg",
            json=tree.model_dump()
        )

        assert response.status_code == 200
