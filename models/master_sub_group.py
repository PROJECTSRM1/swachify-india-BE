# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from core.database import Base

# class MasterSubGroup(Base):
#     __tablename__ = "master_sub_group"

#     id = Column(Integer, primary_key=True, index=True)
#     sub_service_id = Column(Integer, ForeignKey("master_sub_service.id"), nullable=False)
#     sub_group_name = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)

#     sub_service = relationship("MasterSubService", backref="sub_groups")




from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class MasterSubGroup(Base):
    __tablename__ = "master_sub_group"

    id = Column(Integer, primary_key=True)
    sub_group_name = Column(String)
    sub_service_id = Column(Integer, ForeignKey("master_sub_service.id"))
    is_active = Column(Boolean)
