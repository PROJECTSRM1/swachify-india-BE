from sqlalchemy import Column, Integer, String
from core.database import Base

class MasterAddOn(Base):
    __tablename__ = "master_add_on"

    id = Column(Integer, primary_key=True, index=True)
    add_on_name = Column(String(255), nullable=False)
