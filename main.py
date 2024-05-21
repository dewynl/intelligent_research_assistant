import logging
from typing import List

from fastapi import FastAPI, Request, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from data_sources.data_extractor import DataExtractor
from db import create_all_tables, get_db, Article
from sqlalchemy import func

logging.basicConfig(level=logging.DEBUG)

create_all_tables()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Hello World"


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/search/{platform}")
async def search_data(request: Request, platform:str):
    search = request.query_params.get('query')
    extractor = DataExtractor.get_extractor_class(platform=platform)
    if extractor:
        results = extractor.get_results(search)
        results = [result.model_dump() for result in results]
        return results
    else:
        logging.error(f"Unsupported platform: {platform}")
        return []


@app.get('/search')
async def search_articles(request: Request, db: Session = Depends(get_db)):
    search_term = request.query_params.get('query', '')
    found_articles = db.query(Article).filter(func.lower(Article.title).contains(search_term.lower()))
    return found_articles.all()

@app.post("/extract/{platform}")
def extract_data(_: Request, platform: str, article_ids: List[str] = Body(...)):
    extractor = DataExtractor.get_extractor_class(platform=platform)
    if extractor:
        process_id = extractor.extract_data(article_ids)
        return { 'process_id': str(process_id) }
    else:
        logging.error(f"Unsupported platform: {platform}")
        return "Unsupported platform"
