# from sqlalchemy import (
#     JSON, Column, Integer, String, Boolean,
#     Date, DateTime, ForeignKey
# )
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from core.database import Base
# from models.master_role import MasterRole
# from models.master_status import MasterStatus

# class UserRegistration(Base):
#     __tablename__ = "user_registration"

#     id = Column(Integer, primary_key=True, index=True)
#     unique_id = Column(String, nullable=False)

#     first_name = Column(String)
#     last_name = Column(String)

#     email = Column(String, unique=True, nullable=False)
#     mobile = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)

#     gender_id = Column(Integer)
#     dob = Column(Date)
#     age = Column(Integer)

#     role_id = Column(Integer, ForeignKey("master_role.id"), nullable=False)
#     status_id = Column(Integer, ForeignKey("master_status.id"), default=2)

#     is_active = Column(Boolean, default=True)

#     government_id = Column(JSON)
#     experience_in_years = Column(String(255))

#     user_services_id = Column(Integer, ForeignKey("user_services.id"))
#     user_skill_id = Column(Integer, ForeignKey("user_skill.id"))

#     state_id = Column(Integer)
#     district_id = Column(Integer)
#     address = Column(String)

#     created_date = Column(DateTime, server_default=func.now())
#     modified_date = Column(DateTime, onupdate=func.now())

#     # ✅ REQUIRED relationships
#     role = relationship(
#         "MasterRole",
#         back_populates="users"
#     )

#     status = relationship(
#         "MasterStatus"
#     )
#     services = relationship(
#         "UserServices",
#         foreign_keys="UserServices.user_id",
#         back_populates="user"
#     )
#     skills = relationship(
#         "UserSkill",
#         foreign_keys="UserSkill.user_id",
#         back_populates="user"
#     )




from sqlalchemy import (
    JSON, Column, Integer, String, Boolean,
    Date, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base


class UserRegistration(Base):
    __tablename__ = "user_registration"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, nullable=False)

    # -------------------------
    # Personal Info
    # -------------------------
    first_name = Column(String(100))
    last_name = Column(String(100))

    email = Column(String(150), unique=True, nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    password = Column(String, nullable=False)

    gender_id = Column(Integer)
    dob = Column(Date)
    age = Column(Integer)

    # -------------------------
    # Role & Status
    # -------------------------
    role_id = Column(Integer, ForeignKey("master_role.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("master_status.id"), nullable=False)

    role = relationship("MasterRole", back_populates="users")
    status = relationship("MasterStatus")

    # -------------------------
    # Professional
    # -------------------------
    government_id = Column(JSON)
    experience_in_years = Column(String(50))

    # -------------------------
    # Address
    # -------------------------
    state_id = Column(Integer)
    district_id = Column(Integer)
    address = Column(String(255))

    is_active = Column(Boolean, default=True)

    created_date = Column(DateTime, server_default=func.now())
    modified_date = Column(DateTime, onupdate=func.now())

    # -------------------------
    # RELATION TABLES (IMPORTANT)
    # -------------------------
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
