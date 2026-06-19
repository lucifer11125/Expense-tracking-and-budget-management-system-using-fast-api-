import os

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# ---------- Connection ----------
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("POSTGRES_URL")
)

# Neon / Vercel uses 'postgres://' which psycopg2 doesn't accept
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Lazy connection pool – created on first use so cold-start import won't fail
_pool = None


def _get_pool():
    """Return the connection pool, creating it on first call."""
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            raise RuntimeError(
                "No DATABASE_URL or POSTGRES_URL environment variable set. "
                "Please configure a PostgreSQL connection string."
            )
        _pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            dsn=DATABASE_URL,
            cursor_factory=RealDictCursor,
        )
    return _pool


def get_conn():
    """Get a connection from the pool."""
    return _get_pool().getconn()


def put_conn(conn):
    """Return a connection to the pool."""
    _get_pool().putconn(conn)


def get_db():
    """FastAPI dependency – yields a connection, auto-commits or rolls back."""
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        put_conn(conn)


# ---------- Table creation ----------
_CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id          TEXT PRIMARY KEY,
    username    TEXT UNIQUE NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    amount      DOUBLE PRECISION NOT NULL,
    category    TEXT NOT NULL,
    spent_on    DATE NOT NULL,
    note        TEXT
);

CREATE TABLE IF NOT EXISTS budgets (
    id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category    TEXT NOT NULL,
    limit_amount DOUBLE PRECISION NOT NULL,
    month       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_email    ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_expenses_user  ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_budgets_user   ON budgets(user_id);
"""


def create_tables() -> None:
    """Create all tables if they don't already exist."""
    try:
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(_CREATE_TABLES_SQL)
            conn.commit()
        finally:
            put_conn(conn)
    except Exception as e:
        print(f"DATABASE CONNECTION ERROR: {e}", flush=True)
        raise
