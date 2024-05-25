import requests

from celery_setup import celery_app
from data_sources.data_extractor import DataExtractor
from db import get_db, Research

ENDPOINT_BASE_URL = 'http://localhost:8000/related-articles'

SUPPORTED_PLATFORMS = ['arxiv']

@celery_app.task
def find_related_articles(research_id, connection_id=None):
    print(f"Trying to find articles related to research ID: {research_id}")
    db_conn = next(get_db())

    research = db_conn.query(Research).filter_by(id=research_id).first()

    related_articles = []
    for platform in SUPPORTED_PLATFORMS:
        extractor = DataExtractor.get_extractor_class(platform=platform)
        query = ' '.join(research.keywords)
        if extractor:
            results = extractor.get_results(query)
            results = [result.model_dump() for result in results]
            related_articles.extend(results)

    # Query external sources to find related articles based on the associated articles
    data = {
        'related_articles': related_articles
    }

    # Send a POST request to the FastAPI endpoint with the related articles data
    url = f"{ENDPOINT_BASE_URL}/{connection_id}"
    response = requests.post(url, json=data)

    if response.status_code != 200:
        print(f"Error sending related articles to FastAPI endpoint: {response.text}")