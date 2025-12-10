from sqlalchemy import Column, Integer, String
from core.database import Base

class MasterSubGroup(Base):
    __tablename__ = "master_sub_group"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(255), nullable=False)
