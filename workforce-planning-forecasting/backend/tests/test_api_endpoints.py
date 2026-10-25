from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.database import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def override_db() -> None:
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_create_and_get_employee(client: TestClient) -> None:
    department_response = client.post("/api/departments", json={"name": "IT", "description": "Technology"})
    assert department_response.status_code == 201
    department_id = department_response.json()["id"]

    employee_payload = {
        "employee_id": "EMP1001",
        "name": "John Doe",
        "department_id": department_id,
        "job_role": "Software Engineer",
        "age": 30,
        "gender": "M",
        "experience_years": 4,
        "joining_date": "2021-01-15",
        "salary": 120000,
        "performance_score": 88,
        "satisfaction_score": 8.5,
        "employment_type": "FULL_TIME",
        "location": "Chennai",
        "attrition_status": "ACTIVE",
    }

    create_response = client.post("/api/employees", json=employee_payload)
    assert create_response.status_code == 201

    list_response = client.get("/api/employees")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    single_response = client.get("/api/employees/EMP1001")
    assert single_response.status_code == 200
    assert single_response.json()["name"] == "John Doe"


def test_get_employees_supports_search_and_filters(client: TestClient) -> None:
    dep = client.post("/api/departments", json={"name": "Sales", "description": "Sales"})
    department_id = dep.json()["id"]
    client.post(
        "/api/employees",
        json={
            "employee_id": "EMP2001",
            "name": "Amelia Stone",
            "department_id": department_id,
            "job_role": "Sales Executive",
            "age": 28,
            "gender": "F",
            "experience_years": 3,
            "joining_date": "2023-06-10",
            "salary": 95000,
            "performance_score": 82,
            "satisfaction_score": 7.8,
            "employment_type": "FULL_TIME",
            "location": "Bengaluru",
            "attrition_status": "ACTIVE",
        },
    )

    response = client.get("/api/employees?search=Amelia&department_id={}&employment_type=FULL_TIME".format(department_id))
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_update_employee_and_duplicate_validation(client: TestClient) -> None:
    department = client.post("/api/departments", json={"name": "HR", "description": "Human Resources"})
    department_id = department.json()["id"]

    employee = client.post(
        "/api/employees",
        json={
            "employee_id": "EMP3001",
            "name": "Riya Shah",
            "department_id": department_id,
            "job_role": "HR Specialist",
            "age": 27,
            "gender": "F",
            "experience_years": 2,
            "joining_date": "2022-09-01",
            "salary": 85000,
            "performance_score": 80,
            "satisfaction_score": 8.1,
            "employment_type": "FULL_TIME",
            "location": "Pune",
            "attrition_status": "ACTIVE",
        },
    )
    assert employee.status_code == 201

    update_response = client.put(
        "/api/employees/EMP3001",
        json={"salary": 90000, "location": "Mumbai"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["salary"] == 90000
    assert update_response.json()["location"] == "Mumbai"

    duplicate_response = client.post(
        "/api/employees",
        json={
            "employee_id": "EMP3001",
            "name": "Duplicate Person",
            "department_id": department_id,
            "job_role": "Analyst",
            "age": 32,
            "gender": "M",
            "experience_years": 5,
            "joining_date": "2020-02-01",
            "salary": 97000,
            "performance_score": 83,
            "satisfaction_score": 7.4,
            "employment_type": "PART_TIME",
            "location": "Delhi",
            "attrition_status": "ACTIVE",
        },
    )
    assert duplicate_response.status_code == 409


def test_delete_employee_and_department_validation(client: TestClient) -> None:
    department = client.post("/api/departments", json={"name": "Finance", "description": "Finance"})
    dept_id = department.json()["id"]

    employee = client.post(
        "/api/employees",
        json={
            "employee_id": "EMP4001",
            "name": "Aarav Mehta",
            "department_id": dept_id,
            "job_role": "Finance Manager",
            "age": 35,
            "gender": "M",
            "experience_years": 9,
            "joining_date": "2019-04-10",
            "salary": 160000,
            "performance_score": 91,
            "satisfaction_score": 7.9,
            "employment_type": "FULL_TIME",
            "location": "Hyderabad",
            "attrition_status": "ACTIVE",
        },
    )
    assert employee.status_code == 201

    delete_response = client.delete("/api/employees/EMP4001")
    assert delete_response.status_code == 200
    assert "deleted successfully" in delete_response.json()["detail"]

    missing_employee = client.get("/api/employees/EMP4001")
    assert missing_employee.status_code == 404

    delete_department = client.delete(f"/api/departments/{dept_id}")
    assert delete_department.status_code == 200


def test_department_list_and_employee_listing(client: TestClient) -> None:
    create_response = client.post("/api/departments", json={"name": "Operations", "description": "Operations team"})
    assert create_response.status_code == 201
    department_id = create_response.json()["id"]

    employee_response = client.post(
        "/api/employees",
        json={
            "employee_id": "EMP5001",
            "name": "Neha Rao",
            "department_id": department_id,
            "job_role": "Operations Lead",
            "age": 34,
            "gender": "F",
            "experience_years": 7,
            "joining_date": "2018-05-12",
            "salary": 110000,
            "performance_score": 87,
            "satisfaction_score": 8.4,
            "employment_type": "FULL_TIME",
            "location": "Kolkata",
            "attrition_status": "ACTIVE",
        },
    )
    assert employee_response.status_code == 201

    departments_response = client.get("/api/departments")
    assert departments_response.status_code == 200
    assert any(item["name"] == "Operations" for item in departments_response.json())

    department_employees = client.get(f"/api/departments/{department_id}/employees")
    assert department_employees.status_code == 200
    assert department_employees.json()[0]["employee_id"] == "EMP5001"


def test_invalid_employee_inputs_and_pagination(client: TestClient) -> None:
    department = client.post("/api/departments", json={"name": "Marketing", "description": "Brand"})
    department_id = department.json()["id"]

    for idx in range(3):
        employee_payload = {
            "employee_id": f"EMP60{idx}",
            "name": f"Person {idx}",
            "department_id": department_id,
            "job_role": "Marketing Analyst",
            "age": 26 + idx,
            "gender": "F" if idx % 2 == 0 else "M",
            "experience_years": 2 + idx,
            "joining_date": "2022-01-01",
            "salary": 70000 + idx * 5000,
            "performance_score": 78 + idx,
            "satisfaction_score": 7.0 + idx / 10,
            "employment_type": "FULL_TIME",
            "location": "Delhi",
            "attrition_status": "ACTIVE",
        }
        create_response = client.post("/api/employees", json=employee_payload)
        assert create_response.status_code == 201

    invalid_salary = client.post(
        "/api/employees",
        json={
            "employee_id": "EMP9999",
            "name": "Bad Salary",
            "department_id": department_id,
            "job_role": "Marketing Analyst",
            "age": 29,
            "gender": "F",
            "experience_years": 4,
            "joining_date": "2023-01-02",
            "salary": -100,
            "performance_score": 80,
            "satisfaction_score": 7.9,
            "employment_type": "FULL_TIME",
            "location": "Jaipur",
            "attrition_status": "ACTIVE",
        },
    )
    assert invalid_salary.status_code == 422

    paginated = client.get("/api/employees?page=1&page_size=2")
    assert paginated.status_code == 200
    assert paginated.json()["page_size"] == 2
    assert paginated.json()["total"] >= 3


def test_csv_import_valid_and_invalid(client: TestClient) -> None:
    department = client.post("/api/departments", json={"name": "Customer Success", "description": "Support"})
    dept_name = department.json()["name"]

    csv_content = (
        "employee_id,name,department,job_role,age,gender,experience_years,joining_date,salary,performance_score,satisfaction_score,employment_type,location,attrition_status\n"
        "EMP7001,Test User1,{dept},Support Analyst,29,F,4.5,2022-02-15,80000,82,8.2,FULL_TIME,Chennai,ACTIVE\n"
        "EMP7002,Test User2,{dept},Client Partner,33,M,6.0,2021-01-20,98000,85,7.9,FULL_TIME,Bangalore,ACTIVE\n"
    ).format(dept=dept_name)

    valid_csv = client.post(
        "/api/employees/import",
        files={"file": ("employees.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")},
    )
    assert valid_csv.status_code == 200
    assert valid_csv.json()["successfully_imported"] == 2

    invalid_csv = client.post(
        "/api/employees/import",
        files={"file": ("bad.csv", io.BytesIO(b"employee_id,name\nEMP8001,Bad Row\n"), "text/csv")},
    )
    assert invalid_csv.status_code == 400


def test_health_endpoint(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] in {"healthy", "degraded"}
