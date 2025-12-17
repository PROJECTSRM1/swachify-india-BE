# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from core.database import get_db
# from services.master_module_service import *
# from services.sub_module_service import *
# from services.master_service_service import *
# from services.master_sub_service_service import (
#     create_sub_service,
#     get_all_sub_services,
#     get_sub_service,
#     update_sub_service,
#     delete_sub_service
# )
# from services.master_sub_group_service import (
#     create_sub_group,
#     get_all_sub_groups,
#     get_sub_group,
#     update_sub_group,
#     delete_sub_group
# )
# from services.master_service_type_service import (
#     create_service_type,
#     get_all_service_types,
#     get_service_type,
#     update_service_type,
#     delete_service_type
# )
# from services.master_time_slot_service import (
#     create_time_slot,
#     get_all_time_slots,
#     get_time_slot,
#     update_time_slot,
#     delete_time_slot
# )



# router = APIRouter(prefix="/master", tags=["Master API"])


# VALID_TYPES = ["module", "submodule", "service", "subservice","subgroup","servicetype","timeslot"]


# @router.post("/{type}")
# def create_master(type: str, data: dict, db: Session = Depends(get_db)):
#     if type not in VALID_TYPES:
#         raise HTTPException(400, "Invalid master type")

#     if type == "module":
#         return create_module(db, data)

#     if type == "submodule":
#         return create_sub_module(db, data)

#     if type == "service":
#         return create_service(db, data)
#     if type == "subservice":
#         return create_sub_service(db, data)
#     if type == "subgroup":
#         return create_sub_group(db, data)
#     if type == "servicetype":
#         return create_service_type(db, data)
#     if type == "timeslot":
#         return create_time_slot(db, data)




# @router.get("/{type}")
# def get_all_master(type: str, db: Session = Depends(get_db)):
#     if type == "module":
#         return get_all_modules(db)

#     if type == "submodule":
#         return get_all_sub_modules(db)

#     if type == "service":
#         return get_all_services(db)
#     if type == "subservice":
#         return get_all_sub_services(db)
#     if type == "subgroup":
#         return get_all_sub_groups(db)
#     if type == "servicetype":
#         return get_all_service_types(db)
#     if type == "timeslot":
#         return get_all_time_slots(db)


   

#     raise HTTPException(400, "Invalid master type")


# @router.get("/{type}/{id}")
# def get_master(type: str, id: int, db: Session = Depends(get_db)):
#     if type == "module":
#         return get_module_by_id(db, id)

#     if type == "submodule":
#         return get_sub_module(db, id)

#     if type == "service":
#         return get_service(db, id)
#     if type == "subservice":
#         return get_sub_service(db, id)
#     if type == "subgroup":
#         return get_sub_group(db, id)
#     if type == "servicetype":
#         return get_service_type(db, id)
#     if type == "timeslot":
#         return get_time_slot(db, id)



#     raise HTTPException(400, "Invalid master type")


# @router.put("/{type}/{id}")
# def update_master(type: str, id: int, data: dict, db: Session = Depends(get_db)):
#     if type == "module":
#         return update_module(db, id, data)

#     if type == "submodule":
#         return update_sub_module(db, id, data)

#     if type == "service":
#         return update_service(db, id, data)
#     if type == "subservice":
#         return update_sub_service(db, id, data)
#     if type == "subgroup":
#         return update_sub_group(db, id, data)
#     if type == "servicetype":
#         return update_service_type(db, id, data)
#     if type == "timeslot":
#         return update_time_slot(db, id, data)



#     raise HTTPException(400, "Invalid master type")


# @router.delete("/{type}/{id}")
# def delete_master(type: str, id: int, db: Session = Depends(get_db)):
#     if type == "module":
#         return delete_module(db, id)

#     if type == "submodule":
#         return delete_sub_module(db, id)

#     if type == "service":
#         return delete_service(db, id)
    
