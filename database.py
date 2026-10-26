import os
import sqlite3
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "passwords.db")

_wal_initialized = False


def get_connection():
    global _wal_initialized

    conn = sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)

    if not _wal_initialized:
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            _wal_initialized = True
        except sqlite3.OperationalError:
            pass  # kilitliyse devam et, sistemi durdurma

    return conn


def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password_text TEXT NOT NULL UNIQUE
            )
        """)
        conn.commit()
    finally:
        conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def insert_password(password):
    hashed_password = hash_password(password)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO passwords (password_text) VALUES (?)",
            (hashed_password,)
        )
        conn.commit()
    finally:
        conn.close()


def password_exists(password):
    hashed_password = hash_password(password)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM passwords WHERE password_text = ?",
            (hashed_password,)
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()
