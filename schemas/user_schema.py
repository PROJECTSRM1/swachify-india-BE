from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re
import uuid


class RegisterUser(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")
    password: str
    confirm_password: str
    gender_id: int
    address: str

    @field_validator("email")
    def email_must_be_gmail(cls, v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Email must end with @gmail.com")
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
class LoginRequest(BaseModel):
    email_or_phone: str
    password: str


class LoginResponse(BaseModel):
    id:int
    email_or_phone: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int


class UpdateUser(BaseModel):
    user_id: int  

    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")
    password: Optional[str] = None
    gender_id: Optional[int] = None
    address: Optional[str] = None


    @field_validator("email")
    def email_must_be_gmail(cls, v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Email must end with @gmail.com")
        return v

    @field_validator("password")
    def strong_password(cls, v):
        if v is None:
            return v
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must have uppercase, lowercase, number & special char and be 8+ chars."
            )
        return v

    @field_validator("first_name")
    def validate_first_last(cls, v, info):
        last_name = info.data.get("last_name")
        if last_name and v.lower() == last_name.lower():
            raise ValueError("First name and Last name must NOT be the same")
        return v

    @field_validator("address")
    def validate_address(cls, v):
        parts = [p.strip() for p in v.split(",")]
        if len(parts) < 4:
            raise ValueError("Address must be: Area, City, District, State")
        return v


class VerifyTokenRequest(BaseModel):
    token: str


class VerifyTokenResponse(BaseModel):
    authenticated: bool
    token_type: Optional[str] = None
    user_id: Optional[int] = None
    email: Optional[str] = None
    message: Optional[str] = None

class RefreshRequest(BaseModel):
    user_id: int
    refresh_token: str


# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr

# class VerifyOtpRequest(BaseModel):
#     email: EmailStr
#     otp: str = Field(min_length=4, max_length=8)

# class ResetPasswordRequest(BaseModel):
#     reset_token: str
#     new_password: str = Field(min_length=6)
#     confirm_password: str = Field(min_length=6)



class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    otp: str = Field(min_length=4, max_length=8)


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)
