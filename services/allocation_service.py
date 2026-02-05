from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, and_
from fastapi import HTTPException, status

from models.generated_models import (
    HomeServiceBooking,
    UserRegistration,
    UserServices
)

from core.constants import (
    CUSTOMER_ROLE_ID,
    FREELANCER_ROLE_ID,
    STATUS_APPROVED,
    BOOKING_STATUS_ASSIGNED,
    WORK_STATUS_ON_THE_WAY
)

def get_allocation_options(
    db: Session,
    booking_id: int,
    user_id: int
):
    # Validate booking ownership
    booking = db.query(HomeServiceBooking).filter(
        HomeServiceBooking.id == booking_id,
        HomeServiceBooking.created_by == user_id,
        HomeServiceBooking.is_active.is_(True)
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access"
        )

    if booking.assigned_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already allocated"
        )

    # ✅ SHOW ALL APPROVED FREELANCERS
    freelancers = (
        db.query(
            UserRegistration.id,
            UserRegistration.first_name,
            UserRegistration.last_name,
            UserRegistration.address,
            func.coalesce(func.avg(HomeServiceBooking.rating), 0).label("avg_rating")
        )
        .outerjoin(
            HomeServiceBooking,
            and_(
                HomeServiceBooking.assigned_to == UserRegistration.id,
                HomeServiceBooking.is_active.is_(True)
            )
        )
        .filter(
            UserRegistration.role_id == FREELANCER_ROLE_ID,
            UserRegistration.status_id == STATUS_APPROVED,
            UserRegistration.is_active.is_(True)
        )
        .group_by(UserRegistration.id)
        .order_by(desc("avg_rating"))
        .all()
    )

    return [
        {
            "employee_id": emp.id,
            "name": f"{emp.first_name} {emp.last_name}",
            "address": emp.address,
            "rating": round(emp.avg_rating, 1)
        }
        for emp in freelancers
    ]

# ---------------------------------------------------------
# AUTO ALLOCATION (ROUND-ROBIN + RATING)
# ---------------------------------------------------------
def auto_allocate_employee(
    db: Session,
    booking_id: int,
    system_user_id: int
):
    """
    Auto allocation strategy:
    1. Fewest active assignments
    2. Highest rating
    """

    booking = db.query(HomeServiceBooking).filter(
        HomeServiceBooking.id == booking_id,
        HomeServiceBooking.created_by == system_user_id,
        HomeServiceBooking.is_active.is_(True)
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.assigned_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already allocated"
        )

    freelancer = (
        db.query(UserRegistration)
        .join(
            UserServices,
            and_(
                UserServices.user_id == UserRegistration.id,
                UserServices.module_id == booking.module_id
            )
        )
        .outerjoin(
            HomeServiceBooking,
            and_(
                HomeServiceBooking.assigned_to == UserRegistration.id,
                HomeServiceBooking.is_active.is_(True)
            )
        )
        .filter(
            UserRegistration.role_id == FREELANCER_ROLE_ID,
            UserRegistration.status_id == STATUS_APPROVED,
            UserRegistration.is_active.is_(True)
        )
        .group_by(UserRegistration.id)
        .order_by(
            asc(func.count(HomeServiceBooking.id)),   # workload
            desc(func.coalesce(func.avg(HomeServiceBooking.rating), 0))  # rating
        )
        .first()
    )

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No freelancers available for this service"
        )

    booking.assigned_to = freelancer.id
    booking.status_id = BOOKING_STATUS_ASSIGNED
    booking.work_status_id = WORK_STATUS_ON_THE_WAY

    db.commit()
    db.refresh(booking)

    return {
        "message": "Employee auto-allocated successfully",
        "booking_id": booking.id,
        "assigned_to": freelancer.id,
        "strategy": "Round-robin with rating priority"
    }


# ---------------------------------------------------------
# MANUAL ALLOCATION (ADMIN / CUSTOMER)
# ---------------------------------------------------------
def manual_allocate_employee(
    db: Session,
    booking_id: int,
    employee_id: int,
    current_user_id: int
):
    booking = db.query(HomeServiceBooking).filter(
        HomeServiceBooking.id == booking_id,
        HomeServiceBooking.created_by == current_user_id,
        HomeServiceBooking.is_active.is_(True)
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.assigned_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already allocated"
        )

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == employee_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.status_id == STATUS_APPROVED,
        UserRegistration.is_active.is_(True)
    ).first()

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Freelancer not found or not approved"
        )

    booking.assigned_to = freelancer.id
    booking.status_id = BOOKING_STATUS_ASSIGNED   # ✅ FIXED (NO TUPLE)
    booking.work_status_id = WORK_STATUS_ON_THE_WAY
    booking.modified_by = current_user_id

    db.commit()
    db.refresh(booking)

    return {
        "message": "Employee manually allocated successfully",
        "booking_id": booking.id,
        "assigned_to": freelancer.id
    }
