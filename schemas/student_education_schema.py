import datetime
from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, List, Any
from datetime import date,datetime
from decimal import Decimal

class JobOpeningCreate(BaseModel):
    job_id: int
    company_name: str
    company_address: Optional[str] = None
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
    location_type_id: Optional[int] = None
    work_type_id: Optional[int] = None
    role_description: Optional[str] = None
    requirements: Optional[str] = None
    is_active: bool
    created_date: Optional[datetime] = None

    class Config:
        from_attributes = True

#job appliaction
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

    title: Optional[str] = None
    company: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    company_city_id: Optional[int] = None
    description: Optional[str] = None

    current_ctc: Optional[Decimal] = None
    expected_ctc: Optional[Decimal] = None

    fresher: Optional[bool] = None
    experienced: Optional[bool] = None

    created_date: Optional[datetime] = None
    modified_by: Optional[int] = None
    modified_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

#student certification
class StudentCertificateCreate(BaseModel):
    certificate_name: str
    issued_by: str
    year: int
    upload_certificate: Optional[str] = None


class StudentCertificateResponse(BaseModel):
    id: int
    certificate_name: str
    issued_by: str
    year: int
    upload_certificate: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

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


class StudentProfileResponse(BaseModel):
    user_id: int  
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    government_id: Any
    location: Optional[str]
    service_name: str

    class Config:
        from_attributes = True

class StudentEducationCreate(BaseModel):
    degree: str
    institute: str
    percentage: str
    passing_year: Optional[int] = None

class StudentEducationFullCreate(BaseModel):
    education: Optional[List[StudentEducationCreate]] = None
    certificates: Optional[List[StudentCertificateCreate]] = None
    noc: Optional[StudentNOCUpdate] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if not (values.education or values.certificates or values.noc):
            raise ValueError("At least one of education, certificates, or noc must be provided.")
        return values

class StudentListResponse(BaseModel):
    user_id: int
    student_name: str
    joined_date: Optional[datetime]

    skill_id: Optional[int]
    skill: Optional[str]

    attendance_percentage: Optional[Decimal]
    aggregate: Optional[str]

    certificate_name: Optional[str]
    degree: Optional[str]

    internship_status: Optional[str]
    rating: Optional[Decimal]

    class Config:
        from_attributes = True