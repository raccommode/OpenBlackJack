"""SQLite database utilities for user and token management."""
from __future__ import annotations

import shutil
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path("data/blackjack.db")
BACKUP_DIR = Path("data/backups")
BACKUP_INTERVAL_SECONDS = 60

_connection_lock = threading.Lock()
_connection: Optional[sqlite3.Connection] = None
_backup_thread: Optional[threading.Thread] = None
_stop_backup = threading.Event()


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
    return _connection


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_tokens (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()


def create_user(username: str, password_hash: str) -> int:
    with _connection_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, balance, created_at) VALUES (?, ?, ?, ?)",
            (username, password_hash, 1000, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cursor.lastrowid


def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    with _connection_lock:
        cursor = get_connection().cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()


def get_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    with _connection_lock:
        cursor = get_connection().cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()


def update_user_balance(user_id: int, new_balance: int) -> None:
    with _connection_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
        conn.commit()


def save_token(token: str, user_id: int) -> None:
    with _connection_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO auth_tokens (token, user_id, created_at) VALUES (?, ?, ?)",
            (token, user_id, datetime.utcnow().isoformat()),
        )
        conn.commit()


def get_token(token: str) -> Optional[sqlite3.Row]:
    with _connection_lock:
        cursor = get_connection().cursor()
        cursor.execute("SELECT * FROM auth_tokens WHERE token = ?", (token,))
        return cursor.fetchone()


def delete_token(token: str) -> None:
    with _connection_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM auth_tokens WHERE token = ?", (token,))
        conn.commit()


def start_backup_thread() -> None:
    global _backup_thread
    if _backup_thread and _backup_thread.is_alive():
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    _stop_backup.clear()

    def _run_backup() -> None:
        while not _stop_backup.is_set():
            time.sleep(BACKUP_INTERVAL_SECONDS)
            try:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                backup_file = BACKUP_DIR / f"players_backup_{timestamp}.db"
                with _connection_lock:
                    conn = get_connection()
                    conn.commit()
                    if DB_PATH.exists():
                        shutil.copy(DB_PATH, backup_file)
            except Exception:
                # Best-effort backup; errors are ignored to avoid crashing the app.
                continue

    _backup_thread = threading.Thread(target=_run_backup, name="backup-thread", daemon=True)
    _backup_thread.start()


def stop_backup_thread() -> None:
    _stop_backup.set()
    if _backup_thread and _backup_thread.is_alive():
        _backup_thread.join(timeout=1)


__all__ = [
    "init_db",
    "create_user",
    "get_user_by_username",
    "get_user_by_id",
    "update_user_balance",
    "save_token",
    "get_token",
    "delete_token",
    "start_backup_thread",
    "stop_backup_thread",
]
