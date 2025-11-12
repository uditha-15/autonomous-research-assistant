# Step-by-Step Guide: Hosting on Render

This guide will walk you through hosting the Autonomous Research Assistant on Render, step by step.

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] A Google account (for Gemini API)
- [ ] A GitHub account (free)
- [ ] A Render account (free tier available)

---

## Step 1: Get Your Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy your API key (it looks like: `AIzaSy...`)
5. **Save it somewhere safe** - you'll need it later

---

## Step 2: Create a GitHub Account (if you don't have one)

1. Go to [github.com](https://github.com)
2. Click **"Sign up"**
3. Follow the registration process
4. Verify your email

---

## Step 3: Push Your Code to GitHub

### Option A: Using GitHub Web Interface (Easiest)

1. **Create a new repository:**
   - Go to [github.com/new](https://github.com/new)
   - Repository name: `autonomous-research-assistant`
   - Choose **Public** or **Private**
   - **Don't** initialize with README (we already have one)
   - Click **"Create repository"**

2. **Upload your files:**
   - On the new repository page, you'll see instructions
   - Click **"uploading an existing file"**
   - Drag and drop ALL files from your `autonomous-research-assistant` folder
   - **Important:** Make sure to upload:
     - All `.py` files
     - `requirements.txt`
     - `Procfile`
     - `render.yaml`
     - `runtime.txt`
     - `README.md`
     - `templates/` folder (with `index.html`)
     - `.env.example`
     - `.gitignore`
   - Scroll down, add commit message: "Initial commit"
   - Click **"Commit changes"**

### Option B: Using Git Command Line (If you have Git installed)

```bash
# Navigate to your project folder
cd autonomous-research-assistant

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/autonomous-research-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 4: Create a Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Choose **"Sign up with GitHub"** (recommended - easiest)
4. Authorize Render to access your GitHub account
5. Complete the signup process

---

## Step 5: Deploy on Render

### Method 1: Using render.yaml (Automatic - Recommended)

1. **Create a New Blueprint:**
   - In Render dashboard, click **"New +"** (top right)
   - Select **"Blueprint"**
   - Connect your GitHub account if not already connected
   - Select your repository: `autonomous-research-assistant`
   - Click **"Apply"**

2. **Render will automatically:**
   - Detect `render.yaml`
   - Create the web service
   - Set up everything

3. **Add Environment Variable:**
   - After the service is created, click on it
   - Go to **"Environment"** tab (left sidebar)
   - Click **"Add Environment Variable"**
   - Key: `GOOGLE_API_KEY`
   - Value: Paste your API key from Step 1
   - Click **"Save Changes"**

4. **Deploy:**
   - Go to **"Manual Deploy"** tab
   - Click **"Deploy latest commit"**
   - Wait 5-10 minutes for build to complete

### Method 2: Manual Setup (Step-by-Step)

1. **Create a New Web Service:**
   - In Render dashboard, click **"New +"**
   - Select **"Web Service"**
   - Connect your GitHub account if prompted
   - Select your repository: `autonomous-research-assistant`
   - Click **"Connect"**

2. **Configure the Service:**
   - **Name:** `autonomous-research-assistant` (or any name you like)
   - **Region:** Choose closest to you
   - **Branch:** `main` (or `master`)
   - **Root Directory:** Leave empty (or `./` if needed)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

3. **Add Environment Variable:**
   - Scroll down to **"Environment Variables"** section
   - Click **"Add Environment Variable"**
   - Key: `GOOGLE_API_KEY`
   - Value: Your API key from Step 1
   - Click **"Add"**

4. **Choose Plan:**
   - Select **"Free"** plan (for testing)
   - Or **"Starter"** ($7/month) for always-on service

5. **Deploy:**
   - Scroll to bottom
   - Click **"Create Web Service"**
   - Wait 5-10 minutes for build

---

## Step 6: Monitor the Deployment

1. **Watch the Build Logs:**
   - You'll see build progress in real-time
   - Look for: "Build successful" or "Deployed successfully"

2. **Check for Errors:**
   - If build fails, check the logs
   - Common issues:
     - Missing dependencies → Check `requirements.txt`
     - API key not set → Add `GOOGLE_API_KEY` environment variable
     - Port issues → Make sure `$PORT` is used in start command

3. **Get Your App URL:**
   - Once deployed, you'll see: `https://your-app-name.onrender.com`
   - Click it to open your app!

---

## Step 7: Test Your Deployment

1. **Visit Your App:**
   - Go to your Render app URL
   - You should see the web interface

2. **Test Health Endpoint:**
   - Visit: `https://your-app-name.onrender.com/api/health`
   - Should return: `{"status": "healthy", "api_configured": true}`

3. **Start a Research Task:**
   - Enter a domain (or leave empty for auto-selection)
   - Click "Start Research"
   - Wait for it to complete (may take 5-15 minutes)

---

## Troubleshooting

### Build Fails

**Problem:** Build fails with dependency errors
**Solution:**
- Check `requirements.txt` has all dependencies
- Make sure Python version is correct (3.11.0)
- Check build logs for specific error

### App Crashes on Start

**Problem:** App starts but immediately crashes
**Solution:**
- Check logs in Render dashboard
- Verify `GOOGLE_API_KEY` is set correctly
- Make sure `Procfile` or start command is correct

### Research Tasks Don't Work

**Problem:** Tasks start but fail
**Solution:**
- Check API key is valid
- Verify API key has proper permissions
- Check logs for specific error messages

### App Goes to Sleep (Free Tier)

**Problem:** App takes time to respond after inactivity
**Solution:**
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Consider upgrading to Starter plan ($7/month) for always-on

---

## Important Notes

### Free Tier Limitations:
- ✅ 750 hours/month (enough for testing)
- ✅ 512MB RAM
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 30-second HTTP timeout

### For Production:
- Upgrade to Starter plan ($7/month) for always-on
- Consider adding Redis for task queues
- Add monitoring and logging
- Set up custom domain

---

## Quick Reference

**Your App URL:** `https://your-app-name.onrender.com`

**API Endpoints:**
- `GET /` - Web interface
- `GET /api/health` - Health check
- `POST /api/research/start` - Start research
- `GET /api/research/status/<task_id>` - Check status
- `GET /api/research/report/<task_id>` - Download report

**Environment Variables Needed:**
- `GOOGLE_API_KEY` (required)

---

## Need Help?

1. **Render Docs:** https://render.com/docs
2. **Render Community:** https://community.render.com
3. **Check Logs:** Render dashboard → Your service → Logs tab

---

## Summary Checklist

- [ ] Got Google Gemini API key
- [ ] Created GitHub account
- [ ] Pushed code to GitHub
- [ ] Created Render account
- [ ] Deployed web service
- [ ] Added GOOGLE_API_KEY environment variable
- [ ] Build completed successfully
- [ ] App is accessible via URL
- [ ] Tested health endpoint
- [ ] Started a research task successfully

**Congratulations! Your app is now live! 🎉**

