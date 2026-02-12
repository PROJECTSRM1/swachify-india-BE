
# from pydantic import BaseModel, EmailStr, Field, field_validator
# from typing import Optional, List
# from datetime import date
# import re
# class GovernmentID(BaseModel):
#     id_type: str
#     id_number: str


# class ProfessionalDetails(BaseModel):
#     experience_years: Optional[int] = Field(None, ge=0, le=50)
#     expertise_in: List[int] = Field(default_factory=list)  
# from pydantic import BaseModel, EmailStr, Field, field_validator
# from typing import Optional, List, Dict
# from datetime import date
# import re


# # ---------------------------
# # Registration Request Schema
# # ---------------------------
# class RegisterUser(BaseModel):
#     """
#     Registration schema based strictly on UI.
#     Only UI fields are required.
#     Everything else is optional.
#     """

#     # ===== REQUIRED (UI) =====
#     first_name: str = Field(..., min_length=2, max_length=255)
#     last_name: str = Field(..., min_length=1, max_length=255)

#     email: EmailStr
#     mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")

#     password: str
#     confirm_password: str

#     # ===== OPTIONAL (DB only) =====
#     gender_id: Optional[int] = None
#     dob: Optional[date] = None
#     age: Optional[int] = None
#     role_id: Optional[int] = None

#     state_id: Optional[int] = None
#     district_id: Optional[int] = None
#     address: Optional[str] = None

#     profile_image: Optional[str] = None
#     experience_summary: Optional[str] = None
#     experience_doc: Optional[str] = None

#     government_id: Optional[Dict] = None

#     status_id: Optional[int] = None
#     reg_payment_done: Optional[bool] = None
#     reg_fee: Optional[float] = None
#     experience_in_years: Optional[str] = None

#     noc_number: Optional[str] = None
#     police_station_name: Optional[str] = None
#     issue_year: Optional[int] = None
#     upload_noc: Optional[str] = None

#     latitude: Optional[float] = None
#     longitude: Optional[float] = None

#     business_type_id: Optional[int] = None
#     product_name: Optional[str] = None
#     business_description: Optional[str] = None
#     org_name: Optional[int] = None
#     gst_number: Optional[str] = None
#     job_skill_id: Optional[int] = None

#     vehicle_insurance: Optional[str] = None
#     driver_license: Optional[str] = None
#     vehicle_rc: Optional[str] = None
#     pollution_certificate: Optional[bool] = None
#     upload_pollution_certificate: Optional[str] = None
#     purchase_year: Optional[date] = None
#     vehicle_model: Optional[str] = None

#     work_type_id: Optional[int] = None

#     hospital_name: Optional[str] = None
#     upload_certificate: Optional[str] = None
#     doctor_designation: Optional[str] = None

#     # ---------------------------
#     # Validators
#     # ---------------------------
#     @field_validator("email")
#     @classmethod
#     def allow_gmail_only(cls, v: str):
#         if not v.endswith("@gmail.com"):
#             raise ValueError("Only Gmail addresses are allowed")
#         return v

#     @field_validator("password")
#     @classmethod
#     def strong_password(cls, v: str):
#         pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
#         if not re.match(pattern, v):
#             raise ValueError(
#                 "Password must contain uppercase, lowercase, number and special character"
#             )
#         return v

#     @field_validator("confirm_password")
#     @classmethod
#     def passwords_match(cls, v: str, info):
#         if v != info.data.get("password"):
#             raise ValueError("Passwords do not match")
#         return v
    

# class RegisterUserResponse(BaseModel):
#     message: str

#     user_id: int
#     unique_id: str

#     first_name: str
#     last_name: str

#     email: EmailStr
#     mobile: str

#     role_id: Optional[int] = None
#     status_id: Optional[int] = None
#     work_type_id: Optional[int] = None

#     is_active: bool


# class LoginRequest(BaseModel):
#     email_or_phone: str
#     password: str
#     latitude: Optional[float] = None
#     longitude: Optional[float] = None


# class LoginResponse(BaseModel):
#     """Response after successful login with role-based data."""
#     message: str  
#     user_id: int
#     email_or_phone: str

#     # service_ids: List[int] 
#     # skill_ids: List[int] 

#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"
#     expires_in: int
#     refresh_expires_in: int
#     latitude: Optional[float] = None
#     longitude: Optional[float] = None
#     # role: str  

