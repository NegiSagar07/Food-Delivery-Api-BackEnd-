# File: tests/test_main.py (This is correct)

import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus

# This is a regular, synchronous test function
def test_read_root(client: TestClient):
    """
    Test the main '/' endpoint.
    """
    response = client.get("/")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"msg": "Welcome to the Food Delivery Api"}