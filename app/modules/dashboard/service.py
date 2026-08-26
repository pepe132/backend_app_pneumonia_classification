from datetime import datetime, timezone

from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session

from app.modules.evaluations.models import Evaluation
from app.modules.patients.models import Patient
from app.modules.radiographs.models import Radiograph


def _apply_period(query, column, date_from, date_to):
    if date_from:
        query = query.filter(column >= date_from)
    if date_to:
        query = query.filter(column <= date_to)
    return query


def _distribution(db, model, column, date_column, date_from, date_to):
    query = db.query(column, func.count()).filter(column.isnot(None))
    query = _apply_period(query, date_column, date_from, date_to)
    return [
        {"label": label, "count": count}
        for label, count in query.group_by(column).order_by(column).all()
    ]


def get_dashboard_summary(
    db: Session, date_from: datetime | None, date_to: datetime | None
) -> dict:
    patient_query = db.query(func.count(Patient.patient_id)).filter(
        Patient.active == True
    )
    patient_query = _apply_period(
        patient_query, Patient.created_at, date_from, date_to
    )
    evaluation_query = _apply_period(
        db.query(func.count(Evaluation.evaluation_id)),
        Evaluation.created_at,
        date_from,
        date_to,
    )
    radiograph_query = _apply_period(
        db.query(func.count(Radiograph.radiograph_id)),
        Radiograph.created_at,
        date_from,
        date_to,
    )
    day = cast(Evaluation.created_at, Date)
    trend_query = _apply_period(
        db.query(day.label("date"), func.count(Evaluation.evaluation_id)),
        Evaluation.created_at,
        date_from,
        date_to,
    )

    return {
        "generated_at": datetime.now(timezone.utc),
        "date_from": date_from,
        "date_to": date_to,
        "active_patients": patient_query.scalar() or 0,
        "evaluations": evaluation_query.scalar() or 0,
        "radiographs": radiograph_query.scalar() or 0,
        "severity_tabular": _distribution(
            db, Evaluation, Evaluation.severity_tabular, Evaluation.created_at,
            date_from, date_to
        ),
        "final_severity": _distribution(
            db, Evaluation, Evaluation.final_severity, Evaluation.created_at,
            date_from, date_to
        ),
        "radiographic_classes": _distribution(
            db, Radiograph, Radiograph.image_class, Radiograph.created_at,
            date_from, date_to
        ),
        "evaluation_trend": [
            {"date": item_date, "count": count}
            for item_date, count in trend_query.group_by(day).order_by(day).all()
        ],
    }

