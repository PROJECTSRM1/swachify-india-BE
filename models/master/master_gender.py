from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class MasterGender(Base):
    __tablename__ = "master_gender"

    id = Column(Integer, primary_key=True)
    gender_name = Column(String(150))
    is_active = Column(Boolean, default=True)
