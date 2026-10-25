from __future__ import annotations

from datetime import date

from app.db.database import SessionLocal, create_db_and_tables
from app.models.department import Department
from app.models.employee import Employee
from app.models.forecast import Forecast
from app.models.user import User
from app.models.workforce_history import WorkforceHistory


DEPARTMENT_NAMES = ["IT", "HR", "Finance", "Sales", "Marketing", "Operations"]


def seed_departments(db_session) -> dict[str, int]:
    dept_map: dict[str, int] = {}
    for name in DEPARTMENT_NAMES:
        department = db_session.query(Department).filter(Department.name == name).first()
        if department is None:
            department = Department(name=name, description=f"{name} department")
            db_session.add(department)
            db_session.commit()
            db_session.refresh(department)
        dept_map[name] = department.id
    return dept_map


def seed_users(db_session) -> None:
    existing = db_session.query(User).filter(User.email == "admin@workforce.local").first()
    if existing is None:
        admin_user = User(
            username="hr_admin",
            email="admin@workforce.local",
            password_hash="hashed_password_for_development_only",
            role="HR_ADMIN",
            is_active=True,
        )
        db_session.add(admin_user)
        db_session.commit()


def seed_employees(db_session, departments: dict[str, int]) -> None:
    employees = [
        ("EMP001", "Aisha Khan", "IT", "Senior Software Engineer", 31, "F", 7.5, "2021-04-15", 145000, 92, 8.7, "FULL_TIME", "Chicago", "ACTIVE"),
        ("EMP002", "Daniel Lewis", "IT", "Data Analyst", 28, "M", 4.2, "2022-03-12", 97000, 88, 8.3, "FULL_TIME", "New York", "ACTIVE"),
        ("EMP003", "Priya Nair", "Finance", "Financial Analyst", 34, "F", 6.1, "2019-11-08", 110000, 86, 7.9, "FULL_TIME", "Boston", "ACTIVE"),
        ("EMP004", "Marcus Reed", "Sales", "Account Executive", 29, "M", 5.4, "2023-01-25", 88000, 81, 7.6, "FULL_TIME", "Atlanta", "ACTIVE"),
        ("EMP005", "Sofia Gomez", "HR", "HR Manager", 36, "F", 9.0, "2017-06-19", 122000, 89, 8.8, "FULL_TIME", "Austin", "ACTIVE"),
        ("EMP006", "Ethan Brooks", "Operations", "Operations Manager", 40, "M", 12.5, "2015-02-02", 138000, 90, 8.4, "FULL_TIME", "Denver", "ACTIVE"),
        ("EMP007", "Maya Singh", "Marketing", "Brand Manager", 33, "F", 7.0, "2020-08-14", 101000, 87, 8.2, "FULL_TIME", "Seattle", "ACTIVE"),
        ("EMP008", "Nathan White", "IT", "DevOps Engineer", 27, "M", 3.8, "2023-05-10", 93000, 85, 8.1, "FULL_TIME", "Portland", "ACTIVE"),
        ("EMP009", "Olivia Chen", "Finance", "Controller", 42, "F", 15.2, "2012-09-17", 154000, 93, 8.9, "FULL_TIME", "Chicago", "ACTIVE"),
        ("EMP010", "James Patel", "Sales", "Sales Lead", 38, "M", 11.0, "2018-04-22", 128000, 85, 7.8, "FULL_TIME", "Miami", "ACTIVE"),
        ("EMP011", "Lucia Silva", "HR", "Recruitment Specialist", 26, "F", 2.9, "2024-02-05", 76000, 79, 8.0, "FULL_TIME", "Houston", "ACTIVE"),
        ("EMP012", "Charles Young", "Operations", "Logistics Analyst", 30, "M", 5.1, "2021-07-29", 82000, 80, 7.5, "FULL_TIME", "Dallas", "ACTIVE"),
        ("EMP013", "Anna Hall", "Marketing", "Marketing Analyst", 29, "F", 4.6, "2022-08-18", 87000, 82, 7.9, "FULL_TIME", "Los Angeles", "ACTIVE"),
        ("EMP014", "David Kim", "IT", "QA Engineer", 32, "M", 6.4, "2020-10-11", 99000, 84, 8.3, "FULL_TIME", "Phoenix", "ACTIVE"),
        ("EMP015", "Rina Joseph", "Finance", "Payroll Specialist", 25, "F", 2.5, "2024-06-02", 69000, 77, 7.4, "FULL_TIME", "San Diego", "ACTIVE"),
        ("EMP016", "Leo Martin", "Sales", "Customer Success Manager", 35, "M", 8.7, "2019-01-09", 115000, 88, 8.5, "FULL_TIME", "Charlotte", "ACTIVE"),
        ("EMP017", "Hannah Green", "Operations", "Supply Chain Analyst", 31, "F", 5.9, "2021-11-30", 91000, 82, 8.0, "FULL_TIME", "Minneapolis", "ACTIVE"),
        ("EMP018", "Omar Ali", "IT", "Machine Learning Engineer", 34, "M", 8.3, "2019-03-14", 142000, 91, 8.6, "FULL_TIME", "Boston", "ACTIVE"),
    ]

    for employee in employees:
        employee_id, name, dept_name, job_role, age, gender, experience_years, joining_date, salary, performance_score, satisfaction_score, employment_type, location, attrition_status = employee
        existing = db_session.query(Employee).filter(Employee.employee_id == employee_id).first()
        if existing is None:
            db_session.add(
                Employee(
                    employee_id=employee_id,
                    name=name,
                    department_id=departments[dept_name],
                    job_role=job_role,
                    age=age,
                    gender=gender,
                    experience_years=experience_years,
                    joining_date=date.fromisoformat(joining_date),
                    salary=salary,
                    performance_score=performance_score,
                    satisfaction_score=satisfaction_score,
                    employment_type=employment_type,
                    location=location,
                    attrition_status=attrition_status,
                )
            )
    db_session.commit()


