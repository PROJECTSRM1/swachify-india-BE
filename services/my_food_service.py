from sqlalchemy.orm import Session
from models.generated_models import FoodOrder, FoodOrderStatusHistory, UserRegistration, FoodOrderRefundRequest, FoodOrderReview, MasterRestaurant
from fastapi import HTTPException
from schemas.my_food_schema import FoodOrderCreate, FoodOrderStatusHistoryCreate, FoodOrderRefundRequestCreate, FoodOrderReviewCreate


def create_food_order(db: Session, order: FoodOrderCreate):

    db_order = FoodOrder(
        customer_id=order.customer_id,
        restaurant_id=order.restaurant_id,
        location_type=order.location_type,
        location_details=order.location_details,
        customer_name=order.customer_name,
        contact_number=order.contact_number,
        allocation_type=order.allocation_type,
        delivery_date=order.delivery_date,
        delivery_time_slot=order.delivery_time_slot,
        extra_hours=order.extra_hours,
        convenience_fee=order.convenience_fee,
        total_amount=order.total_amount
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def get_food_orders(db: Session):

    return db.query(FoodOrder).all()


def get_food_order_by_id(db: Session, order_id: int):

    return db.query(FoodOrder).filter(FoodOrder.id == order_id).first()


def create_food_order_status_history(
    db: Session,
    payload: FoodOrderStatusHistoryCreate
):

    # validate user
    user = db.query(UserRegistration).filter(
        UserRegistration.id == payload.created_by,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid created_by user"
        )

    # validate order
    order = db.query(FoodOrder).filter(
        FoodOrder.id == payload.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    obj = FoodOrderStatusHistory(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

# ---------------- REFUND REQUEST ----------------
def create_food_order_refund_request(
    db: Session,
    payload: FoodOrderRefundRequestCreate
):

    user = db.query(UserRegistration).filter(
        UserRegistration.id == payload.created_by,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid created_by user")

    order = db.query(FoodOrder).filter(
        FoodOrder.id == payload.order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    customer = db.query(UserRegistration).filter(
        UserRegistration.id == payload.customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    obj = FoodOrderRefundRequest(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ---------------- FOOD REVIEW ----------------
def create_food_order_review(
    db: Session,
    payload: FoodOrderReviewCreate
):

    user = db.query(UserRegistration).filter(
        UserRegistration.id == payload.created_by,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid created_by user")

    order = db.query(FoodOrder).filter(
        FoodOrder.id == payload.order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    customer = db.query(UserRegistration).filter(
        UserRegistration.id == payload.customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    restaurant = db.query(MasterRestaurant).filter(
        MasterRestaurant.id == payload.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    obj = FoodOrderReview(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj