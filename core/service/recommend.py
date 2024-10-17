# export const useFormStore = create<FormState>((set) => ({
#   electricityUsage: { type: "", cost: "" },
#   solarSystem: {
#     systemType: "",
#     phaseType: "",
#     workingHours: [6, 18],
#     offHours: [19, 23]
#   },
#   locationList: [],
#   // use bangkok as default center
#   center: { lat: 13.7563, lng: 100.5018 },
#   setElectricityUsage: (data) => set(() => ({ electricityUsage: data })),
#   setSolarSystem: (data) => set(() => ({ solarSystem: data })),
#   setLocationList: (data) => set(() => ({ locationList: data })),
#   setCenter: (data) => set(() => ({ center: data }))
# }));
# data format from js
import asyncio
from pydantic import BaseModel
from core.data_adapter.db import get_monthly_payment_by_cardid
# from api.recommend.recommend import OfferReq


class OfferReq(BaseModel):
    electricityUsage: dict
    solarSystem: dict
    locationList: list
    center: dict


async def calculate_offer(user_id: str, data: OfferReq):
    # extract data
    electricityUsage = data.electricityUsage
    solarSystem = data.solarSystem
    locationList = data.locationList
    center = data.center
    # calculate offer
    # ...

    await asyncio.sleep(1)
    # sleep 1 second
    return {"price": 1000, "offerID": "offer-0001"}


async def get_monthly_payment_pea(user_id: str):
    payment_info = get_monthly_payment_by_cardid(user_id)
    # print("payment_info", payment_info)

    if payment_info is None or len(payment_info) == 0:
        # throw error
        raise Exception("payment info not found")

    # return {"monthlyPayment": 0, "cardID": user_id}

    return {"monthlyPayment": payment_info[0][1], "cardID": user_id}
