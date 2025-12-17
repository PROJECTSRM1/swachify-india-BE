from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class MasterStatus(Base):
    __tablename__ = "master_status"

    id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
