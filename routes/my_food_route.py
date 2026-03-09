from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.my_food_schema import FoodOrderCreate, FoodOrderResponse, FoodOrderStatusHistoryCreate, FoodOrderRefundRequestCreate, FoodOrderReviewCreate
from services.my_food_service import (create_food_order,get_food_orders,get_food_order_by_id,create_food_order_status_history,create_food_order_refund_request,create_food_order_review)

router = APIRouter(prefix="/food-orders", tags=["Food Orders"])

@router.post("/", response_model=FoodOrderResponse)
def create_order(order: FoodOrderCreate, db: Session = Depends(get_db)):
    return create_food_order(db, order)

@router.get("/", response_model=list[FoodOrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return get_food_orders(db)

@router.get("/{order_id}", response_model=FoodOrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_food_order_by_id(db, order_id)

@router.post("/food-order-status-history")
def create_food_order_status_history_api(
    payload: FoodOrderStatusHistoryCreate,
    db: Session = Depends(get_db)
):
    return create_food_order_status_history(db, payload)

# ---------------- REFUND REQUEST ----------------
@router.post("/food-order-refund-request")
def create_food_order_refund_request_api(
    payload: FoodOrderRefundRequestCreate,
    db: Session = Depends(get_db)
):
    return create_food_order_refund_request(db, payload)


# ---------------- FOOD REVIEW ----------------
@router.post("/food-order-review")
def create_food_order_review_api(
    payload: FoodOrderReviewCreate,
    db: Session = Depends(get_db)
):
    return create_food_order_review(db, payload)