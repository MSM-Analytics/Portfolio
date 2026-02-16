from pydantic import BaseModel
from typing import List


class AlertItem(BaseModel):
    code: str
    level: str  # info | warning | danger
    message: str


class AlertsResponse(BaseModel):
    alerts: List[AlertItem]
