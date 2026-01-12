from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.db.models import URL

def create_tables():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="URL Shortner")

app.include_router(api_router)
