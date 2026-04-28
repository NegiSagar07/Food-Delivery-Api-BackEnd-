import uuid
from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient) -> dict:
    """Helper to register a new user and return the Authorization header."""
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "testpassword"
    
    # Register
    client.post("/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": password
    })
    
    # Login
    response = client.post("/auth/token", data={
        "username": email,
        "password": password
    })
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
