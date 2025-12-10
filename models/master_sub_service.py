from sqlalchemy import Column, Integer, String
from core.database import Base

class MasterSubService(Base):
    __tablename__ = "master_sub_service"

    id = Column(Integer, primary_key=True, index=True)
    sub_service_name = Column(String(255), nullable=False)
