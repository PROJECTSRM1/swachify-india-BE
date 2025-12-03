
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException
from app.config.settings import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_EXPIRE_MINUTES = settings.JWT_EXPIRE_MINUTES
REFRESH_EXPIRE_DAYS = settings.REFRESH_EXPIRE_DAYS


def create_access_token(subject: dict) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_EXPIRE_MINUTES)

    payload = {
        "sub": str(subject["user_id"]),
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
        "sub": str(subject["user_id"]),
        "email": subject.get("email"),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "refresh",
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    print("\n========== VERIFY TOKEN CALLED ==========")
    print("TOKEN RECEIVED:", token)
    print("TOKEN LENGTH:", len(token))
    print("USING SECRET_KEY:", SECRET_KEY)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODE SUCCESS PAYLOAD:", payload)
        return payload

    except ExpiredSignatureError as e:
        print("ERROR TYPE: ExpiredSignatureError")
        print("ERROR MESSAGE:", str(e))
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTError as e:
        print("ERROR TYPE:", type(e).__name__)
        print("ERROR MESSAGE:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
