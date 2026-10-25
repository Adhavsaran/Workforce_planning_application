from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.schemas.department import DepartmentCreate, DepartmentUpdate


def _department_to_response(department: Department) -> dict[str, Any]:
    return {
        "id": department.id,
        "name": department.name,
        "description": department.description,
        "created_at": department.created_at.isoformat() if department.created_at else None,
        "updated_at": department.updated_at.isoformat() if department.updated_at else None,
    }


def get_departments(db: Session) -> list[dict[str, Any]]:
    departments = db.query(Department).order_by(Department.name.asc()).all()
    return [_department_to_response(department) for department in departments]


def get_department_by_id(db: Session, department_id: int) -> dict[str, Any]:
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return _department_to_response(department)


def create_department(db: Session, payload: DepartmentCreate) -> dict[str, Any]:
    normalized_name = payload.name.strip()
    if not normalized_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Department name cannot be empty")

    existing = db.query(Department).filter(Department.name == normalized_name).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Department '{normalized_name}' already exists",
        )

    department = Department(name=normalized_name, description=payload.description)
    db.add(department)
    db.commit()
    db.refresh(department)
    return _department_to_response(department)


def update_department(db: Session, department_id: int, payload: DepartmentUpdate) -> dict[str, Any]:
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"] is not None:
        new_name = update_data["name"].strip()
        if not new_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Department name cannot be empty")
        duplicate = db.query(Department).filter(Department.name == new_name, Department.id != department_id).first()
        if duplicate is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Department '{new_name}' already exists")
        department.name = new_name

    if "description" in update_data:
        department.description = update_data["description"]

    db.commit()
    db.refresh(department)
    return _department_to_response(department)


def delete_department(db: Session, department_id: int) -> dict[str, str]:
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    employees_count = db.query(Employee).filter(Employee.department_id == department_id).count()
    if employees_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department has associated employees. Reassign or delete employees before deleting the department.",
        )

    db.delete(department)
    db.commit()
    return {"detail": f"Department '{department.name}' deleted successfully"}


def get_department_employees(db: Session, department_id: int) -> list[dict[str, Any]]:
    department = db.query(Department).filter(Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    employees = db.query(Employee).filter(Employee.department_id == department_id).order_by(Employee.name.asc()).all()
    return [
        {
            "id": employee.id,
            "employee_id": employee.employee_id,
            "name": employee.name,
            "job_role": employee.job_role,
            "department": {"id": department.id, "name": department.name},
            "location": employee.location,
            "employment_type": employee.employment_type,
            "salary": employee.salary,
            "performance_score": employee.performance_score,
            "attrition_status": employee.attrition_status,
        }
        for employee in employees
    ]
