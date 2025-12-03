from pydantic import BaseModel, EmailStr,field_validator
from typing import Optional
from datetime import date
import re

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class RegisterUser(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    mobile: str
    password: str
    confirm_password: str
    gender_id: int
    unique_id: Optional[str] = None
    dob: Optional[date] = None
    age: Optional[int] = None
    role_id: Optional[int] = None
    state_id: Optional[int] = None
    district_id: Optional[int] = None
    created_by: Optional[int] = None
    profile_image: Optional[str] = None
    skill_id: Optional[int] = None
    experience_summary: Optional[str] = None
    experience_doc: Optional[str] = None
    government_id: Optional[str] = None
    address:Optional[str]=None

    @field_validator("email")
    def validate_email(cls,value):
        if not value.endswith("@gmail.com"):
            raise ValueError("Email must have @gmail.com.")
        return value
    
    @field_validator("mobile")
    def validate_mobile(cls, value):
        pattern = r"^[6-9]\d{9}$"
        if not re.fullmatch(pattern,value):
            raise ValueError("Mobile NO. must be 10 digits and must be start with 6,7,8,9.")
        return value
    
    @field_validator("password")
    def validate_password(cls,value):
        """
        Strong password rules:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least 8 characters, including uppercase, lowercase, number, and special character."
            )
        return value
    
    @field_validator("confirm_password")
    def passwords_match(cls,value,values):
        if "password" in values and value!=values["password"]:
             raise ValueError("Passowrd and Confirm Password does not match.")
        return value
    
    @field_validator("gender_id")
    def validate_gender(cls, value):
        if value < 1:
            raise ValueError("gender_id must start from 1 ")
        return value

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str

    @field_validator("email_or_phone")
    def validate_email_or_mobile(cls, value):
        value = value.strip()

        email_pattern = r"^\S+@\S+\.\S+$"
        phone_pattern = r"^[6-9]\d{9}$"

        
        if not (re.match(email_pattern, value) or re.match(phone_pattern, value)):
            raise ValueError("Enter valid email or 10-digit Indian mobile number.")

        return value

class LoginResponse(BaseModel):
    email_or_phone: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int


class LogoutRequest(BaseModel):
    user_id: int


class UpdateUser(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile: Optional[str] = None
    password: Optional[str] = None
    dob: Optional[date] = None
    age: Optional[int] = None
    profile_image: Optional[str] = None
    experience_summary: Optional[str] = None
    experience_doc: Optional[str] = None
    government_id: Optional[str] = None
    gender_id: Optional[int] = None
    role_id: Optional[int] = None
    state_id: Optional[int] = None
    district_id: Optional[int] = None
    skill_id: Optional[int] = None

class VerifyTokenRequest(BaseModel):
    token: str


class VerifyTokenResponse(BaseModel):
    authenticated: bool
    token_type: Optional[str] = None
    user_id: Optional[int] = None
    email: Optional[str] = None
    message: Optional[str] = None
