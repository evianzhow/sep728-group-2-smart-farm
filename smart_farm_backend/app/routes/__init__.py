from fastapi import APIRouter
from .auth import auth_router
from .rules import rules_router
from .sensors import sensors_router
from .controllers import controllers_router

# Create a single APIRouter instance to include all routes
api_router = APIRouter()

# Include individual routers
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(rules_router, tags=["Rules"])
api_router.include_router(sensors_router, tags=["Sensors"])
api_router.include_router(controllers_router, tags=["Controllers"])
# Export the api_router as app for use in the main application
app = api_router
