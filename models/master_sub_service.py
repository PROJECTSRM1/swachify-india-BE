from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterSubService(Base):
    __tablename__ = "master_sub_service"

    id = Column(Integer, primary_key=True)
    sub_service_name = Column(String)
    service_id = Column(Integer, ForeignKey("master_service.id"))
    is_active = Column(Boolean)