#     if type == "subservice":
#         return delete_sub_service(db, id)
#     if type == "subgroup":
#         return delete_sub_group(db, id)
#     if type == "servicetype":
#         return delete_service_type(db, id)
#     if type == "timeslot":
#         return delete_time_slot(db, id)



#     raise HTTPException(400, "Invalid master type")





from fastapi import APIRouter, Depends
from core.database import get_db
from sqlalchemy.orm import Session
from models.master_module import MasterModule
from models.master_sub_module import MasterSubModule
from models.master_service import MasterService
from models.master_sub_service import MasterSubService
from models.master_sub_group import MasterSubGroup
from models.master_service_type import MasterServiceType
from models.home_service import HomeService
from fastapi import HTTPException

from schemas.master_module_schema import MasterModuleCreate,MasterModuleUpdate,MasterModuleResponse
from schemas.sub_module_schema import SubModuleResponse,SubModuleCreate,SubModuleUpdate
from schemas.master_service_schema import MasterServiceCreate, MasterServiceResponse, MasterServiceUpdate
from schemas.master_sub_service_schema import SubServiceCreate,SubServiceResponse,SubServiceUpdate
from schemas.master_sub_group_schema import SubGroupCreate,SubGroupResponse,SubGroupUpdate
from schemas.master_service_type_schema import ServiceTypeCreate,ServiceTypeUpdate,ServiceTypeResponse
from schemas.home_schema import (HomeServiceCreate,HomeServiceUpdate,HomeServiceResponse)


from services.master_module_service import get_modules_service,create_module_service,update_module_service,delete_module_service
from services.master_sub_module_service import get_sub_modules_service,create_sub_module_service,update_sub_module_service,delete_sub_module_service
from services.master_service_service import get_services_by_sub_module,create_service_service,update_service_service,delete_service_service
from services.master_sub_service_service import get_sub_services,create_sub_service,update_sub_service,delete_sub_service
from services.master_sub_group_service import (get_sub_groups,create_sub_group,update_sub_group,delete_sub_group)
from services.master_service_type_service import (get_service_types,get_service_type,create_service_type,update_service_type,delete_service_type)
from services.home_service import (get_home_services,get_home_service,create_home_service,update_home_service,delete_home_service)


router = APIRouter(prefix="/api", tags=["Cleaning Services"])

#master_module
@router.get("/modules", response_model=list[MasterModuleResponse])
def get_modules(db: Session = Depends(get_db)):
    return get_modules_service(db)

@router.post("/modules", response_model=MasterModuleResponse)
def create_module(data: MasterModuleCreate,db: Session = Depends(get_db)):
    return create_module_service(db, data)

@router.put("/modules/{id}", response_model=MasterModuleResponse)
def update_module(id: int,data: MasterModuleUpdate,db: Session = Depends(get_db)):
    return update_module_service(db, id, data)


@router.delete("/modules/{id}")
def delete_module(id: int, db: Session = Depends(get_db)):
    return delete_module_service(db, id)

#master_sub_module
@router.get("/modules/{module_id}/sub-modules",response_model=list[SubModuleResponse])
def get_sub_modules(module_id: int, db: Session = Depends(get_db)):
    return get_sub_modules_service(db, module_id)

@router.post("/sub-modules", response_model=SubModuleResponse)
def create_sub_module(data: SubModuleCreate,db: Session = Depends(get_db)):
    return create_sub_module_service(db, data)

@router.put("/sub-modules/{id}", response_model=SubModuleResponse)
def update_sub_module(id: int,data: SubModuleUpdate,db: Session = Depends(get_db)):
    return update_sub_module_service(db, id, data)

@router.delete("/sub-modules/{id}")
def delete_sub_module(id: int, db: Session = Depends(get_db)):
    return delete_sub_module_service(db, id)


#master-services
@router.get("/sub-modules/{sub_module_id}/services",response_model=list[MasterServiceResponse])
def list_services(sub_module_id: int, db: Session = Depends(get_db)):
    return get_services_by_sub_module(db, sub_module_id)


@router.post("/services", response_model=MasterServiceResponse)
def add_service(data: MasterServiceCreate,db: Session = Depends(get_db)):
    return create_service_service(db, data)


