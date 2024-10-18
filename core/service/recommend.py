import json
import math
from typing import List, Any
from dateutil.relativedelta import relativedelta
from datetime import datetime
from google.oauth2 import service_account
import ee
from geopy.distance import geodesic

import asyncio
from pydantic import BaseModel
from core.data_adapter.db import get_monthly_payment_by_cardid

# from api.recommend.recommend import OfferReq
from fastapi import HTTPException
import os


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


# Load service account credentials from google_account.json
# SERVICE_ACCOUNT_FILE = "./google_account.json"
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE,
#     scopes=["https://www.googleapis.com/auth/earthengine.readonly"],
# )

# Build the service account info from environment variables
service_account_info = {
    "type": os.getenv("GOOGLE_TYPE"),
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
}

# Load service account credentials from the environment variables
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine.readonly"],
)


# Initialize Google Earth Engine with service account credentials
def initialize_earth_engine():
    try:
        ee.Initialize(credentials)
        print("Google Earth Engine initialized")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to initialize Earth Engine: {e}"
        )


# สร้าง Polygon ของพื้นที่กรุงเทพมหานคร
# # ต้องการเป็น coordinate เป็น key
# def calculate(polygon: List[List[float]]):
#     # polygon = [[[100.46697782333419, 13.495665330651736], [100.4007799199477, 13.490637567256401], [100.41157677574756, 13.512069607026717], [100.38951093987794, 13.611805120709732], [100.34594770712096, 13.656918647077873], [100.32698245577569, 13.751073105739238], [100.33566409712034, 13.79871877675015], [100.48836795531685, 13.798098660025119], [100.5217509299614, 13.848198961313017], [100.5515165552448, 13.94785696152951], [100.6785889023559, 13.918039659402723], [100.90482832236916, 13.94979482696965], [100.89692182827969, 13.846803697332746], [100.92358686724009, 13.813420721788873], [100.8492761581681, 13.709163520280242], [100.85537397712733, 13.691981106542812], [100.71321211134983, 13.711514796870347], [100.68587527882102, 13.660019233400874], [100.66401614762708, 13.652965400033167], [100.59823205026885, 13.658391425423929], [100.58526126509526, 13.666763007506802], [100.59590661030177, 13.69714874951518], [100.56138675319608, 13.703582465258535], [100.51937381405025, 13.662783922040376], [100.49922000519905, 13.665445257892316], [100.49379397980829, 13.59984202678811], [100.46304650259395, 13.583512275571024],[100.46697782333419,13.495665330651736]]]
#     bangkok_roi = ee.Geometry.Polygon(polygon)

#     # Define the BANDS dictionary
#     BANDS = {
#         "solar_radiation": {
#             "topic": "surface_net_solar_radiation_sum",
#             "unit": "W/m^2",
#             "location": "Bangkok",
#         },
#         "precipitation": {
#             "topic": "surface_latent_heat_flux_sum",
#             "unit": "mm",
#             "location": "Bangkok",
#         },
#         "wind": {
#             "topic": "u_component_of_wind_10m",
#             "unit": "m/s",
#             "location": "Bangkok",
#         },
#         "pressure": {"topic": "surface_pressure", "unit": "pa", "location": "Bangkok"},
#         "temperature": {
#             "topic": "temperature_2m",
#             "unit": "Celsius",
#             "location": "Bangkok",
#         },
#     }

#     # Define the date range
#     start_date = datetime.now() + relativedelta(days=-10)
#     end_date = datetime.now() + relativedelta(days=-9)

#     # Function to calculate the mean for a given band
#     def calculate_mean_for_band(band_name):
#         dataset = (
#             ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
#             .select(band_name)
#             .filterBounds(bangkok_roi)
#             .filterDate(start_date, end_date)
#         )

#         # Reduce the ImageCollection to a single image (mean across all images)
#         mean_image = dataset.mean()

