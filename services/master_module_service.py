from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.generated_models import MasterModule
from schemas.master_module_schema import (MasterModuleCreate,MasterModuleUpdate)
from models.generated_models import VehicleServiceBooking, VehicleBrandFuel, BookingServiceMapping

def get_all_vehicle_service_bookings(db: Session):
    return db.query(VehicleServiceBooking).order_by(
        VehicleServiceBooking.id.desc()
    ).all()



def create_module_service(db: Session, data: MasterModuleCreate):
    obj = MasterModule(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_module_service(db: Session,module_id: int,data: MasterModuleUpdate):
    obj = db.get(MasterModule, module_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Module not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_module_service(db: Session, module_id: int):
    obj = db.get(MasterModule, module_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Module not found")

    if not obj.is_active:
        return {"message": "Module already deleted"}

    obj.is_active = False
    db.commit()
    db.refresh(obj)

    return {"message": "Module deleted successfully"}




# ✅ CREATE BOOKING
def create_vehicle_service_booking(db: Session, payload):
    booking = VehicleServiceBooking(**payload.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ✅ GET ALL BOOKINGS
def get_all_vehicle_service_bookings(db: Session):
    return db.query(VehicleServiceBooking).order_by(
        VehicleServiceBooking.id.desc()
    ).all()


def create_vehicle_brand_fuel(db: Session, payload):
    obj = VehicleBrandFuel(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_vehicle_brand_fuel(db: Session):
    return db.query(VehicleBrandFuel).order_by(
        VehicleBrandFuel.id.desc()
    ).all()
    
    
def create_booking_service_mapping(db: Session, payload):
    obj = BookingServiceMapping(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all_booking_service_mapping(db: Session):
    return db.query(BookingServiceMapping).order_by(
        BookingServiceMapping.id.desc()
    ).all()
