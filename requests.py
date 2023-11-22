from __future__ import annotations

from pydantic import BaseModel


class GenerateSecretRequest(BaseModel):
    secret: str
    phrase: str


class GetSecretRequest(BaseModel):
    phrase: str
