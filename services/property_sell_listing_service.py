from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.generated_models import PropertySellListing, PropertyListing,UserRegistration
from models.generated_models import MasterCity
from models.master_module import MasterModule
from models.master_sub_module import MasterSubModule
from schemas.property_sell_listing_schema import (PropertySellListingCreate,PropertyListingCreate)



def create_property_sell_listing(payload: PropertySellListingCreate,db: Session):
    if not db.query(MasterModule).filter(
        MasterModule.id == payload.module_id
    ).first():
        raise HTTPException(400, "Invalid module_id")

    if not db.query(MasterSubModule).filter(
        MasterSubModule.id == payload.sub_module_id
    ).first():
        raise HTTPException(400, "Invalid sub_module_id")

    if not db.query(MasterCity).filter(
        MasterCity.id == payload.city_id
    ).first():
        raise HTTPException(400, "Invalid city_id")

    listing = PropertySellListing(**payload.dict())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


def get_all_property_sell_listings(db: Session):
    return db.query(PropertySellListing).filter(
        PropertySellListing.is_active == True
    ).all()


def get_property_sell_listing_by_id(listing_id: int,db: Session):
    listing = db.query(PropertySellListing).filter(
        PropertySellListing.id == listing_id,
        PropertySellListing.is_active == True
    ).first()

    if not listing:
        raise HTTPException(404, "PropertySellListing not found")

    return listing




def create_property_listing(
    payload: PropertyListingCreate,
    db: Session
):
    # ✅ Validate property_sell_listing
    sell_listing = db.query(PropertySellListing).filter(
        PropertySellListing.id == payload.property_sell_listing_id,
        PropertySellListing.is_active == True
    ).first()

    if not sell_listing:
        raise HTTPException(
            status_code=400,
            detail="Invalid property_sell_listing_id"
        )

    # ✅ Validate user
    user = db.query(UserRegistration).filter(
        UserRegistration.id == payload.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id"
        )

    listing = PropertyListing(
        property_sell_listing_id=payload.property_sell_listing_id,
        user_id=payload.user_id,
        created_by=payload.created_by
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


# ---------------- GET ALL ----------------
def get_all_property_listings(db: Session):
    return db.query(PropertyListing).filter(
        PropertyListing.is_active == True
    ).all()


# ---------------- GET BY ID ----------------
def get_property_listing_by_id(
    listing_id: int,
    db: Session
):
    listing = db.query(PropertyListing).filter(
        PropertyListing.id == listing_id,
        PropertyListing.is_active == True
    ).first()

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="PropertyListing not found"
        )

    return listing