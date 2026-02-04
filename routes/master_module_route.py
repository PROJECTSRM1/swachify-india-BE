from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.master_module_service import get_all_home_services
from schemas.home_schema import HomeServiceBookingResponse

router = APIRouter(
    prefix="/home-services",
    tags=["Home Services"]
)

@router.get(
    "",
    response_model=list[HomeServiceBookingResponse]
)
def fetch_all_home_services(db: Session = Depends(get_db)):
    return get_all_home_services(db)
