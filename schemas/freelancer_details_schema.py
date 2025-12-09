# schemas/freelancer_detail_schema.py
from typing import Optional, List
from pydantic import BaseModel

class FreelancerSkill(BaseModel):
    skill_id: int
    skill_name: str

class FreelancerDetailResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    mobile: str
    gender: Optional[str]
    state: Optional[str]
    district: Optional[str]
    address: Optional[str]
    
    government_id_type: Optional[str]
    government_id_number: Optional[str]
    
    skill_id: Optional[int]
    skill_name: Optional[str]
    
    experience_summary: Optional[str]
    rating: Optional[float]
    completed_jobs: Optional[int]
    status: Optional[str]

    class Config:
        from_attributes = True
