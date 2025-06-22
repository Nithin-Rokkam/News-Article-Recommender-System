@echo off
echo 🚀 Starting News Article Recommender System Deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Check if dataset exists
if not exist "Dataset\result_final.csv" (
    echo ❌ Dataset not found at Dataset\result_final.csv
    echo Please ensure your dataset is in the correct location.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose down

REM Build the Docker image
echo 🔨 Building Docker image...
docker-compose build --no-cache

REM Start the application
echo 🚀 Starting the application...
docker-compose up -d

REM Wait for the application to start
echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Check if the application is running
echo 🔍 Checking application status...
docker-compose ps

echo.
echo 📋 Useful commands:
echo   View logs: docker-compose logs -f
echo   Stop app: docker-compose down
echo   Restart app: docker-compose restart
echo   Update app: deploy.bat
echo.
echo 🌐 Access your application at: http://localhost:5000
echo.
echo 🎉 Deployment completed successfully!
pause 