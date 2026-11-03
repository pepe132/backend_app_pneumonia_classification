from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Radiograph(Base):
    __tablename__ = "Radiographs"
    __table_args__ = {"schema": "dbo"}

    radiograph_id = Column(String(40), primary_key=True, index=True)
    evaluation_id = Column(
        String(40),
        ForeignKey("dbo.Evaluations.evaluation_id"),
        nullable=False,
        unique=True,
        index=True,
    )
    uploaded_by = Column(String(40), ForeignKey("dbo.Users.user_id"), nullable=False)

    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)

    image_class = Column(String(40), nullable=False)
    confidence = Column(Float, nullable=False)
    prob_covid = Column(Float, nullable=False)
    prob_normal = Column(Float, nullable=False)
    prob_bacterial = Column(Float, nullable=False)
    prob_viral = Column(Float, nullable=False)
    model_version = Column(String(100), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    evaluation = relationship("Evaluation", back_populates="radiograph")
    uploader = relationship("User")