def seed_workforce_history(db_session, departments: dict[str, int]) -> None:
    history_rows = []
    for dept_name in DEPARTMENT_NAMES:
        dept_id = departments[dept_name]
        for year, month, employee_count, hired, left, growth, project in [
            (2024, 1, 90, 7, 2, 1.5, 8),
            (2024, 2, 94, 6, 2, 2.2, 9),
            (2024, 3, 98, 8, 3, 2.8, 11),
            (2024, 4, 102, 7, 3, 3.1, 12),
            (2024, 5, 108, 10, 2, 4.4, 13),
            (2024, 6, 112, 9, 2, 4.7, 14),
            (2025, 1, 116, 8, 3, 3.6, 12),
            (2025, 2, 118, 7, 2, 3.9, 13),
            (2025, 3, 122, 9, 3, 4.1, 14),
        ]:
            history_rows.append(
                WorkforceHistory(
                    department_id=dept_id,
                    year=year,
                    month=month,
                    employee_count=employee_count,
                    employees_hired=hired,
                    employees_left=left,
                    business_growth=growth,
                    project_count=project,
                )
            )
    for row in history_rows:
        existing = db_session.query(WorkforceHistory).filter(
            WorkforceHistory.department_id == row.department_id,
            WorkforceHistory.year == row.year,
            WorkforceHistory.month == row.month,
        ).first()
        if existing is None:
            db_session.add(row)
    db_session.commit()


def seed_forecasts(db_session, departments: dict[str, int]) -> None:
    for dept_name in DEPARTMENT_NAMES:
        dept_id = departments[dept_name]
        forecast = Forecast(
            department_id=dept_id,
            forecast_period="2027-Q4",
            forecasted_employee_count=120 + (len(DEPARTMENT_NAMES) * 5),
            model_name="Linear Regression",
            confidence_score=0.86,
        )
        db_session.add(forecast)
    db_session.commit()


def main() -> None:
    create_db_and_tables()
    db_session = SessionLocal()
    try:
        seed_users(db_session)
        departments = seed_departments(db_session)
        seed_employees(db_session, departments)
        seed_workforce_history(db_session, departments)
        seed_forecasts(db_session, departments)
        db_session.commit()
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
