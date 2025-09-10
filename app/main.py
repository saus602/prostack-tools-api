from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "ProStack Tools API"), version="0.1.0")

# CORS
origins = [o.strip() for o in os.getenv("CORS_ORIGINS","").split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
from app.routes.health import router as health_router
from app.routes.licenses import router as licenses_router
from app.routes.intake import router as intake_router
from app.routes.reports import router as reports_router
from app.routes.prequal import router as prequal_router
from app.routes.stack import router as stack_router
from app.routes.applications import router as apps_router
from app.routes.subtracker import router as sub_router

app.include_router(health_router, tags=["health"])
app.include_router(licenses_router, prefix="/v1", tags=["licenses"])
app.include_router(intake_router, prefix="/v1", tags=["intake"])
app.include_router(reports_router, prefix="/v1", tags=["reports"])
app.include_router(prequal_router, prefix="/v1", tags=["prequal"])
app.include_router(stack_router, prefix="/v1", tags=["stack"])
app.include_router(apps_router, prefix="/v1", tags=["applications"])
app.include_router(sub_router, prefix="/v1", tags=["sub-tracker"])
