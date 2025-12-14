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
from sqlalchemy.orm import Session
from core.database import get_db
from models.master_module import MasterModule
from models.master_sub_module import MasterSubModule
from models.master_service import MasterService
from models.master_sub_service import MasterSubService
from models.master_sub_group import MasterSubGroup
from models.master_service_type import MasterServiceType
from models.home_service import HomeService
from schemas.home_schema import HomeServiceCreate
from schemas.master_module_schema import (
    MasterModuleCreate,
    MasterModuleUpdate,
    MasterModuleResponse
)
from fastapi import HTTPException

from schemas.sub_module_schema import SubModuleResponse,SubModuleCreate,SubModuleUpdate
from schemas.master_service_schema import MasterServiceCreate, MasterServiceResponse, MasterServiceUpdate
from schemas.master_sub_service_schema import SubServiceCreate,SubServiceResponse,SubServiceUpdate
from schemas.master_sub_group_schema import SubGroupCreate,SubGroupResponse,SubGroupUpdate
from schemas.master_service_type_schema import ServiceTypeCreate,ServiceTypeUpdate,ServiceTypeResponse

router = APIRouter(prefix="/api", tags=["Frontend APIs"])



#master_module
@router.get("/modules")
def get_modules(db: Session = Depends(get_db)):
    return db.query(MasterModule).filter_by(is_active=True).all()

@router.post("/modules", response_model=MasterModuleResponse)
def create_module(
    data: MasterModuleCreate,
    db: Session = Depends(get_db)
):
    obj = MasterModule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/modules/{id}", response_model=MasterModuleResponse)
def update_module(id: int,data: MasterModuleUpdate,db: Session = Depends(get_db)):
    obj = db.get(MasterModule, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Module not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/modules/{id}")
def delete_module(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterModule, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Module not found")

    if not obj.is_active:
        return {"message": "Module already deleted"}

    obj.is_active = False
    db.commit()
    db.refresh(obj)

    return {"message": "Module deleted successfully"}


#master_sub_module
@router.get("/modules/{module_id}/sub-modules", response_model=list[SubModuleResponse])
def get_sub_modules(module_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MasterSubModule)
        .filter(
            MasterSubModule.module_id == module_id,
            MasterSubModule.is_active == True
        )
        .all()
    )

@router.post("/sub-modules",response_model=SubModuleResponse)
def create_sub_module(data: SubModuleCreate,db: Session = Depends(get_db)):
    obj = MasterSubModule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/sub-modules/{id}",response_model=SubModuleResponse)
def update_sub_module(id: int,data: SubModuleUpdate,db: Session = Depends(get_db)):

    obj = db.get(MasterSubModule, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sub module not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/sub-modules/{id}")
def delete_sub_module(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterSubModule, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sub module not found")
    if not obj.is_active:
        return {"message": "Sub module already deleted"}
    obj.is_active = False
    db.commit()
    return {"message": "Sub module deleted successfully"}



#master-services
@router.get("/sub-modules/{sub_module_id}/services",response_model=list[MasterServiceResponse])
def get_services(sub_module_id: int, db: Session = Depends(get_db)):
    return db.query(MasterService).filter_by(
        sub_module_id=sub_module_id,
        is_active=True
    ).all()


@router.post("/services", response_model=MasterServiceResponse)
def create_service(data: MasterServiceCreate, db: Session = Depends(get_db)):
    obj = MasterService(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/services/{id}", response_model=MasterServiceResponse)
def update_service(id: int, data: MasterServiceUpdate, db: Session = Depends(get_db)):
    obj = db.get(MasterService, id)
    if not obj:
        raise HTTPException(404, "Service not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/services/{id}")
def delete_service(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterService, id)
    if not obj:
        raise HTTPException(404, "Service not found")

    obj.is_active = False
    db.commit()
    return {"message": "Service deleted"}

#sub-services
@router.get("/services/{service_id}/sub-services",response_model=list[SubServiceResponse])
def get_sub_services(service_id: int, db: Session = Depends(get_db)):
    return db.query(MasterSubService).filter_by(
        service_id=service_id,
        is_active=True
    ).all()


@router.post("/sub-services", response_model=SubServiceResponse)
def create_sub_service(data: SubServiceCreate, db: Session = Depends(get_db)):
    obj = MasterSubService(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/sub-services/{id}", response_model=SubServiceResponse)
def update_sub_service(id: int, data: SubServiceUpdate, db: Session = Depends(get_db)):
    obj = db.get(MasterSubService, id)
    if not obj:
        raise HTTPException(404, "Sub-service not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/sub-services/{id}")
def delete_sub_service(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterSubService, id)
    if not obj:
        raise HTTPException(404, "Sub-service not found")

    obj.is_active = False
    db.commit()
    return {"message": "Sub-service deleted"}

#master-sub-groups
@router.get("/sub-services/{sub_service_id}/sub-groups",response_model=list[SubGroupResponse])
def get_sub_groups(sub_service_id: int, db: Session = Depends(get_db)):
    return db.query(MasterSubGroup).filter_by(
        sub_service_id=sub_service_id,
        is_active=True
    ).all()

@router.post("/sub-groups",response_model=SubGroupResponse)
def create_sub_group(data: SubGroupCreate,db: Session = Depends(get_db)):
    obj = MasterSubGroup(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/sub-groups/{id}",response_model=SubGroupResponse)
def update_sub_group(id: int,data: SubGroupUpdate,db: Session = Depends(get_db)):
    obj = db.get(MasterSubGroup, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub group not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/sub-groups/{id}")
def delete_sub_group(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterSubGroup, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Sub group not found")

    obj.is_active = False
    db.commit()

    return {"message": "Sub group deleted successfully"}

#master-service-type
@router.get("/service-type", response_model=list[ServiceTypeResponse])
def get_service_types(db: Session = Depends(get_db)):
    return (
        db.query(MasterServiceType)
        .filter(MasterServiceType.is_active == True)
        .all()
    )

@router.get("/service-type/{id}",response_model=ServiceTypeResponse)
def get_service_type(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterServiceType, id)

    if not obj or not obj.is_active:
        raise HTTPException(status_code=404, detail="Service type not found")

    return obj


@router.post("/service-type",response_model=ServiceTypeResponse)
def create_service_type(data: ServiceTypeCreate,db: Session = Depends(get_db)):
    obj = MasterServiceType(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/service-type/{id}",response_model=ServiceTypeResponse)
def update_service_type(id: int,data: ServiceTypeUpdate,db: Session = Depends(get_db)):
    obj = db.get(MasterServiceType, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Service type not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/service-type/{id}")
def delete_service_type(id: int, db: Session = Depends(get_db)):
    obj = db.get(MasterServiceType, id)

    if not obj:
        raise HTTPException(status_code=404, detail="Service type not found")

    if not obj.is_active:
        return {"message": "Service type already deleted"}

    obj.is_active = False
    db.commit()

    return {"message": "Service type deleted successfully"}




#master-home-service
@router.post("/home-service")
def create_home_service(data: HomeServiceCreate, db: Session = Depends(get_db)):
    booking = HomeService(**data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return {"message": "Service booked successfully", "id": booking.id}
