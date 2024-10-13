from student_onboard_batch_service.common.app_constants import WfResponse
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.onboarding.onboarding_wf import OnboardingWfImpl
from student_onboard_batch_service.wf.staging_data.staging_data_reader_wf import StagingDataReaderWfImpl


class OnBoardStudentsFacade:

    def __init__(self):
        pass

    def execute(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx) -> int:
        result: int = StagingDataReaderWfImpl().execute(req_ctx, resp_ctx)
        result: int = OnboardingWfImpl().execute(req_ctx, resp_ctx)
        return WfResponse.SUCCESS