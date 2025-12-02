# utils/jwt_utils.py

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException
import os

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES",120))
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS",7))


def create_access_token(subject: dict) -> str:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=ACCESS_EXPIRE_MINUTES)

    payload = {
        "sub": str(subject["user_id"]),       # 🔥 FIXED: must be string
        "email": subject.get("email"),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: dict) -> str:
    now = datetime.utcnow()
    expire = now + timedelta(days=REFRESH_EXPIRE_DAYS)

    payload = {
        "sub": str(subject["user_id"]),       # 🔥 FIXED
        "email": subject.get("email"),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTError as e:
        # Print actual decode error for debugging
        print("JWT DECODE ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
