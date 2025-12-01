# utils/jwt_utils.py

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "change_me")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 15))
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


# ---------------------------------------------------------
# CREATE ACCESS TOKEN
# ---------------------------------------------------------
def create_access_token(subject: dict) -> str:
    """
    subject should be: { "user_id": 1, "email": "x@y.com" }
    We store only user_id in "sub"
    """
    now = datetime.utcnow()
    payload = {
        "sub": subject["user_id"],        # <---- only store user_id
        "email": subject.get("email"),    # optional
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_EXPIRE_MINUTES),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# CREATE REFRESH TOKEN
# ---------------------------------------------------------
def create_refresh_token(subject: dict) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject["user_id"],
        "email": subject.get("email"),
        "iat": now,
        "exp": now + timedelta(days=REFRESH_EXPIRE_DAYS),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# VERIFY TOKEN (Used in /me and verify-token API)
# ---------------------------------------------------------
def verify_token(token: str) -> dict:
    """
    Returns decoded payload if valid.
    Raises ExpiredSignatureError if expired,
    Raises JWTError if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token expired")

    except JWTError:
        raise JWTError("Invalid token")
