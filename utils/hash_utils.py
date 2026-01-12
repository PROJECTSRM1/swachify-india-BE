
from passlib.context import CryptContext

_password_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    """
    Hash user passwords using sha256_crypt.
    This must be compatible with login / registration.
    """
    return _password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the stored hash.
    """
    return _password_context.verify(plain_password, hashed_password)
