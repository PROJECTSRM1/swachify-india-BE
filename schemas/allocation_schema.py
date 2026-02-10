from pydantic import BaseModel
from typing import List, Optional
class EmployeeCard(BaseModel):
    employee_id: int
    name: str
    rating: float
    distance_km: float
    experience_years: int
    available_slots: List[str]
class AutoAssignResponse(BaseModel):
    booking_id: int
    assigned_employee_id: int
    employee_name: str
    allocation_type: str
    message: str

class ManualAssignRequest(BaseModel):
    employee_id: int

class ManualAssignResponse(BaseModel):
    booking_id: int
    assigned_employee_id: int
    allocation_type: str
    message: str

