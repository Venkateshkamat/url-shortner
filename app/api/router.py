from fastapi import APIRouter
from app.api.routes import urls

api_router = APIRouter()
api_router.include_router(urls.router)