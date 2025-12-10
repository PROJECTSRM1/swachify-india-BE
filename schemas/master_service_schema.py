from pydantic import BaseModel

class MasterServiceBase(BaseModel):
    sub_module_id: int
    service_name: str
    is_active: bool = True

class MasterServiceCreate(MasterServiceBase):
    pass

class MasterServiceUpdate(BaseModel):
    service_name: str | None = None
    is_active: bool | None = None

class MasterServiceResponse(MasterServiceBase):
    id: int

    class Config:
        from_attributes = True
