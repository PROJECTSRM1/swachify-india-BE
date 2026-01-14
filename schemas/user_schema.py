# from pydantic import BaseModel, EmailStr, Field, field_validator
# from typing import Optional, List
# from datetime import date
# import re


# class GovernmentID(BaseModel):
#     id_type: str
#     id_number: str


# class ProfessionalDetails(BaseModel):
#     experience_years: Optional[int] = Field(None, ge=0, le=50)
#     expertise_in: Optional[List[int]] = None  # ✅ SKILL IDs ONLY


# class RegisterUser(BaseModel):
#     first_name: str = Field(..., min_length=2, max_length=50)
#     last_name: Optional[str] = None

#     email: EmailStr
#     mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")

#     password: str
#     confirm_password: str

#     gender_id: Optional[int]
#     dob: Optional[date]

#     work_type: int = Field(..., description="1=Customer, 2=Freelancer, 3=Both")

#     service_ids: List[int] = Field(..., min_items=1)

#     government_id: Optional[List[GovernmentID]] = None
#     professional_details: Optional[ProfessionalDetails] = None

#     state_id: Optional[int]
#     district_id: Optional[int]
#     address: Optional[str]

#     # ---------------- Validators ----------------
#     @field_validator("email")
#     def gmail_only(cls, v):
#         if not v.endswith("@gmail.com"):
#             raise ValueError("Only Gmail allowed")
#         return v

#     @field_validator("password")
#     def strong_password(cls, v):
#         pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
#         if not re.match(pattern, v):
#             raise ValueError("Weak password")
#         return v

#     @field_validator("confirm_password")
#     def passwords_match(cls, v, info):
#         if v != info.data.get("password"):
#             raise ValueError("Passwords do not match")
#         return v


# class RegisterResponse(BaseModel):
#     message: str
#     user_id: int
#     unique_id: str
#     email: EmailStr
#     mobile: str
#     role_id: int
#     status_id: int


# # ==================================================
# # 🔹 LOGIN
# # ==================================================
# class LoginRequest(BaseModel):
#     email_or_phone: str
#     password: str


# class LoginResponse(BaseModel):
#     user_id: int
#     email_or_phone: str
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
#     expires_in: int
#     refresh_expires_in: int


# # ==================================================
# # 🔹 UPDATE USER
# # ==================================================
# class UpdateUser(BaseModel):
#     user_id: int

#     first_name: Optional[str] = Field(None, min_length=2, max_length=50)
#     last_name: Optional[str] = Field(None, min_length=2, max_length=50)
#     email: Optional[EmailStr] = None
#     mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")
#     password: Optional[str] = None
#     gender_id: Optional[int] = None
#     address: Optional[str] = None

#     # -------------------------
#     # Validators
#     # -------------------------
#     @field_validator("email")
#     def email_must_be_gmail(cls, v):
#         if v and not v.endswith("@gmail.com"):
#             raise ValueError("Email must end with @gmail.com")
#         return v

#     @field_validator("password")
#     def strong_password(cls, v):
#         if v is None:
#             return v
#         pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
#         if not re.match(pattern, v):
#             raise ValueError(
#                 "Password must contain uppercase, lowercase, number & special character"
#             )
#         return v

#     @field_validator("first_name")
#     def validate_first_last(cls, v, info):
#         last_name = info.data.get("last_name")
#         if last_name and v.lower() == last_name.lower():
#             raise ValueError("First name and Last name must not be the same")
#         return v

#     @field_validator("address")
#     def validate_address(cls, v):
#         if v:
#             parts = [p.strip() for p in v.split(",")]
#             if len(parts) < 4:
#                 raise ValueError("Address must be: Area, City, District, State")
#         return v


# # ==================================================
# # 🔹 TOKEN VERIFICATION
# # ==================================================
# class VerifyTokenRequest(BaseModel):
#     token: str


# class VerifyTokenResponse(BaseModel):
#     authenticated: bool
#     token_type: Optional[str] = None
#     user_id: Optional[int] = None
#     email: Optional[str] = None
#     role_id: Optional[int] = None
#     message: Optional[str] = None


# # ==================================================
# # 🔹 REFRESH TOKEN
# # ==================================================
# class RefreshRequest(BaseModel):
#     user_id: int
#     refresh_token: str


# # ==================================================
# # 🔹 PASSWORD RESET FLOW
# # ==================================================
# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr


