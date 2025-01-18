import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # Correctly initialize TestClient with the app object

def test_sse():
    with client.stream("GET", "/books/updates") as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"
        
        # Read a few events from the stream
        for line in response.iter_lines():
            assert line.startswith(b"data:")
            break
