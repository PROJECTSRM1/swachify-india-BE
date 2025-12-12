from pydantic import BaseModel

class MasterSubModuleBase(BaseModel):
    sub_module_name: str
    module_id: int
    is_active: bool = True

class MasterSubModuleCreate(MasterSubModuleBase):
    pass
class MasterSubModuleUpdate(MasterSubModuleBase):
    pass

class MasterSubModuleResponse(MasterSubModuleBase):
    id: int
    
    class Config:
        orm_mode = True
