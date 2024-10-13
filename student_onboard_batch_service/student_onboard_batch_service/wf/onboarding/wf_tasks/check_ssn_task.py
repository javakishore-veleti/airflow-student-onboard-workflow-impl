# student_onboard_batch_service/wf/wf_tasks/check_ssn_task.py
from overrides import override

from student_onboard_batch_service.common.app_constants import WfResponse
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.onboarding.wf_interfaces import OnboardWfTask


class CheckSSNTask(OnboardWfTask):
    def __init__(self):
        self.name = "Check SSN Task"

    def __init__(self):
        pass

    @override
    def execute_wf_task(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx):
        return WfResponse.SUCCESS
