from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from models.generated_models import PropertySellListing
from schemas.property_sell_listing_schema import (
    PropertySellListingCreate,
    PropertySellListingUpdate
)
from models.generated_models import PropertyListing
from schemas.property_sell_listing_schema import (
    PropertyListingCreate,
    PropertyListingUpdate
)
# =========================
# CREATE
# =========================

def create_property_sell_listing(
    db: Session,
    payload: PropertySellListingCreate
):
    listing = PropertySellListing(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow(),
        is_active=True
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


# =========================
# GET BY ID
# =========================

def get_property_sell_listing_by_id(
    db: Session,
    listing_id: int
):
    listing = (
        db.query(PropertySellListing)
        .filter(
            PropertySellListing.id == listing_id,
            PropertySellListing.is_active == True
        )
        .first()
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Property sell listing not found"
        )

    return listing


# =========================
# GET ALL
# =========================

def get_all_property_sell_listings(db: Session):
    return (
        db.query(PropertySellListing)
        .filter(PropertySellListing.is_active == True)
        .order_by(PropertySellListing.created_date.desc())
        .all()
    )


# =========================
# UPDATE
# =========================

def update_property_sell_listing(
    db: Session,
    listing_id: int,
    payload: PropertySellListingUpdate
):
    listing = get_property_sell_listing_by_id(db, listing_id)

    update_data = payload.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for key, value in update_data.items():
        setattr(listing, key, value)

    listing.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(listing)
    return listing


# =========================
# SOFT DELETE
# =========================

def delete_property_sell_listing(
    db: Session,
    listing_id: int,
    modified_by: int
):
    listing = get_property_sell_listing_by_id(db, listing_id)

    listing.is_active = False
    listing.modified_by = modified_by
    listing.modified_date = datetime.utcnow()

    db.commit()
    return {
        "message": "Property sell listing deleted successfully"
    }




# =========================
# CREATE
# =========================

def create_property_listing(
    db: Session,
    payload: PropertyListingCreate
):
    listing = PropertyListing(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow(),
        is_active=True
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


# =========================
# GET BY ID
# =========================

def get_property_listing_by_id(
    db: Session,
    listing_id: int
):
    listing = (
        db.query(PropertyListing)
        .filter(
            PropertyListing.id == listing_id,
            PropertyListing.is_active == True
        )
        .first()
    )

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="Property listing not found"
        )

    return listing


# =========================
# GET ALL
# =========================

def get_all_property_listings(db: Session):
    return (
        db.query(PropertyListing)
        .filter(PropertyListing.is_active == True)
        .order_by(PropertyListing.created_date.desc())
        .all()
    )


# =========================
# UPDATE
# =========================

def update_property_listing(
    db: Session,
    listing_id: int,
    payload: PropertyListingUpdate
):
    listing = get_property_listing_by_id(db, listing_id)

    update_data = payload.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for key, value in update_data.items():
        setattr(listing, key, value)

    listing.modified_date = datetime.utcnow()

    db.commit()
    db.refresh(listing)
    return listing


# =========================
# SOFT DELETE
# =========================

def delete_property_listing(
    db: Session,
    listing_id: int,
    modified_by: int
):
    listing = get_property_listing_by_id(db, listing_id)

    listing.is_active = False
    listing.modified_by = modified_by
    listing.modified_date = datetime.utcnow()

    db.commit()
    return {
        "message": "Property listing deleted successfully"
    }

#filtered_property_sell_listings


def get_filtered_property_sell_listings(
    db: Session,
    p_id: int = -1,
    p_property_type_id: int = -1,
    p_listing_type_id: int = -1,
    p_updated_range: str = "-1",
    p_min_rating: int = -1,
    p_limit: int = 10,
    p_offset: int = 0
):
    query = text("""
        SELECT *
        FROM public.fn_get_filtered_property_listings(
            :p_id,
            :p_property_type_id,
            :p_listing_type_id,
            :p_updated_range,
            :p_min_rating,
            :p_limit,
            :p_offset
        )
    """)

    result = db.execute(
        query,
        {
            "p_id": p_id,
            "p_property_type_id": p_property_type_id,
            "p_listing_type_id": p_listing_type_id,
            "p_updated_range": p_updated_range,
            "p_min_rating": p_min_rating,
            "p_limit": p_limit,
            "p_offset": p_offset
        }
    ).mappings().all()

    return result


# from sqlalchemy.orm import Session
# from datetime import datetime
# from fastapi import HTTPException

# from models.generated_models import (
#     PropertySellListing,
#     PropertyListing,
#     PropertySellListingService
# )
# from schemas.property_sell_listing_schema import (
#     PropertyCompositeCreate,
#     PropertyCompositeUpdate
# )

# # ======================================================
# # CREATE PROPERTY (COMPOSITE)
# # ======================================================

# def create_property_full(
#     db: Session,
#     payload: PropertyCompositeCreate
# ):
#     try:
#         # 1️⃣ Property Sell Listing
#         sell = PropertySellListing(
#             **payload.property_sell_listing.dict(exclude_unset=True),
#             created_date=datetime.utcnow()
#         )
#         db.add(sell)
#         db.flush()  # get sell.id

#         # 2️⃣ Property Listing (optional)
#         listing_obj = None
#         if payload.property_listing:
#             listing_obj = PropertyListing(
#                 property_sell_listing_id=sell.id,
#                 **payload.property_listing.dict(exclude_unset=True),
#                 created_date=datetime.utcnow()
#             )
#             db.add(listing_obj)

#         # 3️⃣ Services (optional)
#         service_ids = None
#         if payload.services:
#             service_ids = payload.services.service_ids
#             for sid in service_ids:
#                 db.add(
#                     PropertySellListingService(
#                         property_sell_listing_id=sell.id,
#                         service_id=sid,
#                         is_active=True
#                     )
#                 )

#         db.commit()
#         db.refresh(sell)
#         if listing_obj:
#             db.refresh(listing_obj)

#         return {
#             "property_sell_listing": sell,
#             "property_listing": listing_obj,
#             "services": {"service_ids": service_ids} if service_ids else None,
#             "message": "Property created successfully"
#         }

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e))


