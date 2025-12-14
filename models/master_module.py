# from sqlalchemy import Column, Integer, String, Boolean
# from core.database import Base
# from sqlalchemy.orm import relationship
# class MasterModule(Base):
#     __tablename__ = "master_module"

#     id = Column(Integer, primary_key=True, index=True)
#     module_name = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)

#     submodules = relationship("MasterSubModule", back_populates="module")



from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class MasterModule(Base):
    __tablename__ = "master_module"

    id = Column(Integer, primary_key=True)
    module_name = Column(String)
    is_active = Column(Boolean)
