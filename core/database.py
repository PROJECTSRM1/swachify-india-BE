# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
# import os
# import urllib.parse

# load_dotenv()

# DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_NAME = os.getenv("DB_NAME", "postgres")
# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# USER_ENC = urllib.parse.quote_plus(DB_USER)
# PASSWORD_ENC = urllib.parse.quote_plus(DB_PASSWORD)

# DATABASE_URL = f"postgresql://{USER_ENC}:{PASSWORD_ENC}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
#     pool_size=5,
#     max_overflow=10,
#     connect_args={"connect_timeout": 5},
#     future=True,
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import urllib.parse

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# -------------------------------------------------
# Encode credentials (important for special chars)
# -------------------------------------------------
USER_ENC = urllib.parse.quote_plus(DB_USER)
PASSWORD_ENC = urllib.parse.quote_plus(DB_PASSWORD)

DATABASE_URL = (
    f"postgresql://{USER_ENC}:{PASSWORD_ENC}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -------------------------------------------------
# SQLAlchemy Engine (PRODUCTION SAFE)
# -------------------------------------------------
engine = create_engine(
    DATABASE_URL,

    # ---- Connection Pooling ----
    pool_size=5,              # base pool size
    max_overflow=10,          # temporary extra connections
    pool_pre_ping=True,       # auto-reconnect dead connections
    pool_recycle=1800,        # recycle connections every 30 min

    # ---- Stability ----
    connect_args={
        "connect_timeout": 5  # fail fast if DB is unreachable
    },

    isolation_level="READ COMMITTED",
    echo=False,               # set True ONLY for debugging
    future=True,
)

# -------------------------------------------------
# Session Factory
# -------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# -------------------------------------------------
# Base Model
# -------------------------------------------------
Base = declarative_base()

# -------------------------------------------------
# FastAPI Dependency
# -------------------------------------------------
def get_db():
    """
    Dependency that provides a SQLAlchemy session
    and guarantees connection cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
