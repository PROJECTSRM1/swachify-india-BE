from pydantic import BaseModel

class SubModuleBase(BaseModel):
    sub_module_name: str
    module_id: int
    is_active: bool = True

class SubModuleCreate(SubModuleBase):
    pass

class SubModuleUpdate(BaseModel):
    sub_module_name: str | None = None
    module_id: int | None = None
    is_active: bool | None = None

class SubModuleResponse(SubModuleBase):
    id: int

    class Config:
        from_attributes = True
