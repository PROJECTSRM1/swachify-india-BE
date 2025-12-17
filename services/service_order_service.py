
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
