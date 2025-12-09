# main.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, utils

app = FastAPI()

# Create tables on startup
models.init_db()

# Database Dependency
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ShortenRequest(BaseModel):
    original_url: str

@app.post("/api/shorten")
def create_short_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    # 1. Insert original URL to get a unique ID
    new_mapping = models.UrlMapping(original_url=payload.original_url)
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    
    # 2. Generate short code (Offset ID by 10000 to avoid single digit codes)
    code = utils.encode_base62(new_mapping.id + 10000)
    new_mapping.short_code = code
    db.commit()
    
    return {"original_url": payload.original_url, "short_code": code}

@app.get("/{short_code}")
def redirect_to_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    mapping = db.query(models.UrlMapping).filter(models.UrlMapping.short_code == short_code).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Short code not found")
    
    # Track the click
    click = models.Click(
        url_mapping_id=mapping.id,
        client_ip=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    db.add(click)
    db.commit()
    
    return RedirectResponse(url=mapping.original_url, status_code=302)

@app.get("/api/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    mapping = db.query(models.UrlMapping).filter(models.UrlMapping.short_code == short_code).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Not found")
        
    return {
        "short_code": short_code,
        "original_url": mapping.original_url,
        "total_clicks": len(mapping.clicks)
    }