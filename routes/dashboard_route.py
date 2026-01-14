from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user
from services.dashboard_service import get_dashboard

router = APIRouter(prefix="/api", tags=["User Dashboard"])


@router.get("/User/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_dashboard(db, current_user)
