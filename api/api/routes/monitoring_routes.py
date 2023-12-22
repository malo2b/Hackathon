

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/healthcheck", tags=["monitoring"])
def healthcheck():
    """Healthcheck endpoint"""
    return Response(status_code=status.HTTP_200_OK, content="Ca vie hein!!")
