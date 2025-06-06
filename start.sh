#!/bin/bash

# Esporta tutte le variabili definite nel file .env (ignorando i commenti)
export $(grep -v '^#' .env | xargs)

FILE=./.done

# Se il file ".done" NON esiste, esegue la configurazione iniziale
if test ! -f "$FILE"; then
    echo "Checking Environment"

    # Verifica se lo script è in esecuzione su WSL2 (Windows Subsystem for Linux)
    WSL=$(uname -a | grep microsoft-standard-WSL2)
    echo "ip:" ${#WSL} ${WSL}

    # Se è in WSL, imposta IP statico; altrimenti, recupera l'IP locale
    if [ -n "$WSL" ]; then
       IP="10.0.8.3"
    else
       # Recupera il secondo campo della seconda riga da ifconfig (in modo grezzo)
       IP=$(ifconfig | awk '{print $2}' | head -n 2 | tail -n 1)
    fi

    # Estrae l'indirizzo IP dal valore KEYCLOAK_URL (presumibilmente da .env)
    OLD_IP=$(echo $KEYCLOAK_URL | cut -c 9- | cut -d ":" -f 1)

    echo "ip:" $IP "old_ip:" $OLD_IP

    # Costruisce la stringa per sed che sostituirà l'IP vecchio con quello nuovo
    SED_STRING=s/$OLD_IP/$IP/g
    echo "Sed string:" $SED_STRING

    # Applica la sostituzione nei file di configurazione
    sed -i $SED_STRING ./opensearch-dashboards.yml
    sed -i $SED_STRING ./config.yml
    sed -i $SED_STRING ./setup_keycloak.sh
    sed -i $SED_STRING ./backup/config.yml
    sed -i $SED_STRING ./.env

    echo "Creating CERTS"
    # Esegue lo script per creare certificati autofirmati
    ./setup_certs.sh

    echo "Deploying Keycloak"
    # Avvia il container Docker di Keycloak in background
    docker compose up -d keycloak

    # Attende finché il servizio Keycloak non risponde "UP"
    while true
    do
        if [ "$(curl -k -s https://localhost:8443/auth/health/ready status | jq -r '.status')" = "UP" ]; then
            break
        fi
        sleep 1
    done

    # Configura Keycloak
    ./setup_keycloak.sh

    # Avvia il nodo OpenSearch
    docker compose up -d os01

    # Attende che il servizio OpenSearch sia attivo (riceve risposta HTTP)
    while true
    do
        TE=$(curl -k -s https://localhost:9200)
        if [ -n "$TE" ]; then
            break
        fi
        sleep 1
    done

    # Configura la sicurezza di OpenSearch
    ./security_admin.sh
    sleep 5
    ./upload_security.sh

    # Avvia tutti gli altri container
    docker compose up -d dashboards
    docker compose up -d analyzer
    docker compose up -d backend
    docker compose up -d webapp_analyzer_bridge
    docker compose up -d webapp

    # Crea il file .done per indicare che l'installazione è stata completata
    touch .done
fi

# Se il file ".done" ESISTE, avvia solo i container (fase di avvio normale)
if test -f "$FILE"; then
    echo "Starting Services"

    docker compose up -d keycloak

    # Attende Keycloak come prima
    while true
        do
            if [ "$(curl -k -s https://localhost:8443/auth/health/ready status | jq -r '.status')" = "UP" ]; then
                break
            fi
            sleep 1
        done

    # Avvia i servizi restanti
    docker compose up -d os01 dashboards
    docker compose up -d analyzer
    docker compose up -d backend
    docker compose up -d webapp_analyzer_bridge
    docker compose up -d webapp
fi
