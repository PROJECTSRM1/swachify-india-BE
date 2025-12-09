# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from core.database import get_db
# from schemas.service_schema import ServiceOrder
# from services.service_order_service import save_service_order

# router = APIRouter(prefix="/api/cleaning", tags=["Service Booking"])

# @router.post("/service")
# def create_service_order(payload: ServiceOrder, db: Session = Depends(get_db)):
#     order_id = save_service_order(db, payload)
    
#     return {
#         "message": "Service order created successfully!",
#         "order_id": order_id,
#     }




from fastapi import APIRouter, HTTPException
from schemas.service_schema import ServiceOrder
from services.service_order_service import (
    save_service_order,
    get_all_orders,
    get_order_by_id,
    update_order,
    delete_order
)

router = APIRouter(prefix="/api/cleaning", tags=["Cleaning Services"])


# -----------------------
# CREATE ORDER
# -----------------------
@router.post("/service")
def create_service_order(payload: ServiceOrder):
    order_id = save_service_order(payload)

    return {
        "message": "Service order created successfully!",
        "order_id": order_id,
        "customer": payload.fullName,
        "service": payload.moduleTitle,
    }


# -----------------------
# GET ALL ORDERS
# -----------------------
@router.get("/service")
def fetch_all_orders():
    return {
        "total_orders": len(get_all_orders()),
        "orders": get_all_orders()
    }


# -----------------------
# GET ORDER BY ID
# -----------------------
@router.get("/service/{order_id}")
def fetch_order(order_id: int):
    order = get_order_by_id(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# -----------------------
# UPDATE ORDER
# -----------------------
@router.put("/service/{order_id}")
def update_service(order_id: int, payload: ServiceOrder):
    updated = update_order(order_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "message": "Order updated successfully",
        "data": updated
    }


# -----------------------
# DELETE ORDER
# -----------------------
@router.delete("/service/{order_id}")
def delete_service(order_id: int):
    deleted = delete_order(order_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": f"Order {order_id} deleted successfully"}
