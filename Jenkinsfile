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
                sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo ./mvnw clean package"'
                echo 'Build Maven et tests unitaires terminés.'

                def services = ['spring-petclinic-admin-server', 'spring-petclinic-api-gateway', 
                                'spring-petclinic-config-server', 'spring-petclinic-customers-service', 
                                'spring-petclinic-discovery-server', 'spring-petclinic-vets-service', 
                                'spring-petclinic-visits-service']

                // Attendre la présence des fichiers JAR
                services.each { service ->
                    def jarPath = "/app/${service}/target/${service}-3.2.0.jar"
                    def maxWait = 120 // Délai d'attente maximal en secondes
                    def waitInterval = 10 // Intervalles de vérification en secondes

                    echo "Vérification de la présence du fichier JAR pour ${service}..."
                    while (true) {
                        def jarExists = sh(script: "cd dev-vagrant && vagrant ssh -c '[ -f ${jarPath} ] && echo true || echo false'", returnStdout: true).trim()
                        if (jarExists.toBoolean()) {
                            echo "Fichier JAR trouvé pour ${service}."
                            break
                        }
                        if (maxWait <= 0) {
                            error "Le fichier JAR pour ${service} est manquant après le temps d'attente maximal."
                        }
                        sleep(waitInterval)
                        maxWait -= waitInterval
                    }
                }

                echo 'Tous les fichiers JAR sont présents et vérifiés.'
            }
        }
    }

        stage('Deploy to Dev/QA') {
            steps {
                script {
                sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo docker-compose up -d"'

                // Attendre que tous les conteneurs soient "up and running"
                sh '''
                    MAX_WAIT=120  # Maximum wait time in seconds
                    WAIT_INTERVAL=10  # Interval to wait between checks in seconds
                    while [ $MAX_WAIT -gt 0 ]; do
                        if docker-compose ps | grep -q "(healthy)"; then
                            echo "Tous les conteneurs sont en état 'healthy'."
                            break
                        fi
                        echo "En attente des conteneurs... Reste $MAX_WAIT secondes."
                        sleep $WAIT_INTERVAL
                        MAX_WAIT=$(($MAX_WAIT-$WAIT_INTERVAL))
                    done
                    if [ $MAX_WAIT -le 0 ]; then
                        echo "Timeout atteint. Tous les conteneurs ne sont pas 'up and running'."
                        exit 1
                    fi
                '''
            }
            }
        }

        stage('Download & Run Selenium Tests') {
        steps {
            script {
                // Télécharger le fichier tests.py depuis le référentiel GitHub
                sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/tests.py"'

                // Exécuter les tests Selenium dans l'environnement Dev/QA
                sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo python3 tests.py"'

                // Collecter les résultats des tests Selenium
                junit 'test-reports/*.xml'
            }
        }
    }


        stage('Setup Application in Preprod Environment') {
            steps {
                script {
                    sh 'cd preprod-vagrant && vagrant up'
                    // Cloner le dépôt de l'application dans l'environnement de préproduction
                    sh 'cd preprod-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'
                }
            }
        }

        stage('Deploy to Preprod') {
            steps {
                script {

                    // Déployer dans l'environnement de préproduction
                    sh 'cd preprod-vagrant && vagrant ssh -c "cd /app && sudo docker-compose up -d"'
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