# class UpdateUser(BaseModel):
#     user_id: int

#     first_name: Optional[str] = Field(None, min_length=2, max_length=50)
#     last_name: Optional[str] = Field(None, min_length=2, max_length=50)
#     email: Optional[EmailStr] = None
#     mobile: Optional[str] = Field(None, pattern=r"^[6-9]\d{9}$")
#     password: Optional[str] = None
#     # gender_id: Optional[int] = None
#     # address: Optional[str] = None


#     @field_validator("email")
#     @classmethod
#     def email_must_be_gmail(cls, v):
#         if v and not v.endswith("@gmail.com"):
#             raise ValueError("Email must end with @gmail.com")
#         return v

#     @field_validator("password")
#     @classmethod
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
#     @classmethod
#     def validate_first_last(cls, v, info):
#         last_name = info.data.get("last_name")
#         if last_name and v.lower() == last_name.lower():
#             raise ValueError("First name and last name must not be the same")
#         return v

#     # @field_validator("address")
#     # @classmethod
#     # def validate_address(cls, v):
#     #     if v:
#     #         parts = [p.strip() for p in v.split(",")]
#     #         if len(parts) < 4:
#     #             raise ValueError("Address must be: Area, City, District, State")
#     #     return v



# class VerifyTokenRequest(BaseModel):
#     token: str


# class VerifyTokenResponse(BaseModel):
#     authenticated: bool
#     token_type: Optional[str] = None
#     user_id: Optional[int] = None
#     email: Optional[str] = None
#     role_id: Optional[int] = None
#     message: Optional[str] = None


# class RefreshRequest(BaseModel):
#     user_id: int
#     refresh_token: str

# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr


# class VerifyOtpRequest(BaseModel):
#     otp: str = Field(min_length=4, max_length=8)


# class ResetPasswordRequest(BaseModel):
#     new_password: str
#     confirm_password: str

#     @field_validator("new_password")
#     @classmethod
#     def strong_password(cls, v):
#         pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
#         if not re.match(pattern, v):
#             raise ValueError("Weak password")
#         return v

#     @field_validator("confirm_password")
#     @classmethod
#     def passwords_match(cls, v, info):
#         if v != info.data.get("new_password"):
#             raise ValueError("Passwords do not match")
#         return v


from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import date
import re


# -----------------------------
# Nested Schemas
# -----------------------------
class ProfessionalDetails(BaseModel):
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    expertise_in: List[int] = Field(default_factory=list)


# -----------------------------
# Register Request
# -----------------------------
class RegisterUser(BaseModel):
    # Required (UI)
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    password: str
    confirm_password: str

    work_type_id: int = Field(
        ..., description="1=Customer, 2=Freelancer, 3=Both, 4=Student"
    )

    # Optional
    service_ids: Optional[List[int]] = None
    professional_details: Optional[ProfessionalDetails] = None

    gender_id: Optional[int] = None
    dob: Optional[date] = None
    state_id: Optional[int] = None
    district_id: Optional[int] = None
    address: Optional[str] = None

    business_type_id: Optional[int] = None
    product_name: Optional[str] = None
    business_description: Optional[str] = None
    org_name: Optional[int] = None
    gst_number: Optional[str] = None

    job_skill_id: Optional[int] = None
    government_id: Optional[dict] = None

    @field_validator("email")
    @classmethod
    def gmail_only(cls, v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses are allowed")
        return v

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError("Weak password")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get("password"):
            raise ValueError("Passwords do not match")
        return v


# -----------------------------
# Register Response
# -----------------------------
class RegisterResponse(BaseModel):
    message: str

    user_id: int
    unique_id: str

    first_name: str
    last_name: str

    email: EmailStr
    mobile: str

    role_id: int
    status_id: int
    work_type_id: int

    is_active: bool

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int


# -----------------------------
# Login
# -----------------------------
class LoginRequest(BaseModel):
    email_or_phone: str
    password: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LoginResponse(BaseModel):
    message: str
    user_id: int
    email_or_phone: str

    service_ids: List[int]
    skill_ids: List[int]

    latitude: Optional[float]
    longitude: Optional[float]

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_expires_in: int
    role: str
    
class ForgotPasswordRequest(BaseModel):
    email_or_phone: str


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get("new_password"):
            raise ValueError("Passwords do not match")
        return v

