from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from core.constants import FREELANCER_ROLE_ID, STATUS_APPROVED
from utils.jwt_utils import verify_token
# from models.user_registration import UserRegistration
from models.generated_models import UserRegistration

security = HTTPBearer()

def get_current_freelancer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Authenticate and validate current freelancer from JWT token.
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
    
    Returns:
        Dictionary with freelancer_id, email, role_id, and status_id
    
    Raises:
        HTTPException: If token invalid, user not freelancer, or not approved
    """
    token = credentials.credentials
    payload = verify_token(token)

    # Extract freelancer ID and role_id from JWT token
    freelancer_id = payload.get("user_id")
    role_id = payload.get("role_id")

    # Validate token contains required fields
    if not freelancer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user_id"
        )

    # Validate user is a freelancer
    if role_id != FREELANCER_ROLE_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized: user is not a freelancer"
        )

    freelancer_id = int(freelancer_id)

    # Query database to verify freelancer exists and is active
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == FREELANCER_ROLE_ID,
        UserRegistration.is_active == True
    ).first()

    if not freelancer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Freelancer not found or inactive"
        )

    # Validate freelancer is APPROVED
    if freelancer.status_id != STATUS_APPROVED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Freelancer account is not approved by admin"
        )

    return {
        "user_id": freelancer.id,
        "email": freelancer.email,
        "role_id": freelancer.role_id,
        "status_id": freelancer.status_id
    }
