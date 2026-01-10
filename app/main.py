from fastapi import FastAPI
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.db.models import URL

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortner")

app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    create_tables()