#         # Calculate the mean for the region of interest
#         mean_value = mean_image.reduceRegion(
#             reducer=ee.Reducer.mean(),
#             geometry=bangkok_roi,
#             scale=10000,  # Scale in meters
#             maxPixels=1e9,
#         )

#         return mean_value.get(band_name).getInfo()

#     real_output = {"response": [], "geometry_lst": polygon}
#     # Calculate mean for each band and print the results
#     for band_key, band_name in BANDS.items():
#         output = {}
#         mean_value = calculate_mean_for_band(band_name["topic"])
#         print(band_name["topic"])
#         print(f'Mean value for {band_key} ({band_name["topic"]}): {int(mean_value)}')
#         output["band"] = band_name["topic"]
#         output["value"] = (
#             round((math.ceil(mean_value) - 32) / 1.8, 1)
#             if band_name["topic"] == "temperature_2m"
#             else math.ceil(mean_value)
#         )
#         output["unit"] = band_name["unit"]
#         output["loaction"] = band_name["location"]
#         real_output["response"].append(output)

#     print(json.dumps(real_output, indent=4))

#     return real_output


# def process(array: List[List[float]]):
#     return calculate(array)


# ----

# import ee
# import json
# import math
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from typing import List


# คำนวณพื้นที่ของ Polygon (แปลงพิกัดองศาเป็นระยะทางจริง)
def calculate_area_km2(polygon_coords):
    # แปลงพิกัด latitude, longitude เป็นระยะทางจริงในหน่วยเมตร (ใช้ geodesic)
    area = 0.0
    for i in range(len(polygon_coords) - 1):
        p1 = polygon_coords[i]
        p2 = polygon_coords[i + 1]
        # คำนวณระยะทางระหว่างแต่ละจุด (ระยะทางในหน่วยกิโลเมตร)
        dist = geodesic(p1, p2).meters
        area += dist
    return area / 2.0  # ใช้สูตรหารสองสำหรับพื้นที่ของ polygon


def calculate(polygon: List[List[float]], start_date: datetime, end_date: datetime):
    # Define the region of interest (ROI) based on the polygon

    # print("polygon", polygon)
    bangkok_roi = ee.Geometry.Polygon(polygon)

    e = []
    for i in range(len(polygon)):
        e.append((polygon[i][1], polygon[i][0]))

    area = calculate_area_km2(e)

    # Define the BANDS dictionary
    BANDS = {
        "solar_radiation": {
            "topic": "surface_net_solar_radiation_sum",
            "unit": "W/m^2",
        },
        "precipitation": {
            "topic": "surface_latent_heat_flux_sum",
            "unit": "mm",
        },
        "wind": {
            "topic": "u_component_of_wind_10m",
            "unit": "m/s",
        },
        "pressure": {
            "topic": "surface_pressure",
            "unit": "Pa",
        },
        "temperature": {
            "topic": "temperature_2m",
            "unit": "Celsius",
        },
    }

    # Combine all band topics to retrieve them in one request
    band_names = [band_info["topic"] for band_info in BANDS.values()]

    # Retrieve the dataset once, for all bands
    dataset = (
        ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")
        .select(band_names)
        .filterBounds(bangkok_roi)
        .filterDate(start_date, end_date)
    )

    # Calculate the mean for all bands in one go
    mean_image = dataset.mean()

    # Calculate mean values for the region of interest for all bands at once
    mean_values = mean_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=bangkok_roi,
        scale=30000,  # Scale in meters
        maxPixels=1e9,
    ).getInfo()  # Fetch all values in one go

    # Prepare the output structure
    real_output = {"response": []}

    # Loop through the bands and retrieve the computed mean values
    for band_key, band_info in BANDS.items():
        print(
            f"Mean value for {band_key} ({band_info['topic']}): {mean_values.get(band_info['topic'])}"
        )
        mean_value = mean_values.get(band_info["topic"])

        # If no mean value is returned, skip the band
        if mean_value is None:
            # map deafult value for each type
            if band_info["topic"] == "surface_net_solar_radiation_sum":
                # mean_value = 300 * area from polygon
                mean_value = 1361 * area
            else:
                # else if band_info["topic"] == "surface_net_solar_radiation_sum":
                #     mean_value = 600
                # else if band_info["topic"] == "surface_latent_heat_flux_sum":

                continue

            # continue

        output = {
            "band": band_info["topic"],
            "value": (
                round(math.ceil(mean_value) - 273, 1)
                if band_info["topic"] == "temperature_2m"
                else math.ceil(mean_value)
            ),
            "unit": band_info["unit"],
            "location": "Bangkok",  # Static location
        }
        real_output["response"].append(output)

    # Output the final result in a JSON formatted structure
    # print(json.dumps(real_output, indent=4))

    return real_output["response"]


