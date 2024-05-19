import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from data_sources.data_extractor import DataExtractor
from db import create_all_tables

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
