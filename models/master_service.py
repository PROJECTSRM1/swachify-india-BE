from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterService(Base):
    __tablename__ = "master_service"

    id = Column(Integer, primary_key=True)
    service_name = Column(String)
    sub_module_id = Column(Integer, ForeignKey("master_sub_module.id"))
    is_active = Column(Boolean)
