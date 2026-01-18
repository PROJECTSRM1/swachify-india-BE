from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import and_,func,desc, asc
from sqlalchemy.sql import literal
from models.generated_models import HomeService,UserRegistration,UserServices
from core.constants import (
    CUSTOMER_ROLE_ID,
    FREELANCER_ROLE_ID,
    STATUS_APPROVED,
    BOOKING_STATUS_ASSIGNED,
    WORK_STATUS_ON_THE_WAY
)
from fastapi import HTTPException

def get_allocation_options(db, booking_id: int, user_id: int):

    # 1. Validate booking ownership
    booking = db.query(HomeService).filter(
        HomeService.id == booking_id,
        HomeService.created_by == user_id,
        HomeService.is_active == True
    ).first()

    if not booking:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this booking"
        )
    
    # Check if already allocated
    if booking.assigned_to:
        raise HTTPException(
            status_code=400,
            detail="Booking is already allocated to a freelancer"
        )

    employees = (
        db.query(
            UserRegistration.id,
            UserRegistration.first_name,
            UserRegistration.last_name,
            UserRegistration.address,
            func.coalesce(func.avg(HomeService.rating), 0).label("avg_rating")
        )
        .join(UserServices, UserServices.user_id == UserRegistration.id)
        .outerjoin(
            HomeService,
            HomeService.assigned_to == UserRegistration.id
        )
        .filter(
            UserServices.module_id == booking.module_id,
            UserRegistration.is_active == True,
            UserRegistration.role_id == FREELANCER_ROLE_ID,
            UserRegistration.status_id == STATUS_APPROVED,
            UserRegistration.is_active == True
        )
        .group_by(UserRegistration.id)
        .order_by(desc("avg_rating"))
        .all()
    )

    # 3. Response mapping (UI-friendly)
    return [
        {
            "employee_id": emp.id,
            "name": f"{emp.first_name} {emp.last_name}",
            "address": emp.address,
            "rating": round(emp.avg_rating, 1)
        }
        for emp in employees
    ]

def auto_allocate_employee(
    db: Session,
    booking_id: int,
    system_user_id: int
):
    """
    Auto-allocate booking using ROUND-ROBIN strategy:
    - Prefers freelancers with fewer active assignments
    - Falls back to highest rating if workload is equal
    - Ensures fair distribution across team
    """
    booking = db.query(HomeService).filter(
        HomeService.id == booking_id,
        HomeService.created_by == system_user_id,
        HomeService.is_active.is_(True)
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.assigned_to:
        raise HTTPException(
            status_code=400,
            detail="Employee already assigned"
        )

    # 🔹 Find employees who provide this module/service
    # ✅ ORDER BY: Workload (ASC) → Rating (DESC)
    # This ensures fair distribution while maintaining quality
    employee = (
        db.query(UserRegistration)
        .join(UserServices, UserServices.user_id == UserRegistration.id)
        .outerjoin(
            HomeService,
            HomeService.assigned_to == UserRegistration.id
        )
        .filter(
            UserRegistration.role_id == FREELANCER_ROLE_ID,
            UserServices.module_id == booking.module_id,
            UserRegistration.is_active.is_(True),
            UserRegistration.status_id == STATUS_APPROVED
        )
        .group_by(UserRegistration.id)
        .order_by(
            asc(func.count(HomeService.id)),  # 🟢 Fewest assignments first
            desc(func.coalesce(func.avg(HomeService.rating), 0))  # 🟢 Then highest rating
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="No employees available for this service"
        )

    booking.assigned_to = employee.id
    booking.status_id = BOOKING_STATUS_ASSIGNED
    booking.work_status_id = WORK_STATUS_ON_THE_WAY

    db.commit()
    db.refresh(booking)

    return {
        "message": "Employee auto-allocated successfully (Round-Robin strategy)",
        "booking_id": booking.id,
        "assigned_to": employee.id,
        "strategy": "Distributes work evenly across freelancers"
    }


def manual_allocate_employee(
    db: Session,
    booking_id: int,
    employee_id: int,
    current_user_id: int
):
    booking = db.query(HomeService).filter(
        HomeService.id == booking_id,
        HomeService.created_by == current_user_id,
        HomeService.is_active.is_(True)
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )
    
    # Check if already allocated
    if booking.assigned_to:
        raise HTTPException(
            status_code=400,
            detail="Booking is already allocated to a freelancer. Cannot allocate again."
        )

    employee = db.query(UserRegistration).filter(
        UserRegistration.id == employee_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active.is_(True),
        UserRegistration.status_id == STATUS_APPROVED
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    booking.assigned_to = employee.id
    booking.status_id = BOOKING_STATUS_ASSIGNED, # ASSIGNED
    booking.work_status_id = WORK_STATUS_ON_THE_WAY
    booking.modified_by = current_user_id

    db.commit()
    db.refresh(booking)

    return {
        "message": "Employee manually allocated",
        "booking_id": booking.id,
        "assigned_to": employee.id
    }
