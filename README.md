# Expense Tracking and Budget Management API

A simple FastAPI project built from the JWT authentication example. It uses:

- FastAPI for API routes
- JWT for login and protected endpoints
- SQLAlchemy for database tables and queries
- SQLite by default, so it runs without installing PostgreSQL

## Project Structure

```text
app/
  app.py        FastAPI routes
  database.py   SQLAlchemy database connection and tables
  utils.py      JWT, password hashing, current user dependency
  crud.py       Database CRUD functions
  schemas.py    Pydantic request and response schemas
DIAGRAMS.md     ER and schema diagrams
README.md       Project guide
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
JWT_SECRET_KEY=qwertyuiopasdfghjklzxcvbnm
JWT_REFRESH_SECRET_KEY=zxcvbnmasdfghjklqwertyuiop
```

Optional PostgreSQL example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_tracker
```

For PostgreSQL, install a PostgreSQL driver such as `psycopg2-binary`. For class/demo use, the default SQLite database is simpler.

## Run

```powershell
uvicorn app.app:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Open the app UI:

```text
http://127.0.0.1:8000
```

## Main Endpoints

### Auth

- `POST /signup` - create user
- `POST /login` - get access token and refresh token
- `GET /me` - view logged in user

### Expenses

- `POST /expenses` - add expense
- `GET /expenses` - list expenses
- `PUT /expenses/{expense_id}` - update expense
- `DELETE /expenses/{expense_id}` - delete expense

### Budgets

- `POST /budgets` - add budget
- `GET /budgets` - list budgets
- `PUT /budgets/{budget_id}` - update budget
- `DELETE /budgets/{budget_id}` - delete budget

### Summary

- `GET /summary` - total spending and budget status

## How to Use JWT in Swagger

1. Call `POST /signup`.
2. Call `POST /login` with username or email and password.
3. Copy the `access_token`.
4. Click `Authorize` in Swagger UI.
5. Paste the token as:

```text
Bearer your_access_token_here
```

Now the expense, budget, and summary endpoints will work.

## How to Explain the Code

- `database.py` creates the real database tables: `users`, `expenses`, and `budgets`.
- `schemas.py` validates request data and controls response data.
- `utils.py` handles password hashing, JWT creation, and checking the logged-in user.
- `crud.py` contains create, read, update, and delete database queries.
- `app.py` connects API endpoints to JWT and CRUD functions.

## Diagrams

See [DIAGRAMS.md](DIAGRAMS.md) for:

- ER diagram
- Simple app schema / flow diagram
