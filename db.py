import json
import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Table, DateTime, TypeDecorator, Enum, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = "intelligent_research_assistant"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}.sqlite"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


authors_articles_association = Table(
    "authors_articles_association",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

researches_articles_association = Table(
    "researches_articles_association",
    Base.metadata,
    Column("research_id", Integer, ForeignKey("researches.id")),
    Column("article_id", Integer, ForeignKey("articles.id")),
)

class Status(enum.Enum):
    NOT_PROCESSED = "not_processed"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class ArrayType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

class Research(Base):
    __tablename__ = "researches"
    id = Column(Integer, primary_key=True)
    articles = relationship("Article", secondary=researches_articles_association, back_populates='researches')
    research_category = Column(String, nullable=True)
    research_process_status = Column(Enum(Status), default=Status.NOT_PROCESSED)
    added_at = Column(DateTime, default=datetime.utcnow)


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
    pdf_url = Column(String, nullable=True)
    source = Column(String)
    source_id = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)
    authors = relationship("Author", secondary=authors_articles_association, back_populates="articles")
    researches = relationship("Research", secondary=researches_articles_association, back_populates='articles')

    # fields to store pre-processed data.
    cleaned_title = Column(String, nullable=True)
    cleaned_abstract = Column(String, nullable=True)
    title_vector = Column(ArrayType, nullable=True)
    abstract_vector = Column(ArrayType, nullable=True)

def create_all_tables():
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
