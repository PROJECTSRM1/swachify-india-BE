from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

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

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str


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
