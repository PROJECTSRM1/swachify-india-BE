# models/master_service_type.py
from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class MasterServiceType(Base):
    __tablename__ = "master_service_type"

    id = Column(Integer, primary_key=True)
    service_type = Column(String)
    is_active = Column(Boolean)
