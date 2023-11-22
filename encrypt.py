from __future__ import annotations

from cryptography.fernet import Fernet
from hashlib import md5


def encrypt(data: bytes, key: bytes | str) -> str:
    """
    Encrypt incoming data and returning result as string
    :param bytes data: must be passed as byte array
    :param Union[bytes, str] key: must be Fernet key like object - 32 url-safe base64-encoded bytes
    :return:
    """
    return Fernet(key=key).encrypt(data).decode()


def decrypt(data: bytes | str, key: bytes | str) -> str:
    """
    Decrypt data and returning result as string
    :param Union[bytes, str] data: may be byte array or string object
    :param Union[bytes, str] key: must be Fernet key like object - 32 url-safe base64-encoded bytes
    :return:
    """
    return Fernet(key=key).decrypt(data).decode()


def compare_phrase(hashed_phrase, phrase: str) -> bool:
    """
    Compare stored phrase and incoming: check equals by hashes
    :param hashed_phrase:
    :param phrase:
    :return:
    """
    return hashed_phrase == md5(phrase.encode()).hexdigest()