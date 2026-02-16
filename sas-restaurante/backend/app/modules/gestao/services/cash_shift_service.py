from datetime import datetime

def get_shift_by_time(dt: datetime) -> str:
    hour = dt.hour

    if 6 <= hour < 12:
        return "MANHA"
    elif 12 <= hour < 18:
        return "TARDE"
    else:
        return "NOITE"
