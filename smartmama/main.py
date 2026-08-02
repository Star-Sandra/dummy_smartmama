"""
Main Application Initialization Entrypoint for SmartMama.
Sets up the unified router matrix mapping, manages database creation hooks, 
and exposes the complete Swagger UI.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

# 1. ABSOLUTE PATH IMPORTS (CLEARS THE PYLANCE RESOLUTION ERROR)
from smartmama.database import engine, Base


# 2. ABSOLUTE ROUTER MATRIX IMPORTS
from smartmama.routers import auth_router, chv_router, location_router, mother_router, visit_router


# 3. DEFINE AUTOMATED LIFECYCLE HOOKS TO SYNC TABLES ON STARTUP
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This automatically builds any missing database tables on startup
    Base.metadata.create_all(bind=engine)
    yield


# 4. INITIALIZE THE MASTER APP CONFIGURATIONS UNIFIED
app = FastAPI(
    title="SmartMama Community Maternal Healthcare API System",
    description="""
    Backend orchestration 
    This interface coordinates maternal tracking records, exact geolocated coordinates, 
    risk classification triggers, and clinical follow-up routing pipelines securely.
    """,
    version="1.0.0",
    docs_url="/docs",      
    redoc_url="/redoc",
    lifespan=lifespan  # Links the automatic table builder
)

API_V1_PREFIX = "/api/v1"

# 5. UNIFIED ROUTER MATRIX
app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(chv_router, prefix=API_V1_PREFIX)
app.include_router(location_router, prefix=API_V1_PREFIX)
app.include_router(mother_router, prefix=API_V1_PREFIX)
app.include_router(visit_router, prefix=API_V1_PREFIX)


@app.get("/", tags=["0. System Status"], summary="Root Platform Health Ping")
def read_root():
    """
    Diagnostic system status check node verifying container availability properties.
    """
    return {
        "status": "online",
        "service": "SmartMama execution framework",
        "environment_configuration": "stable"
    }

if __name__ == "__main__":
    import uvicorn
    # Execute using the module layout path syntax matching your root structure
    uvicorn.run("smartmama.main:app", host="0.0.0.0", port=8000, reload=True)
