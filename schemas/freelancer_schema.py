

from pydantic import BaseModel, field_validator
import re
class FreelancerLogin(BaseModel):
    email_or_phone: str
    password: str
    
    @field_validator("email_or_phone")
    @classmethod
    def validate_identifier(cls, v):
        v = v.strip()
        email_pattern = r"^\S+@\S+\.\S+$"
        mobile_pattern = r"^[6-9]\d{9}$"
        if not (re.match(email_pattern, v) or re.match(mobile_pattern, v)):
            raise ValueError("Enter valid email or 10-digit mobile number")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        v = v.strip()
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if len(v) > 72:
            raise ValueError("Password cannot exceed 72 characters (bcrypt limit)")
        return v

