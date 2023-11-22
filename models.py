from __future__ import annotations

from sqlalchemy import UUID, Column, String

from .database import Base


class Secret(Base):
    __tablename__ = "secrets"
    key = Column(UUID, primary_key=True, index=True)
    secret = Column(String)
    phrase = Column(String)
