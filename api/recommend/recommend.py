from core.service.recommend import OfferReq, calculate_offer, get_monthly_payment_pea
from fastapi import APIRouter, Header
from typing import Annotated
import http
from pydantic import BaseModel
from fastapi.responses import JSONResponse

recommendRouter = APIRouter(tags=["recommend"])


@recommendRouter.post("/offer", status_code=http.HTTPStatus.OK)
async def recommend(offerReq: OfferReq, x_user_id: Annotated[str, Header()] = None):
    print("/offer", x_user_id, offerReq)
    offer = await calculate_offer(x_user_id, offerReq)
    return {"status": "ok", "message": "recommend", "data": offer}


# POST [/get-monthly-payment?id=1234567890]
@recommendRouter.get("/get-monthly-payment", status_code=http.HTTPStatus.OK)
async def get_monthly_payment(id: str, x_user_id: Annotated[str, Header()] = None):
    try:
        payment = await get_monthly_payment_pea(id)
    except Exception as e:
        # return {"status": "error", "message": str(e)}
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e),
                "data": {"monthlyPayment": 0, "cardID": id},
            }
        )
    return {"status": "ok", "message": "recommend", "data": payment}
