# PostgreSQL Migration Guide

This project has been updated to use **PostgreSQL** instead of SQLite. This guide will help you set it up.

## Local Development Setup

### 1. Install PostgreSQL
- **Windows**: Download from https://www.postgresql.org/download/windows/
- **Mac**: `brew install postgresql@15`
- **Linux**: `sudo apt-get install postgresql postgresql-contrib`

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE expense_tracker;

# Create user (if not using postgres user)
CREATE USER app_user WITH PASSWORD 'your_password';
ALTER ROLE app_user SET client_encoding TO 'utf8';
ALTER ROLE app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE app_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO app_user;

# Exit
\q
```

### 3. Update `.env` File

```env
JWT_SECRET_KEY=qwertyuiopasdfghjklzxcvbnm
JWT_REFRESH_SECRET_KEY=zxcvbnmasdfghjklqwertyuiop
DATABASE_URL=postgresql://app_user:your_password@localhost:5432/expense_tracker
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the App

```bash
uvicorn app.app:app --reload
```

## Production Deployment (Vercel/Cloud)

### Option 1: Railway.app (Recommended - Free)

1. Go to https://railway.app
2. Sign up with GitHub
3. Create a new project → Add PostgreSQL
4. Copy the DATABASE_URL from the PostgreSQL plugin
5. Add to your Vercel environment variables

### Option 2: Vercel Postgres

1. Go to https://vercel.com/docs/storage/vercel-postgres
2. Add Vercel Postgres to your project
3. Copy the DATABASE_URL
4. Add to environment variables

### Option 3: Render.com

1. Go to https://render.com
2. Create a PostgreSQL database
3. Copy connection string
4. Add to environment variables

### Option 4: AWS RDS / DigitalOcean / Other Providers

Use the standard PostgreSQL connection string:
```
postgresql://username:password@host:port/database_name
```

## Environment Variables

For **Vercel Dashboard**, add these environment variables:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
JWT_SECRET_KEY=your_secret_key
JWT_REFRESH_SECRET_KEY=your_refresh_secret_key
```

## Testing Connection

```python
# Quick test in Python
import psycopg2
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost:5432/expense_tracker"
engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print("Connected successfully!")
```

## Migrating from SQLite (If You Have Existing Data)

If you have data in the old SQLite database and want to migrate it:

```bash
# 1. Export from SQLite
sqlite3 expense_tracker.db .dump > backup.sql

# 2. Install migration tool
pip install pgloader

# 3. Migrate data
pgloader sqlite:///expense_tracker.db postgresql://user:password@localhost:5432/expense_tracker
```

## Notes

- PostgreSQL is more reliable for production than SQLite
- It persists data across app restarts
- Supports concurrent connections better
- Better for scalable applications
- Most free tiers provide enough resources for small projects

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL is running
- Check host, port, username, password in DATABASE_URL
- Verify database exists

### psycopg2 Installation Issues
- On Windows: Install PostgreSQL with pgAdmin/development tools
- On Mac: `brew install postgresql`
- On Linux: `sudo apt-get install libpq-dev`

### SSL Certificate Errors
Add to DATABASE_URL:
```
postgresql://user:password@host:port/dbname?sslmode=require
```

## Performance Tips

- Use connection pooling (already configured with pool_size=10)
- Add indexes on frequently queried columns
- Regular backups of your database
- Monitor query performance
