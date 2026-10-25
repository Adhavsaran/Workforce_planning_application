from __future__ import annotations

import csv
import io
from datetime import date
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

ALLOWED_SORT_FIELDS = {"name", "joining_date", "salary", "performance_score", "employee_id"}
ALLOWED_SORT_ORDERS = {"asc", "desc"}


def _employee_to_response(employee: Employee) -> dict[str, Any]:
    department_data = None
    if employee.department is not None:
        department_data = {"id": employee.department.id, "name": employee.department.name}

    return {
        "id": employee.id,
        "employee_id": employee.employee_id,
        "name": employee.name,
        "department": department_data,
        "job_role": employee.job_role,
        "age": employee.age,
        "gender": employee.gender,
        "experience_years": employee.experience_years,
        "joining_date": employee.joining_date.isoformat() if employee.joining_date else None,
        "salary": employee.salary,
        "performance_score": employee.performance_score,
        "satisfaction_score": employee.satisfaction_score,
        "employment_type": employee.employment_type,
        "location": employee.location,
        "attrition_status": employee.attrition_status,
        "created_at": employee.created_at.isoformat() if employee.created_at else None,
        "updated_at": employee.updated_at.isoformat() if employee.updated_at else None,
    }


def get_employees(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    department_id: int | None = None,
    job_role: str | None = None,
    employment_type: str | None = None,
    attrition_status: str | None = None,
    location: str | None = None,
    sort_by: str = "name",
    sort_order: str = "asc",
) -> dict[str, Any]:
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page must be at least 1")
    if page_size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page size must be at least 1")
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sort field")
    if sort_order.lower() not in ALLOWED_SORT_ORDERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sort order")

    query = db.query(Employee).join(Department, Employee.department_id == Department.id)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Employee.employee_id.ilike(term),
                Employee.name.ilike(term),
                Employee.job_role.ilike(term),
            )
        )
    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)
    if job_role:
        query = query.filter(Employee.job_role.ilike(f"%{job_role.strip()}%"))
    if employment_type:
        query = query.filter(Employee.employment_type == employment_type)
    if attrition_status:
        query = query.filter(Employee.attrition_status == attrition_status)
    if location:
        query = query.filter(Employee.location.ilike(f"%{location.strip()}%"))

    total = query.count()
    sort_column = getattr(Employee, sort_by)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    offset = (page - 1) * page_size
    employees = query.offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if total else 0

    return {
        "items": [_employee_to_response(employee) for employee in employees],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_employee_by_id(db: Session, employee_id: str) -> dict[str, Any]:
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {employee_id} not found")
    return _employee_to_response(employee)


def create_employee(db: Session, payload: EmployeeCreate) -> dict[str, Any]:
    department = db.query(Department).filter(Department.id == payload.department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    existing_employee = db.query(Employee).filter(Employee.employee_id == payload.employee_id).first()
    if existing_employee is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with ID {payload.employee_id} already exists",
        )

    employee = Employee(
        employee_id=payload.employee_id,
        name=payload.name,
        department_id=payload.department_id,
        job_role=payload.job_role,
        age=payload.age,
        gender=payload.gender,
        experience_years=payload.experience_years,
        joining_date=payload.joining_date,
        salary=payload.salary,
        performance_score=payload.performance_score,
        satisfaction_score=payload.satisfaction_score,
        employment_type=payload.employment_type,
        location=payload.location,
        attrition_status=payload.attrition_status,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return _employee_to_response(employee)


def update_employee(db: Session, employee_id: str, payload: EmployeeUpdate) -> dict[str, Any]:
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {employee_id} not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "department_id" in update_data and update_data["department_id"] is not None:
        department = db.query(Department).filter(Department.id == update_data["department_id"]).first()
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    if "employee_id" in update_data and update_data["employee_id"] is not None:
        candidate_id = update_data["employee_id"]
        if candidate_id != employee.employee_id:
            duplicate = db.query(Employee).filter(Employee.employee_id == candidate_id).first()
            if duplicate is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Employee with ID {candidate_id} already exists",
                )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return _employee_to_response(employee)


def delete_employee(db: Session, employee_id: str) -> dict[str, str]:
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {employee_id} not found")

    for prediction in list(employee.attrition_predictions):
        db.delete(prediction)

    db.delete(employee)
    db.commit()
    return {"detail": f"Employee with ID {employee_id} deleted successfully"}


def import_employees_csv(db: Session, file: UploadFile) -> dict[str, Any]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload a CSV file")

    contents = file.file.read()
    try:
        text = contents.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV file is not valid UTF-8") from exc

    reader = csv.DictReader(io.StringIO(text))
    required_columns = {
        "employee_id",
        "name",
        "department",
        "job_role",
        "age",
        "gender",
        "experience_years",
        "joining_date",
        "salary",
        "performance_score",
        "satisfaction_score",
        "employment_type",
        "location",
        "attrition_status",
    }

    if reader.fieldnames is None or not required_columns.issubset(set(reader.fieldnames)):
        missing = sorted(required_columns.difference(set(reader.fieldnames or [])))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV is missing required columns: {', '.join(missing)}",
        )

    total_rows = 0
    imported_rows = 0
    skipped_rows = 0
    failed_rows = 0
    errors: list[str] = []

    for index, row in enumerate(reader, start=2):
        total_rows += 1
        if row is None:
            skipped_rows += 1
            continue

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
            payload = EmployeeCreate(
                employee_id=raw_row["employee_id"],
                name=raw_row["name"],
                department_id=department.id,
                job_role=raw_row["job_role"],
                age=int(raw_row["age"]),
                gender=raw_row["gender"],
                experience_years=float(raw_row["experience_years"]),
                joining_date=date.fromisoformat(raw_row["joining_date"]),
                salary=float(raw_row["salary"]),
                performance_score=float(raw_row["performance_score"]),
                satisfaction_score=float(raw_row["satisfaction_score"]),
                employment_type=raw_row["employment_type"],
                location=raw_row["location"],
                attrition_status=raw_row["attrition_status"],
            )
        except (TypeError, ValueError, Exception) as exc:  # noqa: BLE001
            errors.append(f"Row {index}: invalid employee data - {exc}")
            failed_rows += 1
            continue

        if db.query(Employee).filter(Employee.employee_id == payload.employee_id).first() is not None:
            errors.append(f"Row {index}: employee ID {payload.employee_id} already exists")
            skipped_rows += 1
            continue

        employee = Employee(
            employee_id=payload.employee_id,
            name=payload.name,
            department_id=payload.department_id,
            job_role=payload.job_role,
            age=payload.age,
            gender=payload.gender,
            experience_years=payload.experience_years,
            joining_date=payload.joining_date,
            salary=payload.salary,
            performance_score=payload.performance_score,
            satisfaction_score=payload.satisfaction_score,
            employment_type=payload.employment_type,
            location=payload.location,
            attrition_status=payload.attrition_status,
        )
        db.add(employee)
        imported_rows += 1

    db.commit()
    return {
        "total_rows": total_rows,
        "successfully_imported": imported_rows,
        "skipped_rows": skipped_rows,
        "failed_rows": failed_rows,
        "error_details": errors,
    }
