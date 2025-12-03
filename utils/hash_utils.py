from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    if len(password) > 72:
        password = password[:72] 
    return pwd_context.hash(password)
