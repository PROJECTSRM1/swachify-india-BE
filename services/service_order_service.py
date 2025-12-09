# from sqlalchemy import text
# from sqlalchemy.orm import Session
# from schemas.service_schema import ServiceOrder
# import json

# def save_service_order(db: Session, payload: ServiceOrder):

#     query = text("""
#         INSERT INTO service_booking (
#             main_category_key,
#             sub_category_key,
#             module_title,
#             module_description,
#             base_price,
#             service_type,
#             property_size_sqft,
#             bedrooms,
#             bathrooms,
#             preferred_date,
#             addons,
#             instructions,
#             full_name,
#             email,
#             mobile,
#             address,
#             computed_price
#         )
#         VALUES (
#             :main_category_key,
#             :sub_category_key,
#             :module_title,
#             :module_description,
#             :base_price,
#             :service_type,
#             :property_size_sqft,
#             :bedrooms,
#             :bathrooms,
#             :preferred_date,
#             :addons,
#             :instructions,
#             :full_name,
#             :email,
#             :mobile,
#             :address,
#             :computed_price
#         )
#         RETURNING id;
#     """)

#     params = {
#         "main_category_key": payload.mainCategoryKey,
#         "sub_category_key": payload.subCategoryKey,
#         "module_title": payload.moduleTitle,
#         "module_description": payload.moduleDescription,
#         "base_price": payload.basePrice,
#         "service_type": payload.serviceType,
#         "property_size_sqft": payload.propertySizeSqft,
#         "bedrooms": payload.bedrooms,
#         "bathrooms": payload.bathrooms,
#         "preferred_date": payload.preferredDate,
#         "addons": json.dumps(payload.addons),
#         "instructions": payload.instructions,
#         "full_name": payload.fullName,
#         "email": payload.email,
#         "mobile": payload.mobile,
#         "address": payload.address,
#         "computed_price": payload.computedPrice
#     }

#     result = db.execute(query, params).fetchone()
#     db.commit()

#     return result[0]







# services/service_order_service.py

from schemas.service_schema import ServiceOrder

FAKE_DB = []
ORDER_ID_COUNTER = 1   # Start from 1


# CREATE ORDER
def save_service_order(payload: ServiceOrder):
    global ORDER_ID_COUNTER

    order_data = payload.dict()
    order_data["order_id"] = ORDER_ID_COUNTER

    FAKE_DB.append(order_data)

    ORDER_ID_COUNTER += 1  # Increase for next order

    return order_data["order_id"]


# GET ALL ORDERS
def get_all_orders():
    return FAKE_DB


# GET ORDER BY ID
def get_order_by_id(order_id: int):
    for order in FAKE_DB:
        if order["order_id"] == order_id:
            return order
    return None


# UPDATE ORDER
def update_order(order_id: int, payload: ServiceOrder):
    for index, order in enumerate(FAKE_DB):
        if order["order_id"] == order_id:

            updated = payload.dict()
            updated["order_id"] = order_id

            FAKE_DB[index] = updated
            return updated

    return None


# DELETE ORDER
def delete_order(order_id: int):
    for index, order in enumerate(FAKE_DB):
        if order["order_id"] == order_id:
            FAKE_DB.pop(index)
            return True
    return False
