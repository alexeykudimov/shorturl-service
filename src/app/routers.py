from fastapi import APIRouter

from src.app.shortener.endpoints import router as shortener_router


api_router = APIRouter()

api_router.include_router(shortener_router, prefix='/shortener', tags=['Shortener'])