def process(array: List[List[float]]):
    # Set the date range for the calculation (reused across function calls)
    start_date = datetime.now() + relativedelta(days=-100)
    end_date = datetime.now() + relativedelta(days=-9)

    return calculate(array, start_date, end_date)


# -----

import math


# ฟังก์ชันคำนวณพลังงานที่ผลิตได้ (kWh ต่อวัน)
def calculate_energy_generated(solar_radiation, area, efficiency, time, theta):
    cos_theta = math.cos(math.radians(theta))  # แปลงมุมเป็นรัศมีและคำนวณ cos(θ)
    energy_generated = (solar_radiation * area * efficiency * time * cos_theta) / 1000
    return energy_generated


# ฟังก์ชันคำนวณการประหยัดพลังงาน (บาท/ปี)
def calculate_yearly_savings(energy_generated_per_day, electricity_price):
    yearly_energy = energy_generated_per_day * 365  # พลังงานที่ผลิตได้ต่อปี (kWh)
    yearly_savings = yearly_energy * electricity_price  # เงินที่ประหยัดได้ต่อปี (บาท)
    return yearly_savings


# ฟังก์ชันคำนวณการลดการปล่อย CO2 (กิโลกรัม CO2 ต่อปี)
def calculate_co2_reduction(energy_generated_per_day):
    yearly_energy = energy_generated_per_day * 365  # พลังงานที่ผลิตได้ต่อปี (kWh)
    co2_reduction = yearly_energy * 0.707  # CO2 ที่ลดได้ (กิโลกรัม) ต่อ kWh
    return co2_reduction


# ฟังก์ชันคำนวณการคืนทุน (ปี)
def calculate_payback_period(plan_cost, yearly_savings):
    return plan_cost / yearly_savings  # ระยะเวลาคืนทุน (ปี)


# ฟังก์ชันคำนวณการทดแทนค่าไฟ (เป็นเปอร์เซ็นต์)
def calculate_electricity_replacement(
    energy_generated_per_year, current_electricity_bill, electricity_price
):
    current_electricity_usage_kWh = (
        current_electricity_bill / electricity_price
    )  # ปริมาณการใช้ไฟฟ้าปัจจุบัน (kWh)
    replacement_percentage = (
        energy_generated_per_year / current_electricity_usage_kWh
    ) * 100
    return replacement_percentage


