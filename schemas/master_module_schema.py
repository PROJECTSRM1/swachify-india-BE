from pydantic import BaseModel, Field
from typing import Optional
class MasterModuleBase(BaseModel):
    module_name: str = Field(..., min_length=2)
    is_active: bool = True

    model_config = {
        "from_attributes": True 
    }
class MasterModuleCreate(MasterModuleBase):
    pass

class MasterModuleUpdate(BaseModel):
    module_name: Optional[str] = None 
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
class MasterModuleResponse(MasterModuleBase):
    id: int
