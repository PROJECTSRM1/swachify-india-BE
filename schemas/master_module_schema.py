from pydantic import BaseModel,Field


class MastermoduleBase(BaseModel):
    module_name : str=Field(...,min_length=2)
    is_active:bool = True

    class Config:
        from_attributes:True

class MasterModuleCreate(MastermoduleBase):
    pass

class MasterModuleUpdate(BaseModel):
    Module_name:str | None = None
    is_active:bool | None = None

class MasterModuleResponse(MastermoduleBase):
    id : int