# # ======================================================
# # GET PROPERTY BY ID (COMPOSITE)
# # ======================================================

# def get_property_full_by_id(
#     db: Session,
#     property_sell_listing_id: int
# ):
#     sell = db.query(PropertySellListing).filter(
#         PropertySellListing.id == property_sell_listing_id,
#         PropertySellListing.is_active == True
#     ).first()

#     if not sell:
#         raise HTTPException(status_code=404, detail="Property not found")

#     listing = db.query(PropertyListing).filter(
#         PropertyListing.property_sell_listing_id == sell.id,
#         PropertyListing.is_active == True
#     ).first()

#     services = db.query(PropertySellListingService.service_id).filter(
#         PropertySellListingService.property_sell_listing_id == sell.id,
#         PropertySellListingService.is_active == True
#     ).all()

#     service_ids = [s.service_id for s in services]

#     return {
#         "property_sell_listing": sell,
#         "property_listing": listing,
#         "services": {"service_ids": service_ids} if service_ids else None,
#         "message": "Property fetched successfully"
#     }


# # ======================================================
# # UPDATE PROPERTY (COMPOSITE)
# # ======================================================

# def update_property_full(
#     db: Session,
#     property_sell_listing_id: int,
#     payload: PropertyCompositeUpdate
# ):
#     try:
#         sell = db.query(PropertySellListing).filter(
#             PropertySellListing.id == property_sell_listing_id,
#             PropertySellListing.is_active == True
#         ).first()

#         if not sell:
#             raise HTTPException(status_code=404, detail="Property not found")

#         # 1️⃣ Update Property Sell Listing
#         if payload.property_sell_listing:
#             for key, value in payload.property_sell_listing.dict(
#                 exclude_unset=True
#             ).items():
#                 setattr(sell, key, value)

#             sell.modified_date = datetime.utcnow()

#         # 2️⃣ Update Property Listing
#         listing = db.query(PropertyListing).filter(
#             PropertyListing.property_sell_listing_id == sell.id,
#             PropertyListing.is_active == True
#         ).first()

#         if payload.property_listing:
#             if listing:
#                 for key, value in payload.property_listing.dict(
#                     exclude_unset=True
#                 ).items():
#                     setattr(listing, key, value)

#                 listing.modified_date = datetime.utcnow()
#             else:
#                 listing = PropertyListing(
#                     property_sell_listing_id=sell.id,
#                     **payload.property_listing.dict(exclude_unset=True),
#                     created_date=datetime.utcnow()
#                 )
#                 db.add(listing)

#         # 3️⃣ Update Services (replace strategy)
#         if payload.services:
#             db.query(PropertySellListingService).filter(
#                 PropertySellListingService.property_sell_listing_id == sell.id
#             ).update({"is_active": False})

#             for sid in payload.services.service_ids:
#                 db.add(
#                     PropertySellListingService(
#                         property_sell_listing_id=sell.id,
#                         service_id=sid,
#                         is_active=True
#                     )
#                 )

#         db.commit()
#         db.refresh(sell)
#         if listing:
#             db.refresh(listing)

#         return {
#             "property_sell_listing": sell,
#             "property_listing": listing,
#             "services": payload.services.dict() if payload.services else None,
#             "message": "Property updated successfully"
#         }

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e))
