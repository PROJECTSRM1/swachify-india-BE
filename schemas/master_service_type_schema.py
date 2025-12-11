from pydantic import BaseModel

class ServiceTypeBase(BaseModel):
    service_type: str
    is_active: bool = True

class ServiceTypeCreate(ServiceTypeBase):
    pass

class ServiceTypeUpdate(ServiceTypeBase):
    pass

class ServiceTypeResponse(ServiceTypeBase):
    id: int

    class Config:
        orm_mode = True
