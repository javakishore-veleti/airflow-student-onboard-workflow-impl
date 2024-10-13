from pandas import DataFrame

from student_onboard_batch_service.common.app_constants import ScheduleTypes


class StudentInfo:
    def __init__(self):
        self.row_no = 0
        self.ssn = ""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.course_id = ""
        self.dob = ""

    def __str__(self):
        return f"StudentInfo(row_no={self.row_no}, ssn={self.ssn}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, course_id={self.course_id}, dob={self.dob})"


class OnboardStudentReqCtx:
    def __init__(self):
        self.students_list: list[StudentInfo] = []
        self.staging_path_provided = False
        self.staging_path = ""
        self.student_list_df: DataFrame = None
        self.student_data_df_list: list[(str, DataFrame)] = []
        self.schedule_type = ScheduleTypes.NEAR_REAL_TIME

    def __str__(self):
        students_str = ', '.join(str(student) for student in self.students_list)
        return f"OnboardStudentReqCtx(students_list=[{students_str}], staging_path_provided={self.staging_path_provided}, staging_path={self.staging_path})"


class OnboardStudentRespCtx:
    def __init__(self):
        self.ctx_data = {}
        self.status = 0
        self.reason_codes: list[str] = []

    def __str__(self):
        return f"OnboardStudentRespCtx(ctx_data={self.ctx_data}, status={self.status}, reason_codes={self.reason_codes})"



