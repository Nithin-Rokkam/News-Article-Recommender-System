# 🐳 Docker Deployment Guide for News Article Recommender System

## ✅ Vercel Files Removed, Docker Setup Complete!

All Vercel-specific files have been deleted and replaced with Docker configuration.

## 📁 Files Created:

- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Exclude unnecessary files
- `DOCKER_DEPLOYMENT.md` - This guide

## 🚀 Quick Start with Docker Compose (Recommended)

### Prerequisites:
- Docker installed
- Docker Compose installed
- Git repository with your code

### Step 1: Build and Run
```bash
# Build and start the application
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### Step 2: Access Your Application
- Open browser and go to: `http://localhost:5000`
- Your News Article Recommender System is now running!

### Step 3: Stop the Application
```bash
# Stop the containers
docker-compose down

# Stop and remove volumes (if needed)
docker-compose down -v
```

## 🔧 Manual Docker Commands

### Build the Image
```bash
docker build -t news-recommender .
```

### Run the Container
```bash
docker run -p 5000:5000 -v $(pwd)/Dataset:/app/Dataset news-recommender
```

### Run in Background
```bash
docker run -d -p 5000:5000 -v $(pwd)/Dataset:/app/Dataset --name news-app news-recommender
```

## 📊 Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build

# View running containers
docker-compose ps
```

## 🛠️ Configuration Options

### Environment Variables
You can modify `docker-compose.yml` to add environment variables:

```yaml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  - DATASET_PATH=/app/Dataset/result_final.csv
```

### Port Configuration
Change the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Host port 8080, container port 5000
```

### Volume Mounts
The current setup mounts:
- `./Dataset` → `/app/Dataset` (your data)
- `./templates` → `/app/templates` (HTML templates)

## 🔍 Monitoring and Debugging

### View Container Logs
```bash
# All containers
docker-compose logs

# Specific service
docker-compose logs news-recommender

# Follow logs
docker-compose logs -f
```

### Access Container Shell
```bash
# Interactive shell
docker-compose exec news-recommender bash

# Or with docker run
docker exec -it news-app bash
```

### Health Check
The application includes a health check endpoint:
- URL: `http://localhost:5000/api/health`
- Returns: Application status and model loading info

## 🚨 Troubleshooting

### Common Issues:

1. **Port Already in Use**
   ```bash
   # Check what's using port 5000
   netstat -tulpn | grep :5000
   
   # Change port in docker-compose.yml
   ports:
     - "8080:5000"
   ```

2. **Permission Issues**
   ```bash
   # Fix file permissions
   chmod -R 755 Dataset/
   chmod -R 755 templates/
   ```

3. **Build Failures**
   ```bash
   # Clean build
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

4. **Memory Issues**
   ```bash
   # Increase Docker memory limit
   # In Docker Desktop settings
   ```

### Performance Optimization:

1. **Multi-stage Build** (for production)
2. **Caching** (already implemented)
3. **Resource Limits** (add to docker-compose.yml)

## 🌐 Production Deployment

### Using Docker Compose in Production:
```bash
# Production build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# With environment file
docker-compose --env-file .env.prod up -d
```

### Using Docker Swarm:
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml news-recommender
```

### Using Kubernetes:
- Create Kubernetes manifests
- Deploy to your cluster
- Use ingress for external access

## 📈 Scaling

### Horizontal Scaling:
```bash
# Scale to multiple instances
docker-compose up --scale news-recommender=3
```

### Load Balancing:
- Use nginx reverse proxy
- Configure Docker Swarm
- Use Kubernetes ingress

## 🔒 Security Best Practices

1. **Non-root User**: Already configured in Dockerfile
2. **Minimal Base Image**: Using python:3.9-slim
3. **No Secrets in Images**: Use environment variables
4. **Regular Updates**: Keep base images updated

## 📝 Maintenance

### Update Dependencies:
```bash
# Rebuild with new requirements
docker-compose up --build
```

### Backup Data:
```bash
# Backup dataset
docker cp news-app:/app/Dataset ./backup/
```

### Cleanup:
```bash
# Remove unused containers/images
docker system prune -f

# Remove all containers/images
docker system prune -a
```

---

## 🎉 Success!

Your News Article Recommender System is now containerized and ready for deployment!

### Quick Commands Summary:
```bash
# Start: docker-compose up --build
# Stop:  docker-compose down
# Logs:  docker-compose logs -f
# Shell: docker-compose exec news-recommender bash
```

**Happy Containerizing! 🐳** 