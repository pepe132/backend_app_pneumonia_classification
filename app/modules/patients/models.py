from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Patient(Base):
    __tablename__ = "Patients"
    __table_args__ = {"schema": "dbo"}

    patient_id = Column(String(40), primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    age_months = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    guardian_name = Column(String(100), nullable=True)
    created_by = Column(String(40), ForeignKey("dbo.Users.user_id"), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("app.modules.auth.models.User")
