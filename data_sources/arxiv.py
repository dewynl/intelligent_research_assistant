import logging

import arxiv
from typing import List

from background_processes.nlp.extract_keywords import extract_keywords
from background_processes.create_research import save_research_data
from celery_setup import celery_app
from data_sources.data_extractor import DataExtractor
from schemas import ArticleListItem

logging.basicConfig(level=logging.DEBUG)
def extract_id_from_url(url):
    try:
        start_index = url.index("abs/") + 4
        return url[start_index:]
    except ValueError:
        return None

def format_arxiv_result(results) -> List[ArticleListItem]:
    formatted_results = []
    for result in results:
        article_id = extract_id_from_url(result.entry_id)
        link = [a for a in result.links if a.rel == "alternate"][0].href
        formatted_result = ArticleListItem(
            id=article_id,
            title=result.title,
            authors=[a.name for a in result.authors],
            abstract=result.summary,
            categories=result.categories,
            link=link,
            doi=result.doi,
            pdf_url=result.pdf_url,
        )
        formatted_results.append(formatted_result)

    return formatted_results


class ArxivExtractor(DataExtractor):
    def __init__(self):
        super().__init__()
        self.client = arxiv.Client()

    def get_results(self, query: str, offset=0, max_results=10) -> List[ArticleListItem]:
        # Extract keywords from the query for better search results.
        keywords = extract_keywords(query)
        joined_keywords = " ".join(keywords)
        search = arxiv.Search(
            query=joined_keywords,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        results = self.client.results(search, offset=offset)
        formatted_results = format_arxiv_result(results)
        return formatted_results

    def extract_data(self, ids: List[str]):
        process_id = process_new_research_submission.delay(ids)
        return process_id


@celery_app.task
def process_new_research_submission(ids):
    arxiv_client = arxiv.Client()
    logging.info(f"Processing article with ids: {ids}")
    search_by_id = arxiv.Search(id_list=ids)

    articles_result = arxiv_client.results(search_by_id)
    formatted_articles = format_arxiv_result(articles_result)
    articles_as_dict = [dict(fa) for fa in formatted_articles]

    process_id = save_research_data.delay(articles_as_dict, 'arxiv')
    return process_id
