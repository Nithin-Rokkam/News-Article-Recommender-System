# News Article Recommender System - Docker Deployment

This guide will help you deploy the News Article Recommender System using Docker and Docker Compose.

## 🐳 Prerequisites

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Dataset**: Ensure `Dataset/result_final.csv` exists in your project directory

## 🚀 Quick Start

### Option 1: Using the Deployment Script (Recommended)

1. **Make the script executable** (Linux/Mac):
   ```bash
   chmod +x deploy.sh
   ```

2. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

### Option 2: Manual Deployment

1. **Build the Docker image**:
   ```bash
   docker-compose build
   ```

2. **Start the application**:
   ```bash
   docker-compose up -d
   ```

3. **Check the status**:
   ```bash
   docker-compose ps
   ```

## 🌐 Access the Application

Once deployed, access your application at:
- **Local**: http://localhost:5000
- **Network**: http://your-server-ip:5000

## 📋 Docker Commands

### Basic Operations

```bash
# Start the application
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Restart the application
docker-compose restart

# Check container status
docker-compose ps
```

### Development Commands

```bash
# Build without cache
docker-compose build --no-cache

# Run in foreground (see logs)
docker-compose up

# Access container shell
docker-compose exec news-recommender bash

# View container resources
docker stats
```

### Troubleshooting

```bash
# Check container logs
docker-compose logs news-recommender

# Check container health
docker-compose ps

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🏗️ Architecture

### Docker Components

1. **Base Image**: Python 3.11-slim
2. **Web Server**: Gunicorn with 2 workers
3. **Application**: Flask-based news recommender
4. **Health Checks**: Automatic monitoring
5. **Security**: Non-root user execution

### File Structure

```
News-Article-Recommender-System/
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Multi-container setup
├── .dockerignore             # Exclude files from build
├── deploy.sh                 # Automated deployment script
├── wsgi.py                   # Production WSGI entry point
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
├── static/                   # Static assets
└── Dataset/                  # News dataset (mounted as volume)
    └── result_final.csv
```

## ⚙️ Configuration

### Environment Variables

You can customize the deployment by modifying `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  # Add custom variables here
```

### Port Configuration

Default port is 5000. To change it, modify the ports section:

```yaml
ports:
  - "8080:5000"  # External:Internal
```

### Resource Limits

Add resource constraints in `docker-compose.yml`:

```yaml
services:
  news-recommender:
    # ... other config
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

## 🔧 Production Deployment

### 1. Production Dockerfile

The current Dockerfile is production-ready with:
- Gunicorn WSGI server
- Health checks
- Non-root user
- Optimized layers

### 2. Reverse Proxy Setup

For production, add a reverse proxy (nginx):

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - news-recommender
```

### 3. SSL/TLS Configuration

Add SSL certificates and configure HTTPS:

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx.key -out nginx.crt
```

## 📊 Monitoring

### Health Checks

The application includes automatic health checks:
- **Interval**: 30 seconds
- **Timeout**: 30 seconds
- **Retries**: 3 attempts
- **Start Period**: 5 seconds

### Logging

View application logs:
```bash
# Real-time logs
docker-compose logs -f news-recommender

# Last 100 lines
docker-compose logs --tail=100 news-recommender
```

### Metrics

Monitor container resources:
```bash
# Resource usage
docker stats news-recommender-app

# Container info
docker inspect news-recommender-app
```

## 🔒 Security

### Security Features

1. **Non-root user**: Application runs as `appuser`
2. **Read-only volumes**: Dataset mounted as read-only
3. **Minimal base image**: Python slim image
4. **No sensitive data**: No secrets in images

### Security Best Practices

1. **Regular updates**: Keep base images updated
2. **Vulnerability scanning**: Scan images regularly
3. **Network isolation**: Use custom networks
4. **Resource limits**: Prevent resource exhaustion

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Check what's using port 5000
   netstat -tulpn | grep :5000
   # Change port in docker-compose.yml
   ```

2. **Dataset not found**:
   ```bash
   # Ensure dataset exists
   ls -la Dataset/result_final.csv
   ```

3. **Memory issues**:
   ```bash
   # Increase memory limit
   docker-compose down
   # Edit docker-compose.yml to add memory limits
   docker-compose up -d
   ```

4. **Build failures**:
   ```bash
   # Clean build
   docker-compose down
   docker system prune -f
   docker-compose build --no-cache
   ```

### Debug Mode

For debugging, run in foreground:
```bash
docker-compose up
```

### Container Shell Access

Access the running container:
```bash
docker-compose exec news-recommender bash
```

## 📈 Scaling

### Horizontal Scaling

Scale the application:
```bash
# Scale to 3 instances
docker-compose up -d --scale news-recommender=3
```

### Load Balancing

Add a load balancer in `docker-compose.yml`:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - news-recommender
```

## 🔄 Updates

### Application Updates

1. **Pull latest code**:
   ```bash
   git pull origin main
   ```

2. **Rebuild and restart**:
   ```bash
   ./deploy.sh
   ```

### Dependency Updates

1. **Update requirements.txt**
2. **Rebuild image**:
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review container logs: `docker-compose logs`
3. Check health status: `docker-compose ps`
4. Create an issue in the repository

---

**Happy Deploying! 🚀** 