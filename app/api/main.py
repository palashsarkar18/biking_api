from fastapi import APIRouter

from app.api.routes import bikes, amortization

# Create an API router for including various endpoints
api_router = APIRouter()

# Include the bikes endpoint with a prefix
api_router.include_router(bikes.router, prefix="/bikes")

# Include the amortization endpoint with a prefix
api_router.include_router(amortization.router, prefix="/amortization")
