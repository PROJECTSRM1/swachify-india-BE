

# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from models.generated_models import MasterModule
# from schemas.master_module_schema import (MasterModuleCreate,MasterModuleUpdate)
# from models.generated_models import VehicleServiceBooking, VehicleBrandFuel, BookingServiceMapping

# def get_all_vehicle_service_bookings(db: Session):
#     return db.query(VehicleServiceBooking).order_by(
#         VehicleServiceBooking.id.desc()
#     ).all()



# def create_module_service(db: Session, data: MasterModuleCreate):
#     obj = MasterModule(**data.model_dump())
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def update_module_service(db: Session,module_id: int,data: MasterModuleUpdate):
#     obj = db.get(MasterModule, module_id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Module not found")

#     update_data = data.model_dump(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(obj, key, value)

#     db.commit()
#     db.refresh(obj)
#     return obj


# def delete_module_service(db: Session, module_id: int):
#     obj = db.get(MasterModule, module_id)

#     if not obj:
#         raise HTTPException(status_code=404, detail="Module not found")

#     if not obj.is_active:
#         return {"message": "Module already deleted"}

#     obj.is_active = False
#     db.commit()
#     db.refresh(obj)

#     return {"message": "Module deleted successfully"}




# # ✅ CREATE BOOKING
# def create_vehicle_service_booking(db: Session, payload):
#     booking = VehicleServiceBooking(**payload.dict())
#     db.add(booking)
#     db.commit()
#     db.refresh(booking)
#     return booking


# # ✅ GET ALL BOOKINGS
# def get_all_vehicle_service_bookings(db: Session):
#     return db.query(VehicleServiceBooking).order_by(
#         VehicleServiceBooking.id.desc()
#     ).all()


# def create_vehicle_brand_fuel(db: Session, payload):
#     obj = VehicleBrandFuel(**payload.model_dump())
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def get_all_vehicle_brand_fuel(db: Session):
#     return db.query(VehicleBrandFuel).order_by(
#         VehicleBrandFuel.id.desc()
#     ).all()
    
    
# def create_booking_service_mapping(db: Session, payload):
#     obj = BookingServiceMapping(**payload.model_dump())
#     db.add(obj)
#     db.commit()
#     db.refresh(obj)
#     return obj


# def get_all_booking_service_mapping(db: Session):
#     return db.query(BookingServiceMapping).order_by(
#         BookingServiceMapping.id.desc()
#     ).all()




from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.generated_models import HomeServiceBooking, MasterGarage, MasterMechanic, UserRegistration
from schemas.home_schema import HomeServiceBookingCreateSchema, MasterMechanicCreateSchema


def create_home_service_booking(
    db: Session,
    data: HomeServiceBookingCreateSchema
):
    booking = HomeServiceBooking(
        module_id=data.module_id,
        sub_module_id=data.sub_module_id,
        service_id=data.service_id,
        sub_service_id=data.sub_service_id,

        full_name=data.full_name,
        email=data.email,
        mobile=data.mobile,
        address=data.address,
        preferred_date=data.preferred_date,

        service_summary=data.service_summary,
        total_amount=data.total_amount,

        others_address=data.others_address,
        latitude=data.latitude,
        longitude=data.longitude,

        time_slot_id=data.time_slot_id,
        extra_hours=data.extra_hours,
        bhk_type_id=data.bhk_type_id,
        brand_id=data.brand_id,
        fuel_id=data.fuel_id,
        garage_id=data.garage_id,
        garage_service_id=data.garage_service_id,
        mechanic_id=data.mechanic_id,

        special_instructions=data.special_instructions,
        upload_photos=data.upload_photos,

        payment_done=data.payment_done,
        status_id=data.status_id,

        convenience_fee=data.convenience_fee,
        item_total=data.item_total,

        created_by=data.created_by,
        is_active=True
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking




def get_home_service_bookings(
    db: Session,
    booking_id: int | None = None
):
    query = db.query(HomeServiceBooking).filter(
        HomeServiceBooking.is_active == True
    )

    # 🔹 Fetch by booking id
    if booking_id:
        query = query.filter(HomeServiceBooking.id == booking_id)

    return query.order_by(
        HomeServiceBooking.created_date.desc()
    ).all()


def create_master_mechanic(
    db: Session,
    data: MasterMechanicCreateSchema
):
    # ✅ Validate garage
    garage = db.query(MasterGarage).filter(
        MasterGarage.id == data.garage_id,
        MasterGarage.is_active == True
    ).first()

    if not garage:
        raise HTTPException(
            status_code=400,
            detail=f"Garage ID {data.garage_id} does not exist"
        )

    # ✅ Validate user
    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"User ID {data.user_id} does not exist"
        )

    # ✅ Prevent duplicate (garage_id + user_id)
    existing = db.query(MasterMechanic).filter(
        MasterMechanic.garage_id == data.garage_id,
        MasterMechanic.user_id == data.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Mechanic already exists for this garage"
        )

    mechanic = MasterMechanic(
        garage_id=data.garage_id,
        user_id=data.user_id,
        mechanic_name=data.mechanic_name,
        rating=data.rating,
        is_active=True
    )

    db.add(mechanic)
    db.commit()
    db.refresh(mechanic)

    return mechanic

def get_all_home_services(db: Session):
    query = text("""
        SELECT *
        FROM vw_home_service_booking_summary
        ORDER BY id DESC
    """)

    return db.execute(query).mappings().all()