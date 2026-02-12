from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.swachify_products_schema import (
    ProductRegistrationCreate,
    # ProductRegistrationUpdate,
    ProductRegistrationResponse,
    ProductOrderCreate,
    ProductOrderResponse
)
from services.swachify_products_service import (
    create_product_registration,
    get_product_registration_by_id,
    get_all_product_registrations,
    # update_product_registration,
    # delete_product_registration,
    create_product_order,
    get_product_order_by_id
)

router = APIRouter(prefix="/product-registration",tags=["Swachify Products"])

@router.post("/",response_model=ProductRegistrationResponse)
def create_product(payload: ProductRegistrationCreate,db: Session = Depends(get_db)):
    return create_product_registration(db, payload)

@router.get("/{product_id}",response_model=ProductRegistrationResponse)
def get_product(product_id: int,db: Session = Depends(get_db)):
    return get_product_registration_by_id(db, product_id)

@router.get("/",response_model=List[ProductRegistrationResponse])
def get_products(db: Session = Depends(get_db)):
    return get_all_product_registrations(db)

# @router.put("/{product_id}",response_model=ProductRegistrationResponse)
# def update_product(product_id: int,payload: ProductRegistrationUpdate,db: Session = Depends(get_db)):
#     return update_product_registration(db, product_id, payload)


# @router.delete("/{product_id}")
# def delete_product(
#     product_id: int,
#     modified_by: int,
#     db: Session = Depends(get_db)
# ):
#     return delete_product_registration(db, product_id, modified_by)

# ===============================
# POST - CREATE ORDER
# ===============================

@router.post("/orders", response_model=ProductOrderResponse)
def create_order(order: ProductOrderCreate, db: Session = Depends(get_db)):
    return create_product_order(db, order)


# ===============================
# GET - ORDER BY ID
# ===============================

@router.get("/orders/{order_id}", response_model=ProductOrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = get_product_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Product order not found")
    return order