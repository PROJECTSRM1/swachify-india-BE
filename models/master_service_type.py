from sqlalchemy import Column, Integer, String
from core.database import Base

class MasterServiceType(Base):
    __tablename__ = "master_service_type"

    id = Column(Integer, primary_key=True, index=True)
    service_type_name = Column(String(255), nullable=False)
