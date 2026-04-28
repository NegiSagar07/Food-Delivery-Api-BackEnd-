from fastapi.testclient import TestClient
from http import HTTPStatus
import uuid
from tests.utils import get_auth_headers

def test_create_restaurant(client: TestClient):
    headers = get_auth_headers(client)
    restaurant_name = f"Test Rest {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/restaurant/",
        json={"name": restaurant_name, "rating": 4.5},
        headers=headers
    )
    
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["name"] == restaurant_name
    assert "owner" in data
    assert "id" in data

def test_create_restaurant_duplicate(client: TestClient):
    headers = get_auth_headers(client)
    restaurant_name = f"Test Rest Dupe {uuid.uuid4().hex[:8]}"

    client.post("/restaurant/", json={"name": restaurant_name, "rating": 4.5}, headers=headers)
    response = client.post("/restaurant/", json={"name": restaurant_name, "rating": 4.5}, headers=headers)
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Restaurant name already exist"

def test_get_all_restaurants(client: TestClient):
    headers = get_auth_headers(client)
    # Ensure at least one exists
    client.post("/restaurant/", json={"name": f"Rest {uuid.uuid4().hex[:8]}"}, headers=headers)
    
    response = client.get("/restaurant/")
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) >= 1
    assert "id" in data[0]

def test_add_menu_item_to_restaurant(client: TestClient):
    headers = get_auth_headers(client)
    
    # 1. Create a food
    food_name = f"Food Menu Add {uuid.uuid4().hex[:8]}"
    food_response = client.post("/foods/", json={"name": food_name}, headers=headers)
    food_id = food_response.json()["id"]
    
    # 2. Create a restaurant
    restaurant_name = f"Rest Menu Add {uuid.uuid4().hex[:8]}"
    rest_response = client.post("/restaurant/", json={"name": restaurant_name}, headers=headers)
    rest_id = rest_response.json()["id"]

    # 3. Add food to menu
    response = client.post(
        f"/restaurant/{rest_id}/menu",
        json={"food_id": food_id, "price": 10.99},
        headers=headers
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["food_id"] == food_id
    assert data["price"] == 10.99
    
    # Check duplicate
    dup_response = client.post(
        f"/restaurant/{rest_id}/menu",
        json={"food_id": food_id, "price": 10.99},
        headers=headers
    )
    assert dup_response.status_code == HTTPStatus.BAD_REQUEST

def test_get_menu_of_restaurant(client: TestClient):
    headers = get_auth_headers(client)
    
    food_response = client.post("/foods/", json={"name": f"Food Get Menu {uuid.uuid4().hex[:8]}"}, headers=headers)
    food_id = food_response.json()["id"]
    
    rest_response = client.post("/restaurant/", json={"name": f"Rest Get Menu {uuid.uuid4().hex[:8]}"}, headers=headers)
    rest_id = rest_response.json()["id"]

    client.post(f"/restaurant/{rest_id}/menu", json={"food_id": food_id, "price": 5.0}, headers=headers)
    
    response = client.get(f"/restaurant/{rest_id}/menu")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["food_id"] == food_id
    assert data[0]["price"] == 5.0
