from api.settings import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models


class QdrantAccessObject:
    """QdrantAccessObject is a class that provides access to Qdrant database."""

    def __init__(self) -> None:
        self.qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    def search(
        self, collection_name: str, vector: list[float], top: int, category: str
    ) -> dict:
        """Search for the nearest neighbors of a vector in a collection

        Args:
            collection_name (str): Collection name
            vector (list): Vector
            top (int): Number of neighbors

        Returns:
            dict: Nearest neighbors
        """
        return self.qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=top,
            offset=1,
            score_threshold=0.8,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="category",
                        match=models.MatchValue(
                            value=category,
                        ),
                    ),
                ]
            ),
        )
