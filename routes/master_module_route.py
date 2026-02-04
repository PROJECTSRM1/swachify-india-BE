from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from services.master_module_service import (
    get_home_service_booking_summary
)

router = APIRouter(
    prefix="/master-module",
    tags=["Master Module"]
)

# ======================================================
# HOME SERVICE BOOKING SUMMARY
# ======================================================

@router.get("/home-service-booking-summary")
def home_service_booking_summary_api(
    institution_id: int = Query(
        -1,
        description="Pass institution_id or -1 to fetch all"
    ),
    db: Session = Depends(get_db)
):
    return get_home_service_booking_summary(
        db=db,
        institution_id=institution_id
    )
