from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from models.generated_models import ProductRegistration,ProductOrder,UserRegistration,MasterVehicleType
from schemas.swachify_products_schema import (ProductRegistrationCreate,ProductRegistrationUpdate,ProductOrderCreate)

def create_product_registration(db: Session, request: ProductRegistrationCreate):

    new_product = ProductRegistration(
        user_id=request.user_id,
        category_id=request.category_id,
        company_name=request.company_name,
        product_name=request.product_name,
        address=request.address,
        product_price=request.product_price,
        description=request.description,
        product_image=request.product_image,
        longitude=request.longitude,
        latitude=request.latitude,

        # ✅ Auto assign created_by = user_id
        created_by=request.user_id,

        is_active=request.is_active
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_product_registration_by_id(db: Session,product_id: int):
    product = db.query(ProductRegistration).filter(
        ProductRegistration.id == product_id,
        ProductRegistration.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

def get_all_product_registrations(db: Session):
    return db.query(ProductRegistration).filter(
        ProductRegistration.is_active == True
    ).all()

def update_product_registration(db: Session,product_id: int,payload: ProductRegistrationUpdate):
    product = get_product_registration_by_id(db, product_id)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(product, key, value)
    product.modified_date = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product

def delete_product_registration(db: Session,product_id: int,modified_by: int):
    product = get_product_registration_by_id(db, product_id)
    product.is_active = False
    product.modified_by = modified_by
    product.modified_date = datetime.utcnow()
    db.commit()
    return {"message": "Product deleted successfully"}


# ===============================
# CREATE ORDER
# ===============================

def create_product_order(db: Session, order_data: ProductOrderCreate):

    # 🔎 Validate User
    user = db.query(UserRegistration).filter(
        UserRegistration.id == order_data.user_id,
        UserRegistration.is_active == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id. User does not exist."
        )

    # 🔎 Validate Product
    product = db.query(ProductRegistration).filter(
        ProductRegistration.id == order_data.product_id,
        ProductRegistration.is_active == True
    ).first()

    if not product:
        raise HTTPException(
            status_code=400,
            detail="Invalid product_id. Product does not exist."
        )

    # 🔎 Validate Vehicle Type (if provided)
    if order_data.vehicle_type_id:
        vehicle = db.query(MasterVehicleType).filter(
            MasterVehicleType.id == order_data.vehicle_type_id
        ).first()

        if not vehicle:
            raise HTTPException(
                status_code=400,
                detail="Invalid vehicle_type_id. Vehicle type does not exist."
            )

    # ✅ Create Order
    new_order = ProductOrder(**order_data.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


# ===============================
# GET ORDER BY ID
# ===============================

def get_product_order_by_id(db: Session, order_id: int) -> Optional[ProductOrder]:
    return db.query(ProductOrder).filter(
        ProductOrder.id == order_id,
        ProductOrder.is_active == True
    ).first()