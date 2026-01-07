from sqlalchemy import (
    JSON, Column, Integer, String, Boolean,
    Date, DateTime, ForeignKey, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base
from models.master_status import MasterStatus
from models.master_role import MasterRole  # ✅ IMPORTANT


class UserRegistration(Base):
    __tablename__ = "user_registration"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, nullable=False)

    first_name = Column(String)
    last_name = Column(String)

    email = Column(String, unique=True, nullable=False)
    mobile = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    gender_id = Column(Integer)
    dob = Column(Date)
    age = Column(Integer)

    # ✅ WORK TYPE = ROLE
    role_id = Column(
        Integer,
        ForeignKey("master_role.id"),
        nullable=False
    )

    status_id = Column(
        Integer,
        ForeignKey("master_status.id"),
        default=2
    )

    is_active = Column(Boolean, default=True)

    # ✅ JSON government ID
    government_id = Column(JSON, nullable=True)

    profile_image = Column(String)
    experience_doc = Column(String)
    experience_summary = Column(String)

    skill_id = Column(Integer)

    # multiple services → JSON array

    state_id = Column(Integer)
    district_id = Column(Integer)

    created_by = Column(Integer)
    created_date = Column(DateTime, server_default=func.now())
    modified_by = Column(Integer)
    modified_date = Column(DateTime, onupdate=func.now())

    address = Column(String)

    # ✅ RELATIONSHIPS
    status = relationship("MasterStatus", lazy="joined")
    role = relationship("MasterRole", lazy="joined")
