#!/bin/bash

# News Article Recommender System - Docker Deployment Script

echo "🚀 Starting News Article Recommender System Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if dataset exists
if [ ! -f "Dataset/result_final.csv" ]; then
    echo "❌ Dataset not found at Dataset/result_final.csv"
    echo "Please ensure your dataset is in the correct location."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build --no-cache

# Start the application
echo "🚀 Starting the application..."
docker-compose up -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 Access your application at: http://localhost:5000"
    echo "📊 Health check: http://localhost:5000/"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "📋 Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop app: docker-compose down"
echo "  Restart app: docker-compose restart"
echo "  Update app: ./deploy.sh"
echo ""
echo "🎉 Deployment completed successfully!" 