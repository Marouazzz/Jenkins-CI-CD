
pipeline {
    agent any

    triggers {
        cron('H/5 * * * *')
        githubPush()
    }

    environment {
        VENV_DIR = ".venv"
        HOST = "0.0.0.0"
        PORT = "5000"
        APP_MODULE = "app:app"
    }

    stages {

        stage('Setup Virtual Environment') {
            steps {
                echo 'Setting up Python virtual environment...'

                sh '''
                    python3 --version
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            when {
                not {
                    changeset "README.md"
                }
            }

            parallel {
                stage('Test File 1') {
                    steps {
                        echo 'Running tests from test_app.py'

                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -m pytest test_app.py -v
                        '''
                    }
                }

                stage('Test File 2') {
                    steps {
                        echo 'Running tests from test_app_2.py'

                        sh '''
                            . ${VENV_DIR}/bin/activate
                            python -m pytest test_app_2.py -v
                        '''
                    }
                }
            }
        }

        stage('Deploy (Local with Gunicorn)') {
            steps {
                echo 'Starting Flask application using Gunicorn...'

                sh '''
                    . ${VENV_DIR}/bin/activate

                    nohup gunicorn \
                        --bind ${HOST}:${PORT} \
                        ${APP_MODULE} \
                        > gunicorn.log 2>&1 &

                    echo "Gunicorn started on port ${PORT}"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
            echo "Build URL: ${BUILD_URL}"
        }

        failure {
            echo 'Pipeline failed!'
            echo "Build URL: ${BUILD_URL}"
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
