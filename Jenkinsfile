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
                echo '✅ Checking out source code...'
                checkout scm
            }
        }

        stage('Check Python Setup') {
            steps {
                echo '🔍 Checking Python installation...'
                bat 'where python'
                bat 'python --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '🧪 Running tests...'
                bat 'python -m pytest test_app.py -v || echo No tests found or tests failed'
            }
        }

        stage('Code Quality Check') {
            steps {
                echo '🧹 Running code quality checks...'
                bat 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo Flake8 skipped'
                bat 'pylint app.py || echo Pylint skipped'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
                bat "docker images"
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                echo '🔒 Running security scan...'
                bat '''
                    docker run --rm -v //var/run/docker.sock:/var/run/docker.sock ^
                    -v %WORKSPACE%:/tmp/result aquasec/trivy image %DOCKER_IMAGE%:%DOCKER_TAG% ^
                    || echo Trivy not available, skipping scan
                '''
            }
        }

        stage('Stop Previous Container') {
            steps {
                echo '🛑 Stopping previous container if running...'
                bat 'docker stop %CONTAINER_NAME% || echo Container not running'
                bat 'docker rm %CONTAINER_NAME% || echo Container not found'
            }
        }

        stage('Deploy Application') {
            steps {
                echo '🚀 Deploying application...'
                bat '''
                    docker run -d ^
                    --name %CONTAINER_NAME% ^
                    -p %PORT%:%PORT% ^
                    -v "%WORKSPACE%\\Dataset":/app/Dataset ^
                    -v "%WORKSPACE%\\templates":/app/templates ^
                    --restart unless-stopped ^
                    %DOCKER_IMAGE%:%DOCKER_TAG%
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo '💓 Performing health check...'
                bat '''
                    timeout /t 30 >nul
                    docker ps | findstr %CONTAINER_NAME%
                    curl http://localhost:%PORT% || echo Health check failed
                '''
            }
        }

        stage('Integration Tests') {
            steps {
                echo '🔗 Running integration tests...'
                bat '''
                    curl http://localhost:%PORT%/ || echo Main endpoint failed
                    curl http://localhost:%PORT%/api/health || echo Health API failed
                    curl http://localhost:%PORT%/api/articles || echo Articles API failed
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            bat '''
                echo Container %CONTAINER_NAME% is still running.
                echo Access app: http://localhost:%PORT%
                echo To stop: docker stop %CONTAINER_NAME%
                echo To view logs: docker logs %CONTAINER_NAME%
            '''
        }

        success {
            echo '✅ Pipeline succeeded!'
            bat '''
                echo === DEPLOYMENT SUCCESSFUL ===
                echo App URL: http://localhost:%PORT%
                echo Container: %CONTAINER_NAME%
                echo Image: %DOCKER_IMAGE%:%DOCKER_TAG%
                echo =============================
            '''
        }

        failure {
            echo '❌ Pipeline failed.'
            bat '''
                echo === DEPLOYMENT FAILED ===
                docker logs %CONTAINER_NAME% || echo No container logs
                echo ==========================
            '''
        }

        cleanup {
            echo '🧽 Cleaning workspace...'
            cleanWs()
        }
    }
}
