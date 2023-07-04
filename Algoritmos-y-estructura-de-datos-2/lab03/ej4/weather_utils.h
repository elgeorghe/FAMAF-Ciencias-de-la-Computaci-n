/*
  @file weather_utils.h
  @brief defines weather utils methods.
*/

#ifndef _WEATHER_UTILS_H
#define _WEATHER_UTILS_H

#include "array_helpers.h"

/**
 * Returns the minimun TempMin in the history of Cordoba
 */
int min_TempMin(WeatherTable a);

/**
 * Registers the maximus TempMax per year of Cordoba
 */
void max_TempMax_per_year(WeatherTable a, int output[YEARS]);

/**
 * Registers the month per year with the most amount of rainfall
 */
void month_max_amount_Rainfall_per_year(WeatherTable a, unsigned int output[YEARS]);

#endif