from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Role(Base):
    __tablename__ = "Roles"
    __table_args__ = {"schema": "dbo"}

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(20), nullable=False)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    user_id = Column(String(40), primary_key=True, index=True)
    user_name = Column(String(40), nullable=False)
    user_password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("dbo.Roles.role_id"), nullable=False)
    email = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    role = relationship("Role", back_populates="users")
