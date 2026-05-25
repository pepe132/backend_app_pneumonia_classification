from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Evaluation(Base):
    __tablename__ = "Evaluations"
    __table_args__ = {"schema": "dbo"}

    evaluation_id = Column(String(40), primary_key=True, index=True)
    patient_id = Column(String(40), ForeignKey("dbo.Patients.patient_id"), nullable=False, index=True)
    created_by = Column(String(40), ForeignKey("dbo.Users.user_id"), nullable=False)

    edad_meses = Column(Integer, nullable=False)
    peso_kg = Column(Float, nullable=False)
    fr = Column(Integer, nullable=False)
    fc = Column(Integer, nullable=False)
    temperatura_c = Column(Float, nullable=False)
    spo2 = Column(Integer, nullable=False)
    tiraje = Column(Boolean, nullable=False, default=False)
    aleteo_nasal = Column(Boolean, nullable=False, default=False)
    quejido_espiratorio = Column(Boolean, nullable=False, default=False)
    cianosis = Column(Boolean, nullable=False, default=False)
    apnea = Column(Boolean, nullable=False, default=False)
    rechazo_comer = Column(Boolean, nullable=False, default=False)
    vomita_todo = Column(Boolean, nullable=False, default=False)
    convulsiones = Column(Boolean, nullable=False, default=False)
    glasgow = Column(Integer, nullable=False)
    desnutricion = Column(Boolean, nullable=False, default=False)
    antecedentes_cronicos = Column(Boolean, nullable=False, default=False)
    sibilancias = Column(Boolean, nullable=False, default=False)
    dias_sintomas = Column(Integer, nullable=False)
    dias_fiebre = Column(Integer, nullable=False)
    dias_tos = Column(Integer, nullable=False)
    dias_dificultad_respiratoria = Column(Integer, nullable=False)
    crepitantes = Column(Boolean, nullable=False, default=False)
    disminucion_murmullo_vesicular = Column(Boolean, nullable=False, default=False)
    dolor_toracico = Column(Boolean, nullable=False, default=False)

    severity_tabular = Column(String(20), nullable=True)
    prob_low = Column(Float, nullable=True)
    prob_medium = Column(Float, nullable=True)
    prob_high = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    patient = relationship("app.modules.patients.models.Patient")
    creator = relationship("app.modules.auth.models.User")
