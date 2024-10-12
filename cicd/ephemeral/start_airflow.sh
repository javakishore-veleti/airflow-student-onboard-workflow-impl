#!/bin/bash

# Start Docker Compose for Apache Airflow using a specific Docker Compose file
docker-compose -f ./cicd/ephemeral/airflow/docker-compose.yaml up -d

# Print a message indicating that Airflow has been started
echo "Apache Airflow has started successfully!"
