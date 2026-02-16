from datetime import time
from app.modules.gestao.enums.shift_type import ShiftType


def get_shift_time_range(shift: ShiftType):
    if shift == ShiftType.MORNING:
        return time(6, 0), time(11, 59)

    if shift == ShiftType.AFTERNOON:
        return time(12, 0), time(17, 59)

    if shift == ShiftType.NIGHT:
        return time(18, 0), time(23, 59)

    return None, None
