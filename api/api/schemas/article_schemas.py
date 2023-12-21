import datetime
from pydantic import BaseModel

from typing import Optional


class Article(BaseModel):
    """Article schema."""

    id: Optional[int] = None
    title: str
    category: str
    short_description: str
    link: str
    date: datetime.date
    authors: str
    embedding: Optional[list[float]] = None


class Articles(BaseModel):
    """Articles schema."""

    data: list[Article]


class ArticleAndRelated(BaseModel):
    """Article and related schema."""

    article: Article
    related: list[Article]


__all__ = ["Article"]
