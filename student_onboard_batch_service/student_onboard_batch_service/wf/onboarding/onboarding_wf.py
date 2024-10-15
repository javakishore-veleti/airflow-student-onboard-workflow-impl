# student_onboard_batch_service/wf/onboarding_wf.py
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.onboarding.tasks_factory import OnBoardTasksFactory
import logging

LOGGER = logging.getLogger(__name__)


class OnboardingWfImpl:
    def __init__(self):
        self.tasks = [
            "check_ssn", "course_subjects", "calculate_cost", "register_student", "send_email"
        ]

    # This method will execute all the tasks in the workflow
    # Since Each Airflow Task can be deployed as a separate container or kubernetes pod or non-kubernetes Celery task,
    # that requires serialization and de-serialization of each sub-tasks input and output values, by design
    # this OnboardingWfImpl class is developed to run the core business logic in a single container or
    # kubernetes pod
    def execute(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx):
        for task in self.tasks:
            LOGGER.info(f"Executing task START : {task}")

            task_obj = OnBoardTasksFactory.get_task(task)
            # Execute the task
            return_val:int = task_obj.execute_wf_task(req_ctx, resp_ctx)

            LOGGER.info(f"Executing task END : {task} with return value : {return_val}")
