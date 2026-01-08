from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class UserServices(Base):
    __tablename__ = "user_services"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_registration.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("master_module.id"), nullable=False)

    user = relationship("UserRegistration", back_populates="services")
