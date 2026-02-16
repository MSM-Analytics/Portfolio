from pydantic import BaseModel
from typing import List
from decimal import Decimal


class LineChart(BaseModel):
    labels: List[str]
    values: List[Decimal]


class PieChart(BaseModel):
    labels: List[str]
    values: List[Decimal]


class BarChart(BaseModel):
    labels: List[str]
    values: List[Decimal]
