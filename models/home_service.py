
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

    module_id = Column(Integer, nullable=False)
    sub_module_id = Column(Integer, nullable=False)
    service_id = Column(BigInteger, nullable=False)
    sub_service_id = Column(Integer, nullable=False)

    full_name = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False)
    mobile = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    others_address = Column(String(255), nullable=True)

    service_type_id = Column(Integer, nullable=False)
    issue_id = Column(BigInteger)
    problem_description = Column(String(500))
    property_size_sqft = Column(String(150))
    duration_id = Column(Integer, nullable=False)

    preferred_date = Column(Date, nullable=False)
    time_slot_id = Column(Integer, nullable=False)

    payment_type_id = Column(Integer, nullable=False)
    service_price = Column(Numeric(10, 2))
    payment_done = Column(Boolean, default=False)

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
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    is_active = Column(Boolean, default=True)


work_status = relationship(
        "MasterWorkStatus",
        lazy="joined"
    )