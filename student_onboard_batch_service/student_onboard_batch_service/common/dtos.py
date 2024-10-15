from pandas import DataFrame
import json

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

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        student_info = StudentInfo()  # Initialize with None
        student_info.row_no = data['row_no']
        student_info.ssn = data['ssn']
        student_info.first_name = data['first_name']
        student_info.last_name = data['last_name']
        student_info.email = data['email']
        student_info.course_id = data['course_id']
        student_info.dob = data['dob']

        return student_info


class OnboardStudentReqCtx:
    def __init__(self):
        self.students_list: list[StudentInfo] = []
        self.staging_path_provided = False
        self.staging_path = ""
        self.student_list_df: DataFrame = None
        self.student_data_df_list: list[(str, DataFrame)] = []
        self.schedule_type = str(ScheduleTypes.NEAR_REAL_TIME)
        self.excel_file_distributed = False

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        students_str = ', '.join(str(student) for student in self.students_list)
        return f"OnboardStudentReqCtx(students_list=[{students_str}], staging_path_provided={self.staging_path_provided}, staging_path={self.staging_path})"

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        req_ctx = OnboardStudentReqCtx()  # Initialize with None
        req_ctx.students_list = data['students_list']
        req_ctx.staging_path_provided = data['staging_path_provided']
        req_ctx.staging_path = data['staging_path']
        req_ctx.student_list_df = DataFrame(data['student_list_df']) if data['student_list_df'] else None
        req_ctx.student_data_df_list = [(name, DataFrame.from_records(df)) for name, df in data['student_data_df_list']]

        req_ctx.schedule_type = data['schedule_type']
        req_ctx.excel_file_distributed = data['excel_file_distributed']

        return req_ctx


class OnboardStudentRespCtx:
    def __init__(self):
        self.ctx_data = {}
        self.status = 0
        self.reason_codes: list[str] = []

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return f"OnboardStudentRespCtx(ctx_data={self.ctx_data}, status={self.status}, reason_codes={self.reason_codes})"

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        resp_ctx = OnboardStudentRespCtx()  # Initialize with None
        resp_ctx.ctx_data = data['ctx_data']
        resp_ctx.status = data['status']
        resp_ctx.reason_codes = data['reason_codes']

        return resp_ctx



