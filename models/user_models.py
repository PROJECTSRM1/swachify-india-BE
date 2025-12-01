from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP
from sqlalchemy.sql import text
from core.database import Base

class UserRegistration(Base):
    __tablename__ = "user_registration"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    mobile = Column(String(100), nullable=False)
    password = Column(String(500), nullable=False)

    gender_id = Column(Integer, nullable=False)  

    dob = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=True)
    state_id = Column(Integer, nullable=True)
    district_id = Column(Integer, nullable=True)

    created_by = Column(Integer, nullable=True)
    created_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(Integer, nullable=True)
    modified_date = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, server_default=text("true"))

