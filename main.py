import json
import logging
import os
from fastapi import FastAPI, Request
from celery import Celery

from data_sources.data_extractor import DataExtractor
from db import create_all_tables

logging.basicConfig(level=logging.DEBUG)

create_all_tables()

app = FastAPI()

celery_broker_url = os.environ.get('CELERY_BROKER_URL', "redis://localhost:6379/0")
celery_app = Celery('tasks', broker=celery_broker_url, backend=celery_broker_url)

@app.get("/")
async def root():
    return {"message": "Hello World"}


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


@app.get("/extract/{platform}")
def extract_data(request: Request, platform:str):
    article_ids = json.loads(request.query_params.get('article_ids', ''))
    extractor = DataExtractor.get_extractor_class(platform=platform)
    if extractor:
        results = extractor.extract_data(article_ids)
        return results
    else:
        logging.error(f"Unsupported platform: {platform}")
        return "Unsupported platform"

