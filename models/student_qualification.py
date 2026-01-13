

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base


class StudentQualification(Base):
    __tablename__ = "student_qualification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_registration.id"), nullable=False)

    degree = Column(String(255), nullable=False)
    institute = Column(String(255), nullable=False)
    percentage = Column(String(255), nullable=False)

    created_by = Column(Integer)
    created_date = Column(DateTime, server_default=func.now())

    modified_by = Column(Integer, nullable=True)
    modified_date = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)
