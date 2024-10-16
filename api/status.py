import http
from core.schemas.schema import Ans, Item
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
import random
from core.data_adapter.cache import get_cache_memory_size

router = APIRouter(tags=["health_checks", "status"])


#  health check endpoints
@router.get("/health-check", status_code=http.HTTPStatus.OK)
async def health_check():
    return JSONResponse(content={"status": "ok"})
