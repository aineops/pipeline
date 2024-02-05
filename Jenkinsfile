pipeline {
    agent any

    stages {
        stage('Checkout Pipeline Repo') {
            steps {
                echo 'Démarrage du checkout du répertoire de pipeline...'
                git 'https://github.com/HoshEnder/pipeline.git'
            }
        }

        stage('Initial Setup') {
            steps {
                echo 'Initialisation de la VM...'
                script {
                    sh 'cd dev-vagrant && vagrant up'
                }
            }
        }

        stage('Setup Application in Dev/QA Environment') {
            steps {
                echo 'Configuration de l’application dans l’environnement Dev/QA...'
                script {
                    sh 'cd dev-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'
                }
            }
        }

        stage('Build and Conditional Deploy in Dev/QA') {
            steps {
                echo 'Démarrage des étapes de build et de déploiement conditionnel...'
                script {
                    def services = ['spring-petclinic-admin-server', 'spring-petclinic-api-gateway', 
                                    'spring-petclinic-config-server', 'spring-petclinic-customers-service', 
                                    'spring-petclinic-discovery-server', 'spring-petclinic-vets-service', 
                                    'spring-petclinic-visits-service']

                    echo 'Téléchargement du script Python avant de lancer les builds'
                    sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/dev-vagrant/deploy_service.py"'

                    services.each { mavenService ->
                        def dockerService = mavenService.replace('spring-petclinic-', '')
                        echo "Traitement de ${mavenService}, service Docker correspondant : ${dockerService}"

                        def buildCmd = "cd dev-vagrant && vagrant ssh -c 'cd /app && sudo ./mvnw clean package -pl ${mavenService} -am'"
                        sh(buildCmd)

                        def jarExistsCmd = "cd dev-vagrant && vagrant ssh -c '[ -f /app/${mavenService}/target/*.jar ] && echo true || echo false'"
                        if (sh(script: jarExistsCmd, returnStatus: true) == 0) {
                            echo "Déploiement du service Docker : ${dockerService}"
                            sh "cd dev-vagrant && vagrant ssh -c 'cd /app && python3 deploy_service.py ${dockerService}'"
                        } else {
                            echo "Échec du build pour ${mavenService}, déploiement de ${dockerService} ignoré."
                        }
                    }
                }
            }
        }

        // stage('Verify Application Accessibility') {
        //     steps {
        //         echo 'Vérification de l’accessibilité de l’application...'
        //         script {
        //             def appUrl = "http://localhost:8282"
        //             sh "curl --fail --silent --head ${appUrl} || exit 1"
        //             echo "Application accessible à ${appUrl}"
        //         }
        //     }
        // }

        stage('Download & Run Selenium Tests') {
            steps {
                echo 'Téléchargement et exécution des tests Selenium...'
                script {
                    def seleniumTestCmd = 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/tests.py && sudo python3 tests.py"'
                    def seleniumOutput = sh(script: seleniumTestCmd, returnStdout: true).trim()
                    echo seleniumOutput
                }
            }
        }

        stage('Setup Application in Preprod Environment') {
            steps {
                echo 'Configuration de l’application dans l’environnement de préproduction...'
                script {
                    sh 'cd preprod-vagrant && vagrant up'
                    sh 'cd preprod-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'
                }
            }
        }

        stage('Deploy to Preprod') {
            steps {
                echo 'Déploiement dans l’environnement de préproduction...'
                script {
                    sh 'cd preprod-vagrant && vagrant ssh -c "cd /app && sudo docker-compose up -d"'
                }
            }
        }
    }

    post {
        always {
            echo 'Nettoyage post-exécution et publication des rapports Selenium...'
            script {
                sh 'cd dev-vagrant && vagrant halt -f'
                sh 'cd preprod-vagrant && vagrant halt -f'
                // sh 'cd dev-vagrant && vagrant destroy -f'
                // sh 'cd preprod-vagrant && vagrant destroy -f'
            }
            
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '/home/a/jen_proj/Selenium',
                reportFiles: 'index.html', // Assurez-vous que ce fichier existe dans le dossier des rapports
                reportName: "Rapport Selenium HTML"
            ])
        }
        success {
            echo "Le pipeline a réussi !"
        }
        failure {
            echo "Le pipeline a échoué !"
        }
    }
}
