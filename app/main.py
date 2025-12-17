from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes.auth import router as user_router
from routes.freelancer_route import router as freelancer_router
from controllers.payment_routes import router as payment_router
from routes.admin_route import router as admin_router
from routes.master_module_route import router as master_module_router
from models import user_registration
from models import master_status

load_dotenv()

app = FastAPI(
    title="Swachify India API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Swachify API started successfully on Render!")

app.include_router(admin_router)
app.include_router(user_router, tags=["Customer"])
app.include_router(freelancer_router, tags=["Freelancer"])
app.include_router(payment_router, prefix="/api/payments", tags=["Payments"])
app.include_router(master_module_router)

@app.get("/")
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
