from sqlalchemy import Boolean, Column, Integer, Numeric, String, Date
from core.database import Base

class HomeService(Base):
    __tablename__ = "home_service"

    id = Column(Integer, primary_key=True, index=True)

    module_id = Column(Integer)
    sub_module_id = Column(Integer)
    service_id = Column(Integer)
    sub_service_id = Column(Integer)
    sub_group_id = Column(Integer)

    full_name = Column(String)
    email = Column(String)
    mobile = Column(String)
    address = Column(String)

    service_type_id = Column(Integer)
    problem_description = Column(String, nullable=True)
    property_size_sqft = Column(Integer, nullable=True)
    # add_on_id = Column(Integer, nullable=True)

    preferred_date = Column(Date)
    time_slot_id = Column(Integer)
    special_instructions = Column(String, nullable=True)
    payment_type_id = Column(Integer)

    service_price = Column(Numeric(10, 2), nullable=True)
    payment_done = Column(Boolean, default=False)