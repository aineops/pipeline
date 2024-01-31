#!/bin/bash

# Utiliser 'default' comme nom de la VM si aucun argument n'est fourni
VM_NAME=${1:-default}

# Récupération du chemin de la clé privée, de l'adresse IP et du port SSH
SSH_CONFIG=$(vagrant ssh-config $VM_NAME)
PRIVATE_KEY=$(echo "$SSH_CONFIG" | grep IdentityFile | awk '{print $2}')
SSH_PORT=$(echo "$SSH_CONFIG" | grep Port | awk '{print $2}')
SSH_HOST=$(echo "$SSH_CONFIG" | grep HostName | awk '{print $2}')

# Construction et exécution de la commande SSH
ssh -i $PRIVATE_KEY -p $SSH_PORT vagrant@$SSH_HOST
