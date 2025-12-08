from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from dotenv import load_dotenv

# ROUTERS
from routes.auth import router as user_router
from routes.freelancer_route import router as freelancer_router

from controllers.payment_routes import router as payment_router


# Load environment first
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
app.include_router(user_router, tags=["Customer"])
app.include_router(freelancer_router, tags=["Freelancer"])
app.include_router(payment_router, prefix="/api/payments", tags=["Payments"])  # <-- NOW VISIBLE IN SWAGGER

@app.get("/")
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
