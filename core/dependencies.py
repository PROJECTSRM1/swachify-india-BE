# from fastapi import Depends, HTTPException, status, Request
# from fastapi.security import HTTPAuthorizationCredentials
# from sqlalchemy.orm import Session

# from core.database import get_db
# from core.security import bearer_scheme
# from utils.jwt_utils import verify_token
# from models.user_registration import UserRegistration


# # ==================================================
# # 🔹 GET CURRENT USER (BEARER TOKEN ONLY)
# # ==================================================
# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
#     db: Session = Depends(get_db)
# ):
#     """
#     Expects:
#     Authorization: Bearer <JWT_TOKEN>
#     """

#     token = credentials.credentials
#     payload = verify_token(token)

#     user_id = payload.get("sub") or payload.get("user_id")

#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token payload"
#         )

#     user = db.query(UserRegistration).filter(
#         UserRegistration.id == int(user_id)
#     ).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )

#     return user


# # ==================================================
# # 🔹 ADMIN-ONLY DEPENDENCY
# # ==================================================
# def get_current_admin(
#     credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
#     db: Session = Depends(get_db)
# ):
#     token = credentials.credentials
#     payload = verify_token(token)

#     user_id = payload.get("sub") or payload.get("user_id")
#     role = payload.get("role")

#     if role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin access required"
#         )

#     user = db.query(UserRegistration).filter(
#         UserRegistration.id == int(user_id)
#     ).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Admin user not found"
#         )

#     return user


# # ==================================================
# # 🔹 OPTIONAL: MANUAL TOKEN EXTRACTION
# # ==================================================
# def get_user_from_request(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     auth_header = request.headers.get("Authorization")

#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authorization header missing"
#         )

#     token = auth_header.replace("Bearer ", "")
#     payload = verify_token(token)

#     user_id = payload.get("sub") or payload.get("user_id")

#     user = db.query(UserRegistration).filter(
#         UserRegistration.id == int(user_id)
#     ).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )

#     return user

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import bearer_scheme
from utils.jwt_utils import verify_token
from models.user_registration import UserRegistration


# ==================================================
# 🔹 GET CURRENT USER (JWT – Bearer Token Only)
# ==================================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Expects:
    Authorization: Bearer <JWT_TOKEN>
    """

    token = credentials.credentials
    payload = verify_token(token)

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

    return user   # ✅ ORM OBJECT


# ==================================================
# 🔹 ADMIN-ONLY DEPENDENCY
# ==================================================
def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
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
# 🔹 OPTIONAL: MANUAL TOKEN EXTRACTION (RARE USE)
# ==================================================
def get_user_from_request(
    request: Request,
    db: Session = Depends(get_db)
):
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
