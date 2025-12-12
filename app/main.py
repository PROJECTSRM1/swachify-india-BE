from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from dotenv import load_dotenv

# ROUTERS
from routes.auth import router as user_router
from routes.freelancer_route import router as freelancer_router
from controllers.payment_routes import router as payment_router
# from routes.service_route import router as home_service_router   # Home Services API
from routes.admin_route import router as admin_router
from routes.master_module_routes import router as master_module_router
from routes.master_sub_module_routes import router as sub_module_router


# Load environment
load_dotenv()

# FastAPI App
app = FastAPI(
    title="Swachify India API",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
Base.metadata.create_all(bind=engine)

# API ROUTES
app.include_router(admin_router)
app.include_router(user_router, tags=["Customer"])
app.include_router(freelancer_router, tags=["Freelancer"])
app.include_router(payment_router, prefix="/api/payments", tags=["Payments"])

# Master Module (temporary file you created)
app.include_router(master_module_router)
app.include_router(sub_module_router)

# Home Service APIs (Cleaning / Electric / Plumbing in future)
# app.include_router(home_service_router, tags=["Home Services"])

@app.get("/")
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
