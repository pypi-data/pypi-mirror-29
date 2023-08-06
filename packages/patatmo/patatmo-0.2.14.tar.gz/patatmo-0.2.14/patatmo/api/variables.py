#!/usr/bin/env python3
# module for global variables
import re

PLAIN_URLENCODED_HEADERS = {
    "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
}

NETATMO_API_SERVER = "api.netatmo.com"

NETATMO_API_TOKEN_URL = "/oauth2/token"
NETATMO_API_GETPUBLICDATA_URL = "/api/getpublicdata"
NETATMO_API_GETMEASURE_URL = "/api/getmeasure"
NETATMO_API_GETSTATIONSDATA_URL = "/api/getstationsdata"

GETPUBLICDATA_ALLOWED_REQUIRED_DATA = \
    ["rain", "humidity", "pressure", "wind", "temperature"]


GETMEASURE_ALLOWED_TYPES_UPTO_MAX = [
    "Temperature",
    "CO2",
    "Humidity",
    "Pressure",
    "Noise",
    "Rain",
    "WindStrength",
    "WindAngle",
    "GustStrength",
    "GustAngle"]

GETMEASURE_ALLOWED_TYPES_UPTO_3HOURS = GETMEASURE_ALLOWED_TYPES_UPTO_MAX.copy()
GETMEASURE_ALLOWED_TYPES_UPTO_3HOURS.extend([
    "min_temp", "max_temp", "min_hum", "max_hum", "min_pressure",
    "max_pressure", "min_noise", "max_noise", "sum_rain", "date_max_gust"])

GETMEASURE_ALLOWED_TYPES_UPTO_1MONTH = \
    GETMEASURE_ALLOWED_TYPES_UPTO_3HOURS.copy()
GETMEASURE_ALLOWED_TYPES_UPTO_1MONTH.extend([
    "min_temp", "max_temp", "min_hum", "max_hum", "min_pressure",
    "max_pressure", "min_noise", "max_noise", "sum_rain", "date_max_gust"])

GETMEASURE_ALLOWED_TYPES_BY_SCALE = {
    "max": GETMEASURE_ALLOWED_TYPES_UPTO_MAX,
    "30min": GETMEASURE_ALLOWED_TYPES_UPTO_3HOURS,
    "1hour": GETMEASURE_ALLOWED_TYPES_UPTO_3HOURS,
    "3hours": GETMEASURE_ALLOWED_TYPES_UPTO_3HOURS,
    "1day": GETMEASURE_ALLOWED_TYPES_UPTO_1MONTH,
    "1week": GETMEASURE_ALLOWED_TYPES_UPTO_1MONTH,
    "1month": GETMEASURE_ALLOWED_TYPES_UPTO_1MONTH,
}

GETPUBLICDATA_REGION_BOUNDS = {
    "lat_ne": [-85, 85],
    "lat_sw": [-85, 85],
    "lon_ne": [-180, 180],
    "lon_sw": [-180, 180],
}

MAC_ADDRESS_REGEX = re.compile(":".join(["[0-9a-f]{2}"] * 6))
