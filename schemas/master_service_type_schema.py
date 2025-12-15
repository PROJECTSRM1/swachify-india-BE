from pydantic import BaseModel, Field
from typing import Optional

class ServiceTypeBase(BaseModel):
    service_type: str = Field(..., min_length=2)
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }


class ServiceTypeCreate(ServiceTypeBase):
    pass


class ServiceTypeUpdate(BaseModel):
    service_type: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


class ServiceTypeResponse(ServiceTypeBase):
    id: int
