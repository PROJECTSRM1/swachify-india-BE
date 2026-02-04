from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from schemas.home_schema import (
    HomeServiceBookingCreate,
    HomeServiceBookingResponse
)
from services.master_module_service import (
    create_home_service_booking,
    get_home_service_booking
)

router = APIRouter(
    prefix="/home-service-booking",
    tags=["Home Service Booking"]
)

@router.post(
    "",
    response_model=HomeServiceBookingResponse,
    status_code=201
)
def create_booking(
    payload: HomeServiceBookingCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_home_service_booking(db, payload)
    except Exception as e:
        print("DB ERROR:", e)   # 👈 IMPORTANT
        raise HTTPException(
            status_code=500,
            detail=str(e)       # 👈 SHOW REAL ERROR
        )

# =========================
# GET BOOKINGS (ALL / BY ID)
# =========================
@router.get(
    "",
    response_model=List[HomeServiceBookingResponse]
)
def fetch_booking(
    id: Optional[int] = Query(
        None,
        description="Booking ID (optional)"
    ),
    db: Session = Depends(get_db)
):
    result = get_home_service_booking(db, id)

    if id and not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # always return list for response_model consistency
    return result if isinstance(result, list) else [result]
