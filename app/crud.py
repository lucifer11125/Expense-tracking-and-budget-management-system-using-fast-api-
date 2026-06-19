from datetime import date
from uuid import uuid4

from app.schemas import BudgetCreate, BudgetUpdate, ExpenseCreate, ExpenseUpdate


# ──────────────────── helpers ────────────────────

def _row_to_dict(row):
    """RealDictRow → plain dict (no-op if already dict)."""
    return dict(row) if row else None


def _new_id() -> str:
    return str(uuid4())


# ──────────────────── users ────────────────────

def find_user(conn, login: str):
    login = login.strip().lower()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, username, email, hashed_password
            FROM users
            WHERE LOWER(email) = %s OR LOWER(username) = %s
            LIMIT 1
            """,
            (login, login),
        )
        row = cur.fetchone()
    return _row_to_dict(row)


def create_user(conn, email: str, username: str, hashed_password: str) -> dict:
    user_id = _new_id()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (id, username, email, hashed_password)
            VALUES (%s, %s, %s, %s)
            RETURNING id, username, email
            """,
            (user_id, username, email, hashed_password),
        )
        row = cur.fetchone()
    conn.commit()
    return _row_to_dict(row)


# ──────────────────── expenses ────────────────────

def list_expenses(conn, user_id: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM expenses WHERE user_id = %s ORDER BY spent_on DESC",
            (user_id,),
        )
        return [dict(r) for r in cur.fetchall()]


def get_expense(conn, user_id: str, expense_id: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM expenses WHERE user_id = %s AND id = %s",
            (user_id, expense_id),
        )
        row = cur.fetchone()
    return _row_to_dict(row)


def create_expense(conn, user_id: str, data: ExpenseCreate) -> dict:
    expense_id = _new_id()
    d = data.model_dump()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO expenses (id, user_id, title, amount, category, spent_on, note)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                expense_id, user_id,
                d["title"], d["amount"], d["category"], d["spent_on"], d["note"],
            ),
        )
        row = cur.fetchone()
    conn.commit()
    return _row_to_dict(row)


def update_expense(conn, expense_id: str, data: ExpenseUpdate) -> dict:
    updates = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if not updates:
        return get_expense(conn, "", expense_id)  # nothing to update

    set_clause = ", ".join(f"{col} = %s" for col in updates)
    values = list(updates.values()) + [expense_id]

    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE expenses SET {set_clause} WHERE id = %s RETURNING *",
            values,
        )
        row = cur.fetchone()
    conn.commit()
    return _row_to_dict(row)


def delete_expense(conn, expense_id: str) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()


# ──────────────────── budgets ────────────────────

def list_budgets(conn, user_id: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM budgets WHERE user_id = %s ORDER BY month DESC",
            (user_id,),
        )
        return [dict(r) for r in cur.fetchall()]


def get_budget(conn, user_id: str, budget_id: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM budgets WHERE user_id = %s AND id = %s",
            (user_id, budget_id),
        )
        row = cur.fetchone()
    return _row_to_dict(row)


def create_budget(conn, user_id: str, data: BudgetCreate) -> dict:
    budget_id = _new_id()
    d = data.model_dump()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO budgets (id, user_id, category, limit_amount, month)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (budget_id, user_id, d["category"], d["limit_amount"], d["month"]),
        )
        row = cur.fetchone()
    conn.commit()
    return _row_to_dict(row)


def update_budget(conn, budget_id: str, data: BudgetUpdate) -> dict:
    updates = {k: v for k, v in data.model_dump(exclude_none=True).items()}
    if not updates:
        return get_budget(conn, "", budget_id)

    set_clause = ", ".join(f"{col} = %s" for col in updates)
    values = list(updates.values()) + [budget_id]

    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE budgets SET {set_clause} WHERE id = %s RETURNING *",
            values,
        )
        row = cur.fetchone()
    conn.commit()
    return _row_to_dict(row)


def delete_budget(conn, budget_id: str) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM budgets WHERE id = %s", (budget_id,))
    conn.commit()


# ──────────────────── summary ────────────────────

def budget_summary(conn, user_id: str) -> dict:
    expenses = list_expenses(conn, user_id)
    budgets = list_budgets(conn, user_id)
    budget_status = []

    for budget in budgets:
        spent = sum(
            exp["amount"]
            for exp in expenses
            if exp["category"].lower() == budget["category"].lower()
            and exp["spent_on"].strftime("%Y-%m") == budget["month"]
        )
        remaining = budget["limit_amount"] - spent
        budget_status.append(
            {
                "budget_id": budget["id"],
                "category": budget["category"],
                "month": budget["month"],
                "limit_amount": budget["limit_amount"],
                "spent": spent,
                "remaining": remaining,
                "status": "within_budget" if remaining >= 0 else "over_budget",
            }
        )

    return {
        "total_spent": sum(exp["amount"] for exp in expenses),
        "expenses_count": len(expenses),
        "budgets": budget_status,
    }
