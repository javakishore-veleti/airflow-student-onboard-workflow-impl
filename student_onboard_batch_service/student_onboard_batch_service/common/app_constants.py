class WfResponse:
    SUCCESS: int = 100
    FAILURE: int = 101
    INVALID_INPUT: int = 102


class ScheduleTypes:
    NEAR_REAL_TIME: str = "NEAR_REAL_TIME"
    END_OF_DAY: str = "END_OF_DAY"
    PREVIOUS_DAY: str = "PREVIOUS_DAY"
    FORT_NIGHT: str = "FORT_NIGHT"

