from pydantic import BaseModel, Field
from typing import Optional
class SubGroupBase(BaseModel):
    sub_group_name: str = Field(..., min_length=2)
    sub_service_id: int
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }
class SubGroupCreate(SubGroupBase):
    pass

class SubGroupUpdate(BaseModel):
    sub_group_name: Optional[str] = None
    sub_service_id: Optional[int] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }

class SubGroupResponse(SubGroupBase):
    id: int
