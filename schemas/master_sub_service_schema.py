from pydantic import BaseModel

class SubServiceBase(BaseModel):
    sub_service_name: str
    service_id: int
    is_active: bool = True

class SubServiceCreate(SubServiceBase):
    pass

class SubServiceUpdate(SubServiceBase):
    pass

class SubServiceResponse(BaseModel):
    id: int
    sub_service_name: str
    is_active: bool
    
    service_id: int
    service_name: str
    
    sub_module_id: int
    sub_module_name: str
    
    module_id: int
    module_name: str

    class Config:
        orm_mode = True