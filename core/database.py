
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

USER_ENC = urllib.parse.quote_plus(DB_USER)
PASSWORD_ENC = urllib.parse.quote_plus(DB_PASSWORD)

DATABASE_URL = (f"postgresql://{USER_ENC}:{PASSWORD_ENC}"f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL,pool_size=5,max_overflow=10,pool_pre_ping=True,pool_recycle=1800,connect_args={"connect_timeout": 5 },isolation_level="READ COMMITTED",echo=False,         future=True,)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False,expire_on_commit=False,)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
