from sqlalchemy import text
from sqlalchemy.orm import Session
from models.generated_models import FoodOrder, FoodOrderRefundRequest
from schemas.my_food_schema import FoodOrderCreate, FoodOrderRefundRequestCreate


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

# def create_refund_request(db: Session, refund: FoodOrderRefundRequestCreate):

#     db_refund = FoodOrderRefundRequest(
#         order_id=refund.order_id,
#         customer_id=refund.customer_id,
#         issue_type=refund.issue_type,
#         issue_description=refund.issue_description,
#         issue_photos=refund.issue_photos,
#         refund_amount=refund.refund_amount
#     )

#     db.add(db_refund)
#     db.commit()
#     db.refresh(db_refund)

#     return db_refund


# def get_all_refund_requests(db: Session):

#     return db.query(FoodOrderRefundRequest).all()


# def get_refund_request_by_id(db: Session, refund_id: int):

#     return db.query(FoodOrderRefundRequest).filter(
#         FoodOrderRefundRequest.id == refund_id
#     ).first()

def create_refund_request(db: Session, refund: FoodOrderRefundRequestCreate):
    db_refund = FoodOrderRefundRequest(
        order_id = refund.order_id,
        customer_id = refund.customer_id,
        issue_type = refund.issue_type,
        issue_description =refund.issue_photos,
        issue_photos = refund.issue_photos,
        refund_amount = refund.refund_amount
    )
    db.add(db_refund)
    db.commit()
    db.refresh(db_refund)

    return db_refund

def get_all_refund_requests(db: Session):
    return db.query(FoodOrderRefundRequest).all()
def get_refund_request_by_id(db: Session, refund_id: int):
    return db.query(FoodOrderRefundRequest).filter(
        FoodOrderRefundRequest.id == refund_id
    ).first()
def get_items_by_restaurant_and_category(db: Session, restaurant_id: int, category_id:int):

    query = text("""
        SELECT * 
        FROM get_items_by_restaurant_and_category(:restaurant_id, :category_id)
    """)
    result = db.execute(
        query,
        {
            "restaurant_id": restaurant_id,
            "category_id": category_id
        }
    )
    return result.mappings().all()

def get_restaurant_view_data(db: Session, restaurant_id: int, category_id: int):

    query = text("""
        SELECT * 
        FROM get_restaurant_view_data(:restaurant_id, :category_id)
    """)

    result = db.execute(
        query,
        {
            "restaurant_id": restaurant_id,
            "category_id": category_id
        }
    )

    return result.mappings().all()