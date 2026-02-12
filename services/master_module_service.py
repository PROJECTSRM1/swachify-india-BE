from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.generated_models import HomeServiceBooking, HomeServiceBookingServiceMap, MasterGarage, MasterGarageService, MasterMechanic, UserRegistration
from schemas.home_schema import HomeServiceBookingCreateSchema, HomeServiceBookingMapCreateSchema, MasterMechanicCreateSchema
from fastapi import HTTPException, Query
from models.generated_models import HomeServiceBooking, HomeServiceBookingAddOn, HomeServicePayment, MasterGarage, MasterMechanic, UserRegistration
from schemas.home_schema import HomeServiceBookingAddOnCreate, HomeServiceBookingCreateSchema, HomeServicePaymentCreate, MasterMechanicCreateSchema


def create_home_service_booking(db: Session,data: HomeServiceBookingCreateSchema):
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

def get_all_home_service_bookings(db: Session):
    query = text("""
        SELECT *
        FROM fn_get_all_home_service_bookings()
    """)

    result = db.execute(query).mappings().all()

    return result

def create_master_mechanic(db: Session,data: MasterMechanicCreateSchema):
    garage = db.query(MasterGarage).filter(
        MasterGarage.id == data.garage_id,
        MasterGarage.is_active == True
    ).first()

    if not garage:
        raise HTTPException(
            status_code=400,
            detail=f"Garage ID {data.garage_id} does not exist"
        )

    user = db.query(UserRegistration).filter(
        UserRegistration.id == data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"User ID {data.user_id} does not exist"
        )

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

def create_home_service_booking_add_on(db: Session,data: HomeServiceBookingAddOnCreate):
    add_on = HomeServiceBookingAddOn(
        home_service_booking_id=data.home_service_booking_id,
        add_on_id=data.add_on_id,
        duration_id=data.duration_id,
        created_by=data.created_by,
        is_active=True
    )
    db.add(add_on)
    db.commit()
    db.refresh(add_on)
    return add_on

def get_all_home_service_booking_add_ons(db: Session):
    return db.query(HomeServiceBookingAddOn)\
             .filter(HomeServiceBookingAddOn.is_active == True)\
             .all()

def get_all_home_service_bookings(db: Session):
    query = text("""
        SELECT *
        FROM fn_get_all_home_service_bookings()
    """)

    try:
        result = db.execute(query).mappings().all()
        return result
    except Exception as e:
        raise Exception(f"Database function error: {str(e)}")

def get_add_ons_by_booking_id(db: Session,home_service_booking_id: int):
    return db.query(HomeServiceBookingAddOn)\
             .filter(
                 HomeServiceBookingAddOn.home_service_booking_id == home_service_booking_id,
                 HomeServiceBookingAddOn.is_active == True
             ).all()

def create_home_service_payment(db: Session,data: HomeServicePaymentCreate):
    payment = HomeServicePayment(
        booking_id=data.booking_id,
        user_id=data.user_id,
        item_total=data.item_total,
        total_paid=data.total_paid,
        payment_mode=data.payment_mode,
        payment_gateway=data.payment_gateway,
        transaction_id=data.transaction_id,
        convenience_fee=data.convenience_fee,
        payment_status=data.payment_status,
        created_by=data.created_by,
        is_active=True
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def get_all_home_service_payments(db: Session):
    return (
        db.query(HomeServicePayment)
        .filter(HomeServicePayment.is_active == True)
        .all()
    )

def get_payment_by_booking_id(db: Session,booking_id: int):
    return (
        db.query(HomeServicePayment)
        .filter(
            HomeServicePayment.booking_id == booking_id,
            HomeServicePayment.is_active == True
        )
        .all()
    )

def get_payment_by_user_id(db: Session,user_id: int):
    return (
        db.query(HomeServicePayment)
        .filter(
            HomeServicePayment.user_id == user_id,
            HomeServicePayment.is_active == True
        )
        .all()
    )

def get_home_service_booking_summary(db: Session):
    query = text("""
        SELECT *
        FROM vw_home_service_booking_summary
        ORDER BY preferred_date DESC
    """)

    result = db.execute(query)
    return result.mappings().all()


def create_booking_service_map(db: Session, data: HomeServiceBookingMapCreateSchema):
    booking = db.query(HomeServiceBooking).filter(
        HomeServiceBooking.id == data.home_service_booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=400, detail="Home service booking not found")
    service = db.query(MasterGarageService).filter(
        MasterGarageService.id == data.garage_service_id
    ).first()
    if not service:
        raise HTTPException(status_code=400, detail="Garage service not found")
    new_map = HomeServiceBookingServiceMap(
        home_service_booking_id=data.home_service_booking_id,
        garage_service_id=data.garage_service_id,
        quantity=data.quantity,
        service_price=data.service_price,
        created_by=data.created_by
    )
    db.add(new_map)
    db.commit()
    db.refresh(new_map)
    return new_map

def get_all_booking_service_maps(db: Session):
    return db.query(HomeServiceBookingServiceMap).filter(
        HomeServiceBookingServiceMap.is_active == True
    ).all()