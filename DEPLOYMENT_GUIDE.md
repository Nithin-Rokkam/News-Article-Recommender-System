# 🚀 Vercel Deployment Guide for News Article Recommender System

## ✅ Your Project is Ready!

Your News Article Recommender System has been prepared for Vercel deployment with all necessary configuration files.

## 📋 Prerequisites

- GitHub account
- Vercel account (free)
- Your code pushed to GitHub

## 🎯 Step-by-Step Deployment

### Step 1: Push to GitHub (if not already done)

```bash
# If you haven't created a GitHub repository yet:
# 1. Go to github.com and create a new repository
# 2. Then run these commands:

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy to Vercel

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up/Login** with your GitHub account
3. **Click "New Project"**
4. **Import your GitHub repository**
5. **Configure the project settings**:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`
6. **Click "Deploy"**

### Step 3: Wait for Deployment

- Vercel will automatically:
  - Install Python dependencies
  - Build your Flask application
  - Deploy to a live URL
- This usually takes 2-5 minutes

### Step 4: Access Your App

- Once deployment is complete, you'll get a URL like:
  - `https://your-project-name.vercel.app`
- Click the URL to access your live application!

## 🔧 Configuration Files Created

Your project now includes these Vercel-specific files:

- `vercel.json` - Vercel configuration
- `runtime.txt` - Python version specification
- `.vercelignore` - Files to exclude from deployment
- `requirements.txt` - Python dependencies

## 🚨 Important Notes

### Dataset Size
- Your dataset (`Dataset/result_final.csv`) will be included in the deployment
- Large datasets may slow down deployment and cold starts
- Consider dataset optimization for better performance

### Cold Start Performance
- First request may take 30-60 seconds (model loading)
- Subsequent requests will be faster
- Consider upgrading to Vercel Pro for better performance

### Memory Limitations
- Free tier has memory limitations
- If you encounter memory issues, consider:
  - Reducing dataset size
  - Optimizing model loading
  - Upgrading to Vercel Pro

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check build logs in Vercel dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **Import Errors**
   - Make sure all packages are listed in `requirements.txt`
   - Check for version conflicts

3. **File Not Found**
   - Ensure `Dataset/result_final.csv` is included in your repository
   - Check file paths in your code

4. **Memory Issues**
   - Consider reducing dataset size
   - Optimize model loading
   - Upgrade to Vercel Pro

### Performance Tips:

1. **Optimize Dataset**
   - Consider using a smaller sample for faster loading
   - Implement data compression if possible

2. **Caching**
   - Implement caching for better performance
   - Use Vercel's edge caching features

3. **Monitoring**
   - Check Vercel analytics for performance insights
   - Monitor function execution times

## 🔄 Automatic Deployments

Once deployed, Vercel will automatically:
- Deploy new versions when you push to GitHub
- Provide preview deployments for pull requests
- Handle rollbacks if needed

## 📊 Monitoring Your App

- **Vercel Dashboard**: Monitor deployments, performance, and errors
- **Function Logs**: Check serverless function execution logs
- **Analytics**: Track usage and performance metrics

## 🆘 Support

If you encounter issues:

1. **Check Vercel Documentation**: https://vercel.com/docs
2. **Python Runtime Guide**: https://vercel.com/docs/runtimes#official-runtimes/python
3. **Flask Deployment Guide**: https://vercel.com/guides/deploying-flask-with-vercel
4. **Vercel Community**: https://github.com/vercel/vercel/discussions

## 🎉 Success!

Once deployed, your News Article Recommender System will be:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Automatically updated on code changes
- ✅ Scalable and reliable

---

**Happy Deploying! 🚀**

Your Flask application is now ready to go live on Vercel! 