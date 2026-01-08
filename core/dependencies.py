# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from utils.jwt_utils import verify_token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# class CurrentUser:
#     def __init__(self, user_id: int, email: str = None, role: str = None):
#         self.id = user_id
#         self.email = email
#         self.role = role


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = verify_token(token)

#     user_id = payload.get("user_id")
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token missing user_id"
#         )

#     return CurrentUser(
#         user_id=user_id,
#         email=payload.get("email"),
#         role=payload.get("role")
#     )






from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import oauth2_scheme
from utils.jwt_utils import verify_token
from models.user_registration import UserRegistration


# ==================================================
# 🔹 GET CURRENT USER (JWT REQUIRED)
# ==================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    - Extracts Bearer token
    - Verifies JWT using verify_token()
    - Fetches user from DB
    """

    payload = verify_token(token)

    # Your JWT uses "sub" or may include user_id
    user_id = payload.get("sub") or payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    user = db.query(UserRegistration).filter(
        UserRegistration.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# ==================================================
# 🔹 ADMIN-ONLY DEPENDENCY
# ==================================================
def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    - Allows access only if role == admin
    - Works with your existing JWT payload
    """

    payload = verify_token(token)

    user_id = payload.get("sub") or payload.get("user_id")
    role = payload.get("role")

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    user = db.query(UserRegistration).filter(
        UserRegistration.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found"
        )

    return user


# ==================================================
# 🔹 OPTIONAL: TOKEN FROM REQUEST (NON-OAUTH)
# ==================================================
def get_user_from_request(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Use this if you manually read Authorization header
    (not recommended for normal routes)
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    token = auth_header.replace("Bearer ", "")
    payload = verify_token(token)

    user_id = payload.get("sub") or payload.get("user_id")

    user = db.query(UserRegistration).filter(
        UserRegistration.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
