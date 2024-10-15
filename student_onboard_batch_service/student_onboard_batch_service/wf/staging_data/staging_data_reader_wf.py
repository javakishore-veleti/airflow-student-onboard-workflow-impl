# student_onboard_batch_service/wf/onboarding_wf.py
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.staging_data.tasks_factory import StagingDataReaderTasksFactory
import logging

LOGGER = logging.getLogger(__name__)

class StagingDataReaderWfImpl:
    def __init__(self):
        self.tasks = [
            "read_stg_data_excel_task", "validate_stg_data_task"
        ]

    def execute(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx):
        for task in self.tasks:
            LOGGER.info(f"Executing task START : {task}")
            task_obj = StagingDataReaderTasksFactory.get_task(task)
            # Execute the task
            return_val:int = task_obj.execute_wf_task(req_ctx, resp_ctx)

            LOGGER.info(f"Executing task END : {task} with return value : {return_val}")
