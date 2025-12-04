from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class MasterSkill(Base):
    __tablename__ = "master_skill"

    id = Column(Integer, primary_key=True, index=True)
    skill = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
