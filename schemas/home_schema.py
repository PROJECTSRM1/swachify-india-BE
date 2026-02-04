from pydantic import BaseModel
from typing import Optional
from datetime import date

class HomeServiceBookingResponse(BaseModel):
    id: int
    full_name: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    address: Optional[str]
    others_address: Optional[str]

    preferred_date: Optional[date]
    time_slot_id: Optional[int]
    extra_hours: Optional[int]
    special_instructions: Optional[str]

    service_summary: Optional[str]
    upload_photos: Optional[str]

    item_total: Optional[float]
    convenience_fee: Optional[float]
    total_amount: Optional[float]
    payment_done: Optional[bool]

    status_id: Optional[int]

    module_name: Optional[str]
    sub_module_name: Optional[str]
    service_name: Optional[str]
    sub_service_name: Optional[str]

    class Config:
        from_attributes = True
