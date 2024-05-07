from sqlalchemy import ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship

DATABASE_NAME = "intelligent_research_assistant"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}.sqlite"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


authors_articles_association = Table(
    "authors_articles_association",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    articles = relationship(
        "Article", secondary=authors_articles_association, back_populates="authors"
    )


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    abstract = Column(String)
    link = Column(String)
    doi = Column(String, nullable=True)
    source = Column(String)
    source_id = Column(String)
    authors = relationship(
        "Author", secondary=authors_articles_association, back_populates="articles"
    )


def create_all_tables():
    Base.metadata.create_all(engine)
