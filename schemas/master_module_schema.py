from pydantic import BaseModel
from typing import Optional


# ------------------------
# MASTER MODULE
# ------------------------

class MasterModuleBase(BaseModel):
    module_name: Optional[str] = None
    is_active: Optional[bool] = True


class MasterModuleCreate(MasterModuleBase):
    module_name: str


class MasterModuleUpdate(MasterModuleBase):
    pass


class MasterModuleResponse(BaseModel):
    id: int
    module_name: str
    is_active: bool

    class Config:
        orm_mode = True


# ------------------------
# MASTER SUB MODULE
# ------------------------

class MasterSubModuleBase(BaseModel):
    sub_module_name: Optional[str] = None
    module_id: Optional[int] = None
    is_active: Optional[bool] = True


class MasterSubModuleCreate(MasterSubModuleBase):
    sub_module_name: str
    module_id: int


class MasterSubModuleUpdate(MasterSubModuleBase):
    pass


class MasterSubModuleResponse(BaseModel):
    id: int
    sub_module_name: str
    module_id: int
    is_active: bool

    class Config:
        orm_mode = True
