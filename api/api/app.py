
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.article_routes import router as article_routes


# Initialize FastAPI app
app = FastAPI()

# Import routes
app.include_router(article_routes)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


__all__ = ["app"]
