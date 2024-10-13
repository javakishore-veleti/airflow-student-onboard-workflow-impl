import os
import glob
import logging
from datetime import datetime, timedelta
from student_onboard_batch_service.common.app_constants import ScheduleTypes

LOGGER = logging.getLogger(__name__)
BEAN_ID = "AppUtil"
LOG_PREFIX = f"[{BEAN_ID}] - "


class AppUtil:

    @staticmethod
    def get_user_home_path():
        return os.path.expanduser("~")

    @staticmethod
    def get_student_data_default_path():
        default_path = AppUtil.get_user_home_path() + "/student_onboard_batch_service/datasets/staging_datazone"
        LOGGER.info(f"{LOG_PREFIX} Default path: {default_path}")

        os.makedirs(default_path, exist_ok=True)
        LOGGER.info(f"{LOG_PREFIX} Executed os.makedirs for Default path: {default_path}")

        return default_path

    @staticmethod
    def get_student_data_default_path_for_schedule_type(schedule_type: str):
        default_path = AppUtil.get_student_data_default_path()
        LOGGER.info(f"{LOG_PREFIX} Default path: {default_path}")

        if schedule_type == ScheduleTypes.NEAR_REAL_TIME or schedule_type is None:
            today = datetime.today()
            default_path = os.path.join(default_path, today.strftime("%Y/%m/%d"))
        elif schedule_type == ScheduleTypes.FORT_NIGHT:
            start_date = datetime.today() - timedelta(days=2)
            default_path = os.path.join(default_path, start_date.strftime("%Y/%m/%d"))
        elif schedule_type == ScheduleTypes.PREVIOUS_DAY:
            previous_day = datetime.today() - timedelta(days=1)
            default_path = os.path.join(default_path, previous_day.strftime("%Y/%m/%d"))
        elif schedule_type == ScheduleTypes.END_OF_DAY:
            end_of_day = datetime.today()
            default_path = os.path.join(default_path, end_of_day.strftime("%Y/%m/%d"))

        os.makedirs(default_path, exist_ok=True)

        LOGGER.info(f"{LOG_PREFIX} Executed os.makedirs for Default path: {default_path}")

        return default_path

    @staticmethod
    def get_student_data_files_list_from_a_path(student_data_folder_path: str) -> list[str]:
        # Get all files in the directory
        files = glob.glob(os.path.join(student_data_folder_path, '*'))

        if not files:
            LOGGER.info(f"{LOG_PREFIX} No files found in the directory: {student_data_folder_path}")
            return []

        # Sort files by creation date and time
        files.sort(key=os.path.getctime, reverse=True)

        # Return the latest 10 files
        return files[:10]

