from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from .auth import auth_router
from .rules import rules_router
from .sensors import sensors_router
from .controllers import controllers_router
from .charts import charts_router
from fastapi.middleware.cors import CORSMiddleware

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

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.status_code,
            "error_message": exc.detail
        }
    )

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domains for security, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Or specify methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # Or specify headers, e.g., ["Authorization", "Content-Type"]
)

app.include_router(api_router)