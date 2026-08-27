import pytest
from fastapi.testclient import TestClient
from api.src.main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data


def test_process_ticket_endpoint():
    payload = {
        "customer_email": "user@example.com",
        "customer_name": "Test User",
        "subject": "Locked out of my account",
        "body": "I cannot login after entering wrong password 5 times. Please help.",
        "customer_tier": "standard",
    }
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "ticket_id" in data
    assert data["status"] in ["AUTO_RESOLVED", "ESCALATED"]
    assert "prediction" in data
    assert data["prediction"]["predicted_category"] is not None
