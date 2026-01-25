from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.db.models import URL
from app.schemas.url import URLCreate
from app.services.shortener import generate_short_code


router = APIRouter()


@router.post("/shorten")
def create_short_url(payload: URLCreate, db: Session = Depends(get_db)):
    for _ in range(10):
        short_code = generate_short_code()
        existing_url = db.query(URL).filter(URL.short_code == short_code).first()
        if not existing_url:
            break
    else:
        raise HTTPException(status_code=500, detail="Failed to generate unique Url")

    url = URL(original_url=str(payload.original_url), short_code=short_code)
    db.add(url)
    try:
        db.commit()
        db.refresh(url)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create short Url")

    return {"short_code": short_code}


@router.get("/stats/{short_code}")
def stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "id": url.id,
        "original_url": str(url.original_url),
        "short_code": url.short_code,
        "created_at": url.created_at.isoformat() if url.created_at else None,
        "expires_at": url.expires_at.isoformat() if url.expires_at else None,
        "clicks": url.clicks,
    }


@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not Available")

    url.clicks += 1
    db.commit()

    return RedirectResponse(str(url.original_url))
