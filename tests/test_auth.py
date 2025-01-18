import pytest
from app.main import app
from starlette.testclient import TestClient

client = TestClient(app)  # Correctly initialize TestClient with the app object

def test_login():
    # Test valid login
    response = client.post("/login", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Test invalid login
    response = client.post("/login", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}
