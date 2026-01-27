from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from datetime import date
from decimal import Decimal

### Added
class JobOpeningCreateSchema(BaseModel):
    job_id: int
    company_name: str
    company_address: str
    location_type_id: int
    work_type_id: int
    role_description: str
    requirements: str
    sub_module_id: int
    category_id: int
    internship_duration_id: int
    stipend_type_id: int
    internship_stipend: bool
    created_by: int


class JobOpeningResponseSchema(BaseModel):
    id: int
    job_id: int
    company_name: str
    company_address: str
    location_type_id: int
    work_type_id: int
    role_description: str
    requirements: str
    sub_module_id: int
    category_id: int
    internship_duration_id: int
    stipend_type_id: int
    internship_stipend: bool
    created_by: int

    class Config:
        from_attibutes = True


class ApplicationReviewResponse(BaseModel):
    application_code: str
    status: str

    full_name: str
    dob: str
    gender: str

    degree: str
    institute: str
    percentage: str

    email: str
    phone: str

    # internship_title: str
    # company: str
    # location: str





class ApplicationUpdateRequest(BaseModel):
    
    # application_code: Optional[str]
    # status: Optional[str]

    full_name: Optional[str]
    dob: Optional[str]
    gender: Optional[str]

    degree: Optional[str]
    institute: Optional[str]
    percentage: Optional[str]

    email: Optional[str]
    phone: Optional[str]

    # internship_title: Optional[str]
    # company: Optional[str]
    # location: Optional[str]



class TrendingStudentResponse(BaseModel):
    full_name: str
    institute: str
    degree: str
    attendance_percentage: float
    active: bool
    
    
    


# MASTER JOB RESPONSE
class MasterJobResponse(BaseModel):
    id: int
    job_name: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_attibutes = True


# UI APPLICATION DETAILS
class ApplicationDetailsSchema(BaseModel):
    position: Optional[str]
    company: Optional[str]
    application_id: str
    # status: str


# UI SUCCESS RESPONSE
class JobSuccessResponse(BaseModel):
    success: bool
    title: str
    message: str
    application_details: ApplicationDetailsSchema
