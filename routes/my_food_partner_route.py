from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from core.database import get_db

from services.my_food_partner_service import *

router = APIRouter(
    prefix="/my-food-partner",
    tags=["My food Partner Dashboard"]
)


# 1 Restaurant items
@router.get("/restaurant-items")
def get_items_by_restaurant_and_category(
        restaurant_id:int,
        category_id:int,
        db:Session = Depends(get_db)
):
    return get_items_by_restaurant_and_category_service(restaurant_id,category_id,db)


# 2 Restaurant view
@router.get("/restaurant-view")
def get_restaurant_view(
        partner_id:int,
        module_id:int,
        db:Session = Depends(get_db)
):
    return get_restaurant_view_data_service(partner_id,module_id,db)


# 3 Partner location
@router.get("/location")
def get_partner_location(
        partner_id:int,
        db:Session = Depends(get_db)
):
    return get_partner_location_service(partner_id,db)


# 4 Order counts
@router.get("/order-counts")
def get_partner_order_counts(
        partner_id:int,
        db:Session = Depends(get_db)
):
    return get_partner_order_counts_service(partner_id,db)


# 5 Revenue by day
@router.get("/revenue")
def get_partner_revenue(
        partner_id:int,
        date:str,
        db:Session = Depends(get_db)
):
    return get_partner_revenue_by_day_service(partner_id,date,db)


# 6 Reviews
@router.get("/reviews")
def get_partner_reviews(
        partner_id:int,
        db:Session = Depends(get_db)
):
    return get_partner_reviews_service(partner_id,db)


# 7 Popular items
@router.get("/popular-items")
def get_popular_items(
        partner_id:int,
        db:Session = Depends(get_db)
):
    return get_popular_items_this_week_service(partner_id,db)


# 8 Menu items by meal
@router.get("/menu-items-by-meal")
def get_menu_items_by_meal(
        partner_id:int,
        meal_id:int,
        db:Session = Depends(get_db)
):
    return get_partner_menu_items_by_meal_id_service(partner_id,meal_id,db)


# 9 Add full menu item
@router.post("/add-full-menu-item")
def add_full_menu_item(
        data:dict,
        db:Session = Depends(get_db)
):
    return add_full_menu_item_service(data,db)

#Notification API
@router.get("/notification")
def get_partner_notifications(
    partner_id: int,
    db: Session = Depends(get_db)
):
    return get_partner_notifications_service(partner_id, db)

#Messages API
@router.get("/messages")
def get_partner_messages(
    partner_id:int,
    db:Session =Depends(get_db)
):
    return get_partner_messages_services(partner_id, db)
    