"""
Main Application Initialization Entrypoint for SmartMama.
Sets up the unified router matrix mapping and exposes the complete Swagger UI.
"""

from fastapi import FastAPI
from smartmama.routers import auth_router, chv_router, location_router, mother_router

app = FastAPI(
    title="SmartMama Community Maternal Healthcare API System",
    description="""
    Backend orchestration 
    This interface coordinates maternal tracking records, exact geolocated coordinates, 
    risk classification triggers, and clinical follow-up routing pipelines securely.
    """,
    version="1.0.0",
    docs_url="/docs",      
    redoc_url="/redoc"     
)

API_V1_PREFIX = "/api/v1"

app.include_router(auth_router.router, prefix=API_V1_PREFIX)
app.include_router(chv_router.router, prefix=API_V1_PREFIX)
app.include_router(location_router.router, prefix=API_V1_PREFIX)
app.include_router(mother_router.router, prefix=API_V1_PREFIX)


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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
