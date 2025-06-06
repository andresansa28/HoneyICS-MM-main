#!/bin/bash

# stampa ogni 500 millisecondi l'ultima riga del log di analyzer
while [[ $result -eq 0 ]]
do
    sleep 0.5
    # prendo ultima linea 
    echo $(docker logs analyzer | grep "%" | tail -1)
done