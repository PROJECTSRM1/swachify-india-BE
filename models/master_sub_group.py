from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterSubGroup(Base):
    __tablename__ = "master_sub_group"

    id = Column(Integer, primary_key=True)
    sub_group_name = Column(String)
    sub_service_id = Column(Integer, ForeignKey("master_sub_service.id"))
    is_active = Column(Boolean)
