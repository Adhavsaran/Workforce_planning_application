from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.services.department_service import (
    create_department,
    delete_department,
    get_department_by_id,
    get_department_employees,
    get_departments,
    update_department,
)

router = APIRouter(prefix="/api/departments", tags=["Departments"])


@router.get(
    "",
    response_model=list,
    summary="Get departments",
    description="Return all departments in the system.",
)
def list_departments(db: Session = Depends(get_db)):
    return get_departments(db)


@router.get(
    "/{department_id}",
    response_model=dict,
    summary="Get department",
    description="Fetch a single department by ID.",
)
def read_department(department_id: int, db: Session = Depends(get_db)):
    return get_department_by_id(db, department_id)


@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Create department",
    description="Create a new department while preventing duplicate names.",
)
def create_new_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    return create_department(db, payload)


@router.put(
    "/{department_id}",
    response_model=dict,
    summary="Update department",
    description="Update department information and enforce unique department names.",
)
def update_existing_department(department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db)):
    return update_department(db, department_id, payload)


@router.delete(
    "/{department_id}",
    summary="Delete department",
    description="Delete a department only if it has no associated employees.",
)
def delete_existing_department(department_id: int, db: Session = Depends(get_db)):
    return delete_department(db, department_id)


@router.get(
    "/{department_id}/employees",
    response_model=list,
    summary="Get department employees",
    description="Return all employees assigned to the selected department.",
)
def list_department_employees(department_id: int, db: Session = Depends(get_db)):
    return get_department_employees(db, department_id)
