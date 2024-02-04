import subprocess
import threading

def launch_service(service_name):
    print(f"Démarrage du service {service_name}...")
    command = f"docker-compose up -d {service_name}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print(f"Service {service_name} démarré avec succès.")
    else:
        print(f"Erreur lors du démarrage du service {service_name}: {stderr.decode()}")

services = [
    'config-server', 'discovery-server', 'customers-service', 
    'visits-service', 'vets-service', 'api-gateway', 
    'tracing-server', 'admin-server', 'grafana-server', 
    'prometheus-server'
]

threads = []
for service in services:
    thread = threading.Thread(target=launch_service, args=(service,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
