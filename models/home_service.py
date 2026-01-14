# # from sqlalchemy import (
# #     Boolean,
# #     Column,
# #     ForeignKey,
# #     Integer,
# #     Numeric,
# #     String,
# #     Date,
# #     DateTime
# # )
# # from sqlalchemy.sql import func
# # from sqlalchemy.orm import relationship
# # from core.database import Base


# # class HomeService(Base):
# #     __tablename__ = "home_service"

# #     # -------------------------
# #     # Primary Key
# #     # -------------------------
# #     id = Column(Integer, primary_key=True, index=True)

# #     # -------------------------
# #     # Service Hierarchy
# #     # -------------------------
# #     module_id = Column(Integer)
# #     sub_module_id = Column(Integer)
# #     service_id = Column(Integer)
# #     sub_service_id = Column(Integer)
# #     sub_group_id = Column(Integer)

# #     # -------------------------
# #     # Customer Details
# #     # -------------------------
# #     full_name = Column(String(150), nullable=False)
# #     email = Column(String(150), nullable=False)
# #     mobile = Column(String(20), nullable=False)
# #     address = Column(String(255), nullable=False)

# #     # -------------------------
# #     # Service Configuration
# #     # -------------------------
# #     service_type_id = Column(Integer, nullable=False)
# #     issue_id = Column(Integer, nullable=True)
# #     problem_description = Column(String, nullable=True)

# #     property_size_sqft = Column(Integer, nullable=True)
# #     duration_id = Column(Integer, nullable=False)

# #     # -------------------------
# #     # Schedule
# #     # -------------------------
# #     preferred_date = Column(Date, nullable=False)
# #     time_slot_id = Column(Integer, nullable=False)

# #     # -------------------------
# #     # Instructions & Payment
# #     # -------------------------
# #     special_instructions = Column(String, nullable=True)
# #     payment_type_id = Column(Integer, nullable=False)

# #     service_price = Column(Numeric(10, 2), nullable=True)
# #     payment_done = Column(Boolean, default=False)

# #     # -------------------------
# #     # Audit Fields
# #     # -------------------------
# #     created_by = Column(Integer, nullable=False)
# #     created_date = Column(DateTime, server_default=func.now())

# #     modified_by = Column(Integer, nullable=True)
# #     modified_date = Column(DateTime, onupdate=func.now())

# #     is_active = Column(Boolean, default=True)

# #     # -------------------------
# #     # Assignment & Status
# #     # -------------------------
# #     assigned_to = Column(
# #         Integer,
# #         ForeignKey("user_registration.id"),
# #         nullable=True
# #     )

# #     status_id = Column(
# #         Integer,
# #         ForeignKey("master_status.id"),
# #         nullable=False
# #     )

# #     # -------------------------
# #     # Relationships (SAFE)
# #     # -------------------------
# #     assigned_user = relationship(
# #         "UserRegistration",
# #         foreign_keys=[assigned_to],
# #         lazy="joined"
# #     )

# #     status = relationship(
# #         "MasterStatus",
# #         foreign_keys=[status_id],
# #         lazy="joined"
# #     )



# from sqlalchemy import (
#     Column, Integer, String, Boolean, Date, DateTime,
#     ForeignKey, Numeric
# )
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from core.database import Base

# class HomeService(Base):
#     __tablename__ = "home_service"

#     id = Column(Integer, primary_key=True)

#     module_id = Column(Integer)
#     service_id = Column(Integer)

#     full_name = Column(String(150), nullable=False)
#     email = Column(String(150), nullable=False)
#     mobile = Column(String(20), nullable=False)
#     address = Column(String(255), nullable=False)

#     preferred_date = Column(Date, nullable=False)
#     time_slot_id = Column(Integer, nullable=False)

#     payment_type_id = Column(Integer, nullable=False)
#     service_price = Column(Numeric(10, 2))
#     payment_done = Column(Boolean, default=False)

#     created_by = Column(Integer, nullable=False)
#     status_id = Column(Integer, ForeignKey("master_status.id"), nullable=False)

#     assigned_to = Column(Integer, ForeignKey("user_registration.id"))
#     is_active = Column(Boolean, default=True)

#     assigned_user = relationship("UserRegistration", foreign_keys=[assigned_to])
#     status = relationship("MasterStatus")

from sqlalchemy import (
    Column, Integer, BigInteger, String,
    Boolean, Date, DateTime, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base



class HomeService(Base):
    __tablename__ = "home_service"

    id = Column(BigInteger, primary_key=True, index=True)

    # Service hierarchy
    module_id = Column(Integer, nullable=False)
    sub_module_id = Column(Integer, nullable=False)
    service_id = Column(BigInteger, nullable=False)
    sub_service_id = Column(Integer, nullable=False)

    # Customer
    full_name = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False)
    mobile = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    others_address = Column(String(255), nullable=True)

    # Service details
    service_type_id = Column(Integer, nullable=False)
    issue_id = Column(BigInteger)
    problem_description = Column(String(500))
    property_size_sqft = Column(String(150))
    duration_id = Column(Integer, nullable=False)

    # Schedule
    preferred_date = Column(Date, nullable=False)
    time_slot_id = Column(Integer, nullable=False)

    # Payment
    payment_type_id = Column(Integer, nullable=False)
    service_price = Column(Numeric(10, 2))
    payment_done = Column(Boolean, default=False)

    # System fields
    created_by = Column(BigInteger, nullable=False)
    created_date = Column(DateTime, server_default=func.now())
    modified_by = Column(BigInteger)
    modified_date = Column(DateTime, onupdate=func.now())

    assigned_to = Column(BigInteger)
    status_id = Column(Integer, nullable=False, default=1)
    work_status_id = Column(
        Integer,
        ForeignKey("master_work_status.id"),
        nullable=False
    )  
    rating = Column(Integer)
    is_active = Column(Boolean, default=True)


work_status = relationship(
        "MasterWorkStatus",
        lazy="joined"
    )