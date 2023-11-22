from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .settings import get_settings


engine = create_engine(get_settings().db_url, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> None:
    """
    Yield session
    :return:
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
