from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(40), primary_key=True, index=True)
    user_name = Column(String(40), unique=True, nullable=False, index=True)
    user_password = Column(String(80), nullable=True)
    role_id = Column(Integer, nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
