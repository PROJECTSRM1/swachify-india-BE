from sqlalchemy import (
    JSON, Column, Integer, Numeric, String, Boolean,
    Date, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
from typing import Optional


class UserRegistration(Base):
    __tablename__ = "user_registration"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, nullable=False)

    first_name = Column(String(100))
    last_name = Column(String(100))

    email = Column(String(150), unique=True, nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    password = Column(String, nullable=False)

    gender_id = Column(Integer)
    dob = Column(Date)
    age = Column(Integer)


    role_id = Column(Integer, ForeignKey("master_role.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("master_status.id"), nullable=False)

    role = relationship("MasterRole", back_populates="users")
    status = relationship("MasterStatus")

    government_id = Column(JSON)
    experience_in_years = Column(String(50))

    state_id = Column(Integer)
    district_id = Column(Integer)
    address = Column(String(255))

    is_active = Column(Boolean, default=True)

    created_date = Column(DateTime, server_default=func.now())
    modified_date = Column(DateTime, onupdate=func.now())
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    services = relationship(
        "UserServices",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    skills = relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan"
    )
