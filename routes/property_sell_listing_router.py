from fastapi import APIRouter, Depends,Query
from requests import session
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.property_sell_listing_schema import (
    PropertySellListingCreate,
    PropertySellListingUpdate,
    PropertySellListingResponse,
    PropertyListingCreate,
    PropertyListingUpdate,
    PropertyListingResponse
)
from services.property_sell_listing_service import (
    create_property_sell_listing,
    get_property_sell_listing_by_id,
    get_filtered_property_sell_listings,
    get_all_property_sell_listings,
    update_property_sell_listing,
    delete_property_sell_listing
)
from services.property_sell_listing_service import (
    create_property_listing,
    get_property_listing_by_id,
    get_all_property_listings,
    update_property_listing,
    delete_property_listing
)

router = APIRouter(prefix="/property",tags=["Buy/Sell/Rental"])

@router.post("/sell-listing",response_model=PropertySellListingResponse)
def create_sell_listing(payload: PropertySellListingCreate,db: Session = Depends(get_db)):
    return create_property_sell_listing(db, payload)

@router.get(
    "/sell-listing/all",
    response_model=list[PropertySellListingResponse]
)
def get_sell_listing_all(db: Session = Depends(get_db)):
    return get_all_property_sell_listings(db)

@router.delete("/delete/sell/{listing_id}")
def delete_sell_listing(
    listing_id: int,
    modified_by: int,
    db: Session = Depends(get_db)
):
    return delete_property_sell_listing(
        db=db,
        listing_id=listing_id,
        modified_by=modified_by
    )

# @router.get("/sell-listing/{listing_id}",response_model=PropertySellListingResponse)
# def get_sell_listing_by_id(listing_id: int,db: Session = Depends(get_db)):
#     return get_property_sell_listing_by_id(db, listing_id)


@router.post("/listing",response_model=PropertyListingResponse)
def create_listing(payload: PropertyListingCreate,db: Session = Depends(get_db)):
    return create_property_listing(db, payload)

@router.get("/listing/all",response_model=list[PropertyListingResponse])
def get_listing_by_id(db: Session = Depends(get_db)):
    return get_all_property_listings(db)


# @router.get("/listing/{listing_id}",response_model=PropertyListingResponse)
# def get_listing_by_id(listing_id: int,db: Session = Depends(get_db)):
#     return get_property_listing_by_id(db, listing_id)

@router.get("/filter")
def fetch_filter_property_sell_listing(
    p_id:int = Query(-1),
    p_property_type_id: int = Query(-1),
    p_listing_type_id: int = Query(-1),
    p_updated_range: str = Query("-1"),
    p_min_rating:int = Query(-1),
    p_limit: int = Query(10),
    p_offset: int = Query(0),
    db:session = Depends(get_db)

):
    return{
        "status":True,
        "data": get_filtered_property_sell_listings(
            db=db,
            p_id=p_id,
            p_property_type_id=p_property_type_id,
            p_listing_type_id=p_listing_type_id,
            p_updated_range=p_updated_range,
            p_min_rating=p_min_rating,
            p_limit=p_limit,
            p_offset=p_offset
        )

    }

@router.delete("/delete/{listing_id}")
def delete_listing(
    listing_id: int,
    modified_by: int,
    db: Session = Depends(get_db)
):
    return delete_property_listing(
        db=db,
        listing_id=listing_id,
        modified_by=modified_by
    )