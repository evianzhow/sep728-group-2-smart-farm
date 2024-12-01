from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from .auth import auth_router
from .rules import rules_router
from .sensors import sensors_router
from .controllers import controllers_router
from .charts import charts_router

# Create a single APIRouter instance to include all routes
api_router = APIRouter()

# Include individual routers
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(rules_router, tags=["Rules"])
api_router.include_router(sensors_router, tags=["Sensors"])
api_router.include_router(controllers_router, tags=["Controllers"])
api_router.include_router(charts_router, tags=["Charts"])
# Export the api_router as app for use in the main application

app = FastAPI()

def handle_http_exception(exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.status_code,
            "error_message": exc.detail
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.status_code,
            "error_message": exc.detail
        }
    )

app.include_router(api_router)