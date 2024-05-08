import logging
from typing import List
from sqlalchemy.orm import sessionmaker

from db import Article, Author, engine
from schemas import ArticleListItem
from celery_setup import celery_app


@celery_app.task
def test_periodic_task():
    logging.info("This is a test periodic task")

@celery_app.task
def save_articles_data(articles: List[ArticleListItem], source: str):
    session = sessionmaker(bind=engine)()

    for article_list_item in articles:
        article = Article(
            title=article_list_item['title'],
            abstract=article_list_item['abstract'],
            link=article_list_item['link'],
            doi=article_list_item['doi'],
            source=source,
            source_id=article_list_item['id'],
        )

        # Save the article to the database
        session.add(article)

        # Process authors
        for author_name in article_list_item['authors']:
            # Check if author already exists
            existing_author = session.query(Author).filter_by(name=author_name).first()

            if existing_author:
                # Add existing author to the article
                article.authors.append(existing_author)
            else:
                # Create a new Author instance
                new_author = Author(name=author_name)
                # Add the new author to the database
                session.add(new_author)
                # Add the new author to the article
                article.authors.append(new_author)

        # Commit the changes to the database
        session.commit()



@celery_app.task
def poll_newly_added_articles():
    logging.info("Polling for new articles that needs processing...")



    pass