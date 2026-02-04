from sqlalchemy.orm import Session

from models.generated_models import HomeServiceBookingAddOn, HomeServicePayment
from schemas.home_schema import HomeServiceBookingAddOnCreate, HomeServicePaymentCreate

#home_service_booking_add_on
# -------- CREATE --------
def create_home_service_booking_add_on(
    db: Session,
    data: HomeServiceBookingAddOnCreate
):
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


# -------- GET ALL --------
def get_all_home_service_booking_add_ons(db: Session):
    return db.query(HomeServiceBookingAddOn)\
             .filter(HomeServiceBookingAddOn.is_active == True)\
             .all()


# -------- GET BY BOOKING ID --------
def get_add_ons_by_booking_id(
    db: Session,
    home_service_booking_id: int
):
    return db.query(HomeServiceBookingAddOn)\
             .filter(
                 HomeServiceBookingAddOn.home_service_booking_id == home_service_booking_id,
                 HomeServiceBookingAddOn.is_active == True
             ).all()

#home_service_payment

# -------- CREATE --------
def create_home_service_payment(
    db: Session,
    data: HomeServicePaymentCreate
):
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


# -------- GET ALL --------
def get_all_home_service_payments(db: Session):
    return db.query(HomeServicePayment)\
             .filter(HomeServicePayment.is_active == True)\
             .all()


# -------- GET BY BOOKING ID --------
def get_payment_by_booking_id(
    db: Session,
    booking_id: int
):
    return db.query(HomeServicePayment)\
             .filter(
                 HomeServicePayment.booking_id == booking_id,
                 HomeServicePayment.is_active == True
             ).all()


# -------- GET BY USER ID --------
def get_payment_by_user_id(
    db: Session,
    user_id: int
):
    return db.query(HomeServicePayment)\
             .filter(
                 HomeServicePayment.user_id == user_id,
                 HomeServicePayment.is_active == True
             ).all()
