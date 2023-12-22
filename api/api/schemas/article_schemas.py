import datetime
from pydantic import BaseModel, Field

from typing import Literal, Optional


category = Literal[
    "ENTERTAINMENT",
    "MEDIA",
    "U.S. NEWS",
    "BLACK VOICES",
    "STYLE & BEAUTY",
    "PARENTING",
    "CRIME",
    "WOMEN",
    "EDUCATION",
    "BUSINESS",
    "QUEER VOICES",
    "ENVIRONMENT",
    "COMEDY",
    "WEIRD NEWS",
    "CULTURE & ARTS",
    "SCIENCE",
    "WELLNESS",
    "POLITICS",
    "WORLD NEWS",
    "HOME & LIVING",
    "FOOD & DRINK",
    "TECH",
    "SPORTS"
]


class ArticleParams(BaseModel):
    """Article search schema."""

    category: Optional[str] = Field(None, description="Category", enum=category)
    per_page: Optional[int] = Field(10, ge=1, le=100, description="Per page")
    page_index: Optional[int] = Field(0, ge=0, le=100, description="Page index")


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
