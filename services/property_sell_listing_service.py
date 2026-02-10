from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from models.generated_models import PropertySellListing
from schemas.property_sell_listing_schema import (PropertySellListingCreate,PropertySellListingUpdate)
from models.generated_models import PropertyListing
from schemas.property_sell_listing_schema import (
    PropertyListingCreate,
    PropertyListingUpdate
)

# ======================================================
# CREATE
# ======================================================

def create_property_sell_listing(db: Session,payload: PropertySellListingCreate):
    listing = PropertySellListing(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow()
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


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
        raise HTTPException(status_code=404, detail="Property sell listing not found")

    return listing


# ======================================================
# GET ALL
# ======================================================

def get_all_property_sell_listings(db: Session):
    return (
        db.query(PropertySellListing)
        .filter(PropertySellListing.is_active == True)
        .order_by(PropertySellListing.created_date.desc())
        .all()
    )


# ======================================================
# UPDATE
# ======================================================

def update_property_sell_listing(
    db: Session,
    listing_id: int,
    payload: PropertySellListingUpdate
):
    listing = get_property_sell_listing_by_id(db, listing_id)

    data = payload.dict(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    for key, value in data.items():
        setattr(listing, key, value)
    listing.modified_date = datetime.utcnow()
    db.commit()
    db.refresh(listing)
    return listing


# ======================================================
# SOFT DELETE
# ======================================================

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
    return {"message": "Property sell listing deleted successfully"}


# =========================
# CREATE
# =========================

def create_property_listing(
    db: Session,
    payload: PropertyListingCreate
):
    listing = PropertyListing(
        **payload.dict(exclude_unset=True),
        created_date=datetime.utcnow()
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

def get_all_property_listings(db: Session):
    return (
        db.query(PropertyListing)
        .filter(PropertyListing.is_active == True)
        .order_by(PropertyListing.created_date.desc())
        .all()
    )

def update_property_listing(db: Session,listing_id: int,payload: PropertyListingUpdate):
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

def delete_property_listing(db: Session,listing_id: int,modified_by: int):
    listing = get_property_listing_by_id(db, listing_id)
    listing.is_active = False
    listing.modified_by = modified_by
    listing.modified_date = datetime.utcnow()
    db.commit()
    return {
        "message": "Property listing deleted successfully"
    }

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