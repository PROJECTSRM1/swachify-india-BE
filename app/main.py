from fastapi import FastAPI
from core.database import Base, engine
from routes.auth import router as user_router
from dotenv import load_dotenv
import os
from routes.freelancer_route import router as freelancer_router
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as user_router

app = FastAPI()  # <-- You must define this BEFORE using app.add_middleware

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_router)

load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user_router)
app.include_router(freelancer_router)



@app.get("/")
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
