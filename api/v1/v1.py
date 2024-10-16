from fastapi import APIRouter
import http
from core.service.transformer import predict
import core.data_adapter.cache as cache

router = APIRouter(tags=["v1"])

# adminRouter.include_router(statusRouter, prefix="/status")


# test endpoint
@router.post("/test/{text}", status_code=http.HTTPStatus.OK)
async def test(text: str):
    if cache.is_cache_exists(text):
        result = cache.get_cache_value(text)
        return {"status": "ok", "message": "test", "req": text, "res": result}
    prediction = predict(text)
    cache.set_cache(text, prediction)
    return {"status": "ok", "message": "test", "req": text, "res": prediction}
