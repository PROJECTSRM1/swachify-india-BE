from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db

from schemas.property_sell_listing_schema import (
    PropertySellListingCreate,
    PropertySellListingResponse,
    PropertyListingCreate,
    PropertyListingResponse
)
from services.property_sell_listing_service import (
    create_property_sell_listing,
    get_all_property_sell_listings,
    get_property_sell_listing_by_id,
    create_property_listing,
    get_all_property_listings,
    get_property_listing_by_id
)

router = APIRouter(prefix="/property",tags=["Buy/Sell/Rent Listing"])

@router.post("-sell-listing",response_model=PropertySellListingResponse)
def create(payload: PropertySellListingCreate,db: Session = Depends(get_db)):
    return create_property_sell_listing(payload, db)

@router.get("-sell-listing",response_model=list[PropertySellListingResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_property_sell_listings(db)

@router.get("-sell-listing/{listing_id}",response_model=PropertySellListingResponse)
def get_by_id(listing_id: int,db: Session = Depends(get_db)):
    return get_property_sell_listing_by_id(listing_id, db)


@router.post("-listing",response_model=PropertyListingResponse)
def create(payload: PropertyListingCreate,db: Session = Depends(get_db)):
    return create_property_listing(payload, db)

@router.get("-listing",response_model=list[PropertyListingResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_property_listings(db)

@router.get("-listing/{listing_id}",response_model=PropertyListingResponse)
def get_by_id(listing_id: int,db: Session = Depends(get_db)):
    return get_property_listing_by_id(listing_id, db)
