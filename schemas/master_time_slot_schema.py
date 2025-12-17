from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base   


class MasterTimeSlot(Base):
    __tablename__ = "master_time_slot"

    id = Column(Integer, primary_key=True, index=True)
    slot_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

