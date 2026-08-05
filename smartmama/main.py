from fastapi import FastAPI
from database import Base, engine
import models
from routers.chv_router import router as chv_router
from routers.mother_router import router as mother_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartMama API",
    version="1",
    description="API for SmartMama application"
)

API_V1_PREFIX = "/api/v1"

app.include_router(chv_router, prefix=API_V1_PREFIX)
app.include_router(mother_router, prefix=API_V1_PREFIX)