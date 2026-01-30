from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import generated_models 

from core.database import Base, engine

from routes.user_registration_route import router as user_registration_router
from routes.dashboard_route import router as dashboard_router
from routes.allocation_route import router as allocation_router
from routes.admin_route import router as admin_router
from routes.freelancer_route import router as freelancer_router
from routes.master_module_route import router as master_module_router
from routes.payment_routes import router as payment_router
from routes.task_router import router as task_router
from routes.student_education_route import router as student_education_router
from routes.job_application_openings_route import router as job_application_openings_router
from routes.property_sell_listing_router import router as property_sell_listing_router
from routes.raw_material_routes import router as raw_material_router
from routes.application_routes import router as application_router
from routes.swachify_products_route import router as swachify_products_router
from routes.institution_route import router as institution_router

from routes.healthcare_route import router as healthcare_router

from routes.student_education_route import router as student_profile_router

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
app.include_router(task_router)
app.include_router(student_education_router)
app.include_router(job_application_openings_router)
app.include_router(application_router)
app.include_router(institution_router)
app.include_router(healthcare_router)
app.include_router(property_sell_listing_router)
app.include_router(raw_material_router)
app.include_router(payment_router)
app.include_router(application_router)
app.include_router(student_profile_router)