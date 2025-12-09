from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class RegisterAdmin(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")
    password: str
    confirm_password: str
    gender_id: int
    address: str

    @field_validator("email")
    def email_must_be_admin(cls, v):
        if not v.endswith("@admin.com"):
            raise ValueError("Admin email must end with @admin.com")
        return v

    @field_validator("password")
    def strong_password(cls, v):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain uppercase, lowercase, number & special char."
            )
        return v

    @field_validator("confirm_password")
    def confirm_password_match(cls, v, info):
        if v != info.data.get("password"):
            raise ValueError("Password and Confirm Password must match")
        return v


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    mobile: str
    gender_id: int
    address: str
    role_id: int
    is_active: bool

    class Config:
        from_attributes = True

class AdminRegisterResponse(BaseModel):
    message: str
    data: UserBase


class AdminLogin(BaseModel):
    username_or_email: str = Field(..., description="Admin email or username")
    password: str = Field(..., min_length=6, max_length=72)

    @field_validator("username_or_email")
    def validate_identifier(cls, value):
        value = value.strip()
        email_pattern = r"^\S+@\S+\.\S+$"
        username_pattern = r"^[a-zA-Z0-9._-]{4,50}$"   # admin usernames allowed

        if not (re.match(email_pattern, value) or re.match(username_pattern, value)):
            raise ValueError("Enter valid email or valid username (4–50 chars)")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        value = value.strip()
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if len(value) > 72:
            raise ValueError("Password cannot exceed bcrypt limit (72 characters).")
        return value

class AdminLogout(BaseModel):
    admin_id: int = Field(..., gt=0, description="Admin database ID")

class AdminUpdateResponse(BaseModel):
    message: str
    data: UserBase
