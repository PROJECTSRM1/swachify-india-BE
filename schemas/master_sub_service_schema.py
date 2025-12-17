from pydantic import BaseModel, Field
from typing import Optional

class SubServiceBase(BaseModel):
    sub_service_name: str = Field(..., min_length=2)
    service_id: int
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }

class SubServiceCreate(SubServiceBase):
    pass
class SubServiceUpdate(BaseModel):
    sub_service_name: Optional[str] = None
    service_id: Optional[int] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }

class SubServiceResponse(SubServiceBase):
    id: int
