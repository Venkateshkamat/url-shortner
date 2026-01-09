from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responsesRedirectResponse,  imort RedirectResponse
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import URL
from app.schemas.url import URLCreate
from app.services.shortener import generate_short_code


router = APIRouter()

@router.post("/shorten")
def create_short_url(payload: URLCreate, db:Session=Depends(get_db)):
    short_code = generate_short_code()

    url = URL(original_url = payload.original_url, short_code=short_code)
    db.add(url)
    db.commit()
    db.refresh(url)

    return {"short_code": short_code}

@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not Available") 
    
    url.click+=1
    db.commit()
    
    return RedirectResponse(url.orignal_url)

@router.get("/stats/{short_code}")
def stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code==short_code).first()

    if not url:
        raise HTTPException(status_code = 404, detail="URL not found")
    
    return url
