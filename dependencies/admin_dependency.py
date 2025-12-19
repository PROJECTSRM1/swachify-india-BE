from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from utils.jwt_utils import verify_token
from models.user_registration import UserRegistration

security = HTTPBearer()
ADMIN_ROLE_ID = 1

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    admin = db.query(UserRegistration).filter(
        UserRegistration.id == payload.get("user_id"),
        UserRegistration.role_id == ADMIN_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found or inactive"
        )

    return admin
