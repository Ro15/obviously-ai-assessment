import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # Correctly initialize TestClient with the app object

def test_rbac():
    # Get tokens for admin and user
    admin_login = client.post("/login", data={"username": "admin", "password": "password123"})
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    user_login = client.post("/login", data={"username": "user", "password": "userpassword"})
    user_token = user_login.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # Admin can delete a book
    book_data = {"title": "RBAC Test", "author": "Author", "published_date": "2025-01-01"}
    book_create = client.post("/books/", json=book_data, headers=admin_headers)
    book_id = book_create.json()["id"]

    delete_response = client.delete(f"/books/{book_id}", headers=admin_headers)
    assert delete_response.status_code == 200

    # User cannot delete a book
    book_create = client.post("/books/", json=book_data, headers=admin_headers)
    book_id = book_create.json()["id"]

    delete_response = client.delete(f"/books/{book_id}", headers=user_headers)
    assert delete_response.status_code == 403
    assert delete_response.json() == {"detail": "You do not have permission to access this resource"}
