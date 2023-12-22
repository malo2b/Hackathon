import os
import uvicorn

from api.app import app

if __name__ == "__main__":

    os.environ["QDRANT_URL"] = "https://9c7ce2ab-e4bb-4fb7-984f-751839b17d72.us-east4-0.gcp.cloud.qdrant.io:6333/"
    os.environ["QDRANT_API_KEY"] = "hP7iNUrHyru2UJRKdCM1ldWmYTl5720sPf83khCiAJcLI2M3BnGh1w"

    os.environ["DATABASE_URL"] = "pg-229deec8-anto2b-5d3b.a.aivencloud.com"
    os.environ["DATABASE_USER"] = "avnadmin"
    os.environ["DATABASE_PASSWORD"] = "AVNS_5l01gACj837gmzIWvO2"
    os.environ["DATABASE_NAME"] = "defaultdb"
    os.environ["DATABASE_PORT"] = "14467"

    uvicorn.run(app, host="0.0.0.0", port=8000)
