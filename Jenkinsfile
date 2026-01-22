pipeline {
    agent any

    environment {
        IMAGE_NAME = "xl-analysis-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/harishkemkar/XL_Analysis.git',
                    credentialsId: '2baaf92a-12d5-4b7a-b4f9-064db044058a'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q || true'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh '''
                        docker rm -f xl-analysis-app || true
                        docker run -d -p 5000:5000 --name xl-analysis-app xl-analysis-app:${BUILD_NUMBER}
                    '''
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