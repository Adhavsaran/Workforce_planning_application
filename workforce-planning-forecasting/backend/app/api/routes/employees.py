from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee_service import create_employee, delete_employee, get_employee_by_id, get_employees, import_employees_csv, update_employee

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.get(
    "",
    response_model=dict,
    summary="Get employees",
    description="Return a paginated list of employees with optional filtering and search support.",
)
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(default=None),
    department_id: int | None = Query(default=None),
    job_role: str | None = Query(default=None),
    employment_type: str | None = Query(default=None),
    attrition_status: str | None = Query(default=None),
    location: str | None = Query(default=None),
    sort_by: str = Query(default="name", pattern="^(name|joining_date|salary|performance_score|employee_id)$"),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    return get_employees(
        db,
        page=page,
        page_size=page_size,
        search=search,
        department_id=department_id,
        job_role=job_role,
        employment_type=employment_type,
        attrition_status=attrition_status,
        location=location,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{employee_id}",
    response_model=dict,
    summary="Get single employee",
    description="Fetch a single employee record by employee ID.",
)
def read_employee(employee_id: str, db: Session = Depends(get_db)):
    return get_employee_by_id(db, employee_id)


@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Create employee",
    description="Create a new employee record after validating employee data and department existence.",
)
def create_new_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db, payload)


@router.put(
    "/{employee_id}",
    response_model=dict,
    summary="Update employee",
    description="Update an existing employee record by employee ID.",
)
def update_existing_employee(employee_id: str, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    return update_employee(db, employee_id, payload)


@router.delete(
    "/{employee_id}",
    summary="Delete employee",
    description="Delete an employee safely. Related attrition prediction records are removed with the employee.",
)
def delete_existing_employee(employee_id: str, db: Session = Depends(get_db)):
    return delete_employee(db, employee_id)


@router.post(
    "/import",
    summary="Import employees from CSV",
    description="Upload a CSV file containing employee records and import valid rows into the database.",
)
def import_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return import_employees_csv(db, file)
