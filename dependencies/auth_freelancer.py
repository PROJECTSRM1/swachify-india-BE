from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.database import get_db
from models.user_registration import UserRegistration
from app.config.settings import settings

security = HTTPBearer()

FREELANCER_ROLE_ID = 4


def get_current_freelancer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("user_id")
        role = payload.get("role")

        if role != "freelancer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized as freelancer"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == user_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Freelancer not found"
        )

    return freelancer
