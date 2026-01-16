from pydantic import BaseModel
from typing import Optional, Any


class StudentCertificateCreate(BaseModel):
    user_id: int
    certificate_name: str
    issued_by: str
    year: int
    upload_certificate: Optional[str] = None


class StudentCertificateResponse(BaseModel):
    id: int
    user_id: int
    certificate_name: str
    issued_by: str
    year: int
    upload_certificate: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True



class StudentNOCUpdate(BaseModel):
    user_id: int
    noc_number: str
    police_station_name: str
    issue_year: int
    upload_noc: Optional[str] = None


class StudentNOCResponse(BaseModel):
    user_id: int
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
    user_id: int
    degree: str
    institute: str
    percentage: str

class StudentProfileRequest(BaseModel):
    user_id: int