def cal_offer(solar_response: int, area_response: int, bill_response: int):
    # ข้อมูลพื้นฐานสำหรับการคำนวณ_
    # solar_radiation = 600  # W/m²
    solar_radiation = solar_response / 86400 * 5  # W/m²
    time = 24  # ชั่วโมงต่อวัน
    electricity_price = 4  # บาทต่อ kWh
    current_electricity_bill = bill_response  # ค่าไฟฟ้าปัจจุบันต่อปี (บาท)

    # แผนการติดตั้ง 3 แบบ (ขนาดพื้นที่และประสิทธิภาพของแผง และค่าใช้จ่ายติดตั้ง)
    plans = [
        {
            "name": "Plan_1",
            "area": area_response,
            "efficiency": 0.155,
            "cost": 125 * 5 * area_response,
        },  # 18.5% efficiency
        {
            "name": "Plan_2",
            "area": area_response,
            "efficiency": 0.201,
            "cost": 150 * 5 * area_response,
        },  # 20.1% efficiency
        {
            "name": "Plan_3",
            "area": area_response,
            "efficiency": 0.240,
            "cost": 200 * 5 * area_response,
        },  # 21.0% efficiency
    ]

    print("plans", plans)

    # สร้าง dictionary เพื่อเก็บข้อมูลแผนทั้งหมด
    solar_plans = {"adjustable": [], "non_adjustable": []}

    # คำนวณสำหรับแผงที่ปรับมุมได้ (cos(0) = 1)
    for plan in plans:
        energy_per_day = calculate_energy_generated(
            solar_radiation, plan["area"], plan["efficiency"], time, 0
        )
        yearly_savings = calculate_yearly_savings(energy_per_day, electricity_price)
        co2_reduction = calculate_co2_reduction(energy_per_day)
        payback_period = calculate_payback_period(plan["cost"], yearly_savings)
        replacement_percentage = calculate_electricity_replacement(
            energy_per_day * 365, current_electricity_bill, electricity_price
        )

        solar_plans["adjustable"].append(
            {
                plan["name"]: {
                    "energy_per_day": {
                        "value": round(energy_per_day, 2),
                        "unit": "kWh",
                    },
                    "yearly_savings": {
                        "value": round(yearly_savings, 2),
                        "unit": "บาท/ปี",
                    },
                    "co2_reduction": {
                        "value": round(co2_reduction, 2),
                        "unit": "กิโลกรัม CO2/ปี",
                    },
                    "payback_period": {"value": round(payback_period, 2), "unit": "ปี"},
                    "electricity_replacement": {
                        "value": round(replacement_percentage, 2),
                        "unit": "%",
                    },
                    "efficiency": {"value": plan["efficiency"] * 100, "unit": "%"},
                    "plan_cost": {"value": plan["cost"], "unit": "บาท"},
                }
            }
        )

    # คำนวณสำหรับแผงที่ปรับมุมไม่ได้ (cos(23.5°) = 0.917)
    for plan in plans:
        energy_per_day = calculate_energy_generated(
            solar_radiation, plan["area"], plan["efficiency"], time, 23.5
        )
        yearly_savings = calculate_yearly_savings(energy_per_day, electricity_price)
        co2_reduction = calculate_co2_reduction(energy_per_day)
        payback_period = calculate_payback_period(plan["cost"], yearly_savings)
        replacement_percentage = calculate_electricity_replacement(
            energy_per_day, current_electricity_bill, electricity_price
        )

        solar_plans["non_adjustable"].append(
            {
                plan["name"]: {
                    "energy_per_day": {
                        "value": round(energy_per_day, 2),
                        "unit": "kWh",
                    },
                    "yearly_savings": {
                        "value": round(yearly_savings, 2),
                        "unit": "บาท/ปี",
                    },
                    "co2_reduction": {
                        "value": round(co2_reduction, 2),
                        "unit": "กิโลกรัม CO2/ปี",
                    },
                    "payback_period": {"value": round(payback_period, 2), "unit": "ปี"},
                    "electricity_replacement": {
                        "value": round(replacement_percentage, 2),
                        "unit": "%",
                    },
                    "efficiency": {
                        "value": round(plan["efficiency"] * 100, 2),
                        "unit": "%",
                    },
                    "plan_cost": {"value": round(plan["cost"], 2), "unit": "บาท"},
                }
            }
        )
    return solar_plans
    # แสดงผลข้อมูลทั้งหมดในรูปแบบ dictionary
    # import json
    # json_output = json.dumps(solar_plans, ensure_ascii=False, indent=4)
    # print(json_output)
