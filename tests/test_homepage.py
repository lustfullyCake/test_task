from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "ok"}
