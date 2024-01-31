pipeline {
    agent any

    stages {
        stage('Checkout Pipeline Repo') {
            steps {
                git 'https://github.com/HoshEnder/pipeline.git'
            }
        }

        stage('Initial Setup') {
            steps {
                script {
                    sh 'cd dev-vagrant && vagrant up'
                    sh 'cd preprod-vagrant && vagrant up'
                }
            }
        }

        stage('Setup Application in Dev/QA Environment') {
            steps {
                script {
                    // Utiliser le script pour se connecter à la VM dev-qa-box et cloner le dépôt
                    sh 'AUTO_ACCEPT_SSH_KEY=true ./vagrant_cnx.sh dev-qa-box "git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'

                    // Sortir de la VM
                    sh 'exit'

                    // Copier le fichier tests.py vers l'environnement Dev/QA
                    sh 'cd dev-vagrant && vagrant scp tests.py dev-qa-box:/app'
                }
            }
        }

        stage('Build and Unit Test in Dev/QA') {
            steps {
                script {
                    // Construire et tester dans l'environnement Dev/QA
                    sh './vagrant_cnx.sh dev-qa-box "cd /app && ./mvnw clean package"'
                }
            }
        }

        stage('Deploy to Dev/QA') {
            steps {
                script {
                    // Déployer dans l'environnement Dev/QA
                    sh './vagrant_cnx.sh dev-qa-box "cd /app && docker-compose up -d"'
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    // Exécuter les tests Selenium dans l'environnement Dev/QA
                    sh './vagrant_cnx.sh dev-qa-box "cd /app && python3 tests.py"'
                }
            }
        }

        stage('Setup Application in Preprod Environment') {
            steps {
                script {
                    // Cloner le dépôt de l'application dans l'environnement de préproduction
                    sh './vagrant_cnx.sh preprod-box "git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'
                }
            }
        }

        stage('Deploy to Preprod') {
            steps {
                script {
                    // Déployer dans l'environnement de préproduction
                    sh './vagrant_cnx.sh preprod-box "cd /app && docker-compose up -d"'
                }
            }
        }
    }

    post {
        always {
            // Nettoyer, par exemple arrêter les VMs Vagrant
            script {
                sh 'cd dev-vagrant && vagrant halt'
                sh 'cd preprod-vagrant && vagrant halt'
            }
        }
        success {
            echo "Le pipeline a réussi !"
        }
        failure {
            echo "Le pipeline a échoué !"
            script {
                sh 'cd dev-vagrant && vagrant halt'
                sh 'cd preprod-vagrant && vagrant halt'
            }
        }
    }
}
