from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class MasterState(Base):
    __tablename__ = "master_state"

    id = Column(Integer, primary_key=True, index=True)
    state_code = Column(Integer)
    state_name = Column(String(255))
    is_active = Column(Boolean, default=True)
