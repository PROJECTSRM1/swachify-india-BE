# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from core.database import Base
# from sqlalchemy.orm import relationship

# class MasterSubService(Base):
#     __tablename__ = "master_sub_service"

#     id = Column(Integer, primary_key=True, index=True)
#     sub_service_name = Column(String(255), nullable=False)
#     service_id = Column(Integer, ForeignKey("master_service.id"), nullable=False)
#     is_active = Column(Boolean, default=True)

#     service = relationship("MasterService", backref="sub_services")




from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterSubService(Base):
    __tablename__ = "master_sub_service"

    id = Column(Integer, primary_key=True)
    sub_service_name = Column(String)
    service_id = Column(Integer, ForeignKey("master_service.id"))
    is_active = Column(Boolean)
