from pydantic import BaseModel
from typing import List, Optional

class HomeServiceMini(BaseModel):
    id: int
    full_name: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    module_id: Optional[int] = None
    sub_module_id: Optional[int] = None
    service_id: Optional[int] = None
    sub_service_id: Optional[int] = None
    sub_group_id: Optional[int] = None
    issue_id: Optional[int] = None
    property_size_sqft: Optional[int] = None
    preferred_date: Optional[str] = None

    class Config:
        orm_mode = True

class TimeSlotBase(BaseModel):
    time_slot: str
    is_active: bool = True

class TimeSlotCreate(TimeSlotBase):
    pass

class TimeSlotUpdate(TimeSlotBase):
    pass

class TimeSlotResponse(TimeSlotBase):
    id: int
    home_service_count: int
    home_services: List[HomeServiceMini]

    class Config:
        orm_mode = True
