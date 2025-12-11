# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from core.database import get_db

# from schemas.master_module_schema import (
#     MasterModuleCreate,
#     MasterModuleUpdate,
#     MasterModuleResponse,
# )

# from services.master_module_service import (
#     create_module,
#     get_all_modules,
#     get_module_by_id,
#     update_module,
#     delete_module
# )

# router = APIRouter(prefix="/master/module", tags=["Master Module"])


# @router.post("/", response_model=MasterModuleResponse)
# def create(data: MasterModuleCreate, db: Session = Depends(get_db)):
#     return create_module(db, data)


# @router.get("/", response_model=list[MasterModuleResponse])
# def get_all(db: Session = Depends(get_db)):
#     return get_all_modules(db)


# @router.get("/{module_id}", response_model=MasterModuleResponse)
# def get_by_id(module_id: int, db: Session = Depends(get_db)):
#     module = get_module_by_id(db, module_id)
#     if not module:
#         raise HTTPException(404, "Module not found")
#     return module


# @router.put("/{module_id}", response_model=MasterModuleResponse)
# def update(module_id: int, data: MasterModuleUpdate, db: Session = Depends(get_db)):
#     updated = update_module(db, module_id, data)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Module not found")
#     return updated

# @router.delete("/{module_id}")
# def delete(module_id: int, db: Session = Depends(get_db)):
#     deleted = delete_module(db, module_id)
#     if not deleted:
#         raise HTTPException(404, "Module not found")
#     return {"message": "Module deleted successfully"}







from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from services.master_module_service import *
from services.sub_module_service import *
from services.master_service_service import *
from services.master_sub_service_service import (
    create_sub_service,
    get_all_sub_services,
    get_sub_service,
    update_sub_service,
    delete_sub_service
)
from services.master_sub_group_service import (
    create_sub_group,
    get_all_sub_groups,
    get_sub_group,
    update_sub_group,
    delete_sub_group
)
from services.master_service_type_service import (
    create_service_type,
    get_all_service_types,
    get_service_type,
    update_service_type,
    delete_service_type
)


router = APIRouter(prefix="/master", tags=["Master API"])


VALID_TYPES = ["module", "submodule", "service", "subservice","subgroup","servicetype"]


@router.post("/{type}")
def create_master(type: str, data: dict, db: Session = Depends(get_db)):
    if type not in VALID_TYPES:
        raise HTTPException(400, "Invalid master type")

    if type == "module":
        return create_module(db, data)

    if type == "submodule":
        return create_sub_module(db, data)

    if type == "service":
        return create_service(db, data)
    if type == "subservice":
        return create_sub_service(db, data)
    if type == "subgroup":
        return create_sub_group(db, data)
    if type == "servicetype":
        return create_service_type(db, data)



@router.get("/{type}")
def get_all_master(type: str, db: Session = Depends(get_db)):
    if type == "module":
        return get_all_modules(db)

    if type == "submodule":
        return get_all_sub_modules(db)

    if type == "service":
        return get_all_services(db)
    if type == "subservice":
        return get_all_sub_services(db)
    if type == "subgroup":
        return get_all_sub_groups(db)
    if type == "servicetype":
        return get_all_service_types(db)

   

    raise HTTPException(400, "Invalid master type")


@router.get("/{type}/{id}")
def get_master(type: str, id: int, db: Session = Depends(get_db)):
    if type == "module":
        return get_module_by_id(db, id)

    if type == "submodule":
        return get_sub_module(db, id)

    if type == "service":
        return get_service(db, id)
    if type == "subservice":
        return get_sub_service(db, id)
    if type == "subgroup":
        return get_sub_group(db, id)
    if type == "servicetype":
        return get_service_type(db, id)



    raise HTTPException(400, "Invalid master type")


@router.put("/{type}/{id}")
def update_master(type: str, id: int, data: dict, db: Session = Depends(get_db)):
    if type == "module":
        return update_module(db, id, data)

    if type == "submodule":
        return update_sub_module(db, id, data)

    if type == "service":
        return update_service(db, id, data)
    if type == "subservice":
        return update_sub_service(db, id, data)
    if type == "subgroup":
        return update_sub_group(db, id, data)
    if type == "servicetype":
        return update_service_type(db, id, data)



    raise HTTPException(400, "Invalid master type")


@router.delete("/{type}/{id}")
def delete_master(type: str, id: int, db: Session = Depends(get_db)):
    if type == "module":
        return delete_module(db, id)

    if type == "submodule":
        return delete_sub_module(db, id)

    if type == "service":
        return delete_service(db, id)
    
    if type == "subservice":
        return delete_sub_service(db, id)
    if type == "subgroup":
        return delete_sub_group(db, id)
    if type == "servicetype":
        return delete_service_type(db, id)



    raise HTTPException(400, "Invalid master type")

