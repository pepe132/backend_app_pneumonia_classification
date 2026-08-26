from datetime import date, datetime

from pydantic import BaseModel


class CountByLabel(BaseModel):
    label: str
    count: int


class DailyCount(BaseModel):
    date: date
    count: int


class DashboardSummaryResponse(BaseModel):
    generated_at: datetime
    date_from: datetime | None
    date_to: datetime | None
    active_patients: int
    evaluations: int
    radiographs: int
    severity_tabular: list[CountByLabel]
    final_severity: list[CountByLabel]
    radiographic_classes: list[CountByLabel]
    evaluation_trend: list[DailyCount]

