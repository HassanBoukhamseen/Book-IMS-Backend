import pytest
from fastapi.testclient import TestClient
import jwt
from api import app  
from app.config import SECRET_KEY, ALGORITHM

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

def test_get_current_user(admin_auth_headers):
    response = client.get("/users/me", headers=admin_auth_headers)
    assert response.status_code == 200
    assert "user" in response.json()
    assert "email" in response.json()["user"]
    assert "fname" in response.json()["user"] 
    assert "lname" in response.json()["user"] 
    assert "role" in response.json()["user"]
    assert response.json()["user"]["email"] == "email_20@gmail.com"
    assert response.json()["user"]["fname"] == "fname_20"
    assert response.json()["user"]["lname"] == "lname_20"
    assert response.json()["user"]["role"] == 1

def test_update_current_user(admin_auth_headers):
    new_user = {
        "fname": "Hassan",
        "lname": "Boukhamseen"
    }
    response = client.put("/users/me", json=new_user, headers=admin_auth_headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "token" in response.json()
    token = response.json()["token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_info = payload.get("sub")
    assert user_info["fname"] == new_user["fname"]
    assert user_info["lname"] == new_user["lname"]
    new_user = {
        "fname": "fname_20",
        "lname": "lname_20"
    }
    response = client.put("/users/me", json=new_user, headers=admin_auth_headers)

def test_health_check():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() is True