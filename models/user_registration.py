from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.sql import func
from core.database import Base


class UserRegistration(Base):
    __tablename__ = "user_registration"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender_id = Column(Integer)
    dob = Column(Date)
    age = Column(Integer)
    role_id = Column(Integer, nullable=False)
    state_id = Column(Integer)
    district_id = Column(Integer)
    created_by = Column(Integer)
    created_date = Column(DateTime, server_default=func.now())
    modified_by = Column(Integer)
    modified_date = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)

    profile_image = Column(String)
    skill_id = Column(Integer)
    experience_summary = Column(String)
    experience_doc = Column(String)
    government_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    unique_id = Column(String)
    address = Column(String)
