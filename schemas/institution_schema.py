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


class StudentAcademicDetailsSchema(BaseModel):
    # DB returns this as string (CSE2024_044)
    student_id: str

    # Make everything OPTIONAL unless DB guarantees it
    roll_number: Optional[str] = None

    institution_id: Optional[int] = None
    institution_name: Optional[str] = None

    course_id: Optional[int] = None
    course_name: Optional[str] = None

    department_id: Optional[int] = None
    department_name: Optional[str] = None

    academic_year: Optional[str] = None
    semester: Optional[str] = None

    status: Optional[str] = None

    # Any extra DB columns you saw in error
    paid_date: Optional[date] = None



class StudentProfileBase(BaseModel):
    branch_id: int
    branch_name: str
    student_name: str
    student_id: str
    academic_year: str
    profile_image_url: Optional[str] = None
    is_active: Optional[bool] = True


class StudentProfileCreate(StudentProfileBase):
    created_by: Optional[int] = None


class StudentProfileUpdate(BaseModel):
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    student_name: Optional[str] = None
    academic_year: Optional[str] = None
    profile_image_url: Optional[str] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None


class StudentProfileResponse(StudentProfileBase):
    id: int
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    student_name: Optional[str] = None
    academic_year: Optional[str] = None
    profile_image_url: Optional[str] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None
    created_by: Optional[int]
    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]

    class Config:
        from_attributes = True
# get_students_by_branch Schema
class StudentResponse(BaseModel):
    student_id: int
    student_code: str
    student_name: str
    year: int
    profile_image: str | None
