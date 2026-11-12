
pipeline {
    agent any

    // AUTOMATIC TRIGGERS
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

        // STEP 1: CHECKOUT
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Marouazzz/Jenkins-CI-CD.git',
                    credentialsId: 'github-token2'
            }
        }

    stage('Setup Virtual Environment') {
        steps {
            sh '''
                python3 --version
                python3 -m venv .venv
                . .venv/bin/activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
            '''
        }
    }

        // STEP 3: RUN TESTS
        stage('Run Tests') {
            when {
                not {
                    changeset "README.md"
                }
            }

            parallel {
                stage('Test File 1') {
                    steps {
                        bat """
                            call %VENV_DIR%\\Scripts\\activate
                            python -m pytest test_app.py -v
                        """
                    }
                }

                stage('Test File 2') {
                    steps {
                        bat """
                            call %VENV_DIR%\\Scripts\\activate
                            python -m pytest test_app_2.py -v
                        """
                    }
                }
            }
        }

        // STEP 4: DEPLOY
        stage('Deploy (Local with Gunicorn)') {
            steps {
                echo 'Starting Flask app locally using Gunicorn...'

                bat """
                    call %VENV_DIR%\\Scripts\\activate
                    start /B gunicorn --bind %HOST%:%PORT% %APP_MODULE% > gunicorn.log 2>&1
                    echo Gunicorn started on http://%HOST%:%PORT%
                """
            }
        }
    }

    // EMAIL NOTIFICATIONS
    post {
        success {
            emailext(
                to: "EMAIL_TO_PLACEHOLDER",
                from: "EMAIL_FROM_PLACEHOLDER",
                replyTo: "EMAIL_REPLY_PLACEHOLDER",
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                mimeType: 'text/html',
                body: """
                    <p>Good news!</p>
                    <p>Build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> succeeded.</p>
                    <p>Check details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """
            )
        }

        failure {
            emailext(
                to: "EMAIL_TO_PLACEHOLDER",
                from: "EMAIL_FROM_PLACEHOLDER",
                replyTo: "EMAIL_REPLY_PLACEHOLDER",
                subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                mimeType: 'text/html',
                body: """
                    <p>Uh oh...</p>
                    <p>Build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> failed.</p>
                    <p>Check logs: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                """
            )
        }
    }
}
