from fastapi import APIRouter
from .auth import auth_router
from .rules import rules_router
from .sensors import sensors_router

# Create a single APIRouter instance to include all routes
api_router = APIRouter()

# Include individual routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(rules_router, prefix="/rules", tags=["Rules"])
api_router.include_router(sensors_router, prefix="/sensors", tags=["Sensors"])

# Export the api_router as app for use in the main application
app = api_router
