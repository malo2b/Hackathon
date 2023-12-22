import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

import pandas as pd
from openai import OpenAI

from .settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class Pipeline:
    """Pipeline to insert articles in the database and in Qdrant"""

    def __init__(self, dataset_file_name: str) -> None:
        """Initialize the pipeline."""
        self.collection_name: str = "articles"
        self.dataset_file_name: str = dataset_file_name
        try:
            self.qdrant_client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
            self.postgre_client = psycopg2.connect(
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD,
                host=settings.DATABASE_URL,
                port=settings.DATABASE_PORT,
                database=settings.DATABASE_NAME,
            )
        except Exception as e:
            raise e

    def __del__(self) -> None:
        """Close the connection to the database."""
        self.postgre_client.close()

    def _get_dataset(self) -> pd.DataFrame:
        """Get a json dataset from a path

        Args:
            path (str): Path to the dataset

        Returns:
            pd.DataFrame: Dataset
        """
        return pd.read_json(self.dataset_file_name, lines=True)

    def _insert_article_in_qdrant(
        self, index: int, article: dict, embedding: list
    ) -> None:
        """Insert an article in Qdrant

        Args:
            article (dict): Article to insert
        """
        try:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    {
                        "id": index,
                        "payload": {
                            "title": article["headline"],
                            "category": article["category"],
                            "short_description": article["short_description"],
                            "link": article["link"],
                            "date": article["date"],
                            "authors": article["authors"],
                        },
                        "vector": embedding,
                    }
                ],
            )
        except Exception as e:
            print(e)

    def _get_embedding(self, input: str) -> list:
        """Get an embedding from a text

        Args:
            input (str): Text to embed

        Returns:
            pd.DataFrame: Embedding
        """
        text = input.replace("\n", " ")
        try:
            return (
                client.embeddings.create(input=[text], model="text-embedding-ada-002")
                .data[0]
                .embedding
            )
        except Exception as e:
            print(e)

    def _insert_article_in_db(
        self, index: int, article: dict, embeddings: list
    ) -> None:
        """Insert an article in the database

        Args:
            article (dict): Article to insert
            vectors (list): Embedding of the article
        """
        query: str = """ INSERT INTO articles
            (id, vector, link, headline, category, short_description, authors, date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            index,
            embeddings,
            article["link"],
            article["headline"],
            article["category"],
            article["short_description"],
            article["authors"],
            article["date"],
        )
        try:
            self.postgre_client.cursor().execute(query, values)
            self.postgre_client.commit()
        except Exception as e:
            print(e)

    def run(self) -> None:
        """Run the pipeline."""

        # Get the dataset
        dataset: pd.DataFrame = self._get_dataset()

        # get 10K first rows
        articles: pd.DataFrame = dataset.head(10000)
        # articles: pd.DataFrame = dataset  # dataset.head(10)

        # Create the collection
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

        # Drop the table if exists
        self.postgre_client.cursor().execute(
            f"DROP TABLE IF EXISTS {self.collection_name}"
        )

        # Create the table
        query: str = f""" CREATE TABLE {self.collection_name} (
            id SERIAL PRIMARY KEY,
            vector FLOAT[],
            link TEXT,
            headline TEXT,
            category TEXT,
            short_description TEXT,
            authors TEXT,
            date DATE
        )
        """
        self.postgre_client.cursor().execute(query)

        # Insert the articles
        for index, article in articles.iterrows():
            embedding: list = self._get_embedding(
                f"""{article["date"]} - {article["short_description"]}"""
            )
            article: dict = article.to_dict()
            self._insert_article_in_qdrant(index, article, embedding)
            self._insert_article_in_db(index, article, embedding)


pipeline = Pipeline("data_pipeline/News_Category_Dataset_v3.json")
pipeline.run()
