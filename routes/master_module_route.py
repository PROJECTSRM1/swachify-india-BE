# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from core.database import get_db

# from core.dependencies import get_current_user
# from models.master_module import MasterModule
# from models.master_sub_module import MasterSubModule
# from models.master_service import MasterService
# from models.master_sub_service import MasterSubService
# from models.master_sub_group import MasterSubGroup
# from models.master_service_type import MasterServiceType

# from schemas.home_schema import (HomeServiceCreate,HomeServiceResponse,HomeServiceUpdate,HomeServiceCreateResponse)
# from schemas.master_data_schema import MasterDataResponse
# from services.home_service import (create_home_service,delete_home_service,get_home_service,get_home_services, mark_payment_success,update_home_service)
# from services.master_data_service import get_master_data

# router = APIRouter(prefix="/api", tags=["Cleaning Services"])

# @router.get("/master-data", response_model=MasterDataResponse)
# def get_all_master_data(db: Session = Depends(get_db)):
#     return get_master_data(db)

# MODEL_MAP = {
#     "module": MasterModule,
#     "sub_module": MasterSubModule,
#     "service": MasterService,
#     "sub_service": MasterSubService,
#     "sub_group": MasterSubGroup,
#     "service_type": MasterServiceType,
# }

# @router.post("/master-data")
# def create_master_data(type: str, data: dict, db: Session = Depends(get_db)):
#     ModelClass = MODEL_MAP.get(type)
#     if not ModelClass:
#         raise HTTPException(status_code=400, detail="Invalid type")
#     obj = ModelClass(**data)
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj

# @router.put("/master-data/{id}")
# def update_master_data(id: int, type: str, data: dict, db: Session = Depends(get_db)):
#     model = MODEL_MAP.get(type)
#     if not model:
#         raise HTTPException(400, "Invalid type")

#     obj = db.query(model).filter(model.id == id).first()
#     if not obj:
#         raise HTTPException(404, "Not found")

#     for key, value in data.items():
#         setattr(obj, key, value)
#     db.commit()
#     db.refresh(obj)
#     return obj


# @router.delete("/master-data/{id}")
# def delete_master_data(id: int, type: str, db: Session = Depends(get_db)):
#     model = MODEL_MAP.get(type)
#     if not model:
#         raise HTTPException(400, "Invalid type")
#     obj = db.query(model).filter(model.id == id).first()
#     if not obj:
#         raise HTTPException(404, "Not found")
#     db.delete(obj)
#     db.commit()
#     return {"message": "Deleted successfully"}

# #================= HOME SERVICE =================
# @router.get("/home-service")
# def read_home_services(db: Session = Depends(get_db)):
#     return get_home_services(db)

# @router.get("/home-service/{id}", response_model=HomeServiceResponse)
# def read_home_service(id: int, db: Session = Depends(get_db)):
#     return get_home_service(db, id)

# # @router.post("/{home_service_id}/payment-success", response_model=HomeServiceResponse)
# # def payment_success(
# #     home_service_id: int,
# #     db: Session = Depends(get_db)
# # ):
# #     return mark_payment_success(db, home_service_id)

# @router.post("/home-service", response_model=HomeServiceCreateResponse)
# def create_new_home_service(
#     data: HomeServiceCreate,
#     db: Session = Depends(get_db)
# ):
#     return create_home_service(db, data)


# @router.put("/home-service/{id}", response_model=HomeServiceResponse)
# def update_existing_home_service(id: int,data: HomeServiceUpdate,db: Session = Depends(get_db)):
#     return update_home_service(db, id, data)

# @router.delete("/home-service/{id}")
# def remove_home_service(id: int, db: Session = Depends(get_db)):
#     return delete_home_service(db, id)



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


@router.put("/master-data/{id}")
def update_master_data(id: int, type: str, data: dict, db: Session = Depends(get_db)):
    ModelClass = MODEL_MAP.get(type)
    if not ModelClass:
        raise HTTPException(400, "Invalid type")

    obj = db.query(ModelClass).filter(ModelClass.id == id).first()
    if not obj:
        raise HTTPException(404, "Not found")

    for key, value in data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/master-data/{id}")
def delete_master_data(id: int, type: str, db: Session = Depends(get_db)):
    ModelClass = MODEL_MAP.get(type)
    if not ModelClass:
        raise HTTPException(400, "Invalid type")

    obj = db.query(ModelClass).filter(ModelClass.id == id).first()
    if not obj:
        raise HTTPException(404, "Not found")

    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}

# ==================== HOME SERVICE BOOKING ====================

@router.get("/home-service", response_model=list[HomeServiceResponse])
def read_home_services(db: Session = Depends(get_db)):
    return get_home_services(db)

@router.get("/home-service/{id}", response_model=HomeServiceResponse)
def read_home_service_by_id(id: int, db: Session = Depends(get_db)):
    return get_home_service(db, id)

# @router.post(
#     "/home-service",
#     response_model=HomeServiceCreateResponse
# )
# def create_new_home_service(
#     data: HomeServiceBase,
#     db: Session = Depends(get_db)
# ):
#     return create_home_service(db, data)

@router.post(
    "/home-service",
    response_model=HomeServiceResponse
)
def create_new_home_service(
    data: HomeServiceCreate,
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_current_user)
):
    """
    Create a new home service booking.
    
    🔹 REQUIRED FIELDS:
    - module_id, sub_module_id, service_id, sub_service_id, sub_group_id
    - full_name, email, mobile (10 digits, starts with 6-9), address
    - service_type_id, duration_id
    - preferred_date, time_slot_id
    - payment_type_id, service_price
    
    🔹 OPTIONAL FIELDS:
    - issue_id, problem_description, property_size_sqft
    
    🔹 NOTES:
    - created_by is automatically set from authenticated user
    - status_id is automatically set to 1 (pending)
    - payment_done defaults to false
    """

    return create_home_service(db, data, current_user.id)



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