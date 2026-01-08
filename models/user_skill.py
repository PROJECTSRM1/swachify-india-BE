from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from core.database import Base
from sqlalchemy.orm import relationship


class UserSkill(Base):
    __tablename__ = "user_skill"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_registration.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("master_skill.id"), nullable=False)

    user = relationship("UserRegistration", back_populates="skills")
