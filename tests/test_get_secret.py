from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def create_secret(data):
    response = client.post("/secret/", json=data)
    print(response.json())
    return response.json().get("key")


def test_get_secret_successful():
    secret = create_secret({"secret": "123456", "phrase": "123456"})
    response = client.post(f"/secret/{secret}/", json={
        "phrase": "123456",
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("secret") == "123456"


def test_get_secret_empty_body():
    secret = create_secret({"secret": "123456", "phrase": "123456"})

    response = client.post(f"/secret/{secret}/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(response.json().get("detail"), list)


def test_get_secret_not_found():
    response = client.post("/secret/8860a399-b982-4f59-ab8b-940922b81f24/", json={
        "phrase": "123456"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(response.json().get("message"), str)


def test_get_secret_invalid_phrase():
    secret = create_secret({"secret": "123456", "phrase": "123456"})

    response = client.post(f"/secret/{secret}/", json={
        "phrase": "12345",
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response.json().get("message"), str)
