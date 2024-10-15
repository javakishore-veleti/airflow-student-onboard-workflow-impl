import os
import sys
import uuid

import requests
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from pandas import DataFrame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from student_onboard_batch_service.wf.onboarding.onboarding_wf import OnboardingWfImpl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.staging_data.staging_data_reader_wf import StagingDataReaderWfImpl

# depends_on_past: Set this to True to prevent the execution of the current run if the previous run failed.
# This is useful when the tasks are dependent on the previous run's success.
# depends_on_past Disable the UI Execution Button: In your DAG definition, ensure that the depends_on_past property is
# set to True. This way, the UI's execution button may be disabled if the previous run is still running or has failed.
# However, the primary control will come from setting schedule_interval to None.

# retries: The number of retries that should be attempted before failing the task.

default_args_value = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 12),
    'retries': 0,
}


def create_dag(default_args=None, dag_id: str = "Main_DAG", dag_description: str = "Main DAG for onboarding students",
               schedule_interval="None", excel_file_distributed: bool = False, deployment_mode: str = "local",
               skip_read_staging_data: bool = False):
    if default_args is None:
        default_args = default_args_value

    # Convert the string "None" to actual Python None
    if schedule_interval == "None":
        schedule_interval = None

    # Define the function that will be called by the PythonOperator
    if default_args is None:
        default_args = default_args_value

    def read_student_data_from_staging_datazone(staging_path=None, staging_path_provided=None,
                                                **kwargs):

        req_ctx = OnboardStudentReqCtx()
        resp_ctx = OnboardStudentRespCtx()

        req_ctx.excel_file_distributed = excel_file_distributed

        # Determine which path to use based on the staging_path_provided flag
        if staging_path_provided and staging_path:
            req_ctx.staging_path = staging_path

        if not skip_read_staging_data:
            StagingDataReaderWfImpl().execute(req_ctx, resp_ctx)

            if deployment_mode == "local":
                # Push both contexts to XCom
                ti = kwargs['ti']
                ti.xcom_push(key='req_ctx', value=req_ctx.to_json())
                ti.xcom_push(key='resp_ctx', value=resp_ctx.to_json())
            elif deployment_mode == "distributed" and excel_file_distributed:

                airflow_url = os.getenv("AIRFLOW_URL", "http://localhost:8080")  # Default to localhost if not set
                trigger_dag_url = f"{airflow_url}/api/v1/dags/Student_OnBoard_DAG_Local_Execution/dagRuns"

                for file_path, student_data_df in req_ctx.student_data_df_list:
                    print(f"Triggering BP_DAG for file {file_path}...")
                    student_data_df: DataFrame = student_data_df
                    counter = 0
                    for index, each_student_row in student_data_df.iterrows():
                        counter = counter + 1
                        student_info_json = each_student_row.to_json()

                        uuid_val = str(uuid.uuid4())

                        # Fire and forget: send the request without waiting for a response
                        trigger_target_dag_start = DummyOperator(task_id=f'trigger_target_dag_start_{uuid_val}')

                        try:
                            trigger_target_dag = TriggerDagRunOperator(
                                task_id=f'trigger_target_dag_{counter}_{str(uuid.uuid4())}',
                                trigger_dag_id='Student_OnBoard_DAG_Local_Execution',
                                conf={"student_info": student_info_json},  # You can pass any configuration you need
                                dag=dag, deferrable=True
                            )

                            trigger_target_dag_end = DummyOperator(task_id=f'trigger_target_dag_end_{uuid_val}')

                            trigger_target_dag_start >> trigger_target_dag >> trigger_target_dag_end

                            print(f"Triggered student_onboard_dag_local_exec for student: {student_info_json}")
                        except Exception as e:
                            print(f"Failed to trigger DAG for student: {student_info_json}, Error: {e}")




    def trigger_bp_dag(**kwargs):
        # Logic to trigger the BP_DAG for each student
        print("Triggering BP_DAG for each student...")

        if deployment_mode == "local":
            ti = kwargs['ti']
            # Pull the contexts from XCom
            req_ctx_json = ti.xcom_pull(task_ids='read_student_data_from_stg_datazone', key='req_ctx')
            resp_ctx_json = ti.xcom_pull(task_ids='read_student_data_from_stg_datazone', key='resp_ctx')

            if req_ctx_json is None:
                req_ctx = OnboardStudentReqCtx()
                resp_ctx = OnboardStudentRespCtx()
            else:
                req_ctx = OnboardStudentReqCtx.from_json(req_ctx_json)
                resp_ctx = OnboardStudentRespCtx.from_json(resp_ctx_json)
        else:
            req_ctx = OnboardStudentReqCtx()
            resp_ctx = OnboardStudentRespCtx()

        OnboardingWfImpl().execute(req_ctx, resp_ctx)

    with DAG(dag_id,
             default_args=default_args,
             description=dag_description,
             schedule_interval=schedule_interval,  # Change the schedule as needed
             catchup=False) as dag:
        # Dummy task to start the workflow
        start = DummyOperator(task_id='start')

        # Task to read student data with parameters for the path and flag
        if not skip_read_staging_data:
            read_student_data_from_staging_datazone = PythonOperator(
                task_id='read_student_data_from_stg_datazone',
                python_callable=read_student_data_from_staging_datazone,
                op_kwargs={
                    'staging_path': '{{ dag_run.conf.get("staging_path", "") }}',
                    # Get the staging path from DAG input params, default to None
                    'staging_path_provided': '{{ dag_run.conf.get("staging_path_provided", "false") }}'
                },
                provide_context=True
            )
        else:
            read_student_data_from_staging_datazone = None

        trigger_bp = None
        if not excel_file_distributed and skip_read_staging_data:
            # Task to trigger the BP_DAG
            trigger_bp = PythonOperator(
                task_id='trigger_bp_dag',
                python_callable=trigger_bp_dag,
                provide_context=True
            )

        end = DummyOperator(task_id='end')

        if not skip_read_staging_data:
            if not excel_file_distributed:
                # Set the task dependencies
                start >> read_student_data_from_staging_datazone >> trigger_bp >> end
            else:
                # Set the task dependencies
                start >> read_student_data_from_staging_datazone >> end
        else:
            # Set the task dependencies
            start >> trigger_bp >> end
