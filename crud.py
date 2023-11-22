from __future__ import annotations

from typing import TYPE_CHECKING

from .models import Secret

if TYPE_CHECKING:
    from schemas import SecretRecord
    from sqlalchemy.orm import Session


def add_secret(db: Session, record: SecretRecord) -> None:
    """
    Save secret record in database table and commit
    :param db:
    :param record:
    :return:
    """
    instance = Secret(
        key=record.key,
        secret=record.secret,
        phrase=record.phrase,
    )
    db.add(instance)
    db.commit()


def find_secret(db: Session, key: str) -> Secret:
    """
    Find the secret by key
    :param db:
    :param key:
    :return:
    """
    return db.query(Secret).filter_by(key=key).first()


def delete_secret(db: Session, instance: Secret) -> None:
    """
    Delete instance and commit
    :param db:
    :param instance:
    :return:
    """
    db.delete(instance)
    db.commit()
