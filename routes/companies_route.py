# routes/companies_route.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from services.companies_service import get_all_companies
from schemas.companies_schema import CompanyListResponse

router = APIRouter(
    prefix="/api/companies",
    tags=["Companies"]
)


@router.get(
    "",
    response_model=List[CompanyListResponse],
    summary="Get all companies "
)
def get_companies_api(
    industry_id: Optional[int] = Query(None),
    company_size_id: Optional[int] = Query(None),
    location: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(
        None,
        description="latest | jobs | internships"
    ),
    db: Session = Depends(get_db)
):
    """
    Default:
    - Returns ALL companies
    - No filters required
    """

    return get_all_companies(
        db=db,
        industry_id=industry_id,
        company_size_id=company_size_id,
        location=location,
        sort_by=sort_by
    )
