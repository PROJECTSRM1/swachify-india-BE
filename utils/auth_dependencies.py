from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from utils.jwt_utils import verify_token
from models.user_registration import UserRegistration

security = HTTPBearer()
FREELANCER_ROLE_ID = 4  # Define the freelancer role ID constant


def get_current_freelancer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)

    freelancer_id = payload.get("sub") or payload.get("user_id")
    role = payload.get("role")

    if not freelancer_id or role != "freelancer":
        raise HTTPException(status_code=403, detail="Not authorized")

    freelancer_id = int(freelancer_id)

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(status_code=401, detail="Invalid freelancer")

    return {
        "user_id": freelancer.id,
        "email": freelancer.email
    }
