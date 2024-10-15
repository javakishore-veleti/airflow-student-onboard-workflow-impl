# Define the default arguments for the DAG
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from datetime import datetime

from onboard_student_dags.student_onboard_dag_util import create_dag

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 12),
    'retries': 1,
}

create_dag(default_args=default_args, dag_id="Student_OnBoard_DAG_Distributed_Execution",
           dag_description="Student OnBoard DAG Distributed for onboarding students",
           deployment_mode="distributed", excel_file_distributed=True,
           schedule_interval="None")
