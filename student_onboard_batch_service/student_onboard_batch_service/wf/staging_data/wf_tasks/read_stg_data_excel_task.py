import logging
from overrides import override
import pandas as pd
from student_onboard_batch_service.common.app_constants import WfResponse
from student_onboard_batch_service.common.dtos import OnboardStudentReqCtx, OnboardStudentRespCtx
from student_onboard_batch_service.utils.app_util import AppUtil
from student_onboard_batch_service.wf.staging_data.wf_interfaces import StagingDataReaderWfTask

LOGGER = logging.getLogger(__name__)
BEAN_ID = "read_stg_data_excel_task"
LOG_PREFIX = f"[{BEAN_ID}] - "


# noinspection PyMethodMayBeStatic
class ReadStgDataExcelTask(StagingDataReaderWfTask):

    def __init__(self):
        pass

    def build_student_df_from_req(self, req_ctx: OnboardStudentReqCtx) -> list[(str, pd.DataFrame)]:
        staging_path = ""
        if req_ctx.staging_path_provided and not req_ctx.staging_path:
            staging_path = req_ctx.staging_path
        else:
            staging_path = AppUtil.get_student_data_default_path_for_schedule_type(req_ctx.schedule_type)

        file_names_list: list[str] = AppUtil.get_student_data_files_list_from_a_path(staging_path)

        student_data_df_list: list[(str, pd.DataFrame)] = []
        for a_file in file_names_list:
            LOGGER.info(f"{LOG_PREFIX} Reading Excel file from staging_path {a_file}")
            a_student_list_df = pd.read_excel(a_file)
            student_data_df_list.append((a_file, a_student_list_df))

        return student_data_df_list

    @override
    def execute_wf_task(self, req_ctx: OnboardStudentReqCtx, resp_ctx: OnboardStudentRespCtx) -> int:
        LOGGER.info(f"{LOG_PREFIX} ENTERED req_ctx = {req_ctx}")

        student_data_df_list = self.build_student_df_from_req(req_ctx)
        if not student_data_df_list:
            LOGGER.error(f"{LOG_PREFIX} No student data found in staging path")
            return WfResponse.INVALID_INPUT

        req_ctx.student_data_df_list = student_data_df_list

        LOGGER.info(f"{LOG_PREFIX} EXITING req_ctx = {req_ctx}")
        return WfResponse.SUCCESS
