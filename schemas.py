from pydantic import BaseModel
from typing import List, Optional


class ArticleListItem(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    categories: List[str]
    link: str
    doi: Optional[str]
    pdf_url: Optional[str]
