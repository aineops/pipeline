#!/bin/bash

# Utiliser 'default' comme nom de la VM si aucun argument n'est fourni
VM_NAME=${1:-default}

# Récupération du chemin de la clé privée, de l'adresse IP et du port SSH
SSH_CONFIG=$(vagrant ssh-config $VM_NAME 2>/dev/null)
if [ -z "$SSH_CONFIG" ]; then
    echo "Erreur : Impossible de récupérer la configuration SSH pour la VM '$VM_NAME'."
    exit 1
fi

PRIVATE_KEY=$(echo "$SSH_CONFIG" | grep IdentityFile | awk '{print $2}')
SSH_PORT=$(echo "$SSH_CONFIG" | grep Port | awk '{print $2}')
SSH_HOST=$(echo "$SSH_CONFIG" | grep HostName | awk '{print $2}')

# Vérification des valeurs extraites
if [ -z "$PRIVATE_KEY" ] || [ -z "$SSH_PORT" ] || [ -z "$SSH_HOST" ]; then
    echo "Erreur : Informations SSH incomplètes."
    exit 1
fi

# Condition pour automatiser la validation de la clé SSH si une variable est définie
if [ -n "$AUTO_ACCEPT_SSH_KEY" ]; then
    SSH_OPTIONS="-o StrictHostKeyChecking=no"
else
    SSH_OPTIONS=""
fi

# Construction et exécution de la commande SSH avec les options SSH
ssh $SSH_OPTIONS -i $PRIVATE_KEY -p $SSH_PORT vagrant@$SSH_HOST
