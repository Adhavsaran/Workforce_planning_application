from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.employee import Employee
from app.models.forecast import Forecast


def get_dashboard_summary(db: Session) -> dict[str, Any]:
    employees = db.query(Employee).all()
    departments = db.query(Department).all()
    active = sum(1 for employee in employees if employee.attrition_status == "ACTIVE")
    left = sum(1 for employee in employees if employee.attrition_status == "LEFT")
    distribution = []
    for department in departments:
        count = db.query(Employee).filter(Employee.department_id == department.id).count()
        distribution.append({
            "department_id": department.id,
            "department_name": department.name,
            "employee_count": count,
        })
    return {
        "total_employees": len(employees),
        "total_departments": len(departments),
        "active_employees": active,
        "left_employees": left,
        "department_distribution": distribution,
    }


def get_gap_analysis(db: Session) -> dict[str, Any]:
    departments = db.query(Department).order_by(Department.name.asc()).all()
    gap_rows: list[dict[str, Any]] = []
    for department in departments:
        current_headcount = db.query(Employee).filter(Employee.department_id == department.id).count()
        forecast = (
            db.query(Forecast)
            .filter(Forecast.department_id == department.id)
            .order_by(Forecast.created_at.desc())
            .first()
        )
        forecast_headcount = forecast.forecasted_employee_count if forecast else current_headcount
        gap = forecast_headcount - current_headcount
        gap_rows.append({
            "department_id": department.id,
            "department_name": department.name,
            "current_supply": current_headcount,
            "forecast_demand": forecast_headcount,
            "gap": gap,
            "sign": "shortage" if gap > 0 else "surplus",
            "recommended_adjustment": max(gap, 0),
        })

    overall_gap = sum(item["gap"] for item in gap_rows)
    return {
        "analysis_period": "current workforce versus latest forecast",
        "sign_convention": "Gap = forecast workforce demand - current workforce supply. Positive values mean shortage; negative values mean surplus.",
        "overall_gap": overall_gap,
        "departments": gap_rows,
    }


def get_attrition_summary(db: Session) -> dict[str, Any]:
    employees = db.query(Employee).all()
    active = [employee for employee in employees if employee.attrition_status == "ACTIVE"]
    left = [employee for employee in employees if employee.attrition_status == "LEFT"]
    total = len(employees)

    at_risk = [
        {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "department_name": employee.department.name if employee.department else "Unassigned",
            "risk_label": "watchlist" if (employee.satisfaction_score < 6.0 or employee.performance_score < 75) else "monitor",
            "satisfaction_score": employee.satisfaction_score,
            "performance_score": employee.performance_score,
        }
        for employee in active
    ]

    by_department = []
    for department in db.query(Department).order_by(Department.name.asc()).all():
        dept_employees = [employee for employee in employees if employee.department_id == department.id]
        dept_left = sum(1 for employee in dept_employees if employee.attrition_status == "LEFT")
        by_department.append({
            "department_name": department.name,
            "total_employees": len(dept_employees),
            "employees_left": dept_left,
            "attrition_rate": round((dept_left / len(dept_employees)) * 100, 2) if dept_employees else 0.0,
        })

    return {
        "total_employees": total,
        "active_employees": len(active),
        "employees_left": len(left),
        "attrition_rate": round((len(left) / total) * 100, 2) if total else 0.0,
        "method": "Decision-support heuristic using current status, satisfaction, and performance indicators. It is not a validated individual risk model.",
        "at_risk_employees": at_risk,
        "by_department": by_department,
    }


def get_recommendations(db: Session) -> list[dict[str, Any]]:
    gap_analysis = get_gap_analysis(db)
    recommendations = []
    for item in gap_analysis["departments"]:
        gap = item["gap"]
        if gap > 0:
            rec_type = "HIRE"
            priority = "HIGH" if gap >= 5 else "MEDIUM"
            text = f"{item['department_name']} shows a staffing shortage of {gap} employees versus the latest workforce forecast. Review hiring plans and backfill critical roles."
        elif gap < 0:
            rec_type = "NO_HIRING"
            priority = "MEDIUM" if abs(gap) >= 3 else "LOW"
            text = f"{item['department_name']} has a projected surplus of {abs(gap)} employees versus current staffing. Consider redeployment or role consolidation."
        else:
            rec_type = "MONITOR"
            priority = "LOW"
            text = f"{item['department_name']} is tracking near current demand levels. Monitor capacity and business activity before making staffing changes."

        recommendations.append({
            "department_id": item["department_id"],
            "department_name": item["department_name"],
            "recommendation_type": rec_type,
            "priority": priority,
            "recommended_employee_count": max(abs(gap), 0),
            "recommendation_text": text,
            "supporting_data": {
                "current_supply": item["current_supply"],
                "forecast_demand": item["forecast_demand"],
                "gap": gap,
            },
        })

    return recommendations
