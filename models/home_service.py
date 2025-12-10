from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from core.database import Base

class HomeService(Base):
    __tablename__ = "home_service"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(15), nullable=False)
    address = Column(String(255), nullable=False)
    problem_description = Column(String(500))
    property_size_sqft = Column(Integer)
    preferred_date = Column(Date)
    special_instructions = Column(String(500))
    is_active = Column(Boolean, default=True)

    module_id = Column(Integer, ForeignKey("master_module.id"))
    sub_module_id = Column(Integer, ForeignKey("master_sub_module.id"))
    service_id = Column(Integer, ForeignKey("master_service.id"))
    sub_service_id = Column(Integer, ForeignKey("master_sub_service.id"))
    sub_group_id = Column(Integer, ForeignKey("master_sub_group.id"))
    service_type_id = Column(Integer, ForeignKey("master_service_type.id"))
    time_slot_id = Column(Integer, ForeignKey("master_time_slot.id"))
    add_on_id = Column(Integer, ForeignKey("master_add_on.id"))
    payment_type_id = Column(Integer, ForeignKey("master_payment_type.id"))

    module = relationship("MasterModule")
    sub_module = relationship("MasterSubModule")
    service = relationship("MasterService")
    sub_service = relationship("MasterSubService")
    sub_group = relationship("MasterSubGroup")
    service_type = relationship("MasterServiceType")
    time_slot = relationship("MasterTimeSlot")
    add_on = relationship("MasterAddOn")
    payment_type = relationship("MasterPaymentType")
