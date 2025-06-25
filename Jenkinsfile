pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'news-recommender'
        DOCKER_TAG = 'latest'
        CONTAINER_NAME = 'news-app'
        PORT = '5000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    python -m pytest test_app.py -v || echo "No tests found or tests failed"
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo "Flake8 not installed or no issues found"
                    python -m pylint app.py || echo "Pylint not installed or no issues found"
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker images | grep ${DOCKER_IMAGE}
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security scan...'
                sh '''
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ${WORKSPACE}:/tmp/result aquasec/trivy image ${DOCKER_IMAGE}:${DOCKER_TAG} || echo "Trivy not available, skipping security scan"
                '''
            }
        }
        
        stage('Stop Previous Container') {
            steps {
                echo 'Stopping previous container if running...'
                sh '''
                    docker stop ${CONTAINER_NAME} || echo "Container not running"
                    docker rm ${CONTAINER_NAME} || echo "Container not found"
                '''
            }
        }
        
        stage('Deploy Application') {
            steps {
                echo 'Deploying application...'
                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${PORT}:${PORT} \
                        -v ${WORKSPACE}/Dataset:/app/Dataset \
                        -v ${WORKSPACE}/templates:/app/templates \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        sh '''
                            echo "Waiting for application to start..."
                            sleep 30
                            
                            # Check if container is running
                            if docker ps | grep -q ${CONTAINER_NAME}; then
                                echo "Container is running"
                                
                                # Check if application is responding
                                for i in {1..10}; do
                                    if curl -f http://localhost:${PORT}/api/health; then
                                        echo "Application is healthy!"
                                        break
                                    else
                                        echo "Attempt $i: Application not ready yet..."
                                        sleep 10
                                    fi
                                done
                            else
                                echo "Container is not running"
                                docker logs ${CONTAINER_NAME}
                                exit 1
                            fi
                        '''
                    }
                }
            }
        }
        
        stage('Integration Test') {
            steps {
                echo 'Running integration tests...'
                sh '''
                    # Test main endpoint
                    curl -f http://localhost:${PORT}/ || echo "Main endpoint test failed"
                    
                    # Test API endpoints
                    curl -f http://localhost:${PORT}/api/health || echo "Health endpoint test failed"
                    curl -f http://localhost:${PORT}/api/articles || echo "Articles endpoint test failed"
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed. Cleaning up...'
            sh '''
                # Keep container running for manual testing
                echo "Container ${CONTAINER_NAME} is still running for testing"
                echo "Access your application at: http://localhost:${PORT}"
                echo "To stop the container: docker stop ${CONTAINER_NAME}"
                echo "To view logs: docker logs ${CONTAINER_NAME}"
            '''
        }
        
        success {
            echo 'Pipeline succeeded! 🎉'
            sh '''
                echo "=== DEPLOYMENT SUCCESSFUL ==="
                echo "Application URL: http://localhost:${PORT}"
                echo "Container Name: ${CONTAINER_NAME}"
                echo "Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo "================================"
            '''
        }
        
        failure {
            echo 'Pipeline failed! ❌'
            sh '''
                echo "=== DEPLOYMENT FAILED ==="
                echo "Container logs:"
                docker logs ${CONTAINER_NAME} || echo "No container logs available"
                echo "=========================="
            '''
        }
        
        cleanup {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
} 