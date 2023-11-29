from __future__ import annotations

from hashlib import md5
from pydantic import BaseModel, Field
from uuid import uuid4

from encrypt import encrypt
from settings import get_settings


class SecretRecord(BaseModel):
    secret: str = Field()
    phrase: str = Field()
    key: uuid4 = Field(default_factory=uuid4, alias="key")

    def process_request(self) -> None:
        """
        Process incoming data to encrypted.
        :return:
        """
        settings = get_settings()

        self.secret = encrypt(self.secret.encode(), settings.secret_key)
        self.phrase = md5(self.phrase.encode()).hexdigest()

    @property
    def key_to_str(self) -> str:
        return str(self.key)

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "secret": "Some secret data",
                "phrase": "123456qwerty",
                "key": "8860a399-b982-4f59-ab8b-940922b81f23",
            }
        }
