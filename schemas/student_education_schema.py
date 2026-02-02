from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, List, Any
from datetime import date, datetime
from decimal import Decimal

from schemas.student_family_schema import StudentFamilyMemberResponse

# =====================================================
# JOB OPENINGS
# =====================================================

class JobOpeningCreate(BaseModel):
    job_id: int
    company_name: str
    company_address: Optional[str] = None

    industry_id: Optional[int] = None        # ✅ ADD
    company_size_id: Optional[int] = None    # ✅ ADD

    location_type_id: Optional[int] = None
    work_type_id: Optional[int] = None
    role_description: Optional[str] = None
    requirements: Optional[str] = None
    sub_module_id: Optional[int] = None


class JobOpeningResponse(BaseModel):
    id: int
    job_id: int
    company_name: str
    company_address: Optional[str] = None
    industry_id: Optional[int] = None          # ✅ ADD
    company_size_id: Optional[int] = None      # ✅ ADD

    location_type_id: Optional[int] = None
    work_type_id: Optional[int] = None
    role_description: Optional[str] = None
    requirements: Optional[str] = None
    is_active: bool
    created_date: Optional[datetime]

    class Config:
        from_attributes = True


# =====================================================
# JOB APPLICATION
# =====================================================

class JobApplicationCreate(BaseModel):
    job_openings_id: int
    first_name: str
    last_name: str
    mobile_number: str
    mobile_code_id: int
    email: EmailStr
    city_id: int

    upload_resume: str
    notice_period_in_days: int

    fresher: bool
    experienced: bool

    company: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    company_city_id: Optional[int] = None
    current_ctc: Optional[Decimal] = None
    expected_ctc: Optional[Decimal] = None
    title: Optional[str] = None
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_fresher_vs_experienced(self):
        if self.fresher and not self.experienced:
            if any([
                self.company,
                self.from_date,
                self.to_date,
                self.company_city_id,
                self.current_ctc
            ]):
                raise ValueError(
                    "Fresher should not have company, dates, city or CTC"
                )

        elif self.experienced and not self.fresher:
            required = [
                self.company,
                self.from_date,
                self.to_date,
                self.company_city_id,
                self.current_ctc
            ]
            if not all(required):
                raise ValueError(
                    "Experienced candidate must provide company, dates, city and current_ctc"
                )
        else:
            raise ValueError(
                "Either fresher=true or experienced=true (not both)"
            )
        return self


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_openings_id: int

    first_name: str
    last_name: str
    mobile_number: str
    mobile_code_id: int
    email: EmailStr

    city_id: int
    upload_resume: str
    notice_period_in_days: int

    title: Optional[str]
    company: Optional[str]
    from_date: Optional[date]
    to_date: Optional[date]
    company_city_id: Optional[int]
    description: Optional[str]

    current_ctc: Optional[Decimal]
    expected_ctc: Optional[Decimal]

    fresher: Optional[bool]
    experienced: Optional[bool]

    created_date: Optional[datetime]
    modified_by: Optional[int]
    modified_date: Optional[datetime]
    is_active: Optional[bool]

    class Config:
        from_attributes = True


# =====================================================
# STUDENT CERTIFICATE
# =====================================================

class StudentCertificateCreate(BaseModel):
    certificate_name: str
    issued_by: str
    year: int
    upload_certificate: Optional[str] = None


class StudentCertificateResponse(BaseModel):
    id: int
    certificate_name: str
    issued_by: Optional[str] = None
    year: Optional[int] = None
    upload_certificate: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True



# =====================================================
# STUDENT EDUCATION
# =====================================================

class StudentEducationCreate(BaseModel):
    degree: str
    institute: str
    percentage: str
    passing_year: Optional[int] = None


class StudentEducationResponse(BaseModel):
    degree: str
    institute: Optional[str] = None
    percentage: Optional[str] = None
    
    class Config:
        from_attributes = True

# =====================================================
# STUDENT NOC
# =====================================================

class StudentNOCUpdate(BaseModel):
    noc_number: str
    police_station_name: str
    issue_year: int
    upload_noc: Optional[str] = None


class StudentNOCResponse(BaseModel):
    noc_number: str
    police_station_name: str
    issue_year: int
    upload_noc: Optional[str]

    class Config:
        from_attributes = True


# =====================================================
# STUDENT PROFILE (BASIC)
# =====================================================

class StudentProfileResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    government_id: Any
    location: Optional[str]
    service_name: str
    family_members: List[StudentFamilyMemberResponse] = []
    
    class Config:
        from_attributes = True


# =====================================================
# STUDENT FULL UPDATE (EDU / CERT / NOC)
# =====================================================

class StudentEducationFullCreate(BaseModel):
    education: Optional[List[StudentEducationCreate]] = None
    certificates: Optional[List[StudentCertificateCreate]] = None
    noc: Optional[StudentNOCUpdate] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not (values.education or values.certificates or values.noc):
            raise ValueError(
                "At least one of education, certificates, or noc must be provided."
            )
        return values


# =====================================================
# STUDENT LIST RESPONSE (NO DUPLICATES)
# =====================================================

class StudentListResponse(BaseModel):
    user_id: int
    student_name: str
    joined_date: Optional[datetime]

    skill_id: Optional[int]
    skill: Optional[str]

    attendance_percentage: Optional[Decimal]
    aggregate: Optional[str]

    internship_status: Optional[str]
    rating: Optional[Decimal]

    education: List[StudentEducationResponse] = []
    certificates: List[StudentCertificateResponse] = []

    class Config:
        from_attributes = True

# # get_students_by_branch Schema
# class StudentResponse(BaseModel):
#     student_id: int
#     student_code: str
#     student_name: str
#     year: int
#     profile_image: str | None