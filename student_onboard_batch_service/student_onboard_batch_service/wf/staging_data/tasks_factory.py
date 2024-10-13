from student_onboard_batch_service.wf.onboarding.wf_interfaces import OnboardWfTask
from student_onboard_batch_service.wf.staging_data.wf_interfaces import StagingDataReaderWfTask
from student_onboard_batch_service.wf.staging_data.wf_tasks.read_stg_data_excel_task import ReadStgDataExcelTask
from student_onboard_batch_service.wf.staging_data.wf_tasks.validate_stg_data_task import ValidateStgDataTask


class StagingDataReaderTasksFactory:
    @staticmethod
    def get_task(task_name: str) -> StagingDataReaderWfTask:
        """Creates and returns an instance of the specified task.

        Args:
            task_name (str): The name of the task to instantiate.

        Returns:
            OnboardWfTask: An instance of the requested task.

        Raises:
            ValueError: If the task name is not recognized.
        """
        task_mapping = {
            'read_stg_data_excel_task': ReadStgDataExcelTask,
            'validate_stg_data_task': ValidateStgDataTask
        }

        task_class = task_mapping.get(task_name)
        if not task_class:
            raise ValueError(f"Task '{task_name}' is not recognized.")

        return task_class()  # Instantiate the task class
