import os
from uuid import uuid4

from sqlalchemy import Column, Date, Float, ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


# Use PostgreSQL if available, fallback to SQLite for development
# Vercel/Neon sets POSTGRES_URL; also check DATABASE_URL for flexibility
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("POSTGRES_URL")
    or "sqlite:///./expense_tracker.db"  # Fallback for development
)
# Neon/Vercel uses 'postgres://' which SQLAlchemy doesn't accept; fix it
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure engine based on database type
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )
else:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    expenses = relationship("Expense", back_populates="user", cascade="all, delete")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    spent_on = Column(Date, nullable=False)
    note = Column(String, nullable=True)

    user = relationship("User", back_populates="expenses")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    limit_amount = Column(Float, nullable=False)
    month = Column(String, nullable=False)

    user = relationship("User", back_populates="budgets")


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
