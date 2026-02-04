from sqlalchemy.orm import Session
from models.generated_models import HomeServiceBooking
from schemas.home_schema import HomeServiceBookingCreate


def create_home_service_booking(
    db: Session,
    payload: HomeServiceBookingCreate
):
    booking = HomeServiceBooking(
        **payload.model_dump(exclude_unset=True)
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_home_service_booking(
    db: Session,
    booking_id: int | None = None
):
    query = db.query(HomeServiceBooking)

    if booking_id:
        return query.filter(HomeServiceBooking.id == booking_id).first()

    return query.order_by(HomeServiceBooking.id.desc()).all()
