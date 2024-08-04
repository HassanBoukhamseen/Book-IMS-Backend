import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    response = client.post("/users/login", json={"username": "email_0@gmail.com", "password": "password_0"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    body = response.json()
    assert body["user_info"]["fname"] == "fname_0"
    assert body["user_info"]["lname"] == "lname_0"
    assert body["user_info"]["role"] == 0
    headers = {"Authorization": f"Bearer {token}"}
    return headers

@pytest.fixture
def admin_auth_headers():
    response = client.post("/users/login", json={"username": "email_20@gmail.com", "password": "password_20"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    body = response.json()
    assert body["user_info"]["fname"] == "fname_20"
    assert body["user_info"]["lname"] == "lname_20"
    assert body["user_info"]["role"] == 1
    headers = {"Authorization": f"Bearer {token}"}
    return headers

def test_get_books(auth_headers):
    response = client.get("/books", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)  # Adjust based on your API response structure
    assert isinstance(response.json().get("books", []), list)

def test_get_book(auth_headers):
    response = client.get("/books/1", headers=auth_headers)
    assert response.status_code == 200 or response.status_code == 404  # Adjust based on your test data
    if response.status_code == 200:
        assert "book" in response.json()

def test_add_book(admin_auth_headers):
    new_book = {
        "title": "New book", 
        "author_id": "22",
        "genre": "genre_20",
        "description": "some_description",
        "year": 2020
    }
    response = client.post("/books", json=new_book, headers=admin_auth_headers)
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    response = client.get(f"/books/{book_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()["book"]["title"] == new_book["title"]

def test_update_book(admin_auth_headers):
    new_book = {
        "title": "New book", 
        "author_id": "22",
        "genre": "genre_20",
        "description": "some_description",
        "year": 2020
    }
    response = client.post("/books", json=new_book, headers=admin_auth_headers)
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    updated_book = {
        "title": "updated book", 
        "author_id": "22",
        "genre": "genre_20",
        "description": "some_description",
        "year": 2020
    }
    response = client.put(f"/books/{book_id}", json=updated_book, headers=admin_auth_headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/books/{book_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()["book"]["title"] == updated_book["title"]

def test_delete_book(admin_auth_headers):
    new_book = {
        "title": "New book", 
        "author_id": "22",
        "genre": "genre_20",
        "description": "some_description",
        "year": 2020
    }
    response = client.post("/books", json=new_book, headers=admin_auth_headers)
    book_id = response.json()["book_id"]
    assert response.status_code == 200

    response = client.delete(f"/books/{book_id}", headers=admin_auth_headers)
    assert response.status_code == 200

    response = client.get(f"/books/{book_id}", headers=admin_auth_headers)
    assert response.status_code == 404
