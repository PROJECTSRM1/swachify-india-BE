from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterSubModule(Base):
    __tablename__ = "master_sub_module"

    id = Column(Integer, primary_key=True, index=True)
    sub_module_name = Column(String, nullable=False)
    module_id = Column(Integer, ForeignKey("master_module.id"), nullable=False)
    is_active = Column(Boolean, default=True)
