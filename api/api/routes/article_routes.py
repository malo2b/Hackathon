from fastapi import APIRouter, Depends, Response, status

from api.schemas.article_schemas import Article, ArticleParams
from api.services.article_services import ArticleService


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("")
async def get_articles(params: ArticleParams = Depends(), service: ArticleService = Depends()) -> Article:
    """Get a random article from the database

    Returns:
        Article: Article
    """
    result = await service.get_articles(params)
    return Response(content=result.model_dump_json(), status_code=status.HTTP_200_OK)


@router.get("/{id}/related")
async def get_related_articles(id: int, service: ArticleService = Depends()) -> Article:
    """Get a random article from the database

    Returns:
        Article: Article
    """
    result = await service.get_related_articles(id)
    return Response(content=result.model_dump_json(), status_code=status.HTTP_200_OK)


__all__ = ["router"]
