import http
from core.schemas.schema import Ans, Item
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
import random
from core.data_adapter.cache import get_cache_memory_size, set_cache

router = APIRouter(tags=["admin"])


# clear cache
@router.post("/clear", status_code=http.HTTPStatus.OK)
async def clear_cache():
    cache_size = get_cache_memory_size()
    clear_cache()

    return JSONResponse(
        content={"status": "ok", "cache_size": cache_size, "message": "cache cleared"}
    )


# cache status
@router.get("/status", status_code=http.HTTPStatus.OK)
async def cache_status():
    cache_size = get_cache_memory_size()
    return JSONResponse(content={"status": "ok", "cache_size": cache_size})
