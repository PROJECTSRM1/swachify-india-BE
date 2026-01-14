
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import models  

from core.database import Base, engine

from routes.user_registration_route import router as user_registration_router
from routes.dashboard_route import router as dashboard_router
from routes.allocation_route import router as allocation_router
from routes.admin_route import router as admin_router
from routes.freelancer_route import router as freelancer_router
from routes.master_module_route import router as master_module_router
from routes.payment_routes import router as payment_router
from routes.student_education_route import router as student_education_router


load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Swachify India API",version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Swachify API started successfully!")

app.include_router(user_registration_router)
app.include_router(dashboard_router)
app.include_router(allocation_router)
app.include_router(admin_router)
app.include_router(freelancer_router)
app.include_router(master_module_router)
app.include_router(student_education_router)
app.include_router(payment_router)

@app.get("/", tags=["Home"])
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
