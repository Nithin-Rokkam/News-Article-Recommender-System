# 🚀 Jenkins Pipeline Setup Guide for News Article Recommender System

## 📋 Prerequisites

### 1. Jenkins Installation
- Jenkins server running (local or cloud)
- Docker installed on Jenkins server
- Git repository with your code

### 2. Required Jenkins Plugins
Install these plugins in Jenkins:
- **Pipeline** (usually pre-installed)
- **Docker Pipeline**
- **Git Integration**
- **Workspace Cleanup**

## 🛠️ Jenkins Server Setup

### Step 1: Install Required Tools on Jenkins Server

```bash
# Install Docker (if not already installed)
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Install curl for health checks
sudo apt-get install curl
```

### Step 2: Verify Docker Access
```bash
# Test if Jenkins can run Docker
sudo -u jenkins docker --version
sudo -u jenkins docker ps
```

## 📁 Project Setup

### Step 1: Push Code to Git Repository
```bash
git add .
git commit -m "Add Jenkins pipeline configuration"
git push origin main
```

### Step 2: Verify Files in Repository
Ensure these files are in your repository:
- `Jenkinsfile` (or `Jenkinsfile-simple`)
- `Dockerfile`
- `requirements.txt`
- `app.py`
- `Dataset/` folder
- `templates/` folder

## 🎯 Jenkins Pipeline Configuration

### Method 1: Using Jenkinsfile (Recommended)

1. **Go to Jenkins Dashboard**
2. **Click "New Item"**
3. **Enter name**: `news-recommender-pipeline`
4. **Select "Pipeline"**
5. **Click "OK"**

### Configure Pipeline:

#### General Settings:
- ✅ **Discard old builds**: Keep 10 builds
- ✅ **GitHub project**: `https://github.com/YOUR_USERNAME/YOUR_REPO`

#### Pipeline Definition:
- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: `https://github.com/YOUR_USERNAME/YOUR_REPO.git`
- **Credentials**: Add your Git credentials if private repo
- **Branch Specifier**: `*/main`
- **Script Path**: `Jenkinsfile`

#### Build Triggers:
- ✅ **Poll SCM**: `H/5 * * * *` (every 5 minutes)
- ✅ **GitHub hook trigger for GITScm polling** (if using GitHub)

### Method 2: Using Jenkinsfile-simple (Easier)

Use `Jenkinsfile-simple` for a basic setup:
- **Script Path**: `Jenkinsfile-simple`

## 🔧 Pipeline Stages Explained

### 1. **Checkout Stage**
- Clones your Git repository
- Downloads all project files

### 2. **Build Docker Image Stage**
- Builds the Docker image using your Dockerfile
- Creates `news-recommender:latest` image

### 3. **Deploy Stage**
- Stops any existing container
- Runs new container with your application
- Maps port 5000 and volumes

### 4. **Health Check Stage**
- Waits for application to start
- Tests the health endpoint
- Verifies deployment success

## 🚀 Running the Pipeline

### Step 1: Build Now
1. Go to your pipeline in Jenkins
2. Click **"Build Now"**
3. Watch the build progress

### Step 2: Monitor Build
- Click on the build number
- Click **"Console Output"** to see logs
- Monitor each stage progress

### Step 3: Access Application
After successful build:
- **URL**: `http://JENKINS_SERVER_IP:5000`
- **Health Check**: `http://JENKINS_SERVER_IP:5000/api/health`

## 🔍 Troubleshooting

### Common Issues:

#### 1. **Docker Permission Denied**
```bash
# Fix Docker permissions
sudo chmod 666 /var/run/docker.sock
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### 2. **Port Already in Use**
```bash
# Check what's using port 5000
sudo netstat -tulpn | grep :5000

# Kill process or change port in Jenkinsfile
```

#### 3. **Build Fails**
- Check Jenkins console output
- Verify all files are in repository
- Check Docker build logs

#### 4. **Health Check Fails**
- Increase sleep time in Jenkinsfile
- Check container logs: `docker logs news-app`
- Verify application is starting properly

### Debugging Commands:
```bash
# Check Jenkins workspace
ls /var/lib/jenkins/workspace/news-recommender-pipeline/

# Check Docker containers
docker ps -a

# Check Docker images
docker images

# View container logs
docker logs news-app

# Access container shell
docker exec -it news-app bash
```

## 📊 Pipeline Monitoring

### Build History:
- View all builds in Jenkins dashboard
- Check build duration and status
- Review console output for each build

### Application Monitoring:
- **Health Endpoint**: `/api/health`
- **Articles Endpoint**: `/api/articles`
- **Main Page**: `/`

## 🔄 Continuous Deployment

### Automatic Triggers:
1. **Poll SCM**: Checks for changes every 5 minutes
2. **Webhook**: Triggers on Git push (GitHub integration)
3. **Manual**: Build when needed

### Branch Strategy:
- **Main branch**: Production deployment
- **Feature branches**: Development testing
- **Pull requests**: Code review and testing

## 🛡️ Security Considerations

### Docker Security:
- Run containers as non-root user (already configured)
- Use specific image tags instead of `latest`
- Regular security scans

### Jenkins Security:
- Use Jenkins credentials for sensitive data
- Restrict pipeline permissions
- Regular Jenkins updates

## 📈 Advanced Features

### 1. **Multi-Environment Deployment**
```groovy
environment {
    ENV = 'production'  // or 'staging', 'development'
}
```

### 2. **Slack Notifications**
```groovy
post {
    success {
        slackSend channel: '#deployments', 
                  color: 'good', 
                  message: 'Deployment successful!'
    }
    failure {
        slackSend channel: '#deployments', 
                  color: 'danger', 
                  message: 'Deployment failed!'
    }
}
```

### 3. **Artifact Archiving**
```groovy
post {
    always {
        archiveArtifacts artifacts: '**/logs/*.log', fingerprint: true
    }
}
```

## 🎉 Success Checklist

- ✅ Jenkins server running
- ✅ Docker installed and accessible
- ✅ Git repository configured
- ✅ Pipeline created and configured
- ✅ First build successful
- ✅ Application accessible
- ✅ Health checks passing
- ✅ Automatic deployment working

---

## 📞 Support

If you encounter issues:
1. Check Jenkins console output
2. Verify Docker permissions
3. Check container logs
4. Review this guide
5. Check Jenkins documentation

**Happy CI/CD! 🚀** 