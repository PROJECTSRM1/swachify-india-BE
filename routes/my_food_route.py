from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.my_food_schema import FoodOrderCreate, FoodOrderRefundRequestCreate, FoodOrderRefundRequestResponse, FoodOrderResponse
from services.my_food_service import (create_food_order, create_refund_request, get_all_refund_requests,get_food_orders,get_food_order_by_id, get_items_by_restaurant_and_category, get_refund_request_by_id, get_restaurant_view_data)
router = APIRouter(prefix="/food-orders", tags=["Food Orders"])


# -----------------------------
# FOOD ORDER APIs
# -----------------------------

@router.post("/", response_model=FoodOrderResponse)
def create_order(order: FoodOrderCreate, db: Session = Depends(get_db)):
    return create_food_order(db, order)


@router.get("/", response_model=list[FoodOrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return get_food_orders(db)


@router.get("/order/{order_id}", response_model=FoodOrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_food_order_by_id(db, order_id)


@router.post("/refund", response_model=FoodOrderRefundRequestResponse)
def create_refund(
    refund: FoodOrderRefundRequestCreate,
    db: Session = Depends(get_db)
):
    return create_refund_request(db, refund)

@router.get("/refund/all")
def get_all_refunds(db: Session = Depends(get_db)):
    return get_all_refund_requests(db)


@router.get("/refund/{refund_id}", response_model=FoodOrderRefundRequestResponse)
def get_refund(refund_id: int, db: Session = Depends(get_db)):
    return get_refund_request_by_id(db, refund_id)

@router.get("/items")
def get_items(
    restaurant_id: int,
    category_id: int,
    db:Session = Depends(get_db)
):
    
    return get_items_by_restaurant_and_category(
        db,
        restaurant_id,
        category_id
    )

@router.get("/view")
def get_restaurant_data(restaurant_id: int,category_id:int,db:Session = Depends(get_db)):
    return get_restaurant_view_data(db,restaurant_id,category_id)
