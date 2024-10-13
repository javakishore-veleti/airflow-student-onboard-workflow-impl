class StudentInfo:
    def __init__(self):
        self.row_no = 0
        self.ssn = ""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.course_id = ""
        self.dob = ""


class OnboardStudentReqCtx:
    def __init__(self):
        self.students_list: list[StudentInfo] = []
        self.staging_path_provided = False
        self.staging_path = ""


class OnboardStudentRespCtx:
    def __init__(self):
        self.ctx_data = {}
        self.status = 0
        self.reason_codes: list[str] = []



