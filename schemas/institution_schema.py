from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# ======================================================
# INSTITUTION REGISTRATION
# ======================================================

class InstitutionRegistrationCreate(BaseModel):
    institution_name: str
    institution_type_id: int
    identity_type_id: int
    identity_number: str
    location: str
    representative_name: str
    email: EmailStr
    phone_number: str

    upload_id_proof: Optional[str] = None
    upload_address_proof: Optional[str] = None
    institute_website: Optional[str] = None
    total_branches: Optional[int] = None
    academic_year_start: Optional[date] = None
    academic_year_end: Optional[date] = None
    created_by: Optional[int] = None
    is_active: Optional[bool] = True

class InstitutionRegistrationResponse(BaseModel):
    id: int

    institution_name: str
    institution_type_id: int
    identity_type_id: int
    identity_number: str
    location: str
    representative_name: str
    email: EmailStr
    phone_number: str

    upload_id_proof: Optional[str] = None
    upload_address_proof: Optional[str] = None
    institute_website: Optional[str] = None
    total_branches: Optional[int] = None
    academic_year_start: Optional[date] = None
    academic_year_end: Optional[date] = None

    created_by: Optional[int] = None
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ======================================================
# INSTITUTION BRANCH
# ======================================================

class InstitutionBranchCreate(BaseModel):
    institution_id: int
    branch_name: str
    city: str
    branch_code: str
    branch_head: str
    is_active: Optional[bool] = True


class InstitutionBranchResponse(BaseModel):
    id: int
    institution_id: int
    branch_name: str
    city: str
    branch_code: str
    branch_head: str
    created_date: datetime
    is_active: bool

    class Config:
        from_attributes = True


# get_students_by_branch Schema
class StudentResponse(BaseModel):
    student_id: int
    student_code: str
    student_name: str
    year: int
    profile_image: str | None