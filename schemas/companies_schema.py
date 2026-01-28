from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompanyListResponse(BaseModel):
    company_id: int
    company_name: str
    location: Optional[str]

    industry_id: Optional[int]
    industry_name: Optional[str]

    company_size_id: Optional[int]
    company_size: Optional[str]

    jobs_count: int
    internships_count: int

    hiring_status: Optional[str]
    last_active_time: Optional[datetime]

    class Config:
        from_attributes = True
