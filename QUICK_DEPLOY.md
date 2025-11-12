# 🚀 Quick Deploy Guide - 5 Minutes

## Step 1: Get API Key (2 minutes)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. **Copy and save your key** (looks like: `AIzaSy...`)

## Step 2: Upload to GitHub (2 minutes)

### Easy Way (Web Interface):
1. Go to: https://github.com/new
2. Repository name: `autonomous-research-assistant`
3. Choose **Public**
4. Click "Create repository"
5. Click "uploading an existing file"
6. **Drag ALL files** from your folder into GitHub
7. Scroll down, type "Initial commit", click "Commit changes"

## Step 3: Deploy on Render (1 minute)

1. Go to: https://render.com
2. Sign up with GitHub (click "Sign up with GitHub")
3. Click **"New +"** → **"Blueprint"**
4. Select your repository: `autonomous-research-assistant`
5. Click **"Apply"**
6. In the service settings:
   - Go to **"Environment"** tab
   - Click **"Add Environment Variable"**
   - Key: `GOOGLE_API_KEY`
   - Value: Paste your API key from Step 1
   - Click **"Save Changes"**
7. Wait 5-10 minutes for build
8. **Done!** Your app will be at: `https://your-app-name.onrender.com`

---

## That's It! 🎉

Your app is now live. Visit the URL and start researching!

**Need more details?** See [HOSTING_GUIDE.md](HOSTING_GUIDE.md)