@router.put("/services/{id}", response_model=MasterServiceResponse)
def edit_service(id: int,data: MasterServiceUpdate,db: Session = Depends(get_db)):
    return update_service_service(db, id, data)


@router.delete("/services/{id}")
def remove_service(id: int, db: Session = Depends(get_db)):
    return delete_service_service(db, id)


#sub-services
@router.get("/services/{service_id}/sub-services",response_model=list[SubServiceResponse])
def list_sub_services(service_id: int, db: Session = Depends(get_db)):
    return get_sub_services(db, service_id)


@router.post("/sub-services", response_model=SubServiceResponse)
def add_sub_service(data: SubServiceCreate,db: Session = Depends(get_db)):
    return create_sub_service(db, data)

@router.put("/sub-services/{id}", response_model=SubServiceResponse)
def edit_sub_service(id: int,data: SubServiceUpdate,db: Session = Depends(get_db)):
    return update_sub_service(db, id, data)


@router.delete("/sub-services/{id}")
def remove_sub_service(id: int, db: Session = Depends(get_db)):
    return delete_sub_service(db, id)


#master-sub-groups

@router.get("/sub-services/{sub_service_id}/sub-groups",response_model=list[SubGroupResponse])
def read_sub_groups(sub_service_id: int, db: Session = Depends(get_db)):
    return get_sub_groups(db, sub_service_id)

@router.post("/sub-groups", response_model=SubGroupResponse)
def create_new_sub_group(data: SubGroupCreate,db: Session = Depends(get_db)):
    return create_sub_group(db, data)

@router.put("/sub-groups/{id}", response_model=SubGroupResponse)
def update_existing_sub_group(id: int,data: SubGroupUpdate,db: Session = Depends(get_db)):
    return update_sub_group(db, id, data)

@router.delete("/sub-groups/{id}")
def remove_sub_group(id: int, db: Session = Depends(get_db)):
    return delete_sub_group(db, id)


#master-service-type
@router.get("/service-type", response_model=list[ServiceTypeResponse])
def read_service_types(db: Session = Depends(get_db)):
    return get_service_types(db)

@router.get("/service-type/{id}", response_model=ServiceTypeResponse)
def read_service_type(id: int, db: Session = Depends(get_db)):
    return get_service_type(db, id)

@router.post("/service-type", response_model=ServiceTypeResponse)
def create_new_service_type(data: ServiceTypeCreate,db: Session = Depends(get_db)):
    return create_service_type(db, data)

@router.put("/service-type/{id}", response_model=ServiceTypeResponse)
def update_existing_service_type(id: int,data: ServiceTypeUpdate,db: Session = Depends(get_db)):
    return update_service_type(db, id, data)

@router.delete("/service-type/{id}")
def remove_service_type(id: int, db: Session = Depends(get_db)):
    return delete_service_type(db, id)




#master-home-service
@router.get("/home-service")
def read_home_services(db: Session = Depends(get_db)):
    return get_home_services(db)



@router.get("/home-service/{id}", response_model=HomeServiceResponse)
def read_home_service(id: int, db: Session = Depends(get_db)):
    return get_home_service(db, id)


@router.post("/home-service", response_model=HomeServiceResponse)
def create_new_home_service(
    data: HomeServiceCreate,
    db: Session = Depends(get_db)
):
    return create_home_service(db, data)


@router.put("/home-service/{id}", response_model=HomeServiceResponse)
def update_existing_home_service(
    id: int,
    data: HomeServiceUpdate,
    db: Session = Depends(get_db)
):
    return update_home_service(db, id, data)


@router.delete("/home-service/{id}")
def remove_home_service(id: int, db: Session = Depends(get_db)):
    return delete_home_service(db, id)




from schemas.master_data_schema import MasterDataResponse
from services.master_data_service import get_master_data


@router.get("/master-data", response_model=MasterDataResponse)
def get_all_master_data(db: Session = Depends(get_db)):
    return get_master_data(db)