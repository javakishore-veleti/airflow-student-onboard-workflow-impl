#!/bin/bash

# Find the webserver process and kill it
pkill -f "airflow webserver"

# Find the scheduler process and kill it
pkill -f "airflow scheduler"


# Optionally remove any persistent data
rm -rf ~/airflow/postgres-data
# shellcheck disable=SC2046
rm -rf $(pwd)/bin/airflow_home/
