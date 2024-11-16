"""
Unit test to check if application is up
"""

from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_health_check_success():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

