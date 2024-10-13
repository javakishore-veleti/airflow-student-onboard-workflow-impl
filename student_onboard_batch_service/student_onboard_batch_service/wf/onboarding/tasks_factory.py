# student_onboard_batch_service/wf/tasks_factory.py
from student_onboard_batch_service.wf.onboarding.wf_interfaces import OnboardWfTask
from student_onboard_batch_service.wf.onboarding.wf_tasks.check_ssn_task import CheckSSNTask
from student_onboard_batch_service.wf.onboarding.wf_tasks.course_subjects_task import CourseSubjectsTask
from student_onboard_batch_service.wf.onboarding.wf_tasks.calculate_cost_task import CalculateCostTask
from student_onboard_batch_service.wf.onboarding.wf_tasks.register_student_task import RegisterStudentTask
from student_onboard_batch_service.wf.onboarding.wf_tasks.send_email_task import SendEmailTask


class OnBoardTasksFactory:
    @staticmethod
    def get_task(task_name: str) -> OnboardWfTask:
        """Creates and returns an instance of the specified task.

        Args:
            task_name (str): The name of the task to instantiate.

        Returns:
            OnboardWfTask: An instance of the requested task.

        Raises:
            ValueError: If the task name is not recognized.
        """
        task_mapping = {
            'check_ssn': CheckSSNTask,
            'course_subjects': CourseSubjectsTask,
            'calculate_cost': CalculateCostTask,
            'register_student': RegisterStudentTask,
            'send_email': SendEmailTask,
        }

        task_class = task_mapping.get(task_name)
        if not task_class:
            raise ValueError(f"Task '{task_name}' is not recognized.")

        return task_class()  # Instantiate the task class
