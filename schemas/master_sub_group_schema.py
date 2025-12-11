from pydantic import BaseModel

class SubGroupBase(BaseModel):
    sub_group_name: str
    sub_service_id: int
    is_active: bool = True

class SubGroupCreate(SubGroupBase):
    pass

class SubGroupUpdate(SubGroupBase):
    pass

class SubGroupResponse(BaseModel):
    id: int
    sub_group_name: str
    is_active: bool

    # relations
    sub_service_id: int
    sub_service_name: str

    service_id: int
    service_name: str

    sub_module_id: int
    sub_module_name: str

    module_id: int
    module_name: str

    class Config:
        orm_mode = True
