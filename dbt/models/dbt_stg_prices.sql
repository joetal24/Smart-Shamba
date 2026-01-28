/*
DBT MODEL: Staging Prices
==========================
Purpose: Clean and standardize raw market price data
Layer: Staging
*/

{{ config(
    materialized='view',
    tags=['staging', 'prices']
) }}

WITH source_data AS (
    SELECT
        district,
        crop,
        price_ugx_per_kg,
        price_7days_ago,
        price_change_pct,
        market_source,
        timestamp,
        loaded_at
    FROM {{ source('raw', 'raw_prices') }}
),

cleaned_data AS (
    SELECT
        -- Location and crop
        UPPER(TRIM(district)) AS district,
        TRIM(crop) AS crop_name,
        
        -- Price information
        ROUND(price_ugx_per_kg, 2) AS current_price_ugx,
        ROUND(price_7days_ago, 2) AS price_7days_ago_ugx,
        ROUND(price_change_pct, 2) AS price_change_7days_pct,
        
        -- Source
        market_source,
        
        -- Timestamps
        CAST(timestamp AS TIMESTAMP) AS price_timestamp,
        loaded_at,
        
        -- Derived fields
        CASE
            WHEN price_change_pct > 10 THEN 'Rising Fast'
            WHEN price_change_pct > 3 THEN 'Rising'
            WHEN price_change_pct > -3 THEN 'Stable'
            WHEN price_change_pct > -10 THEN 'Falling'
            ELSE 'Falling Fast'
        END AS price_trend,
        
        CASE
            WHEN price_change_pct > 5 THEN 'Good Selling Opportunity'
            WHEN price_change_pct < -5 THEN 'Wait to Sell'
            ELSE 'Neutral'
        END AS selling_advice,
        
        -- Calculate absolute price change
        ROUND(price_ugx_per_kg - price_7days_ago, 2) AS price_change_ugx,
        
        -- Price volatility indicator
        ROUND(ABS(price_change_pct), 2) AS price_volatility
        
    FROM source_data
    WHERE price_ugx_per_kg IS NOT NULL
      AND price_ugx_per_kg > 0
      AND district IS NOT NULL
      AND crop IS NOT NULL
)

SELECT * FROM cleaned_data

/*
BUSINESS RULES APPLIED:
- Standardize district and crop names
- Calculate price trends (Rising/Stable/Falling)
- Provide selling advice based on price movements
- Calculate absolute price changes
- Measure price volatility
- Filter out invalid prices (null or negative)
*/
