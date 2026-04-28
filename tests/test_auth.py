from fastapi.testclient import TestClient
from http import HTTPStatus


def test_register_user_success_and_fail(client: TestClient):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert response_data["email"] == user_data["email"]
    assert response_data["name"] == user_data["name"]
    assert "id" in response_data

    # --- 2. Test the "Sad Path" (Duplicate User) ---
    
    # Try to register the *exact same user* again
    response_duplicate = client.post(
        "/auth/register",
        json=user_data
    )

    assert response_duplicate.status_code == HTTPStatus.BAD_REQUEST

    assert response_duplicate.json()["detail"] == "email already exist"