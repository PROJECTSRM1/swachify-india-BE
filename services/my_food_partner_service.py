from requests import session
from sqlalchemy.orm import Session
from sqlalchemy import text


# 1 Get items by restaurant and category
def get_items_by_restaurant_and_category_service(restaurant_id:int, category_id:int, db:Session):

    query = text("""
        SELECT *
        FROM fn_get_items_by_restaurant_and_category(:restaurant_id,:category_id)
    """)

    result = db.execute(query,{
        "restaurant_id":restaurant_id,
        "category_id":category_id
    })

    return [dict(row._mapping) for row in result]


# 2 Restaurant view data
def get_restaurant_view_data_service(partner_id:int,module_id:int,db:Session):

    query = text("""
        SELECT *
        FROM fn_get_restaurant_view_data(:partner_id,:module_id)
    """)

    result = db.execute(query,{
        "partner_id":partner_id,
        "module_id":module_id
    })

    return [dict(row._mapping) for row in result]


# 3 Partner location
def get_partner_location_service(partner_id:int,db:Session):

    query = text("""
        SELECT *
        FROM fn_manage_partner_location(:partner_id)
    """)

    result = db.execute(query,{
        "partner_id":partner_id
    })

    return [dict(row._mapping) for row in result]


# 4 Partner order counts
def get_partner_order_counts_service(partner_id:int,db:Session):

    query = text("""
        SELECT *
        FROM fn_get_partner_order_counts(:partner_id)
    """)

    result = db.execute(query,{
        "partner_id":partner_id
    })

    return [dict(row._mapping) for row in result]


# 5 Partner revenue by day
def get_partner_revenue_by_day_service(partner_id:int,date:str,db:Session):

    query = text("""
        SELECT *
        FROM fn_get_partner_revenue_by_day(:partner_id,:date)
    """)

    result = db.execute(query,{
        "partner_id":partner_id,
        "date":date
    })

    return [dict(row._mapping) for row in result]


# 6 Partner reviews
def get_partner_reviews_service(partner_id:int,db:Session):

    query = text("""
        SELECT *
        FROM fn_get_partner_reviews(:partner_id)
    """)

    result = db.execute(query,{
        "partner_id":partner_id
    })

    return [dict(row._mapping) for row in result]


# 7 Popular items this week
def get_popular_items_this_week_service(partner_id:int,db:Session):

    query = text("""
        SELECT *
        FROM fn_get_popular_items_this_week(:partner_id)
    """)

    result = db.execute(query,{
        "partner_id":partner_id
    })

    return [dict(row._mapping) for row in result]


# 8 Menu items by meal id
def get_partner_menu_items_by_meal_id_service(partner_id:int,meal_id:int,db:Session):

    query = text("""
        SELECT *
        FROM fn_get_partner_menu_items_by_meal_id(:partner_id,:meal_id)
    """)

    result = db.execute(query,{
        "partner_id":partner_id,
        "meal_id":meal_id
    })

    return [dict(row._mapping) for row in result]


# 9 Add full menu item (procedure)
def add_full_menu_item_service(data:dict,db:Session):

    query = text("""
        CALL sp_add_full_menu_item(:data)
    """)

    db.execute(query,{"data":data})
    db.commit()

    return {"message":"Menu item added successfully"}

#get partner notification
def get_partner_notifications_service(partner_id: int, db:Session):
    
    query = text("""
        SELECT *
        FROM fn_get_partner_notifications(:partner_id)
    """)
    
    result = db.execute(query, {
        "partner_id" : partner_id
    })
    
    return [dict(row._mapping) for row in result]

#get partner messages
def get_partner_messages_services(partner_id: int, db:Session):
    query = text("""
        SELECT *
        FROM fn_get_partner_messages(:partner_id)
    """)
    result = db.execute(query,{"partner_id": partner_id})
    return [dict(row._mapping) for row in result]