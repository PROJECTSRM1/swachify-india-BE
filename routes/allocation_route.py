from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db,SessionLocal
from core.dependencies import get_current_user
from models.user_registration import UserRegistration
from services.allocation_service import (
    get_allocation_options,
    auto_allocate_employee,
    manual_allocate_employee
)

router = APIRouter(prefix="/api/allocation", tags=["Allocation"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/options/{booking_id}")
def allocation_options(
    booking_id: int,
    db: Session = Depends(get_db),
    user:UserRegistration=Depends(get_current_user)
):
    return get_allocation_options(db, booking_id, user.id)

@router.post("/auto/{booking_id}")
def auto_allocate(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return auto_allocate_employee(
        db=db,
        booking_id=booking_id,
        system_user_id=current_user.id
    )


@router.post("/manual/{booking_id}/{employee_id}")
def manual_allocate(
    booking_id: int,
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return manual_allocate_employee(
        db=db,
        booking_id=booking_id,
        employee_id=employee_id,
        current_user_id=current_user.id
    )
