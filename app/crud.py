from sqlalchemy import func
from sqlalchemy.orm import Session

from app import database
from app.schemas import BudgetCreate, BudgetUpdate, ExpenseCreate, ExpenseUpdate


def find_user(db: Session, login: str):
    login = login.strip().lower()
    return (
        db.query(database.User)
        .filter(
            (func.lower(database.User.email) == login)
            | (func.lower(database.User.username) == login)
        )
        .first()
    )


def create_user(db: Session, email: str, username: str, hashed_password: str):
    user = database.User(
        email=email,
        username=username,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_expenses(db: Session, user_id: str):
    return db.query(database.Expense).filter(database.Expense.user_id == user_id).all()


def get_expense(db: Session, user_id: str, expense_id: str):
    return (
        db.query(database.Expense)
        .filter(database.Expense.user_id == user_id, database.Expense.id == expense_id)
        .first()
    )


def create_expense(db: Session, user_id: str, data: ExpenseCreate):
    expense = database.Expense(user_id=user_id, **data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def update_expense(db: Session, expense, data: ExpenseUpdate):
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense) -> None:
    db.delete(expense)
    db.commit()


def list_budgets(db: Session, user_id: str):
    return db.query(database.Budget).filter(database.Budget.user_id == user_id).all()


def get_budget(db: Session, user_id: str, budget_id: str):
    return (
        db.query(database.Budget)
        .filter(database.Budget.user_id == user_id, database.Budget.id == budget_id)
        .first()
    )


def create_budget(db: Session, user_id: str, data: BudgetCreate):
    budget = database.Budget(user_id=user_id, **data.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def update_budget(db: Session, budget, data: BudgetUpdate):
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(budget, key, value)
    db.commit()
    db.refresh(budget)
    return budget


def delete_budget(db: Session, budget) -> None:
    db.delete(budget)
    db.commit()


def budget_summary(db: Session, user_id: str) -> dict:
    expenses = list_expenses(db, user_id)
    budgets = list_budgets(db, user_id)
    budget_status = []

    for budget in budgets:
        spent = sum(
            expense.amount
            for expense in expenses
            if expense.category.lower() == budget.category.lower()
            and expense.spent_on.strftime("%Y-%m") == budget.month
        )
        remaining = budget.limit_amount - spent
        budget_status.append(
            {
                "budget_id": budget.id,
                "category": budget.category,
                "month": budget.month,
                "limit_amount": budget.limit_amount,
                "spent": spent,
                "remaining": remaining,
                "status": "within_budget" if remaining >= 0 else "over_budget",
            }
        )

    return {
        "total_spent": sum(expense.amount for expense in expenses),
        "expenses_count": len(expenses),
        "budgets": budget_status,
    }
