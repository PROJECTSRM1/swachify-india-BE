from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base

class MasterTimeSlot(Base):
    __tablename__ = "master_time_slot"

    id = Column(Integer, primary_key=True, index=True)
    time_slot = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # relation to home service
    home_services = relationship("HomeService", backref="time_slot_detail")
