from pydantic import BaseModel
from datetime import date

class HomeServiceCreate(BaseModel):
    full_name: str
    email: str
    mobile: str
    address: str
    problem_description: str | None = None
    property_size_sqft: int | None = None
    preferred_date: date
    special_instructions: str | None = None

    module_id: int
    sub_module_id: int
    service_id: int
    sub_service_id: int
    sub_group_id: int
    service_type_id: int
    time_slot_id: int
    add_on_id: int
    payment_type_id: int
