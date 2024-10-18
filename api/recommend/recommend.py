from core.service.recommend import (
    OfferReq,
    calculate_offer,
    get_monthly_payment_pea,
    initialize_earth_engine,
    process,
    cal_offer,
)
from typing import List, Any

from fastapi import APIRouter, Header, HTTPException
from typing import Annotated
import http
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import ee


recommendRouter = APIRouter(tags=["recommend"])
initialize_earth_engine()


class GeometryData(BaseModel):
    # type: str
    coordinates: List[List[float]]


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


# POST [/preditc-power]
@recommendRouter.post("/predict-power", status_code=http.HTTPStatus.OK)
async def predict_power(geometry: GeometryData):
    # print(geometry)
    result = process(geometry.coordinates)
    return {"status": "ok", "message": "predict-power", "data": result}
    # return {"status": "ok", "message": "predict-power", "data": {"power": 1000}}


class OfferCalReq(BaseModel):
    solar_response: int
    area_response: int
    bill_response: int


# POST [/offer]
@recommendRouter.post("/offer-cal", status_code=http.HTTPStatus.OK)
async def offer(req: OfferCalReq):
    data = cal_offer(req.solar_response, req.area_response, req.bill_response)

    return {"status": "ok", "message": "offer", "data": data}
    # return {"status": "ok", "message": "offer", "data": {"price": 1000, "offerID": "offer-0001"}}


# POST [/get-heat-map]
# async def get_heat_map():
#     return {"status": "ok", "message": "get-heat-map", "data": {"heatMap": []}}


# FastAPI route to fetch Earth Engine data
# @app.get("/earthengine-data")


# Define the request model to accept geometry data


@recommendRouter.post("/get-heat-map", status_code=http.HTTPStatus.OK)
def get_earth_engine_data(geometry: GeometryData):
    try:
        # Parse the geometry data from the request

        # const
        geometry = ee.Geometry.Polygon(
            geometry.coordinates
        )  # Create an Earth Engine polygon geometry

        # Fetch Sentinel-2 satellite image collection with cloud masking
        S2 = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterDate("2020-01-01", "2020-01-30")
            .filterBounds(geometry)
            .median()
        )

        # Select bands for EVI and NDVI calculations
        image = S2.select(["B2", "B3", "B4", "B8"], ["blue", "green", "red", "nir"])

        # Calculate EVI
        evi = image.expression(
            "2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))",
            {
                "nir": image.select("nir").divide(10000),
                "red": image.select("red").divide(10000),
                "blue": image.select("blue").divide(10000),
            },
        ).rename("EVI")

        # Calculate NDVI
        ndvi = image.normalizedDifference(["nir", "red"]).rename("NDVI")

        # Composite weight (for example, averaging EVI and NDVI)
        composite_weight = evi.add(ndvi).divide(2).rename("Composite_Weight")

        # Clip the composite weight to the polygon geometry
        composite_weight_clipped = composite_weight.clip(geometry)

        # Define the color palette for visualization
        pal = [
            "040274",
            "d6e21f",
            "fff705",
            "ffd611",
            "ffb613",
            "ff8b13",
            "ff6e08",
            "ff500d",
            "ff0000",
            "de0101",
            "c21301",
            "a71001",
        ]

        # Visualization parameters with custom color palette
        vis_params = {
            "bands": ["Composite_Weight"],
            "min": -0.1,
            "max": 1.0,
            "palette": pal,  # Apply the custom palette
        }

        # Visualize the clipped composite weight
        image_visualized = composite_weight_clipped.visualize(**vis_params)

        # Get the Map ID and URL
        map_id = ee.data.getMapId({"image": image_visualized})
        map_url = map_id["tile_fetcher"].url_format

        return {"mapUrl": map_url}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch Earth Engine data: {e}"
        )
