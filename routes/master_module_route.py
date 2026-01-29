from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from core.database import get_db

from core.dependencies import get_current_user
from models.generated_models import UserRegistration,MasterModule,MasterSubModule,MasterService,MasterSubService,MasterSubGroup,MasterServiceType
from schemas.home_schema import (
    HomeServiceBase,
    HomeServiceCreate,
    HomeServiceRatingUpdate,
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
    update_home_service,
    update_home_service_rating
)

from services.master_data_service import get_master_data

from schemas.master_module_schema import (
    VehicleServiceBookingCreateSchema,
    VehicleServiceBookingResponseSchema
)

from services.master_module_service import (
    create_vehicle_service_booking,
    get_all_vehicle_service_bookings
)


from schemas.master_module_schema import VehicleBrandFuelCreateSchema, VehicleBrandFuelResponseSchema
from services.master_module_service import create_vehicle_brand_fuel, get_all_vehicle_brand_fuel

from schemas.master_module_schema import BookingServiceMappingCreateSchema, BookingServiceMappingResponseSchema
from services.master_module_service import create_booking_service_mapping, get_all_booking_service_mapping






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

@router.post(
    "/home-service",
    response_model=HomeServiceCreateResponse
)
def create_new_home_service(
    data: HomeServiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_home_service(db, data, current_user.id)


@router.put("/home-service/{service_id}/rating")
def update_rating(
    service_id: int,
    payload: HomeServiceRatingUpdate,
    db: Session = Depends(get_db)
):
    return update_home_service_rating(
        db=db,
        service_id=service_id,
        rating=payload.rating
    )

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




# ✅ VEHICLE SERVICE BOOKING — UNIQUE PATH

@router.post("/vehicle-service-booking", response_model=VehicleServiceBookingResponseSchema)
def create_booking(payload: VehicleServiceBookingCreateSchema, db: Session = Depends(get_db)):
    return create_vehicle_service_booking(db, payload)


@router.get("/vehicle-service-booking", response_model=list[VehicleServiceBookingResponseSchema])
def fetch_all_bookings(db: Session = Depends(get_db)):
    return get_all_vehicle_service_bookings(db)




@router.post("/vehicle-brand-fuel", response_model=VehicleBrandFuelResponseSchema)
def create_vehicle_brand_fuel_api(payload: VehicleBrandFuelCreateSchema, db: Session = Depends(get_db)):
    return create_vehicle_brand_fuel(db, payload)


@router.get("/vehicle-brand-fuel", response_model=list[VehicleBrandFuelResponseSchema])
def get_vehicle_brand_fuel_api(db: Session = Depends(get_db)):
    return get_all_vehicle_brand_fuel(db)


@router.post("/booking-service-mapping", response_model=BookingServiceMappingResponseSchema)
def create_booking_service_mapping_api(payload: BookingServiceMappingCreateSchema, db: Session = Depends(get_db)):
    return create_booking_service_mapping(db, payload)


@router.get("/booking-service-mapping", response_model=list[BookingServiceMappingResponseSchema])
def get_booking_service_mapping_api(db: Session = Depends(get_db)):
    return get_all_booking_service_mapping(db)
