#!/bin/bash

# Find the webserver process and kill it
pkill -f "airflow webserver"

# Find the scheduler process and kill it
pkill -f "airflow scheduler"
