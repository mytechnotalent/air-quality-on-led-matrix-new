/**
 * FILE: air_quality_display.ino
 *
 * DESCRIPTION:
 *   Displays air quality data on an 8x13 LED matrix using Arduino.
 *
 * BRIEF:
 *   Loads frames representing AQI levels on the matrix.
 *   Uses Bridge to fetch air quality from Python backend.
 *
 * AUTHOR: Kevin Thomas
 * CREATION DATE: December 22, 2025
 * UPDATE DATE: December 22, 2025
 */

#include <Arduino_RouterBridge.h>
#include "air_quality_frames.h"
#include "led_matrix.h"

void setup() {
  /**
   * Initializes LED matrix and Bridge.
   */
  matrix.begin();
  matrix.clear();
  Bridge.begin();
}

void loop() {
  /**
   * Fetches air quality from Bridge and displays corresponding frame.
   * Refresh rate: 1 second.
   */
  String airQuality;
  bool ok = Bridge.call("get_air_quality").result(airQuality);
  if (ok) {
    if (airQuality == "Good") loadFrame8x13(good);
    else if (airQuality == "Moderate") loadFrame8x13(moderate);
    else if (airQuality == "Unhealthy for Sensitive Groups") loadFrame8x13(unhealthy_for_sensitive_groups);
    else if (airQuality == "Unhealthy") loadFrame8x13(unhealthy);
    else if (airQuality == "Very Unhealthy") loadFrame8x13(very_unhealthy);
    else if (airQuality == "Hazardous") loadFrame8x13(hazardous);
    else loadFrame8x13(unknown);
  }
  delay(1000);
}