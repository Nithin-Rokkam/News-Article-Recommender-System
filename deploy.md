# Vercel Deployment Guide

## Step 1: Prepare Your GitHub Repository

1. **Create a GitHub repository** (if you haven't already)
2. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Step 2: Deploy via Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Import your GitHub repository**
5. **Configure the project**:
   - Framework Preset: Other
   - Root Directory: `./` (leave as default)
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`
6. **Click "Deploy"**

## Step 3: Environment Variables (if needed)

If your app needs environment variables:
1. Go to your project dashboard in Vercel
2. Click "Settings" → "Environment Variables"
3. Add any required variables

## Step 4: Custom Domain (Optional)

1. In your Vercel project dashboard
2. Go to "Settings" → "Domains"
3. Add your custom domain

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check the build logs in Vercel dashboard
2. **Import Errors**: Make sure all dependencies are in `requirements.txt`
3. **File Not Found**: Ensure your dataset file is included in the repository
4. **Memory Issues**: The free tier has limitations, consider upgrading

### Performance Tips:

1. **Optimize your dataset**: Consider reducing the size for faster loading
2. **Use caching**: Implement caching for better performance
3. **Monitor usage**: Check Vercel analytics for performance insights

## Alternative: Deploy via Git Integration

1. **Connect your GitHub repo to Vercel**
2. **Enable automatic deployments**
3. **Every push to main branch will trigger a new deployment**

## Support

- Vercel Documentation: https://vercel.com/docs
- Python Runtime: https://vercel.com/docs/runtimes#official-runtimes/python
- Flask Deployment: https://vercel.com/guides/deploying-flask-with-vercel 