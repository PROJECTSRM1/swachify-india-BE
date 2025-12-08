from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.service_schema import ServiceOrder
from services.service_order_service import save_service_order

router = APIRouter(prefix="/api/cleaning", tags=["Service Booking"])

@router.post("/service")
def create_service_order(payload: ServiceOrder, db: Session = Depends(get_db)):
    order_id = save_service_order(db, payload)
    
    return {
        "message": "Service order created successfully!",
        "order_id": order_id,
    }
