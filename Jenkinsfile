pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/XL_Analysis.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("xl-analysis-app:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker run -d -p 5000:5000 --name xl-analysis-app-${env.BUILD_NUMBER} xl-analysis-app:${env.BUILD_NUMBER}
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}