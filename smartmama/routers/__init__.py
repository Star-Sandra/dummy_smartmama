from .auth_router import router as auth_router
from .chv_router import router as chv_router
from .location_router import router as location_router
from .mother_router import router as mother_router
from .visit import router as visit_router  # 👈 Add this line to import your file

# Export them all cleanly for main.py to read
__all__ = [
    "auth_router",
    "chv_router",
    "location_router",
    "mother_router",
    "visit_router"  # 👈 Add this line to the list
]
