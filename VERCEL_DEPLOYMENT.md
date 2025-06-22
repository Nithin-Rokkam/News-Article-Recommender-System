# Vercel Deployment Guide

This guide helps you deploy the News Article Recommender System on Vercel and explains the necessary configuration changes.

## Why Vercel?

Vercel is a platform for frontend frameworks and static sites, but it can also host serverless functions, which is how we'll run the Python backend.

## Key Changes for Vercel Deployment

### 1. Project Structure
Vercel expects serverless functions to be in an `api` directory.
- Your Flask application was moved from `app.py` to `api/index.py`.

### 2. Vercel Configuration (`vercel.json`)
A `vercel.json` file was added to tell Vercel how to handle the project:
- **`builds`**: This section tells Vercel that `api/index.py` is a Python serverless function.
- **`routes`**: This rewrites all incoming requests (`/(.*)`) to be handled by your Flask app (`api/index.py`). Your Flask app's internal routing will then take over.

## Deployment Steps

### 1. Push Changes to GitHub
Commit and push the following new and modified files to your GitHub repository:
- `api/index.py` (your renamed app)
- `vercel.json` (the new Vercel configuration)
- `VERCEL_DEPLOYMENT.md` (this file)

### 2. Import Project on Vercel
1.  Log in to your Vercel account.
2.  Click **Add New...** > **Project**.
3.  Import the GitHub repository containing your project.

### 3. Configure the Project
Vercel should automatically detect that this is a Python project because of the `vercel.json` and `requirements.txt` file.

- **Framework Preset**: Vercel might detect "Other". This is fine.
- **Build & Development Settings**: You can leave these as default. Vercel will use the `vercel.json` file for build configuration.
- **Root Directory**: Should be left as the default (root of your project).

### 4. Add Environment Variables (Optional but Recommended)
In your Vercel project settings under **Environment Variables**, you can add:
- `FLASK_ENV`: `production`

### 5. Deploy
Click the **Deploy** button. Vercel will now build and deploy your application.

## Troubleshooting

### "Not Found" on the main page
If your main page shows a 404 error, it might be an issue with Flask finding the templates. The current setup should work, but if it fails, the `Flask` app initialization in `api/index.py` may need to be changed to:
```python
# In api/index.py
app = Flask(__name__, template_folder='templates', static_folder='static')
```
This explicitly tells Flask where to find the `templates` and `static` folders relative to the project root.

### Memory and Timeout Issues
Vercel's Hobby plan has generous limits (1GB memory, 10s timeout), which should be sufficient for the optimized model. If you experience timeouts:
-  Ensure your model loading is as fast as possible.
-  Consider upgrading to a Pro plan for longer execution times if needed.

### Check Deployment Logs
If deployment fails, always check the **Logs** tab in your Vercel project dashboard for detailed error messages. This will show output from the `pip install` process and any errors from your Python code during startup. 