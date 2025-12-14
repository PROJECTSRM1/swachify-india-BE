# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from core.database import Base

# class MasterService(Base):
#     __tablename__ = "master_service"

#     id = Column(Integer, primary_key=True, index=True)
#     sub_module_id = Column(Integer, ForeignKey("master_sub_module.id"), nullable=False)
#     service_name = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)

#     submodule = relationship("MasterSubModule", back_populates="services")



from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterService(Base):
    __tablename__ = "master_service"

    id = Column(Integer, primary_key=True)
    service_name = Column(String)
    sub_module_id = Column(Integer, ForeignKey("master_sub_module.id"))
    is_active = Column(Boolean)
