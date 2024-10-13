# student_onboard_batch_service/wf/onboarding_wf.py
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.onboarding.tasks_factory import OnBoardTasksFactory


class OnboardingWfImpl:
    def __init__(self):
        self.tasks = [
            "check_ssn", "course_subjects", "calculate_cost", "register_student", "send_email"
        ]

    def execute(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx):
        for task in self.tasks:
            task = OnBoardTasksFactory.get_task(task)
            # Execute the task
            return_val:int = task.execute_wf_task(resp_ctx, resp_ctx)
