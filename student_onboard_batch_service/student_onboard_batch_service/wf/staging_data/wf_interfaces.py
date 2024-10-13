# student_onboard_batch_service/common/task_definitions.py

from abc import ABC

from student_onboard_batch_service.common.app_constants import WfResponse
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx


class StagingDataReaderWfTask(ABC):

    def execute_wf_task(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx) -> int:
        """Execute the task logic."""
        return WfResponse.INVALID_INPUT
