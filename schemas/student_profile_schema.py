from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
