from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db

# =========================
# SCHEMAS
# =========================

from schemas.property_sell_listing_schema import (
    PropertySellListingCreate,
    PropertySellListingUpdate,
    PropertySellListingResponse,
    PropertyListingCreate,
    PropertyListingUpdate,
    PropertyListingResponse
)

# =========================
# SERVICES
# =========================

from services.property_sell_listing_service import (
    create_property_sell_listing,
    get_property_sell_listing_by_id,
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

# =========================
# ROUTER
# =========================

router = APIRouter(
    prefix="/property",
    tags=["Property"]
)

# ======================================================
# PROPERTY SELL LISTING ROUTES
# ======================================================

@router.post(
    "/sell-listing",
    response_model=PropertySellListingResponse
)
def create_sell_listing(
    payload: PropertySellListingCreate,
    db: Session = Depends(get_db)
):
    return create_property_sell_listing(db, payload)


@router.get(
    "/sell-listing/{listing_id}",
    response_model=PropertySellListingResponse
)
def get_sell_listing_by_id(
    listing_id: int,
    db: Session = Depends(get_db)
):
    return get_property_sell_listing_by_id(db, listing_id)


@router.get(
    "/sell-listing",
    response_model=List[PropertySellListingResponse]
)
def get_all_sell_listings(
    db: Session = Depends(get_db)
):
    return get_all_property_sell_listings(db)


# @router.put(
#     "/sell-listing/{listing_id}",
#     response_model=PropertySellListingResponse
# )
# def update_sell_listing(
#     listing_id: int,
#     payload: PropertySellListingUpdate,
#     db: Session = Depends(get_db)
# ):
#     return update_property_sell_listing(db, listing_id, payload)


# @router.delete(
#     "/sell-listing/{listing_id}"
# )
# def delete_sell_listing(
#     listing_id: int,
#     modified_by: int,
#     db: Session = Depends(get_db)
# ):
#     return delete_property_sell_listing(db, listing_id, modified_by)

# ======================================================
# PROPERTY LISTING ROUTES
# ======================================================

@router.post(
    "/listing",
    response_model=PropertyListingResponse
)
def create_listing(
    payload: PropertyListingCreate,
    db: Session = Depends(get_db)
):
    return create_property_listing(db, payload)


@router.get(
    "/listing/{listing_id}",
    response_model=PropertyListingResponse
)
def get_listing_by_id(
    listing_id: int,
    db: Session = Depends(get_db)
):
    return get_property_listing_by_id(db, listing_id)


@router.get(
    "/listing",
    response_model=List[PropertyListingResponse]
)
def get_all_listings(
    db: Session = Depends(get_db)
):
    return get_all_property_listings(db)


# @router.put(
#     "/listing/{listing_id}",
#     response_model=PropertyListingResponse
# )
# def update_listing(
#     listing_id: int,
#     payload: PropertyListingUpdate,
#     db: Session = Depends(get_db)
# ):
#     return update_property_listing(db, listing_id, payload)


# @router.delete(
#     "/listing/{listing_id}"
# )
# def delete_listing(
#     listing_id: int,
#     modified_by: int,
#     db: Session = Depends(get_db)
# ):
#     return delete_property_listing(db, listing_id, modified_by)




# from fastapi import APIRouter, Depends, Path
# from sqlalchemy.orm import Session

# from core.database import get_db
# from schemas.property_sell_listing_schema import (
#     PropertyCompositeCreate,
#     PropertyCompositeUpdate,
#     PropertyCompositeResponse
# )
# from services.property_sell_listing_service import (
#     create_property_full,
#     update_property_full,
#     get_property_full_by_id
# )

# router = APIRouter(
#     prefix="/property",
#     tags=["Property"]
# )

# # ======================================================
# # CREATE PROPERTY (COMPOSITE)
# # ======================================================

# @router.post(
#     "/full",
#     response_model=PropertyCompositeResponse
# )
# def create_property_full_api(
#     payload: PropertyCompositeCreate,
#     db: Session = Depends(get_db)
# ):
#     return create_property_full(db, payload)


# # ======================================================
# # GET PROPERTY BY ID (COMPOSITE)
# # ======================================================

# @router.get(
#     "/full/{property_sell_listing_id}",
#     response_model=PropertyCompositeResponse
# )
# def get_property_full_api(
#     property_sell_listing_id: int = Path(..., gt=0),
#     db: Session = Depends(get_db)
# ):
#     return get_property_full_by_id(db, property_sell_listing_id)


# # ======================================================
# # UPDATE PROPERTY (COMPOSITE)
# # ======================================================

# @router.put(
#     "/full/{property_sell_listing_id}",
#     response_model=PropertyCompositeResponse
# )
# def update_property_full_api(
#     payload: PropertyCompositeUpdate,
#     property_sell_listing_id: int = Path(..., gt=0),
#     db: Session = Depends(get_db)
# ):
#     return update_property_full(db, property_sell_listing_id, payload)
