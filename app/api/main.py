from fastapi import APIRouter

from app.api.routes import bikes, amortization

api_router = APIRouter()
api_router.include_router(bikes.router, prefix="/bikes")
api_router.include_router(amortization.router, prefix="/amortization")
