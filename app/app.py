from pathlib import Path
import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.database import create_tables, get_db
from app.schemas import (
    BudgetCreate,
    BudgetOut,
    BudgetUpdate,
    ExpenseCreate,
    ExpenseOut,
    ExpenseUpdate,
    SummaryOut,
    TokenSchema,
    UserAuth,
    UserOut,
)
from app.utils import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_hashed_password,
    verify_password
)

app = FastAPI(title="Expense Tracker API", version="1.0.0")
create_tables()
STATIC_DIR = Path(__file__).with_name("static")

# CORS Configuration for production deployment
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    os.getenv("VERCEL_URL", "").rstrip("/"),
]
# Add Vercel deployment URL if available
if os.getenv("VERCEL_URL"):
    allowed_origins.append(f"https://{os.getenv('VERCEL_URL')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in allowed_origins if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.get("responses", {}).pop("422", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, conn=Depends(get_db)):
    email = str(data.email).strip().lower()
    username = data.username.strip()

    if crud.find_user(conn, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    if crud.find_user(conn, username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )

    return crud.create_user(conn, email, username, get_hashed_password(data.password))

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    conn=Depends(get_db),
):
    user = crud.find_user(conn, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!"
        )

    hashed_pass = user["hashed_password"]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user["email"]),
        "refresh_token": create_refresh_token(user["email"]),
    }

@app.get("/me", response_model=UserOut)
async def my_profile(current_user=Depends(get_current_user)):
    return current_user


@app.post("/expenses", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
async def add_expense(
    data: ExpenseCreate,
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    return crud.create_expense(conn, current_user["id"], data)


@app.get("/expenses", response_model=list[ExpenseOut])
async def get_expenses(
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    return crud.list_expenses(conn, current_user["id"])


@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
async def edit_expense(
    expense_id: str,
    data: ExpenseUpdate,
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    expense = crud.get_expense(conn, current_user["id"], expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return crud.update_expense(conn, expense_id, data)


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_expense(
    expense_id: str,
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    expense = crud.get_expense(conn, current_user["id"], expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    crud.delete_expense(conn, expense_id)


@app.post("/budgets", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
async def add_budget(
    data: BudgetCreate,
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    return crud.create_budget(conn, current_user["id"], data)


@app.get("/budgets", response_model=list[BudgetOut])
async def get_budgets(
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    return crud.list_budgets(conn, current_user["id"])


@app.put("/budgets/{budget_id}", response_model=BudgetOut)
async def edit_budget(
    budget_id: str,
    data: BudgetUpdate,
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    budget = crud.get_budget(conn, current_user["id"], budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return crud.update_budget(conn, budget_id, data)


@app.delete("/budgets/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_budget(
    budget_id: str,
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    budget = crud.get_budget(conn, current_user["id"], budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    crud.delete_budget(conn, budget_id)


@app.get("/summary", response_model=SummaryOut)
async def get_summary(
    current_user=Depends(get_current_user),
    conn=Depends(get_db),
):
    return crud.budget_summary(conn, current_user["id"])
