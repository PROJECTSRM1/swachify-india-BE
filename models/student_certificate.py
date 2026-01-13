from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    BigInteger,
    TIMESTAMP
)
from core.database import Base

class StudentCertificate(Base):
    __tablename__ = "student_certificate"

    id = Column(BigInteger, primary_key=True, index=True)  # BIGSERIAL
    user_id = Column(Integer, nullable=False)              # INT4

    certificate_name = Column(String(255), nullable=False) # VARCHAR(255)
    issued_by = Column(String(255), nullable=False)        # VARCHAR(255)
    year = Column(Integer, nullable=False)                 # INT4

    upload_certificate = Column(String(500), nullable=True)# VARCHAR(500)

    created_by = Column(BigInteger, nullable=False)        # INT8
    created_date = Column(TIMESTAMP, nullable=True)        # TIMESTAMP

    modified_by = Column(BigInteger, nullable=True)        # INT8
    modified_date = Column(TIMESTAMP, nullable=True)      # TIMESTAMP

    is_active = Column(Boolean, default=True)              # BOOL
