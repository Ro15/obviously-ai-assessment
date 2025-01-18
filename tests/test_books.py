import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # Correctly initialize TestClient with the app object

def test_books_crud():
    # Get a token for authentication
    login_response = client.post("/login", data={"username": "admin", "password": "password123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a new book
    new_book = {
        "title": "Test Book",
        "author": "Author Name",
        "published_date": "2025-01-01",
        "summary": "A test summary",
        "genre": "Fiction"
    }
    create_response = client.post("/books/", json=new_book, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]

    # Retrieve the book by ID
    get_response = client.get(f"/books/{book_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test Book"

    # Update the book
    update_data = {"summary": "An updated summary"}
    update_response = client.put(f"/books/{book_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json()["summary"] == "An updated summary"

    # Delete the book
    delete_response = client.delete(f"/books/{book_id}", headers=headers)
    assert delete_response.status_code == 200
