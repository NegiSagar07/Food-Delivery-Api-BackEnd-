from fastapi.testclient import TestClient
from http import HTTPStatus
import uuid
from tests.utils import get_auth_headers

def setup_restaurant_and_food(client: TestClient, headers: dict):
    # Create Food
    food_name = f"Order Food {uuid.uuid4().hex[:8]}"
    food_resp = client.post("/foods/", json={"name": food_name}, headers=headers)
    food_id = food_resp.json()["id"]

    # Create Restaurant
    rest_name = f"Order Rest {uuid.uuid4().hex[:8]}"
    rest_resp = client.post("/restaurant/", json={"name": rest_name}, headers=headers)
    rest_id = rest_resp.json()["id"]

    # Add Food to Menu
    client.post(
        f"/restaurant/{rest_id}/menu",
        json={"food_id": food_id, "price": 20.0},
        headers=headers
    )
    
    return rest_id, food_id

def test_create_order(client: TestClient):
    headers = get_auth_headers(client)
    rest_id, food_id = setup_restaurant_and_food(client, headers)
    
    # Place Order
    response = client.post(
        "/order/",
        json={
            "restaurant_id": rest_id,
            "items": [
                {"food_id": food_id, "quantity": 2}
            ]
        },
        headers=headers
    )
    
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["restaurant"]["id"] == rest_id
    assert data["total_price"] == 40.0
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2

def test_get_my_orders(client: TestClient):
    headers = get_auth_headers(client)
    rest_id, food_id = setup_restaurant_and_food(client, headers)
    
    client.post(
        "/order/",
        json={"restaurant_id": rest_id, "items": [{"food_id": food_id, "quantity": 1}]},
        headers=headers
    )
    
    response = client.get("/order/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    
    assert len(data) >= 1
    assert data[0]["total_price"] == 20.0

def test_get_specific_order(client: TestClient):
    headers = get_auth_headers(client)
    rest_id, food_id = setup_restaurant_and_food(client, headers)
    
    order_resp = client.post(
        "/order/",
        json={"restaurant_id": rest_id, "items": [{"food_id": food_id, "quantity": 3}]},
        headers=headers
    )
    order_id = order_resp.json()["id"]
    
    response = client.get(f"/order/{order_id}", headers=headers)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    
    assert data["id"] == order_id
    assert data["total_price"] == 60.0
    assert data["restaurant"]["id"] == rest_id
