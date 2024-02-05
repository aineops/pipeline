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
                    sh 'cd dev-vagrant && vagrant ssh -c "echo \'Initial Setup Output\' > /app/initial_setup.txt"'
                    sh 'cd dev-vagrant && vagrant scp default:/app/initial_setup.txt /home/a/jen_proj/rapports/initial_setup.txt'
                }
            }
        }

        stage('Setup Application in Dev/QA Environment') {
            steps {
                echo 'Configuration de l’application dans l’environnement Dev/QA...'
                script {
                    sh 'cd dev-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'
                    sh 'cd dev-vagrant && vagrant ssh -c "command -v tree || (sudo apt-get update && sudo apt-get install -y tree)"'
                    sh 'cd dev-vagrant && vagrant ssh -c "tree /app > /app/setup_app_env.txt"'
                    sh 'cd dev-vagrant && vagrant scp default:/app/setup_app_env.txt /home/a/jen_proj/rapports/setup_app_env.txt'
                }
            }
        }

        stage('Build and Conditional Deploy in Dev/QA') {
            steps {
                echo 'Démarrage des étapes de build et de déploiement conditionnel...'
                script {
                    def services = ['admin-server', 'api-gateway', 'config-server', 'customers-service', 'discovery-server', 'vets-service', 'visits-service']
                    sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/dev-vagrant/services_up.py"'
                    sh 'cd dev-vagrant && vagrant ssh -c "test -f /app/services_up.py && echo \'Script Python téléchargé avec succès\' || exit 1"'
                    services.each { mavenService ->
                        def dockerService = mavenService.replace('spring-petclinic-', '')
                        echo "Traitement de ${mavenService}, service Docker correspondant : ${dockerService}"
                        sh "cd dev-vagrant && vagrant ssh -c 'cd /app && sudo ./mvnw clean package -pl ${mavenService} -am -X > /app/${mavenService}_build.txt'"
                        sh "cd dev-vagrant && vagrant scp default:/app/${mavenService}_build.txt /home/a/jen_proj/rapports/${mavenService}_build.txt"
                        def jarExists = sh(script: "cd dev-vagrant && vagrant ssh -c '[ -f /app/${mavenService}/target/*.jar ] && echo true || echo false'", returnStatus: true) == 0
                        if (jarExists) {
                            echo "Déploiement du service Docker : ${dockerService}"
                            sh "cd dev-vagrant && vagrant ssh -c 'cd /app && python3 services_up.py ${dockerService} > /app/${dockerService}_deploy.txt'"
                            sh "cd dev-vagrant && vagrant scp default:/app/${dockerService}_deploy.txt /home/a/jen_proj/rapports/${dockerService}_deploy.txt"
                        } else {
                            echo "Échec du build pour ${mavenService}, déploiement de ${dockerService} ignoré."
                        }
                    }
                }
            }
        }

        stage('Verify Docker Services and Application Accessibility') {
            steps {
                echo 'Vérification de l\'état des services Docker...'
                script {
                    sh 'cd dev-vagrant && vagrant ssh -c "docker-compose -f /docker-compose.yml ps -q | xargs -I {} docker inspect -f \'{{.State.Running}}\' {} > /app/docker_services_status.txt"'
                    sh 'cd dev-vagrant && vagrant scp default:/app/docker_services_status.txt /home/a/jen_proj/rapports/docker_services_status.txt'
                    def servicesStatus = readFile('/home/a/jen_proj/rapports/docker_services_status.txt').trim()
                    echo servicesStatus

                    if (servicesStatus.split().every { it == 'true' }) {
                        echo 'Vérification de l\'accessibilité de l\'application...'
                        sh 'cd dev-vagrant && vagrant ssh -c "curl --fail --silent --head http://localhost:8080 > /app/app_accessibility.txt || echo localhost:8080 n\'est pas accessible > /app/app_accessibility.txt"'
                        sh 'cd dev-vagrant && vagrant ssh -c "docker ps -a > /app/docker_ps.txt"'
                        sh 'cd dev-vagrant && vagrant scp default:/app/app_accessibility.txt /home/a/jen_proj/rapports/app_accessibility.txt'
                        sh 'cd dev-vagrant && vagrant scp default:/app/docker_ps.txt /home/a/jen_proj/rapports/docker_ps.txt'
                    } else {
                        echo 'Un ou plusieurs services Docker ne sont pas opérationnels. Exportation des logs et des informations des conteneurs...'
                        sh 'cd dev-vagrant && vagrant ssh -c "docker-compose -f /docker-compose.yml logs > /app/docker_logs.txt && docker ps -a | xargs -I {} docker inspect {} > /app/docker_inspect.txt"'
                        sh 'cd dev-vagrant && vagrant scp default:/app/docker_logs.txt /home/a/jen_proj/rapports/docker_logs.txt'
                        sh 'cd dev-vagrant && vagrant scp default:/app/docker_inspect.txt /home/a/jen_proj/rapports/docker_inspect.txt'
                    }
                }
            }
        }

        stage('Download & Run Selenium Tests') {
            steps {
                echo 'Téléchargement et exécution des tests Selenium...'
                script {
                    sh 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/tests.py"'
                    sh 'cd dev-vagrant && vagrant ssh -c "test -f /app/tests.py && echo \'Script de tests Selenium téléchargé avec succès\' || exit 1"'
                    sh 'cd dev-vagrant && vagrant ssh -c "cd /app && pytest --html=report.html > /app/selenium_tests.txt"'
                    sh 'cd dev-vagrant && vagrant scp default:/app/selenium_tests.txt /home/a/jen_proj/rapports/selenium_tests.txt'
                    sh 'cd dev-vagrant && vagrant scp default:/app/report.html /home/a/jen_proj/Selenium/report.html'
                }
            }
        }

        stage('Setup Application in Preprod Environment') {
            steps {
                echo 'Configuration de l’application dans l’environnement de préproduction...'
                script {
                    sh 'cd preprod-vagrant && vagrant up'
                    sh 'cd preprod-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"'
                    sh 'cd preprod-vagrant && vagrant ssh -c "echo \'Setup Application in Preprod Environment Output\' > /app/setup_preprod_env.txt"'
                    sh 'cd preprod-vagrant && vagrant scp default:/app/setup_preprod_env.txt /home/a/jen_proj/rapports/setup_preprod_env.txt'
                }
            }
        }

        stage('Deploy to Preprod') {
            steps {
                echo 'Déploiement dans l’environnement de préproduction...'
                script {
                    sh 'cd preprod-vagrant && vagrant ssh -c "cd /app && sudo docker-compose up -d > /app/deploy_preprod.txt"'
                    sh 'cd preprod-vagrant && vagrant scp default:/app/deploy_preprod.txt /home/a/jen_proj/rapports/deploy_preprod.txt'
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
                sh 'cd dev-vagrant && vagrant ssh -c "echo \'Clean up Output\' > /app/cleanup.txt"'
                sh 'cd dev-vagrant && vagrant scp default:/app/cleanup.txt /home/a/jen_proj/rapports/cleanup.txt'
            }
            
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '/home/a/jen_proj/Selenium',
                reportFiles: 'report.html',
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
