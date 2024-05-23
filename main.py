import logging
from typing import List
from fastapi import FastAPI, WebSocket, Request, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload

from data_sources.data_extractor import DataExtractor
from db import create_all_tables, get_db, Article, Research
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Process the received data and send a response if needed
        await websocket.send_text(f"Message received: {data}")


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


@app.get('/researches')
def get_researches(_: Request, db: Session = Depends(get_db)):
    researches = db.query(Research).all()
    return researches


@app.get('/research/{research_id}')
def get_research(_: Request, research_id: str, db_conn: Session = Depends(get_db)):
    research = db_conn.query(Research).options(joinedload(Research.articles).joinedload(Article.authors)).filter_by(id=research_id).first()
    print(research.id)
    return research