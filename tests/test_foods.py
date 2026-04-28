from fastapi.testclient import TestClient
from http import HTTPStatus
import uuid
from tests.utils import get_auth_headers

def test_create_food_success(client: TestClient):
    headers = get_auth_headers(client)
    food_name = f"Test Food {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/foods/",
        json={"name": food_name, "description": "A very tasty test food"},
        headers=headers
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["name"] == food_name
    assert "id" in data

def test_create_food_duplicate(client: TestClient):
    headers = get_auth_headers(client)
    food_name = f"Test Food Dupe {uuid.uuid4().hex[:8]}"

    # Create once
    client.post("/foods/", json={"name": food_name}, headers=headers)
    
    # Create again
    response = client.post("/foods/", json={"name": food_name}, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "A Food item with this name already exist"

def test_create_food_unauthorized(client: TestClient):
    response = client.post("/foods/", json={"name": "Illegal Food"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
