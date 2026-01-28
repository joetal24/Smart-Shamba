/*
DBT MODEL: Staging Weather
===========================
Purpose: Clean and standardize raw weather data
Layer: Staging (first transformation after raw)
*/

{{ config(
    materialized='view',
    tags=['staging', 'weather']
) }}

WITH source_data AS (
    SELECT
        district,
        latitude,
        longitude,
        temperature,
        humidity,
        pressure,
        weather_condition,
        weather_description,
        wind_speed,
        clouds,
        rainfall,
        timestamp,
        loaded_at
    FROM {{ source('raw', 'raw_weather') }}
),

cleaned_data AS (
    SELECT
        -- Location
        UPPER(TRIM(district)) AS district,
        ROUND(latitude, 4) AS latitude,
        ROUND(longitude, 4) AS longitude,
        
        -- Weather metrics
        ROUND(temperature, 1) AS temperature_celsius,
        humidity AS humidity_percent,
        pressure AS pressure_hpa,
        
        -- Conditions
        weather_condition,
        weather_description,
        
        -- Wind and clouds
        ROUND(wind_speed, 1) AS wind_speed_ms,
        clouds AS cloud_cover_percent,
        
        -- Rainfall (convert to mm if needed)
        COALESCE(rainfall, 0) AS rainfall_mm,
        
        -- Timestamps
        CAST(timestamp AS TIMESTAMP) AS measurement_timestamp,
        loaded_at,
        
        -- Derived fields
        CASE
            WHEN rainfall > 10 THEN 'Heavy Rain'
            WHEN rainfall > 2.5 THEN 'Moderate Rain'
            WHEN rainfall > 0 THEN 'Light Rain'
            ELSE 'No Rain'
        END AS rainfall_category,
        
        CASE
            WHEN humidity > 80 THEN 'Very Humid'
            WHEN humidity > 60 THEN 'Humid'
            WHEN humidity > 40 THEN 'Comfortable'
            ELSE 'Dry'
        END AS humidity_category,
        
        -- Calculate heat index (simplified)
        CASE
            WHEN temperature > 27 AND humidity > 40
            THEN ROUND(temperature + (0.05 * humidity), 1)
            ELSE temperature
        END AS heat_index_celsius
        
    FROM source_data
    WHERE temperature IS NOT NULL
      AND district IS NOT NULL
)

SELECT * FROM cleaned_data

/*
BUSINESS RULES APPLIED:
- Standardize district names (uppercase, trimmed)
- Round coordinates to 4 decimal places
- Handle null rainfall values (default to 0)
- Categorize rainfall and humidity for easier analysis
- Calculate heat index for farmer comfort assessment
*/
