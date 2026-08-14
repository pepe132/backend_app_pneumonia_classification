"""Baseline del backend de neumonía pediátrica.

Revision ID: 20260811_0001
Revises: None
Create Date: 2026-08-11
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260811_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "Roles",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("role_name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("role_id", name="PK_Roles"),
        schema="dbo",
    )
    op.execute("SET IDENTITY_INSERT dbo.Roles ON")
    op.bulk_insert(
        sa.table(
            "Roles",
            sa.column("role_id", sa.Integer()),
            sa.column("role_name", sa.String(length=20)),
            schema="dbo",
        ),
        [
            {"role_id": 1, "role_name": "ADMINISTRADOR"},
            {"role_id": 2, "role_name": "ESPECIALISTA"},
            {"role_id": 3, "role_name": "LECTURA"},
        ],
    )
    op.execute("SET IDENTITY_INSERT dbo.Roles OFF")
    op.create_table(
        "Users",
        sa.Column("user_id", sa.String(length=40), nullable=False),
        sa.Column("user_name", sa.String(length=40), nullable=False),
        sa.Column("user_password", sa.String(length=100), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("GETDATE()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["dbo.Roles.role_id"], name="FK_Users_role_id"),
        sa.PrimaryKeyConstraint("user_id", name="PK_Users"),
        schema="dbo",
    )
    op.create_index("IX_Users_user_id", "Users", ["user_id"], unique=False, schema="dbo")
    op.create_table(
        "Patients",
        sa.Column("patient_id", sa.String(length=40), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("age_months", sa.Integer(), nullable=False),
        sa.Column("sex", sa.String(length=10), nullable=False),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("height", sa.Float(), nullable=True),
        sa.Column("guardian_name", sa.String(length=100), nullable=True),
        sa.Column("created_by", sa.String(length=40), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("GETDATE()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("age_months >= 0 AND age_months <= 72", name="CK_Patients_age_months_range"),
        sa.ForeignKeyConstraint(["created_by"], ["dbo.Users.user_id"], name="FK_Patients_Users"),
        sa.PrimaryKeyConstraint("patient_id", name="PK_Patients"),
        schema="dbo",
    )
    op.create_index("IX_Patients_patient_id", "Patients", ["patient_id"], unique=False, schema="dbo")
    op.create_table(
        "Evaluations",
        sa.Column("evaluation_id", sa.String(length=40), nullable=False),
        sa.Column("patient_id", sa.String(length=40), nullable=False),
        sa.Column("created_by", sa.String(length=40), nullable=False),
        sa.Column("edad_meses", sa.Integer(), nullable=False),
        sa.Column("peso_kg", sa.Float(), nullable=False),
        sa.Column("fr", sa.Integer(), nullable=False),
        sa.Column("fc", sa.Integer(), nullable=False),
        sa.Column("temperatura_c", sa.Float(), nullable=False),
        sa.Column("spo2", sa.Integer(), nullable=False),
        sa.Column("tiraje", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("retraccion_xifoidea", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("disociacion_toracoabdominal", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("aleteo_nasal", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("quejido_espiratorio", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("cianosis", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("apnea", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("rechazo_comer", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("vomita_todo", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("convulsiones", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("glasgow", sa.Integer(), nullable=False),
        sa.Column("desnutricion", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("antecedentes_cronicos", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("sibilancias", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("dias_sintomas", sa.Integer(), nullable=False),
        sa.Column("dias_fiebre", sa.Integer(), nullable=False),
        sa.Column("dias_tos", sa.Integer(), nullable=False),
        sa.Column("dias_dificultad_respiratoria", sa.Integer(), nullable=False),
        sa.Column("crepitantes", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("disminucion_murmullo_vesicular", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("dolor_toracico", sa.Boolean(), server_default=sa.text("0"), nullable=False),
        sa.Column("severity_tabular", sa.String(length=20), nullable=True),
        sa.Column("prob_low", sa.Float(), nullable=True),
        sa.Column("prob_medium", sa.Float(), nullable=True),
        sa.Column("prob_high", sa.Float(), nullable=True),
        sa.Column("final_severity", sa.String(length=20), nullable=True),
        sa.Column("radiographic_support", sa.String(length=40), nullable=True),
        sa.Column("concordance", sa.String(length=30), nullable=True),
        sa.Column("fusion_basis", sa.String(length=40), nullable=True),
        sa.Column("fusion_explanation", sa.String(length=500), nullable=True),
        sa.Column("recommendation_code", sa.String(length=50), nullable=True),
        sa.Column("fusion_version", sa.String(length=30), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
        sa.CheckConstraint("edad_meses >= 0 AND edad_meses <= 72", name="CK_Evaluations_edad_meses_range"),
        sa.CheckConstraint("peso_kg > 0 AND peso_kg <= 150", name="CK_Evaluations_peso_kg_range"),
        sa.CheckConstraint("glasgow >= 3 AND glasgow <= 15", name="CK_Evaluations_glasgow_range"),
        sa.CheckConstraint("dias_dificultad_respiratoria >= 0 AND dias_dificultad_respiratoria <= 60", name="CK_Evaluations_dias_dificultad_range"),
        sa.ForeignKeyConstraint(["patient_id"], ["dbo.Patients.patient_id"], name="FK_Evaluations_Patients"),
        sa.ForeignKeyConstraint(["created_by"], ["dbo.Users.user_id"], name="FK_Evaluations_Users"),
        sa.PrimaryKeyConstraint("evaluation_id", name="PK_Evaluations"),
        schema="dbo",
    )
    op.create_index("IX_Evaluations_evaluation_id", "Evaluations", ["evaluation_id"], unique=False, schema="dbo")
    op.create_index("IX_Evaluations_patient_id", "Evaluations", ["patient_id"], unique=False, schema="dbo")
    op.create_table(
        "Radiographs",
        sa.Column("radiograph_id", sa.String(length=40), nullable=False),
        sa.Column("evaluation_id", sa.String(length=40), nullable=False),
        sa.Column("uploaded_by", sa.String(length=40), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("image_class", sa.String(length=40), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("prob_covid", sa.Float(), nullable=False),
        sa.Column("prob_normal", sa.Float(), nullable=False),
        sa.Column("prob_bacterial", sa.Float(), nullable=False),
        sa.Column("prob_viral", sa.Float(), nullable=False),
        sa.Column("model_version", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("SYSDATETIMEOFFSET()"), nullable=False),
        sa.ForeignKeyConstraint(["evaluation_id"], ["dbo.Evaluations.evaluation_id"], name="FK_Radiographs_Evaluations"),
        sa.ForeignKeyConstraint(["uploaded_by"], ["dbo.Users.user_id"], name="FK_Radiographs_Users"),
        sa.PrimaryKeyConstraint("radiograph_id", name="PK_Radiographs"),
        sa.UniqueConstraint("evaluation_id", name="UQ_Radiographs_evaluation_id"),
        schema="dbo",
    )
    op.create_index("IX_Radiographs_radiograph_id", "Radiographs", ["radiograph_id"], unique=False, schema="dbo")


def downgrade() -> None:
    op.drop_index("IX_Radiographs_radiograph_id", table_name="Radiographs", schema="dbo")
    op.drop_table("Radiographs", schema="dbo")
    op.drop_index("IX_Evaluations_patient_id", table_name="Evaluations", schema="dbo")
    op.drop_index("IX_Evaluations_evaluation_id", table_name="Evaluations", schema="dbo")
    op.drop_table("Evaluations", schema="dbo")
    op.drop_index("IX_Patients_patient_id", table_name="Patients", schema="dbo")
    op.drop_table("Patients", schema="dbo")
    op.drop_index("IX_Users_user_id", table_name="Users", schema="dbo")
    op.drop_table("Users", schema="dbo")
    op.drop_table("Roles", schema="dbo")
