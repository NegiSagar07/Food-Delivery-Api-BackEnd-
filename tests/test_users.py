from fastapi.testclient import TestClient
from http import HTTPStatus
from tests.utils import get_auth_headers

def test_get_my_profile(client: TestClient):
    headers = get_auth_headers(client)
    
    response = client.get("/users/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    
    data = response.json()
    assert "email" in data
    assert "name" in data
    assert "id" in data

def test_get_my_profile_unauthorized(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
