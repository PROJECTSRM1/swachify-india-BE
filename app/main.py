from fastapi import FastAPI
from core.database import Base, engine
from routes.auth import router as user_router
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
