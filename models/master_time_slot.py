from sqlalchemy import Column, Integer, String
from core.database import Base

class MasterTimeSlot(Base):
    __tablename__ = "master_time_slot"

    id = Column(Integer, primary_key=True, index=True)
    time_slot_name = Column(String(255), nullable=False)
