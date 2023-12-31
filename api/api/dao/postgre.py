from fastapi import HTTPException, status
import psycopg2

from ..settings import settings

class PostgreAccessObject:
    def __init__(self):
        # self.conn = psycopg2.connect(
        #     host="localhost",
        #     database="mydatabase",
        #     user="myuser",
        #     password="mypassword",
        #     port="5432",
        # )
        self.conn = psycopg2.connect(
            host=settings.DATABASE_URL,
            database=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            port=settings.DATABASE_PORT,
        )
        self.cursor = self.conn.cursor()

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query)
        self.conn.commit()

    def select(self, table, columns, where: str = None, limit: int = None, offset: int = None):
        query = f"SELECT {columns} FROM {table}"
        if where:
            query += f" WHERE {where}"
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            if not limit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Offset cannot be used without limit",
                )
            query += f" OFFSET {offset}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, table, columns, where):
        query = f"UPDATE {table} SET {columns} WHERE {where}"
        self.cursor.execute(query)
        self.conn.commit()

    def delete(self, table, where):
        query = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


__all__ = ["PostgreAccessObject"]
