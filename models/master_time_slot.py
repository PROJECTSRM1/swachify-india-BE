from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base

class MasterTimeSlot(Base):
    __tablename__ = "master_time_slot"

    id = Column(Integer, primary_key=True)
    slot_name = Column(String)
    is_active = Column(Boolean)
