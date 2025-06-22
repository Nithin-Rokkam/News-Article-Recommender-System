# Render Deployment Guide

This guide helps you deploy the News Article Recommender System on Render and troubleshoot model loading issues.

## Key Changes Made for Render

### 1. Model Loading Fix
The main issue was that the model only loaded when running `python app.py` directly, but Render uses Gunicorn which doesn't trigger the `if __name__ == '__main__'` block.

**Solution**: Model now loads at module import time, ensuring it works with both direct execution and Gunicorn.

### 2. Added Health Check Endpoint
Visit `/health` to check if the model loaded successfully:
```bash
curl https://your-app.onrender.com/health
```

### 3. Enhanced Logging
Added comprehensive logging to track model loading progress and identify issues.

## Deployment Steps

### 1. Prepare Your Repository
Ensure your repository has these files:
- `app.py` (updated with model loading fixes)
- `wsgi.py` (simplified for Gunicorn)
- `requirements.txt`
- `render.yaml` (optional, for automatic deployment)
- `Dataset/result_final.csv` (your dataset)

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` configuration
4. Deploy will use the specified settings

#### Option B: Manual Configuration
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set these build settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Python Version**: 3.11

### 3. Environment Variables (Optional)
Set these in Render dashboard:
- `PYTHONPATH`: `.`
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `0`

## Troubleshooting Model Loading Issues

### 1. Check Health Endpoint
Visit `https://your-app.onrender.com/health` to see model status:
```json
{
  "status": "healthy",
  "message": "Model loaded successfully",
  "total_articles": 1000,
  "model_components": {
    "data": true,
    "tfidv": true,
    "nmf": true,
    "topics": true,
    "cosine_sim": true,
    "indices": true
  }
}
```

### 2. Check Render Logs
In Render dashboard, check the logs for:
- Model loading progress messages
- Error messages
- Memory usage

### 3. Common Issues and Solutions

#### Issue: "Dataset file not found"
**Solution**: Ensure `Dataset/result_final.csv` is in your repository and committed to Git.

#### Issue: Memory errors during model loading
**Solution**: 
- Upgrade to a paid Render plan with more memory
- Reduce dataset size
- Optimize the model loading process

#### Issue: Timeout during deployment
**Solution**:
- Increase build timeout in Render settings
- Optimize requirements.txt to install faster

### 4. Debugging Steps

1. **Check if dataset exists**:
   ```bash
   # In Render shell or logs
   ls -la Dataset/
   ```

2. **Check model loading logs**:
   Look for these messages in Render logs:
   ```
   INFO:__main__:Initializing model loading...
   INFO:__main__:Starting model loading...
   INFO:__main__:Loading dataset...
   INFO:__main__:Dataset loaded with X rows
   INFO:__main__:Cleaning data...
   INFO:__main__:Adding categories...
   INFO:__main__:Adding sentiment analysis...
   INFO:__main__:Adding reading time estimation...
   INFO:__main__:Creating text soup...
   INFO:__main__:Performing TF-IDF vectorization...
   INFO:__main__:Performing NMF topic modeling...
   INFO:__main__:Calculating cosine similarity...
   INFO:__main__:Creating indices mapping...
   INFO:__main__:Model loaded successfully!
   ```

3. **Test API endpoints**:
   ```bash
   # Test health endpoint
   curl https://your-app.onrender.com/health
   
   # Test articles endpoint
   curl https://your-app.onrender.com/api/articles
   ```

## Performance Optimization

### 1. Dataset Optimization
- Remove unnecessary columns
- Reduce text length for faster processing
- Consider using a smaller subset for testing

### 2. Model Optimization
- Reduce NMF components (currently 20)
- Use more efficient vectorization settings
- Consider pre-computing similarity matrix

### 3. Render Plan Considerations
- **Free Plan**: Limited memory (512MB), may timeout
- **Starter Plan**: 1GB RAM, better for ML models
- **Standard Plan**: 2GB+ RAM, recommended for production

## Alternative Deployment Options

### 1. Use Docker on Render
If you continue having issues, use the Docker approach:
```dockerfile
# Use the updated Dockerfile with python:3.11-slim
FROM python:3.11-slim
# ... rest of Dockerfile
```

### 2. Pre-compute Model
For very large datasets, consider pre-computing the model and saving it as a pickle file:
```python
import pickle

# Save model components
with open('model_components.pkl', 'wb') as f:
    pickle.dump({
        'tfidv': tfidv,
        'nmf': nmf,
        'topics': topics,
        'cosine_sim': cosine_sim,
        'indices': indices,
        'data': data
    }, f)
```

## Monitoring and Maintenance

### 1. Set up Monitoring
- Use Render's built-in monitoring
- Set up alerts for health check failures
- Monitor memory usage

### 2. Regular Updates
- Keep dependencies updated
- Monitor for security patches
- Test model performance regularly

## Support

If you continue having issues:
1. Check Render's documentation: https://render.com/docs
2. Review the logs in Render dashboard
3. Test locally with the same environment
4. Consider using Render's support for paid plans 