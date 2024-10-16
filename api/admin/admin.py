from api.admin.cache import router as cacheRouter
from fastapi import APIRouter

adminRouter = APIRouter(tags=["admin"])

adminRouter.include_router(cacheRouter, prefix="/cache")
