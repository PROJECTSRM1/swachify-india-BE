from pydantic import BaseModel
from typing import Optional



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

    internship_title: str
    company: str
    location: str





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

