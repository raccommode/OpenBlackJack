"""Authentication helpers for password hashing and token management."""
from __future__ import annotations

import secrets
import sqlite3
from datetime import datetime, timedelta
from typing import Optional

import bcrypt

from . import db

TOKEN_TTL_HOURS = 24


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def generate_token(user_id: int) -> str:
    token = secrets.token_hex(24)
    db.save_token(token, user_id)
    return token


def authenticate(token: str) -> Optional[sqlite3.Row]:
    record = db.get_token(token)
    if not record:
        return None
    created_at = datetime.fromisoformat(record["created_at"])
    if datetime.utcnow() - created_at > timedelta(hours=TOKEN_TTL_HOURS):
        db.delete_token(token)
        return None
    return db.get_user_by_id(record["user_id"])
