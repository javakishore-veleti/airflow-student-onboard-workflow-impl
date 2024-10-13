from overrides import override

from student_onboard_batch_service.common.app_constants import WfResponse
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.staging_data.wf_interfaces import StagingDataReaderWfTask


class ValidateStgDatalTask(StagingDataReaderWfTask):

    def __init__(self):
        pass

    @override
    def execute_wf_task(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx) -> int:
        return WfResponse.SUCCESS
