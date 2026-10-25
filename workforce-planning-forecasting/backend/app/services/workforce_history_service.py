from __future__ import annotations

import csv
import io
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.workforce_history import WorkforceHistory
from app.schemas.workforce_history import WorkforceHistoryCreate, WorkforceHistoryUpdate


def _history_to_response(history: WorkforceHistory) -> dict[str, Any]:
    return {
        "id": history.id,
        "department_id": history.department_id,
        "department_name": history.department.name if history.department else None,
        "year": history.year,
        "month": history.month,
        "employee_count": history.employee_count,
        "employees_hired": history.employees_hired,
        "employees_left": history.employees_left,
        "business_growth": history.business_growth,
        "project_count": history.project_count,
        "created_at": history.created_at.isoformat(),
    }


def get_workforce_history(
    db: Session,
    *,
    department_id: int | None = None,
    year: int | None = None,
    month: int | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page must be at least 1")
    if page_size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page size must be at least 1")

    query = db.query(WorkforceHistory).join(Department, WorkforceHistory.department_id == Department.id)

    if department_id is not None:
        query = query.filter(WorkforceHistory.department_id == department_id)
    if year is not None:
        query = query.filter(WorkforceHistory.year == year)
    if month is not None:
        query = query.filter(WorkforceHistory.month == month)

    total = query.count()
    items = query.order_by(WorkforceHistory.year.asc(), WorkforceHistory.month.asc(), Department.name.asc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_history_to_response(row) for row in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total else 0,
    }


def get_history_by_id(db: Session, history_id: int) -> dict[str, Any]:
    history = db.query(WorkforceHistory).filter(WorkforceHistory.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workforce history record not found")
    return _history_to_response(history)


def create_history_record(db: Session, payload: WorkforceHistoryCreate) -> dict[str, Any]:
    department = db.query(Department).filter(Department.id == payload.department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    existing = db.query(WorkforceHistory).filter(
        WorkforceHistory.department_id == payload.department_id,
        WorkforceHistory.year == payload.year,
        WorkforceHistory.month == payload.month,
    ).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A workforce history record already exists for this department and month.",
        )

    record = WorkforceHistory(
        department_id=payload.department_id,
        year=payload.year,
        month=payload.month,
        employee_count=payload.employee_count,
        employees_hired=payload.employees_hired,
        employees_left=payload.employees_left,
        business_growth=payload.business_growth,
        project_count=payload.project_count,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return _history_to_response(record)


def update_history_record(db: Session, history_id: int, payload: WorkforceHistoryUpdate) -> dict[str, Any]:
    record = db.query(WorkforceHistory).filter(WorkforceHistory.id == history_id).first()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workforce history record not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "department_id" in update_data and update_data["department_id"] is not None:
        department = db.query(Department).filter(Department.id == update_data["department_id"]).first()
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return _history_to_response(record)


def delete_history_record(db: Session, history_id: int) -> dict[str, str]:
    record = db.query(WorkforceHistory).filter(WorkforceHistory.id == history_id).first()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workforce history record not found")

    db.delete(record)
    db.commit()
    return {"detail": "Workforce history record deleted successfully"}


def import_history_csv(db: Session, file: UploadFile) -> dict[str, Any]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload a CSV file")

    contents = file.file.read()
    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV file is not valid UTF-8") from exc

    reader = csv.DictReader(io.StringIO(text))
    required_columns = {"department", "year", "month", "employee_count", "employees_hired", "employees_left", "business_growth", "project_count"}
    if reader.fieldnames is None or not required_columns.issubset(set(reader.fieldnames)):
        missing = sorted(required_columns.difference(set(reader.fieldnames or [])))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"CSV is missing required columns: {', '.join(missing)}")

    total_rows = 0
    imported_rows = 0
    failed_rows = 0
    skipped_rows = 0
    errors: list[str] = []

    for index, row in enumerate(reader, start=2):
        total_rows += 1
        raw_row = {key: (value.strip() if isinstance(value, str) else value) for key, value in row.items()}
        department_name = raw_row.get("department")
        if not department_name:
            errors.append(f"Row {index}: department is required")
            failed_rows += 1
            continue

        department = db.query(Department).filter(Department.name == department_name).first()
        if department is None:
            errors.append(f"Row {index}: department '{department_name}' does not exist")
            failed_rows += 1
            continue

        try:
            year = int(raw_row["year"])
            month = int(raw_row["month"])
            employee_count = int(raw_row["employee_count"])
            employees_hired = int(raw_row["employees_hired"])
            employees_left = int(raw_row["employees_left"])
            business_growth = float(raw_row["business_growth"])
            project_count = int(raw_row["project_count"])
        except (TypeError, ValueError) as exc:
            errors.append(f"Row {index}: invalid numeric values - {exc}")
            failed_rows += 1
            continue

        if not 1 <= month <= 12:
            errors.append(f"Row {index}: month must be between 1 and 12")
            failed_rows += 1
            continue

        duplicate = db.query(WorkforceHistory).filter(
            WorkforceHistory.department_id == department.id,
            WorkforceHistory.year == year,
            WorkforceHistory.month == month,
        ).first()
        if duplicate is not None:
            errors.append(f"Row {index}: duplicate record for {department_name} in {year}-{month:02d}")
            skipped_rows += 1
            continue

        db.add(
            WorkforceHistory(
                department_id=department.id,
                year=year,
                month=month,
                employee_count=employee_count,
                employees_hired=employees_hired,
                employees_left=employees_left,
                business_growth=business_growth,
                project_count=project_count,
            )
        )
        imported_rows += 1

    db.commit()
    return {
        "total_rows": total_rows,
        "successfully_imported": imported_rows,
        "skipped_rows": skipped_rows,
        "failed_rows": failed_rows,
        "error_details": errors,
    }


def get_history_summary(db: Session) -> dict[str, Any]:
    rows = db.query(WorkforceHistory).order_by(WorkforceHistory.year.desc(), WorkforceHistory.month.desc()).all()
    if not rows:
        return {
            "total_records": 0,
            "departments_analyzed": 0,
            "latest_snapshot": None,
        }

    snapshot = rows[0]
    latest_snapshot = {
        "department_id": snapshot.department_id,
        "department_name": snapshot.department.name if snapshot.department else "Unknown",
        "year": snapshot.year,
        "month": snapshot.month,
        "employee_count": snapshot.employee_count,
    }
    departments_analyzed = db.query(WorkforceHistory.department_id).distinct().count()
    return {
        "total_records": len(rows),
        "departments_analyzed": departments_analyzed,
        "latest_snapshot": latest_snapshot,
    }
