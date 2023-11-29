from __future__ import annotations

from fastapi.testclient import TestClient

from encrypt import encrypt, decrypt
from main import app

client = TestClient(app)


def test_encrypt():
    KEY = "MT5nvmFISm3k_NUKJtvSUEUH4R8HmdBSnXAnhvnJOjI="
    data = "123456"

    encrypted_data = encrypt(data.encode(), KEY)
    assert data == decrypt(encrypted_data, KEY)
