#!/bin/bash
docker stop ps
docker rm ps
docker build -t pyimage .
docker run -d --name ps --net opensearch_keycloak_framework -p 5000:80 pyimage
