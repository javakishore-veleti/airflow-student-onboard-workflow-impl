import logging

from overrides import override
from student_onboard_batch_service.common.app_constants import WfResponse
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.wf.staging_data.wf_interfaces import StagingDataReaderWfTask

LOGGER = logging.getLogger(__name__)
BEAN_ID = "ValidateStgDataTask"
LOG_PREFIX = f"[{BEAN_ID}] - "


class ValidateStgDataTask(StagingDataReaderWfTask):

    def __init__(self):
        pass

    @override
    def execute_wf_task(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx) -> int:
        LOGGER.info(f"{LOG_PREFIX} ENTERED req_ctx = {req_ctx}")

        if req_ctx.student_list_df is None:
            LOGGER.error(f"{LOG_PREFIX} Student list DataFrame is None")
            return WfResponse.INVALID_INPUT

        # Filter out rows with blank ssn, first_name, last_name, course_id, or dob
        LOGGER.info(f"{LOG_PREFIX} Started Filtering student_list_df for null values of ssn, first_name, last_name, "
                    f"course_id, dob")
        filtered_df = req_ctx.student_list_df.dropna(subset=['ssn', 'first_name', 'last_name', 'course_id', 'dob'])

        if filtered_df.empty:
            LOGGER.error(f"{LOG_PREFIX} No valid rows found after filtering")
            return WfResponse.INVALID_INPUT

        for index, row in filtered_df.iterrows():
            LOGGER.info(f"{LOG_PREFIX} Processing row: {row}")

        LOGGER.info(f"{LOG_PREFIX} EXITING req_ctx = {req_ctx}")
        return WfResponse.SUCCESS
