/*
DBT MODEL: Staging Vegetation
==============================
Purpose: Clean and standardize raw vegetation/NDVI data
Layer: Staging
*/

{{ config(
    materialized='view',
    tags=['staging', 'vegetation']
) }}

WITH source_data AS (
    SELECT
        district,
        latitude,
        longitude,
        ndvi_value,
        ndvi_14days_ago,
        ndvi_change,
        vegetation_health,
        soil_moisture_pct,
        satellite_source,
        timestamp,
        loaded_at
    FROM {{ source('raw', 'raw_vegetation') }}
),

cleaned_data AS (
    SELECT
        -- Location
        UPPER(TRIM(district)) AS district,
        ROUND(latitude, 4) AS latitude,
        ROUND(longitude, 4) AS longitude,
        
        -- NDVI metrics
        ROUND(ndvi_value, 3) AS ndvi_current,
        ROUND(ndvi_14days_ago, 3) AS ndvi_14days_ago,
        ROUND(ndvi_change, 3) AS ndvi_change_14days,
        
        -- Health classification
        vegetation_health,
        
        -- Soil moisture
        ROUND(soil_moisture_pct, 1) AS soil_moisture_percent,
        
        -- Source
        satellite_source,
        
        -- Timestamps
        CAST(timestamp AS TIMESTAMP) AS measurement_timestamp,
        loaded_at,
        
        -- Derived fields
        CASE
            WHEN ndvi_change > 0.1 THEN 'Improving Rapidly'
            WHEN ndvi_change > 0.03 THEN 'Improving'
            WHEN ndvi_change > -0.03 THEN 'Stable'
            WHEN ndvi_change > -0.1 THEN 'Declining'
            ELSE 'Declining Rapidly'
        END AS vegetation_trend,
        
        CASE
            WHEN soil_moisture_pct < 20 THEN 'Dry - Irrigation Needed'
            WHEN soil_moisture_pct < 30 THEN 'Somewhat Dry'
            WHEN soil_moisture_pct < 40 THEN 'Adequate'
            ELSE 'Very Moist'
        END AS soil_moisture_status,
        
        -- Planting readiness score (0-100)
        ROUND(
            (ndvi_value * 50) + (soil_moisture_pct * 1.5), 
            1
        ) AS planting_readiness_score,
        
        CASE
            WHEN ndvi_value > 0.6 AND soil_moisture_pct > 30 THEN 'Ready for Planting'
            WHEN ndvi_value > 0.4 AND soil_moisture_pct > 25 THEN 'Acceptable'
            ELSE 'Wait for Better Conditions'
        END AS planting_recommendation
        
    FROM source_data
    WHERE ndvi_value IS NOT NULL
      AND ndvi_value BETWEEN -1 AND 1  -- Valid NDVI range
      AND district IS NOT NULL
)

SELECT * FROM cleaned_data

/*
BUSINESS RULES APPLIED:
- Standardize district names
- Validate NDVI values (must be between -1 and 1)
- Classify vegetation trends (improving/stable/declining)
- Assess soil moisture status
- Calculate planting readiness score
- Provide planting recommendations based on NDVI + soil moisture
*/
