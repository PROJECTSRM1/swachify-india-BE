from pydantic import BaseModel, Field
from typing import Optional

# ---------- Base ----------
class MasterModuleBase(BaseModel):
    module_name: str = Field(..., min_length=2)
    is_active: bool = True

    model_config = {
        "from_attributes": True   # ✅ CORRECT for Pydantic v2
    }


# ---------- Create ----------
class MasterModuleCreate(MasterModuleBase):
    pass


# ---------- Update ----------
class MasterModuleUpdate(BaseModel):
    module_name: Optional[str] = None   # ✅ fixed
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


class MasterModuleResponse(MasterModuleBase):
    id: int
