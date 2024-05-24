import json
import logging

from background_processes.nlp.extract_keywords import extract_keywords
from background_processes.nlp.preprocess_text import preprocess_text
from celery_setup import celery_app
from db import get_db, Research, Status

from transformers import pipeline

@celery_app.task
def process_new_research():
    try:
        db_conn = next(get_db())

        unprocessed_research = db_conn.query(Research).filter(
            Research.research_preprocess_status == Status.NOT_PROCESSED).first()
        unprocessed_research.research_preprocess_status = Status.IN_PROGRESS
        db_conn.commit()  # Updating status so another worker doesn't pick it up.

        all_abstracts = ''
        if unprocessed_research:
            for article in unprocessed_research.articles:
                processed_title, vectorized_title = preprocess_text(article.title)
                processed_abstract, vectorized_abstract = preprocess_text(article.abstract)

                article.cleaned_title = processed_title
                article.title_vector = json.dumps(vectorized_title.toarray().tolist())
                article.cleaned_abstract = processed_abstract
                article.abstract_vector = json.dumps(vectorized_abstract.toarray().tolist())

                all_abstracts += article.abstract + '\n\n'

        keywords = extract_keywords(all_abstracts) if all_abstracts else []
        unprocessed_research.keywords = keywords
        unprocessed_research.research_preprocess_status = Status.DONE

        db_conn.commit()
    except Exception as e:
        logging.error(f"Error occurred while summarizing research: {str(e)}")
        db_conn.rollback()
    finally:
        db_conn.close()

@celery_app.task
def summarize_research():
    try:
        db_conn = next(get_db())
        research = db_conn.query(Research).filter(Research.summary_generation_status == Status.NOT_PROCESSED).first()
        research.summary_generation_status = Status.IN_PROGRESS
        db_conn.commit()

        if research:
            all_abstracts = "\n\n".join([article.abstract for article in research.articles])
            summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="pt")
            summary = summarizer(all_abstracts, max_length=750, min_length=100, do_sample=False)
            research.summary = summary[0]['summary_text']
            research.summary_generation_status = Status.DONE
            db_conn.commit()
        else:
            logging.info("No research found for summarization.")
    except Exception as e:
        logging.error(f"Error occurred while summarizing research: {str(e)}")
        db_conn.rollback()
    finally:
        db_conn.close()

