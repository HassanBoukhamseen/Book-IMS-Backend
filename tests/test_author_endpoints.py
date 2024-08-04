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

def test_get_authors(auth_headers):
    response = client.get("/authors", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_author(auth_headers):
    response = client.get("/authors/1", headers=auth_headers)
    assert response.status_code == 200
    assert "author" in response.json()

def test_add_author(admin_auth_headers):
    new_author = {"name": "New Author", "biography": "Bio of new author"}
    response = client.post("/authors", json=new_author, headers=admin_auth_headers)
    assert response.status_code == 200
    print(response.json())
    author_id = response.json()["author_id"]

    response = client.get(f"/authors/{author_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()["author"]["name"] == new_author["name"]

def test_update_author(admin_auth_headers):
    new_author = {"name": "New Author", "biography": "Bio of new author"}
    response = client.post("/authors", json=new_author, headers=admin_auth_headers)
    assert response.status_code == 200
    author_id = response.json()["author_id"]

    updated_author = {"name": "Updated Author", "biography": "Updated bio"}
    response = client.put(f"/authors/{author_id}", json=updated_author, headers=admin_auth_headers)
    assert response.status_code == 200

    response = client.get(f"/authors/{author_id}", headers=admin_auth_headers)
    assert response.status_code == 200
    assert response.json()["author"]["name"] == updated_author["name"]

def test_delete_author(admin_auth_headers):
    new_author = {"name": "New Author", "biography": "Bio of new author"}
    response = client.post("/authors", json=new_author, headers=admin_auth_headers)
    author_id = response.json()["author_id"]
    assert response.status_code == 200

    response = client.delete(f"/authors/{author_id}", headers=admin_auth_headers)
    assert response.status_code == 200

    response = client.get(f"/authors/{author_id}", headers=admin_auth_headers)
    assert response.status_code == 400


