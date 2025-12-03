from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterDistrict(Base):
    __tablename__ = "master_district"

    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey("master_state.id"))
    district_name = Column(String(255))
    is_active = Column(Boolean, default=True)
