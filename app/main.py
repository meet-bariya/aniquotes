from fastapi import FastAPI, Depends, HTTPException, status
from .schemas import Quote
from . import models
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .db import get_db, SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://meetbariya.co",
    "https://meetbariya.co",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def main():
    routes = ['GET / ',
    'GET /quote',
    'GET /quote/{id}',
    'POST /quote',
    'DELETE /quote/{id}',
    'PUT /quote/{id}',
    'GET /random',
    'GET /characters',
    'GET /character/{name}']

    return {'routes':routes} 

@app.get('/quote')
async def get_all_quotes(db: Session = Depends(get_db)):
    quotes = db.query(models.Quote).order_by(models.Quote.created_at.desc()).all()

    if quotes == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Quotes Available")

    return quotes 

@app.get('/quote/{id}')
async def get_quote(id:int,db: Session = Depends(get_db)):
    quote = db.query(models.Quote).filter(models.Quote.id == id).first()

    if quote == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Quote Available")

    return quote 

@app.post('/quote')
async def create_quote(quote: Quote ,db: Session = Depends(get_db)):
    quote = models.Quote(**quote.dict())
    if quote == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Data..")
    
    db.add(quote)
    db.commit()
    db.refresh(quote)

    return quote 

@app.delete('/quote/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(id:int,db: Session = Depends(get_db)):
    quote = db.query(models.Quote).filter(models.Quote.id == id)
    if quote == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Quote with {id} does not exists.")

    quote.delete(synchronize_session=False)
    db.commit()
    return
    
@app.put('/quote/{id}')
async def update_quote(id:int,quote:Quote,db: Session = Depends(get_db)):
    quote = models.Quote(**quote.dict())
    update_quote = db.query(models.Quote).filter(models.Quote.id == id).first()
    if update_quote == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Quote with {id} does not exists.")
    
    update_quote.anime = quote.anime
    update_quote.character = quote.character
    update_quote.quote = quote.quote

    db.commit()
    db.refresh(update_quote)
    return update_quote

@app.get('/random')
async def get_random_quote(db: Session = Depends(get_db)):
    quote = db.query(models.Quote).order_by(func.random()).first()
    return quote

@app.get('/characters')
async def get_characters(db: Session = Depends(get_db)):
    characters = []
    for row in db.query(models.Quote).with_entities(models.Quote.character,models.Quote.id).distinct(models.Quote.character).all():
        characters.append(row.character)

    return characters

@app.get('/character/{name}')
async def search_character(name: str,db: Session = Depends(get_db)):
    characters = db.query(models.Quote).filter(models.Quote.character.like(f'%{name}%')).all()
    return characters