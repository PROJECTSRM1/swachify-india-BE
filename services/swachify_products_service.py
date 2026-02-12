from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from models.generated_models import ProductRegistration
from schemas.swachify_products_schema import (ProductRegistrationCreate,ProductRegistrationUpdate)

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
