from pydantic import BaseModel, Field
from typing import Optional

# =========================
# BASE
# =========================
class SubGroupBase(BaseModel):
    sub_group_name: str = Field(..., min_length=2)
    sub_service_id: int
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }


# =========================
# CREATE
# =========================
class SubGroupCreate(SubGroupBase):
    pass


# =========================
# UPDATE
# =========================
class SubGroupUpdate(BaseModel):
    sub_group_name: Optional[str] = None
    sub_service_id: Optional[int] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


# =========================
# RESPONSE
# =========================
class SubGroupResponse(SubGroupBase):
    id: int
