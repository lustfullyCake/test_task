from __future__ import annotations

from pydantic import BaseModel


class GenerateSecretResponse(BaseModel):
    key: str


class GetSecretResponse(BaseModel):
    secret: str


class MessageResponse(BaseModel):
    message: str