from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.my_food_schema import FoodOrderCreate, FoodOrderRefundRequestCreate, FoodOrderRefundRequestResponse, FoodOrderResponse, MyFoodRegistrationCreate, MyFoodRegistrationUpdate, MyFoodRegistrationResponse
from services.my_food_service import (create_food_order, create_refund_request, get_all_refund_requests,get_food_orders,get_food_order_by_id, get_items_by_restaurant_and_category, get_refund_request_by_id, get_restaurant_view_data, create_my_food_registration, get_my_food_registration, get_all_my_food_registrations, update_my_food_registration, delete_my_food_registration)
from schemas.my_food_schema import FoodOrderCreate, FoodOrderResponse, FoodOrderStatusHistoryCreate, FoodOrderRefundRequestCreate, FoodOrderReviewCreate
from services.my_food_service import (create_food_order,get_food_orders,get_food_order_by_id,create_food_order_status_history,create_food_order_refund_request,create_food_order_review)

router = APIRouter(prefix="/food-orders", tags=["Customer Food Orders"])


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

# -----------------------------
# MY FOOD REGISTRATION APIs
# -----------------------------

@router.post("/my-food-registration", response_model=MyFoodRegistrationResponse)
def create_my_food_registration_api(payload: MyFoodRegistrationCreate, db: Session = Depends(get_db)):
    return create_my_food_registration(db, payload)

@router.get("/my-food-registration", response_model=list[MyFoodRegistrationResponse])
def list_my_food_registrations(db: Session = Depends(get_db)):
    return get_all_my_food_registrations(db)

@router.get("/my-food-registration/{registration_id}", response_model=MyFoodRegistrationResponse)
def get_my_food_registration_api(registration_id: int, db: Session = Depends(get_db)):
    return get_my_food_registration(db, registration_id)

@router.put("/my-food-registration/{registration_id}", response_model=MyFoodRegistrationResponse)
def update_my_food_registration_api(registration_id: int, payload: MyFoodRegistrationUpdate, db: Session = Depends(get_db)):
    return update_my_food_registration(db, registration_id, payload)

@router.delete("/my-food-registration/{registration_id}")
def delete_my_food_registration_api(registration_id: int, db: Session = Depends(get_db)):
    return delete_my_food_registration(db, registration_id)
