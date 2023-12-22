from api.dao.postgre import PostgreAccessObject
from api.dao.qdrant import QdrantAccessObject
from api.schemas.article_schemas import (
    Article,
    Articles,
    ArticleAndRelated,
    ArticleParams,
)


class ArticleService:
    """ArticleService is a class that provides access to articles."""

    def __init__(self) -> None:
        self.qdrant_dao: QdrantAccessObject = QdrantAccessObject()
        self.postgre_dao: PostgreAccessObject = PostgreAccessObject()

    async def get_articles(self, params: ArticleParams) -> Articles:
        """Get all articles from the database

        Returns:
            Articles: Articles
        """
        columns: str = "id, link, headline, category, short_description, authors, date"
        result = self.postgre_dao.select(
            "articles",
            columns,
            where=f"articles.category = '{params.category}'" if params.category else None,
            limit=params.per_page,
            offset=params.per_page * params.page_index,
        )
        articles: Articles = Articles(
            data=[
                Article(
                    id=article[0],
                    link=article[1],
                    title=article[2],
                    category=article[3],
                    short_description=article[4],
                    authors=article[5],
                    date=article[6],
                )
                for article in result
            ]
        )
        return articles

    async def get_related_articles(self, article_id: int) -> Article:
        """Get a random article from the database

        Returns:
            Article: Article
        """
        columns: str = (
            "id, link, headline, category, short_description, authors, date, vector"
        )
        result = self.postgre_dao.select("articles", columns, f"id = {article_id}")
        article: Article = Article(
            id=result[0][0],
            link=result[0][1],
            title=result[0][2],
            category=result[0][3],
            short_description=result[0][4],
            authors=result[0][5],
            date=result[0][6],
            embedding=result[0][7],
        )

        result = self.qdrant_dao.search(
            collection_name="articles", vector=article.embedding, top=3, category=article.category
        )

        related_articles: list[Article] = []
        for related_article in result:
            related_articles.append(
                Article(
                    link=related_article.payload["link"],
                    title=related_article.payload["title"],
                    category=related_article.payload["category"],
                    short_description=related_article.payload["short_description"],
                    authors=related_article.payload["authors"],
                    date=related_article.payload["date"],
                )
            )

        article.embedding = None

        return ArticleAndRelated(
            article=article,
            related=related_articles,
        )


__all__ = ["ArticleService"]