# class VerifyOtpRequest(BaseModel):
#     otp: str = Field(min_length=4, max_length=8)


# class ResetPasswordRequest(BaseModel):
#     new_password: str = Field(min_length=6)
#     confirm_password: str = Field(min_length=6)











from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date
import re

# ==================================================
# 🔹 COMMON MODELS
# ==================================================

class GovernmentID(BaseModel):
    id_type: str
    id_number: str


class ProfessionalDetails(BaseModel):
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    expertise_in: List[int] = Field(default_factory=list)  # ✅ SAFE DEFAULT


# ==================================================
# 🔹 REGISTER
# ==================================================

class RegisterUser(BaseModel):
    """User registration request schema with work_type mapping."""
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: Optional[str] = None

    email: EmailStr
    mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")

    password: str
    confirm_password: str

    gender_id: Optional[int] = None
    dob: Optional[date] = None

    work_type: int = Field(
        ..., 
        description="1=Customer (immediate approval), 2=Freelancer (pending approval), 3=Both (pending approval)"
    )

    service_ids: List[int] = Field(..., min_items=1, description="Service/module IDs to register for")

    government_id: Optional[List[GovernmentID]] = None
    professional_details: Optional[ProfessionalDetails] = None

    state_id: Optional[int] = None
    district_id: Optional[int] = None
    address: Optional[str] = None

    # ---------------- Validators ----------------

    @field_validator("email")
    @classmethod
    def gmail_only(cls, v: str):
        if not v.endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses are allowed")
        return v

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain uppercase, lowercase, number & special character"
            )
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info):
        if v != info.data.get("password"):
            raise ValueError("Passwords do not match")
        return v


class RegisterResponse(BaseModel):
    """Response after successful user registration."""
    message: str  # Role-based success message

    user_id: int
    unique_id: str
    email: EmailStr
    mobile: str
    role_id: int  # 2=Customer, 4=Freelancer
    status_id: int  # 1=Approved, 2=Pending
    work_type: int  # 1=Customer, 2=Freelancer, 3=Both (input mapping)

    service_ids: List[int]  # Services/modules assigned
    skill_ids: List[int]  # Skills for freelancers

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int


# ==================================================
# 🔹 LOGIN
# ==================================================

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str


class LoginResponse(BaseModel):
    """Response after successful login with role-based data."""
    message: str  # "User logged in as a customer" or "User logged in as a freelancer"
    user_id: int
    email_or_phone: str

    service_ids: List[int]  # Services/modules user is registered for
    skill_ids: List[int]  # Skills user has (for freelancers)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int
    role: str  # "customer" or "freelancer"


# ==================================================
# 🔹 UPDATE USER
# ==================================================

class UpdateUser(BaseModel):
    user_id: int

    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")
    password: Optional[str] = None
    gender_id: Optional[int] = None
    address: Optional[str] = None

    # ---------------- Validators ----------------

    @field_validator("email")
    @classmethod
    def email_must_be_gmail(cls, v):
        if v and not v.endswith("@gmail.com"):
            raise ValueError("Email must end with @gmail.com")
        return v

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        if v is None:
            return v
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain uppercase, lowercase, number & special character"
            )
        return v

    @field_validator("first_name")
    @classmethod
    def validate_first_last(cls, v, info):
        last_name = info.data.get("last_name")
        if last_name and v.lower() == last_name.lower():
            raise ValueError("First name and last name must not be the same")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        if v:
            parts = [p.strip() for p in v.split(",")]
            if len(parts) < 4:
                raise ValueError("Address must be: Area, City, District, State")
        return v


# ==================================================
# 🔹 TOKEN VERIFICATION
# ==================================================

class VerifyTokenRequest(BaseModel):
    token: str


class VerifyTokenResponse(BaseModel):
    authenticated: bool
    token_type: Optional[str] = None
    user_id: Optional[int] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    message: Optional[str] = None


# ==================================================
# 🔹 REFRESH TOKEN
# ==================================================

class RefreshRequest(BaseModel):
    user_id: int
    refresh_token: str


# ==================================================
# 🔹 PASSWORD RESET FLOW
# ==================================================

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    otp: str = Field(min_length=4, max_length=8)


class ResetPasswordRequest(BaseModel):
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def strong_password(cls, v):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError("Weak password")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get("new_password"):
            raise ValueError("Passwords do not match")
        return v
