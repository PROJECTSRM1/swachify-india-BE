from pydantic import BaseModel
from datetime import date
from typing import Optional


class HomeServiceCreate(BaseModel):
    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    sub_group_id: int

    full_name: str
    email: str
    mobile: str
    address: str

    service_type_id: int
    issue_id: int

    problem_description: Optional[str]
    property_size_sqft: Optional[str]
    add_on_id: Optional[int]
    preferred_date: Optional[date]
    time_slot_id: Optional[int]
    special_instructions: Optional[str]
    payment_type_id: int

    class Config:
        orm_mode = True
