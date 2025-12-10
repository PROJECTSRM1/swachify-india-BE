from sqlalchemy import Column, Integer, String
from core.database import Base

class MasterPaymentType(Base):
    __tablename__ = "master_payment_type"

    id = Column(Integer, primary_key=True, index=True)
    payment_type_name = Column(String(255), nullable=False)
