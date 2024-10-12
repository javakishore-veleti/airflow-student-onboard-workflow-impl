#!/bin/bash

# Terminate Docker Compose containers, remove volumes, and clean up networks
docker-compose -f ./cicd/ephemeral/airflow/docker-compose.yaml down --volumes --remove-orphans

# Print a message indicating that Airflow has been terminated and cleaned up
echo "Apache Airflow has been terminated and containers have been removed!"
