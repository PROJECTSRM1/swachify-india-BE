# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# from routes.auth import router as user_router
# from routes.freelancer_route import router as freelancer_router
# from controllers.payment_routes import router as payment_router
# from routes.admin_route import router as admin_router
# from routes.master_module_route import router as master_module_router
# # from models import user_registration
# from models import master_status
# from routes.user_registration_route import router as user_router

# from core.database import Base, engine

# Base.metadata.create_all(bind=engine)

# load_dotenv()

# app = FastAPI(
#     title="Swachify India API",
#     version="1.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.on_event("startup")
# def startup_event():
#     print("Swachify API started successfully on Render!")

# app.include_router(admin_router)
# # app.include_router(user_router, tags=["Customer"])
# app.include_router(freelancer_router, tags=["Freelancer"])
# app.include_router(payment_router, prefix="/api/payments", tags=["Payments"])
# app.include_router(master_module_router)
# app.include_router(user_router)


# @app.get("/")
# def home():
#     return {"message": "Swachify India Backend Running Successfully!"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 🔹 IMPORTANT: import ALL models so SQLAlchemy knows tables
import models  

from core.database import Base, engine

# 🔹 ROUTES
# from routes.auth import router as auth_router
from routes.user_registration_route import router as user_registration_router
from routes.admin_route import router as admin_router
from routes.freelancer_route import router as freelancer_router
from routes.auth import router as auth_router
from routes.master_module_route import router as master_module_router
from controllers.payment_routes import router as payment_router


# 🔹 Load environment variables
load_dotenv()

# 🔹 Create DB tables (safe if already exists)
Base.metadata.create_all(bind=engine)

# 🔹 FastAPI App
app = FastAPI(
    title="Swachify India API",
    version="1.0.0"
)

# 🔹 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Startup event
@app.on_event("startup")
def startup_event():
    print("Swachify API started successfully!")

# 🔹 ROUTER REGISTRATION (ORDER MATTERS FOR READABILITY)
# app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_registration_router)
app.include_router(admin_router)
app.include_router(freelancer_router, prefix="/api/v1/freelancer", tags=["Freelancer"])
# app.include_router(auth_router)
app.include_router(master_module_router, prefix="/api/v1/master", tags=["Master"])
app.include_router(payment_router, prefix="/api/v1/payments", tags=["Payments"])

# 🔹 Health Check
@app.get("/", tags=["Health"])
def home():
    return {"message": "Swachify India Backend Running Successfully!"}
