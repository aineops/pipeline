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
                }
            }
        }

        stage('Setup Application in Dev/QA Environment') {
            steps {
                script {

                    // Remplacer par le script pour se connecter à la VM dev-qa-box et cloner le dépôt
                    sh 'cd dev-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'

                    // // Utiliser le script pour se connecter à la VM dev-qa-box et cloner le dépôt
                    // sh 'git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app'
                }
            }
        }

        stage('Build and Unit Test in Dev/QA') {
            steps {
                script {
                    // Construire et tester dans l'environnement Dev/QA
                    sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo ./mvnw clean package"'
                }
            }
        }

        stage('Deploy to Dev/QA') {
            steps {
                script {
                    // Déployer dans l'environnement Dev/QA
                    sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo docker-compose up -d"'


                }
            }
        }

        stage('Download && Run Selenium Tests') {
            steps {
                script {
                    // Télécharger le fichier tests.py depuis le référentiel GitHub
                    sh 'cd /app && curl -LJO https://github.com/HoshEnder/pipeline/raw/master/tests.py'

                    def maxRetryCount = 30
                    def retryCount = 0
                    def curlExitCode = 0

                    // Attendre que localhost:8080 soit accessible ou jusqu'à un certain nombre de tentatives
                    while (retryCount < maxRetryCount) {
                        // Utiliser curl pour vérifier la disponibilité de localhost:8080
                        curlExitCode = sh(script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8080', returnStatus: true)
                        if (curlExitCode == 200) {
                            echo "localhost:8080 est accessible."
                            break
                        } else {
                            echo "localhost:8080 n'est pas encore accessible. Tentative ${retryCount + 1}/${maxRetryCount}..."
                            sleep(5) // Attendre 10 secondes avant la prochaine tentative
                            retryCount++
                        }
                    }

                    // Si la vérification échoue après un certain nombre de tentatives
                    if (curlExitCode != 200) {
                        error "localhost:8080 n'est pas accessible après ${maxRetryCount} tentatives."
                    }

                    // Exécuter les tests Selenium dans l'environnement Dev/QA
                    sh 'cd /app && python3 tests.py'
                }
            }
        }


        stage('Setup Application in Preprod Environment') {
            steps {
                script {
                    sh 'exit'
                    sh 'cd preprod-vagrant && vagrant up'
                    // Cloner le dépôt de l'application dans l'environnement de préproduction
                    sh 'git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app'
                }
            }
        }

        stage('Deploy to Preprod') {
            steps {
                script {

                    // Déployer dans l'environnement de préproduction
                    sh 'cd /app && docker-compose up -d'
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
