#!/bin/bash

echo "CODEBASE_PATH ${CODEBASE_PATH}"

# Set Airflow Home to the local path
# shellcheck disable=SC2155
export AIRFLOW_HOME=$(pwd)/bin/airflow_home

# Set the DAGs folder to the onboard_student_dags folder
export AIRFLOW__CORE__DAGS_FOLDER="${CODEBASE_PATH}/onboard_student_dags"

export AIRFLOW__CORE__LOAD_EXAMPLES=False

# Expose Airflow configuration in the UI
export AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True

# Initialize the database
airflow db init

TEMPLATE_FILE="${CODEBASE_PATH}/bin/airflow_home/airflow-template.cfg"
cp "${CODEBASE_PATH}/bin/airflow/airflow-template.cfg" "${TEMPLATE_FILE}"

# Replace CODEBASE_FULL_PATH with CODEBASE_PATH in the specified file
sed -i '' "s|CODEBASE_FULL_PATH|$CODEBASE_PATH|g" "$TEMPLATE_FILE"

rm "${CODEBASE_PATH}/bin/airflow_home/airflow.cfg"
mv "$TEMPLATE_FILE" "${CODEBASE_PATH}/bin/airflow_home/airflow.cfg"

# Check if the admin user already exists
if ! airflow users list | grep -q "admin"; then
    # Create an admin user if it doesn't already exist
    airflow users create --username admin \
                         --firstname Admin \
                         --lastname User \
                         --role Admin \
                         --email admin@example.com \
                         --password admin123
    echo "Admin user created."
else
    echo "Admin user already exists."
fi

# Start Airflow webserver and scheduler
airflow webserver --port 8080 &  # Run webserver in the background

echo "AIRFLOW_HOME: $AIRFLOW_HOME"
echo "DAGS_FOLDER: $AIRFLOW__CORE__DAGS_FOLDER"

airflow scheduler  # Start the scheduler