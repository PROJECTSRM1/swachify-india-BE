
from pydantic import BaseModel
from typing import List


from schemas.master_module_schema import MasterModuleResponse
from schemas.sub_module_schema import SubModuleResponse
from schemas.master_service_schema import MasterServiceResponse
from schemas.master_sub_service_schema import SubServiceResponse
from schemas.master_sub_group_schema import SubGroupResponse
from schemas.master_service_type_schema import ServiceTypeResponse



class MasterDataResponse(BaseModel):
    modules: List[MasterModuleResponse]
    sub_modules: List[SubModuleResponse]
    services: List[MasterServiceResponse]
    sub_services: List[SubServiceResponse]
    sub_groups: List[SubGroupResponse]
    service_types: List[ServiceTypeResponse]