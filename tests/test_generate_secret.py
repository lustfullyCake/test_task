from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_generate_secret_successful():
    response = client.post("/secret/", json={
        "secret": "123456", "phrase": "123456",
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json().get("key"), str)


def test_generate_secret_empty_body():
    response = client.post("/secret/", json={
        "secret": "123456",
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(response.json().get("detail"), list)
