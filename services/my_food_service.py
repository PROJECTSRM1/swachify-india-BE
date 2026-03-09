from sqlalchemy.orm import Session
from models.generated_models import FoodOrder
from schemas.my_food_schema import FoodOrderCreate


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