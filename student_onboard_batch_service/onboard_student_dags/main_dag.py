# student_onboard_batch_service/onboard_student_dags/main_dag.py
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator


from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.staging_data.staging_data_reader_wf import StagingDataReaderWfImpl
from student_onboard_batch_service.wf.onboarding.onboarding_wf import OnboardingWfImpl

# Add the path to student_onboard_batch_service to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Default path to read student data
# Get the user's home directory
user_home = os.path.expanduser("~")
# Define the default path to read student data from the datasets folder
default_path = os.path.join(user_home, "student_onboard_batch_service", "datasets", "staging_datazone")


# Define the function that will be called by the PythonOperator
def read_student_data_from_staging_datazone(staging_path=None, staging_path_provided=None, **kwargs):
    # Determine which path to use based on the staging_path_provided flag
    if staging_path_provided and staging_path:
        path_to_use = staging_path
    else:
        path_to_use = default_path

    req_ctx = OnboardStudentReqCtx()
    resp_ctx = OnboardStudentRespCtx()
    StagingDataReaderWfImpl().execute(req_ctx, resp_ctx)

    # Push both contexts to XCom
    ti = kwargs['ti']
    ti.xcom_push(key='req_ctx', value=req_ctx)
    ti.xcom_push(key='resp_ctx', value=resp_ctx)

    # Logic to read student data from the specified path
    print(f"Reading student data from: {path_to_use}")


def trigger_bp_dag(**kwargs):
    # Logic to trigger the BP_DAG for each student
    print("Triggering BP_DAG for each student...")

    # Pull the contexts from XCom
    req_ctx = ti.xcom_pull(task_ids='read_student_data_from_stg_datazone', key='req_ctx')
    resp_ctx = ti.xcom_pull(task_ids='read_student_data_from_stg_datazone', key='resp_ctx')


    OnboardingWfImpl().execute(req_ctx, resp_ctx)




# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 12),
    'retries': 1,
}

# Define the DAG
with DAG('Main_DAG',
         default_args=default_args,
         description='Main DAG for onboarding students',
         schedule_interval='@daily',  # Change the schedule as needed
         catchup=False) as dag:
    # Dummy task to start the workflow
    start = DummyOperator(task_id='start')

    # Task to read student data with parameters for the path and flag
    read_student_data_from_staging_datazone = PythonOperator(
        task_id='read_student_data_from_stg_datazone',
        python_callable=read_student_data_from_staging_datazone,
        op_kwargs={
            'staging_path': '{{ dag_run.conf.get("staging_path", "") }}',
            # Get the staging path from DAG input params, default to None
            'staging_path_provided': '{{ dag_run.conf.get("staging_path_provided", "false") }}'
            # Get the boolean flag, default to None
        },
        provide_context=True
    )

    # Task to trigger the BP_DAG
    trigger_bp = PythonOperator(
        task_id='trigger_bp_dag',
        python_callable=trigger_bp_dag,
        provide_context=True
    )

    end = DummyOperator(task_id='end')

    # Set the task dependencies
    start >> read_student_data_from_staging_datazone >> trigger_bp >> end
