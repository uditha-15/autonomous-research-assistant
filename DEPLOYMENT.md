# Deployment Guide for Render

This guide will help you deploy the Autonomous Research Assistant to Render.

## Prerequisites

1. A Render account (sign up at [render.com](https://render.com))
2. A Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))
3. A GitHub account (optional, but recommended)

## Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the service:**
   - **Name**: `autonomous-research-assistant` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

4. **Add Environment Variables:**
   - Click "Environment" tab
   - Add: `GOOGLE_API_KEY` = `your_api_key_here`
   - Add: `PYTHON_VERSION` = `3.11.0` (optional)

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

### Option 2: Deploy using Render.yaml

1. **Push code to GitHub** (same as above)

2. **Create a Blueprint:**
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and configure everything

3. **Add Environment Variables:**
   - In the service settings, add `GOOGLE_API_KEY`

### Option 3: Manual Deploy

1. **Create a new Web Service:**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect via GitHub or use "Public Git repository"

2. **Configure settings:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

3. **Environment Variables:**
   - `GOOGLE_API_KEY`: Your Gemini API key
   - `PYTHON_VERSION`: `3.11.0` (optional)

## Important Configuration

### Environment Variables

Make sure to set these in Render:
- `GOOGLE_API_KEY`: Required - Your Google Gemini API key
- `PORT`: Automatically set by Render (don't override)

### Build Settings

- **Python Version**: 3.11.0 (specified in `runtime.txt`)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`

### Timeout Settings

Research tasks can take 5-15 minutes. Render free tier has a 30-second timeout for HTTP requests, but background tasks will continue. Consider:
- Using Render's background workers for long tasks
- Implementing async task queues (Redis, etc.)
- Upgrading to paid plan for longer timeouts

## Post-Deployment

1. **Test the deployment:**
   - Visit your app URL
   - Check `/api/health` endpoint
   - Try starting a research task

2. **Monitor logs:**
   - Go to "Logs" tab in Render dashboard
   - Watch for any errors or warnings

3. **Set up custom domain** (optional):
   - Go to "Settings" → "Custom Domains"
   - Add your domain

## Troubleshooting

### Build Fails

- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility
- Check build logs for specific errors

### App Crashes on Start

- Verify `GOOGLE_API_KEY` is set correctly
- Check that all required directories exist
- Review error logs in Render dashboard

### Research Tasks Timeout

- Research runs in background threads
- HTTP requests may timeout, but task continues
- Check task status via `/api/research/status/<task_id>`
- Consider implementing proper task queue (Celery, etc.)

### Memory Issues

- Render free tier has limited memory
- Consider reducing number of workers
- Optimize Chroma database usage
- Upgrade to paid plan if needed

## Scaling Considerations

For production use:
1. **Use Background Workers**: Deploy separate worker service for research tasks
2. **Add Redis**: For task queue management
3. **Database**: Consider PostgreSQL for task persistence
4. **Monitoring**: Add logging and monitoring (Sentry, etc.)
5. **Caching**: Cache frequently accessed data

## Security Notes

- Never commit `.env` file or API keys to Git
- Use Render's environment variables for secrets
- Enable HTTPS (automatic on Render)
- Consider rate limiting for API endpoints
- Add authentication if needed

## Cost Estimation

- **Free Tier**: 
  - 750 hours/month
  - 512MB RAM
  - Sleeps after 15 min inactivity
  
- **Starter Plan** ($7/month):
  - Always on
  - 512MB RAM
  - Better for production

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Project Issues: Open an issue on GitHub

