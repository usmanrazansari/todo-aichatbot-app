# Deployment Guide

This guide will help you deploy your Todo App with AI Chatbot to production.

## Architecture Overview

- **Frontend:** Deployed on Vercel (Next.js)
- **Backend:** Deployed on Railway/Render/Fly.io (FastAPI)
- **Database:** PostgreSQL (managed service)

---

## Part 1: Backend Deployment

### Recommended Platforms

1. **Railway** (Easiest, $5/month)
2. **Render** (Free tier available)
3. **Fly.io** (Free tier available)

### Option A: Deploy to Railway

#### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"

#### Step 2: Deploy Backend
1. Click "Deploy from GitHub repo"
2. Select your repository: `usmanrazansari/todo-aichatbot-app`
3. Select the `backend` directory as root
4. Railway will auto-detect Python/FastAPI

#### Step 3: Add PostgreSQL Database
1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a database and set `DATABASE_URL`

#### Step 4: Configure Environment Variables
Go to your backend service → Variables tab and add:

```
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=generate_a_secure_random_string_here
CORS_ORIGINS=https://your-app.vercel.app
APP_ENV=production
DEBUG=false
```

**Note:** `DATABASE_URL` is automatically set by Railway when you add PostgreSQL.

#### Step 5: Deploy
1. Railway will automatically deploy
2. Copy your backend URL (e.g., `https://your-app.up.railway.app`)
3. Test the health endpoint: `https://your-app.up.railway.app/health`

---

### Option B: Deploy to Render

#### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

#### Step 2: Create PostgreSQL Database
1. Click "New" → "PostgreSQL"
2. Name: `todo-app-db`
3. Select free tier
4. Click "Create Database"
5. Copy the "Internal Database URL"

#### Step 3: Deploy Backend
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `todo-app-backend`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

#### Step 4: Add Environment Variables
In the "Environment" tab, add:

```
DATABASE_URL=<paste_internal_database_url_here>
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=generate_a_secure_random_string_here
CORS_ORIGINS=https://your-app.vercel.app
APP_ENV=production
DEBUG=false
```

#### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Copy your backend URL (e.g., `https://todo-app-backend.onrender.com`)

---

### Option C: Deploy to Fly.io

#### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### Step 2: Login and Initialize
```bash
cd backend
fly auth login
fly launch
```

Follow the prompts:
- App name: `todo-app-backend`
- Region: Choose closest to you
- PostgreSQL: Yes (select free tier)

#### Step 3: Set Environment Variables
```bash
fly secrets set OPENAI_API_KEY=your_openai_api_key_here
fly secrets set JWT_SECRET=generate_a_secure_random_string_here
fly secrets set CORS_ORIGINS=https://your-app.vercel.app
```

#### Step 4: Deploy
```bash
fly deploy
```

---

## Part 2: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub

### Step 2: Import Project
1. Click "Add New" → "Project"
2. Import your repository: `usmanrazansari/todo-aichatbot-app`
3. Vercel will auto-detect Next.js

### Step 3: Configure Project
- **Framework Preset:** Next.js
- **Root Directory:** `frontend`
- **Build Command:** `npm run build` (auto-detected)
- **Output Directory:** `.next` (auto-detected)

### Step 4: Add Environment Variables
In the "Environment Variables" section, add:

```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
```

Replace `https://your-backend-url.com` with your actual backend URL from Part 1.

### Step 5: Deploy
1. Click "Deploy"
2. Wait for deployment to complete (2-3 minutes)
3. Copy your frontend URL (e.g., `https://your-app.vercel.app`)

### Step 6: Update Backend CORS
Go back to your backend platform (Railway/Render/Fly.io) and update the `CORS_ORIGINS` environment variable:

```
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-preview.vercel.app
```

**Note:** Add both production and preview URLs for Vercel deployments.

---

## Part 3: Post-Deployment Configuration

### 1. Test Your Deployment

#### Test Backend
```bash
curl https://your-backend-url.com/health
# Should return: {"status":"healthy","service":"todo-api"}
```

#### Test Frontend
1. Open `https://your-app.vercel.app`
2. Register a new account
3. Create a task via the dashboard
4. Test the AI chatbot

### 2. Update GitHub Repository
Update your README.md with the live URLs:

```markdown
## Live Demo

- **Frontend:** https://your-app.vercel.app
- **Backend API:** https://your-backend-url.com
- **API Docs:** https://your-backend-url.com/docs
```

### 3. Monitor Your Application

#### Vercel Dashboard
- View deployment logs
- Monitor performance
- Check analytics

#### Backend Platform Dashboard
- Monitor resource usage
- View application logs
- Check database connections

---

## Environment Variables Summary

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host:port/database
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secure-random-string
CORS_ORIGINS=https://your-app.vercel.app
APP_ENV=production
DEBUG=false
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
```

---

## Troubleshooting

### Frontend can't connect to backend
- Check `NEXT_PUBLIC_API_BASE_URL` is set correctly in Vercel
- Verify backend is running: visit `/health` endpoint
- Check CORS configuration in backend

### Database connection errors
- Verify `DATABASE_URL` is set correctly
- Check database is running and accessible
- Ensure PostgreSQL dependencies are installed

### AI Chatbot not working
- Verify `OPENAI_API_KEY` is set in backend
- Check OpenAI API key is valid and has credits
- Review backend logs for OpenAI API errors

### 401 Unauthorized errors
- Check JWT_SECRET is set consistently
- Clear browser localStorage and re-login
- Verify authentication endpoints are working

---

## Cost Estimates

### Free Tier (Hobby Projects)
- **Vercel:** Free (100GB bandwidth/month)
- **Render:** Free (750 hours/month, sleeps after inactivity)
- **PostgreSQL (Render):** Free (1GB storage, expires after 90 days)
- **Total:** $0/month (with limitations)

### Paid Tier (Production)
- **Vercel Pro:** $20/month
- **Railway:** $5/month (backend + database)
- **Total:** $25/month

---

## Security Checklist

- [ ] Changed default JWT_SECRET
- [ ] OpenAI API key is kept secret (not in code)
- [ ] CORS is configured with specific origins (not "*")
- [ ] Database uses SSL connection
- [ ] Environment variables are set in platform dashboards (not committed to git)
- [ ] .env files are in .gitignore

---

## Next Steps

1. Set up custom domain (optional)
2. Configure SSL certificates (automatic on Vercel/Railway/Render)
3. Set up monitoring and alerts
4. Configure database backups
5. Add rate limiting for API endpoints
6. Set up CI/CD for automatic deployments

---

## Support

If you encounter issues:
1. Check platform-specific documentation
2. Review application logs
3. Test locally with production environment variables
4. Open an issue on GitHub: https://github.com/usmanrazansari/todo-aichatbot-app/issues
