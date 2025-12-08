from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.service_schema import ServiceOrder
import json

def save_service_order(db: Session, payload: ServiceOrder):

    query = text("""
        INSERT INTO service_booking (
            main_category_key,
            sub_category_key,
            module_title,
            module_description,
            base_price,
            service_type,
            property_size_sqft,
            bedrooms,
            bathrooms,
            preferred_date,
            addons,
            instructions,
            full_name,
            email,
            mobile,
            address,
            computed_price
        )
        VALUES (
            :main_category_key,
            :sub_category_key,
            :module_title,
            :module_description,
            :base_price,
            :service_type,
            :property_size_sqft,
            :bedrooms,
            :bathrooms,
            :preferred_date,
            :addons,
            :instructions,
            :full_name,
            :email,
            :mobile,
            :address,
            :computed_price
        )
        RETURNING id;
    """)

    params = {
        "main_category_key": payload.mainCategoryKey,
        "sub_category_key": payload.subCategoryKey,
        "module_title": payload.moduleTitle,
        "module_description": payload.moduleDescription,
        "base_price": payload.basePrice,
        "service_type": payload.serviceType,
        "property_size_sqft": payload.propertySizeSqft,
        "bedrooms": payload.bedrooms,
        "bathrooms": payload.bathrooms,
        "preferred_date": payload.preferredDate,
        "addons": json.dumps(payload.addons),
        "instructions": payload.instructions,
        "full_name": payload.fullName,
        "email": payload.email,
        "mobile": payload.mobile,
        "address": payload.address,
        "computed_price": payload.computedPrice
    }

    result = db.execute(query, params).fetchone()
    db.commit()

    return result[0]
