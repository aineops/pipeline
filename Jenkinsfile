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
                    def initOutput = sh(script: 'cd dev-vagrant && vagrant up', returnStdout: true).trim()
                    echo initOutput
                }
            }
        }

        stage('Setup Application in Dev/QA Environment') {
            steps {
                echo 'Configuration de l’application dans l’environnement Dev/QA...'
                script {
                    def cloneOutput = sh(script: 'cd dev-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"', returnStdout: true).trim()
                    echo cloneOutput
                    def treeOutput = sh(script: 'cd dev-vagrant && vagrant ssh -c "command -v tree || (sudo apt-get update && sudo apt-get install -y tree)"', returnStdout: true).trim()
                    echo treeOutput
                    def appTreeOutput = sh(script: 'cd dev-vagrant && vagrant ssh -c "tree /app"', returnStdout: true).trim()
                    echo appTreeOutput
                }
            }
        }

        stage('Build and Conditional Deploy in Dev/QA') {
            steps {
                echo 'Démarrage des étapes de build et de déploiement conditionnel...'
                script {
                    def services = ['admin-server', 'api-gateway', 'config-server', 'customers-service', 'discovery-server', 'vets-service', 'visits-service']
                    def servicesUpOutput = sh(script: 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/dev-vagrant/services_up.py"', returnStdout: true).trim()
                    echo servicesUpOutput
                    def servicesUpTestOutput = sh(script: 'cd dev-vagrant && vagrant ssh -c "test -f /app/services_up.py && echo \'Script Python téléchargé avec succès\' || exit 1"', returnStdout: true).trim()
                    echo servicesUpTestOutput

                    services.each { mavenService ->
                        def dockerService = mavenService.replace('spring-petclinic-', '')
                        echo "Traitement de ${mavenService}, service Docker correspondant : ${dockerService}"

                        def buildCmdOutput = sh(script: "cd dev-vagrant && vagrant ssh -c 'cd /app && sudo ./mvnw clean package -pl ${mavenService} -am -X'", returnStdout: true).trim()
                        echo buildCmdOutput
                        def jarExistsCmdOutput = sh(script: "cd dev-vagrant && vagrant ssh -c '[ -f /app/${mavenService}/target/*.jar ] && echo true || echo false'", returnStatus: true) == 0
                        if (jarExistsCmdOutput) {
                            echo "Déploiement du service Docker : ${dockerService}"
                            def serviceUpCmdOutput = sh(script: "cd dev-vagrant && vagrant ssh -c 'cd /app && python3 services_up.py ${dockerService}'", returnStdout: true).trim()
                            echo serviceUpCmdOutput
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
                    def servicesCheckCmd = 'cd dev-vagrant && vagrant ssh -c "docker-compose -f /docker-compose.yml ps -q | xargs -I {} docker inspect -f \'{{.State.Running}}\' {}"'
                    def servicesStatus = sh(script: servicesCheckCmd, returnStdout: true).trim()
                    echo servicesStatus

                    if (servicesStatus.split().every { it == 'true' }) {
                        echo 'Vérification de l\'accessibilité de l\'application...'
                        def appAccessOutput = sh(script: 'curl --fail --silent --head http://localhost:8080 || { echo "localhost:8080 n\'est pas accessible"; exit 1; }', returnStdout: true).trim()
                        echo appAccessOutput
                    } else {
                        echo 'Un ou plusieurs services Docker ne sont pas opérationnels. Exportation des logs et des informations des conteneurs...'
                        def exportLogsCmd = 'cd dev-vagrant && vagrant ssh -c "docker-compose -f /docker-compose.yml logs && docker ps -a | xargs -I {} docker inspect {} > /app/logs_inspects.txt"'
                        def exportLogsOutput = sh(script: exportLogsCmd, returnStdout: true).trim()
                        echo exportLogsOutput
                    }
                }
            }
        }

        stage('Download & Run Selenium Tests') {
            steps {
                echo 'Téléchargement et exécution des tests Selenium...'
                script {
                    def downloadTestScriptCmd = 'cd dev-vagrant && vagrant ssh -c "cd /app && sudo curl -LJO https://github.com/HoshEnder/pipeline/raw/master/tests.py"'
                    def testScriptOutput = sh(script: downloadTestScriptCmd, returnStdout: true).trim()
                    echo testScriptOutput
                    def testScriptTestOutput = sh(script: 'cd dev-vagrant && vagrant ssh -c "test -f /app/tests.py && echo \'Script de tests Selenium téléchargé avec succès\' || exit 1"', returnStdout: true).trim()
                    echo testScriptTestOutput

                    def seleniumTestCmd = 'cd dev-vagrant && vagrant ssh -c "cd /app && pytest --html=report.html"'
                    def seleniumTestOutput = sh(script: seleniumTestCmd, returnStdout: true).trim()
                    echo seleniumTestOutput
                }
            }
        }

        stage('Setup Application in Preprod Environment') {
            steps {
                echo 'Configuration de l’application dans l’environnement de préproduction...'
                script {
                    def preprodSetupOutput = sh(script: 'cd preprod-vagrant && vagrant up', returnStdout: true).trim()
                    echo preprodSetupOutput
                    def clonePreprodOutput = sh(script: 'cd preprod-vagrant && vagrant ssh -c "sudo git clone https://github.com/spring-petclinic/spring-petclinic-microservices.git /app"', returnStdout: true).trim()
                    echo clonePreprodOutput
                }
            }
        }

        stage('Deploy to Preprod') {
            steps {
                echo 'Déploiement dans l’environnement de préproduction...'
                script {
                    def deployPreprodOutput = sh(script: 'cd preprod-vagrant && vagrant ssh -c "cd /app && sudo docker-compose up -d"', returnStdout: true).trim()
                    echo deployPreprodOutput
                }
            }
        }
    }

    post {
        always {
            echo 'Nettoyage post-exécution et publication des rapports Selenium...'
            script {
                def haltDevOutput = sh(script: 'cd dev-vagrant && vagrant halt -f', returnStdout: true).trim()
                echo haltDevOutput
                def haltPreprodOutput = sh(script: 'cd preprod-vagrant && vagrant halt -f', returnStdout: true).trim()
                echo haltPreprodOutput
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
