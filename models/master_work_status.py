from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base


class MasterWorkStatus(Base):
    __tablename__ = "master_work_status"

    id = Column(Integer, primary_key=True, index=True)
    work_status_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
