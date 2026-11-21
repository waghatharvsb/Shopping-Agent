"""Database connection helper: Turso (libSQL) when configured, local SQLite otherwise."""

import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv(
    "DB_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "store.db")),
)


def using_turso() -> bool:
    return bool(os.getenv("TURSO_DATABASE_URL") and os.getenv("TURSO_AUTH_TOKEN"))


def get_connection():
    if using_turso():
        import libsql

        return libsql.connect(
            database=os.environ["TURSO_DATABASE_URL"],
            auth_token=os.environ["TURSO_AUTH_TOKEN"],
        )
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def rows_to_dicts(rows, columns):
    return [dict(zip(columns, row)) for row in rows]