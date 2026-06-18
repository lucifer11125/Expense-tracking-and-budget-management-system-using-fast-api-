# Deploying FastAPI App to Vercel

## Prerequisites
1. GitHub account (already have ✓)
2. Vercel account (free at https://vercel.com)
3. Git configured

## Step-by-Step Deployment

### 1. Create Vercel Account
- Go to https://vercel.com
- Sign up with your GitHub account (lucifer11125)
- This connects your GitHub repos automatically

### 2. Connect Your Repository
- Go to https://vercel.com/new
- Import your GitHub repository: `Expense-tracking-and-budget-management-system-using-fast-api-`
- Vercel will auto-detect it's a Python project

### 3. Configure Environment Variables
In Vercel dashboard, add these environment variables:
```
DATABASE_URL=sqlite:///./expense_tracker.db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Note:** For production, use a persistent database like PostgreSQL:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 4. Deploy
- Vercel will automatically build and deploy on push to main
- Your app will be available at: `https://your-project-name.vercel.app`

## Important Considerations

### Database
- **SQLite** (current) won't persist across Vercel's serverless restarts
- **Recommended:** Use PostgreSQL (free tier available on Heroku, Railway, or Vercel Postgres)
- Update your database URL in environment variables

### CORS Configuration
Update your FastAPI CORS settings in `app/app.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-project-name.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Static Files
Vercel serves static files from the `app/static/` directory automatically.

### Cold Starts
Serverless functions may have cold starts (first request takes longer). This is normal.

## Deploy via Git Push
1. Commit changes:
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. Vercel automatically deploys when you push to main

## Troubleshooting

### Build Fails
- Check Vercel logs: Dashboard → Your Project → Deployments
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility (3.9+)

### Database Errors
- Verify DATABASE_URL environment variable
- Ensure database is accessible from Vercel's servers
- For SQLite, use local development only

### CORS Errors
- Update allowed origins in FastAPI CORS middleware
- Include your Vercel domain

### Static Files Not Loading
- Files should be in `app/static/` directory
- Verify paths in index.html are correct
- Use relative paths: `/static/file.css` not absolute paths

## Next Steps
1. Push the `vercel.json` and `.vercelignore` files to GitHub
2. Create Vercel account
3. Import repository to Vercel
4. Set environment variables
5. Deploy!

## Useful Links
- Vercel Docs: https://vercel.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- PostgreSQL on Vercel: https://vercel.com/docs/storage/postgres
