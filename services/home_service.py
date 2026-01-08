# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from pydantic import BaseModel
# from typing import Optional


# from models.home_service import HomeService
# from schemas.home_schema import (
#     HomeServiceCreate,
#     HomeServiceUpdate
# )

# Status_id=1

# def get_home_services(db: Session):
#     return db.query(HomeService).all()


# def get_home_service(db: Session, home_service_id: int):
#     obj = db.get(HomeService, home_service_id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Home service not found")

#     return obj


# # def create_home_service(db: Session, data: HomeServiceCreate):
# #     obj = HomeService(**data.model_dump())
# #     db.add(obj)
# #     db.commit()
# #     db.refresh(obj)
# #     return obj

# def create_home_service(db: Session, data: HomeServiceCreate):
#     obj = HomeService(
#         **data.dict(),
#         status_id=Status_id,
#         assigned_to=None
#     )
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return {
#          "message": "Home service created successfully",
#          "service_id": obj.id,
#          "status_id": obj.status_id,
#          "status_name": "Pending"
#     }





# def mark_payment_success(db: Session, home_service_id: int):
#     obj = db.get(HomeService, home_service_id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Home service not found")

#     obj.payment_done = True
#     db.commit()
#     db.refresh(obj)
#     return obj


# def update_home_service(
#     db: Session,
#     home_service_id: int,
#     data: HomeServiceUpdate
# ):
#     obj = db.get(HomeService, home_service_id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Home service not found")

#     for key, value in data.model_dump(exclude_unset=True).items():
#         setattr(obj, key, value)

#     db.commit()
#     db.refresh(obj)
#     return obj


# def delete_home_service(db: Session, home_service_id: int):
#     obj = db.get(HomeService, home_service_id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Home service not found")

#     db.delete(obj)
#     db.commit()

#     return {"message": "Home service deleted successfully"}

# def get_home_services_by_creator_and_payment(
#     db: Session,
#     created_by: int,
#     payment_done: Optional[bool] = None
# ):
#     query = db.query(HomeService).filter(
#         HomeService.created_by == created_by
#     )

#     if payment_done is not None:
#         query = query.filter(HomeService.payment_done == payment_done)

#     return query.all()



from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.home_service import HomeService
from schemas.home_schema import HomeServiceCreate, HomeServiceUpdate


def create_home_service(db: Session, data: HomeServiceCreate, user_id: int):
    obj = HomeService(
        **data.model_dump(),
        created_by=user_id,
        status_id=1
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return {
        "message": "Service created successfully",
        "service_id": obj.id,
        "status_id": obj.status_id
    }


def get_home_services(db: Session):
    return db.query(HomeService).filter(HomeService.is_active == True).all()


def get_home_service(db: Session, service_id: int):
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")
    return obj


def update_home_service(db: Session, service_id: int, data: HomeServiceUpdate):
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_home_service(db: Session, service_id: int):
    obj = db.query(HomeService).filter(HomeService.id == service_id).first()
    if not obj:
        raise HTTPException(404, "Service not found")

    obj.is_active = False
    db.commit()
    return {"message": "Service deactivated"}




















# from pydantic import BaseModel, EmailStr, Field, field_validator
# from typing import Optional, List
# from datetime import date
# import re

# # ==================================================
# # 🔹 COMMON / NESTED SCHEMAS
# # ==================================================

# class GovernmentID(BaseModel):
#     id_type: str
#     id_number: str


# class ProfessionalDetails(BaseModel):
#     experience_years: Optional[int] = Field(None, ge=0, le=50)
#     expertise_in: Optional[List[int]] = None  # ✅ master_skill IDs only


# # ==================================================
# # 🔹 REGISTER USER
# # ==================================================

# class RegisterUser(BaseModel):
#     first_name: str = Field(..., min_length=2, max_length=50)
#     last_name: Optional[str] = Field(None, max_length=50)

#     email: EmailStr
#     mobile: str = Field(..., pattern=r"^[6-9]\d{9}$")

#     password: str
#     confirm_password: str

#     gender_id: Optional[int]
#     dob: Optional[date]

#     work_type: int = Field(
#         ...,
#         description="1 = Customer, 2 = Freelancer, 3 = Both"
#     )

#     service_ids: List[int] = Field(
#         ...,
#         min_items=1,
#         description="master_module IDs"
#     )

#     government_id: Optional[List[GovernmentID]] = None
#     professional_details: Optional[ProfessionalDetails] = None

#     state_id: Optional[int]
#     district_id: Optional[int]
#     address: Optional[str]

#     # ---------------- Validators ----------------

#     @field_validator("email")
#     def gmail_only(cls, v):
#         if not v.endswith("@gmail.com"):
#             raise ValueError("Only Gmail accounts are allowed")
#         return v

#     @field_validator("password")
#     def strong_password(cls, v):
#         pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
#         if not re.match(pattern, v):
#             raise ValueError(
#                 "Password must contain uppercase, lowercase, number & special character"
#             )
#         return v

#     @field_validator("confirm_password")
#     def passwords_match(cls, v, info):
#         if v != info.data.get("password"):
#             raise ValueError("Passwords do not match")
#         return v


# # ==================================================
# # 🔹 REGISTER RESPONSE
# # ==================================================

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

#     gender_id: Optional[int]
#     address: Optional[str]

#     # ---------------- Validators ----------------

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
#             raise ValueError("Weak password")
#         return v

#     @field_validator("address")
#     def validate_address(cls, v):
#         if v:
#             parts = [p.strip() for p in v.split(",")]
#             if len(parts) < 4:
#                 raise ValueError(
#                     "Address format: Area, City, District, State"
#                 )
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
# # 🔹 PASSWORD RESET
# # ==================================================

# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr


# class VerifyOtpRequest(BaseModel):
#     otp: str = Field(min_length=4, max_length=8)


# class ResetPasswordRequest(BaseModel):
#     new_password: str
#     confirm_password: str
