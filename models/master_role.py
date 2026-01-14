from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base


class MasterRole(Base):
    __tablename__ = "master_role"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    users = relationship(
        "UserRegistration",
        back_populates="role"
    )
