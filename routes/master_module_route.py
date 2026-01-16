from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db

from core.dependencies import get_current_user
from models.master_module import MasterModule
from models.master_sub_module import MasterSubModule
from models.master_service import MasterService
from models.master_sub_service import MasterSubService
from models.master_sub_group import MasterSubGroup
from models.master_service_type import MasterServiceType

from models.user_registration import UserRegistration
from schemas.home_schema import (
    HomeServiceBase,
    HomeServiceCreate,
    HomeServiceUpdate,
    HomeServiceResponse,
    HomeServiceCreateResponse
)

from schemas.master_data_schema import MasterDataResponse

from services.home_service import (
    create_home_service,
    delete_home_service,
    get_home_service,
    get_home_services,
    update_home_service
)

from services.master_data_service import get_master_data

router = APIRouter(prefix="/api/master", tags=["Master Data & Booking"])

@router.get("/master-data", response_model=MasterDataResponse)
def get_all_master_data(db: Session = Depends(get_db)):
  
    """Get all master data (modules, services, etc.)"""

    return get_master_data(db)


MODEL_MAP = {
    "module": MasterModule,
    "sub_module": MasterSubModule,
    "service": MasterService,
    "sub_service": MasterSubService,
    "sub_group": MasterSubGroup,
    "service_type": MasterServiceType,
}


@router.post("/master-data")
def create_master_data(type: str, data: dict, db: Session = Depends(get_db)):
    ModelClass = MODEL_MAP.get(type)
    if not ModelClass:
        raise HTTPException(status_code=400, detail="Invalid type")

    obj = ModelClass(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# @router.put("/master-data/{id}")
# def update_master_data(id: int, type: str, data: dict, db: Session = Depends(get_db)):
#     ModelClass = MODEL_MAP.get(type)
#     if not ModelClass:
#         raise HTTPException(400, "Invalid type")

#     obj = db.query(ModelClass).filter(ModelClass.id == id).first()
#     if not obj:
#         raise HTTPException(404, "Not found")

#     for key, value in data.items():
#         setattr(obj, key, value)

#     db.commit()
#     db.refresh(obj)
#     return obj


# @router.delete("/master-data/{id}")
# def delete_master_data(id: int, type: str, db: Session = Depends(get_db)):
#     ModelClass = MODEL_MAP.get(type)
#     if not ModelClass:
#         raise HTTPException(400, "Invalid type")

#     obj = db.query(ModelClass).filter(ModelClass.id == id).first()
#     if not obj:
#         raise HTTPException(404, "Not found")

#     db.delete(obj)
#     db.commit()
#     return {"message": "Deleted successfully"}

@router.get("/home-service", response_model=list[HomeServiceResponse])
def read_home_services(db: Session = Depends(get_db)):
    return get_home_services(db)

@router.get("/home-service/{id}", response_model=HomeServiceResponse)
def read_home_service_by_id(id: int, db: Session = Depends(get_db)):
    return get_home_service(db, id)

@router.post("/home-service",response_model=HomeServiceResponse)
def create_new_home_service(data: HomeServiceCreate,db: Session = Depends(get_db),current_user: UserRegistration = Depends(get_current_user)):
    return create_home_service(db, data, current_user.id)



# @router.put("/home-service/{id}", response_model=HomeServiceResponse)
# def update_existing_home_service(
#     id: int,
#     data: HomeServiceUpdate,
#     db: Session = Depends(get_db)
# ):
#     return update_home_service(db, id, data)


# @router.delete("/home-service/{id}")
# def remove_home_service(id: int, db: Session = Depends(get_db)):
#     return delete_home_service(db, id)