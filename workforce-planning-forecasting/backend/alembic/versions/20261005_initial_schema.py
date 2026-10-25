"""Initial database schema for workforce planning and forecasting.

Revision ID: 20261005_initial_schema
Revises: 
Create Date: 2026-10-05 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20261005_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_departments_id"), "departments", ["id"], unique=False)
    op.create_index(op.f("ix_departments_name"), "departments", ["name"], unique=True)

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("job_role", sa.String(length=100), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("gender", sa.String(length=30), nullable=False),
        sa.Column("experience_years", sa.Float(), nullable=False),
        sa.Column("joining_date", sa.Date(), nullable=False),
        sa.Column("salary", sa.Float(), nullable=False),
        sa.Column("performance_score", sa.Float(), nullable=False),
        sa.Column("satisfaction_score", sa.Float(), nullable=False),
        sa.Column("employment_type", sa.String(length=30), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=False),
        sa.Column("attrition_status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("employee_id"),
    )
    op.create_index(op.f("ix_employees_department_id"), "employees", ["department_id"], unique=False)
    op.create_index(op.f("ix_employees_employee_id"), "employees", ["employee_id"], unique=True)
    op.create_index(op.f("ix_employees_id"), "employees", ["id"], unique=False)

    op.create_table(
        "workforce_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.SmallInteger(), nullable=False),
        sa.Column("employee_count", sa.Integer(), nullable=False),
        sa.Column("employees_hired", sa.Integer(), nullable=False),
        sa.Column("employees_left", sa.Integer(), nullable=False),
        sa.Column("business_growth", sa.Float(), nullable=False),
        sa.Column("project_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("department_id", "year", "month", name="uq_workforce_history_department_year_month"),
    )
    op.create_index(op.f("ix_workforce_history_department_id"), "workforce_history", ["department_id"], unique=False)
    op.create_index(op.f("ix_workforce_history_id"), "workforce_history", ["id"], unique=False)

    op.create_table(
        "forecasts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("forecast_period", sa.String(length=50), nullable=False),
        sa.Column("forecasted_employee_count", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_forecasts_department_id"), "forecasts", ["department_id"], unique=False)
    op.create_index(op.f("ix_forecasts_id"), "forecasts", ["id"], unique=False)

    op.create_table(
        "attrition_predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("prediction_date", sa.Date(), nullable=False),
        sa.Column("attrition_probability", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(length=20), nullable=False),
        sa.Column("model_name", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_attrition_predictions_employee_id"), "attrition_predictions", ["employee_id"], unique=False)
    op.create_index(op.f("ix_attrition_predictions_id"), "attrition_predictions", ["id"], unique=False)

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=True),
        sa.Column("recommendation_type", sa.String(length=40), nullable=False),
        sa.Column("recommendation_text", sa.String(length=500), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("recommended_employee_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendations_department_id"), "recommendations", ["department_id"], unique=False)
    op.create_index(op.f("ix_recommendations_id"), "recommendations", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_recommendations_id"), table_name="recommendations")
    op.drop_index(op.f("ix_recommendations_department_id"), table_name="recommendations")
    op.drop_table("recommendations")

    op.drop_index(op.f("ix_attrition_predictions_id"), table_name="attrition_predictions")
    op.drop_index(op.f("ix_attrition_predictions_employee_id"), table_name="attrition_predictions")
    op.drop_table("attrition_predictions")

    op.drop_index(op.f("ix_forecasts_id"), table_name="forecasts")
    op.drop_index(op.f("ix_forecasts_department_id"), table_name="forecasts")
    op.drop_table("forecasts")

    op.drop_index(op.f("ix_workforce_history_id"), table_name="workforce_history")
    op.drop_index(op.f("ix_workforce_history_department_id"), table_name="workforce_history")
    op.drop_table("workforce_history")

    op.drop_index(op.f("ix_employees_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_employee_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_department_id"), table_name="employees")
    op.drop_table("employees")

    op.drop_index(op.f("ix_departments_name"), table_name="departments")
    op.drop_index(op.f("ix_departments_id"), table_name="departments")
    op.drop_table("departments")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
