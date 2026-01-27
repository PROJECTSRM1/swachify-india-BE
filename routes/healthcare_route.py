from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.healthcare_schema import (
    AppointmentCreateSchema,
    AppointmentResponseSchema
)
from services.healthcare_service import (
    create_healthcare_appointment,
    get_healthcare_appointments_by_user
)

router = APIRouter(
    prefix="/healthcare",
    tags=["Healthcare"]
)

@router.post(
    "/appointments",
    response_model=AppointmentResponseSchema
)
def book_healthcare_appointment(
    data: AppointmentCreateSchema,
    db: Session = Depends(get_db)
):
    return create_healthcare_appointment(db, data)

@router.get(
    "/appointments/user/{user_id}",
    response_model=list[AppointmentResponseSchema]
)
def get_user_appointments(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_healthcare_appointments_by_user(db, user_id)
