"""
FILE: air_quality.py

DESCRIPTION:
  Fetches air quality data from AQICN API and maps AQI values to descriptive levels.

BRIEF:
  Provides functions to retrieve AQI data and map it to human-readable levels.
  Allows a microcontroller to call these functions via Bridge to display AQI on LED matrix.

AUTHOR: Kevin Thomas
CREATION DATE: December 22, 2025
UPDATE DATE: December 22, 2025
"""

from arduino.app_utils import *
import os
import requests
from dotenv import load_dotenv

# Load .env from current working directory
load_dotenv()

# API token for AQICN API
api_token = os.getenv("API_TOKEN")

# City to fetch data for
city = "Washington, D.C."

# Endpoint for AQICN API
endpoint = f"https://api.waqi.info/feed/{city}/?token={api_token}"

# AQI levels mapping
AQI_LEVELS = [
  {"min": 0, "max": 50, "description": "Good"},
  {"min": 51, "max": 100, "description": "Moderate"},
  {"min": 101, "max": 150, "description": "Unhealthy for Sensitive Groups"},
  {"min": 151, "max": 200, "description": "Unhealthy"},
  {"min": 201, "max": 300, "description": "Very Unhealthy"},
  {"min": 301, "max": 500, "description": "Hazardous"}
]


def map_aqi_level(aqi_value: int) -> str:
  """
  Maps an AQI integer value to its descriptive level.
  
  PARAMETERS:
    aqi_value (int): The AQI value to map.
    
  RETURNS:
    str: Human-readable description of AQI level.
  """
  for level in AQI_LEVELS:
    if level["min"] <= aqi_value <= level["max"]:
      return level["description"]
  return "N/A"


def get_air_quality() -> str:
  """
  Fetches air quality data from AQICN API.
  Extracts AQI value and returns descriptive level.
  
  PARAMETERS:
    None
  
  RETURNS:
    str: AQI description (e.g., "Good", "Moderate") or error message if API fails.
  """
  response = requests.get(endpoint)
  response_json = response.json()
  status = response_json.get("status", None)
  data = response_json.get("data", None)
  if status != 'ok' or not data:
    print(f"API Error: {response_json}")
    return "API Error"
  aqi = data.get("aqi", -1)
  try:
    aqi = int(aqi)
  except (TypeError, ValueError):
    return "No AQI Value"
  if not (0 <= aqi <= 500):
    return "Invalid AQI Value"
  aqi_level = map_aqi_level(aqi)
  return aqi_level


# Expose function to microcontroller via Bridge
Bridge.provide("get_air_quality", get_air_quality)

# Run app
App.run()