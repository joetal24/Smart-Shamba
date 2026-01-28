/*
DBT MODEL: Mart - Planting Advice
==================================
Purpose: Generate actionable crop planting recommendations by district
Layer: Mart (Business Logic Layer)

This model combines:
- Weather conditions
- Vegetation health (NDVI)
- Market prices
To produce: District-level crop recommendations
*/

{{ config(
    materialized='table',
    tags=['mart', 'recommendations']
) }}

WITH weather AS (
    SELECT
        district,
        temperature_celsius,
        humidity_percent,
        rainfall_mm,
        rainfall_category,
        heat_index_celsius,
        measurement_timestamp
    FROM {{ ref('dbt_stg_weather') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY district ORDER BY measurement_timestamp DESC) = 1
),

vegetation AS (
    SELECT
        district,
        ndvi_current,
        vegetation_health,
        soil_moisture_percent,
        vegetation_trend,
        planting_readiness_score,
        planting_recommendation
    FROM {{ ref('dbt_stg_vegetation') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY district ORDER BY measurement_timestamp DESC) = 1
),

prices AS (
    SELECT
        district,
        crop_name,
        current_price_ugx,
        price_trend,
        selling_advice,
        price_change_7days_pct
    FROM {{ ref('dbt_stg_prices') }}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY district, crop_name ORDER BY price_timestamp DESC) = 1
),

-- Crop suitability rules based on Uganda's agricultural best practices
crop_weather_suitability AS (
    SELECT
        w.district,
        p.crop_name,
        
        -- Weather suitability scores (0-10)
        CASE
            WHEN p.crop_name = 'Maize' THEN
                CASE
                    WHEN w.temperature_celsius BETWEEN 18 AND 30 AND w.rainfall_mm > 1 THEN 8
                    WHEN w.temperature_celsius BETWEEN 15 AND 35 THEN 6
                    ELSE 3
                END
            WHEN p.crop_name = 'Beans' THEN
                CASE
                    WHEN w.temperature_celsius BETWEEN 16 AND 28 AND w.rainfall_mm > 0.5 THEN 8
                    WHEN w.temperature_celsius BETWEEN 14 AND 32 THEN 5
                    ELSE 3
                END
            WHEN p.crop_name = 'Cassava' THEN
                CASE
                    WHEN w.temperature_celsius BETWEEN 20 AND 35 THEN 7
                    ELSE 4
                END
            WHEN p.crop_name = 'Sweet Potato' THEN
                CASE
                    WHEN w.temperature_celsius BETWEEN 20 AND 30 AND w.rainfall_mm > 0 THEN 7
                    ELSE 4
                END
            WHEN p.crop_name = 'Coffee' THEN
                CASE
                    WHEN w.temperature_celsius BETWEEN 18 AND 24 AND w.rainfall_mm > 2 THEN 9
                    WHEN w.temperature_celsius BETWEEN 15 AND 28 THEN 6
                    ELSE 3
                END
            WHEN p.crop_name LIKE '%Banana%' THEN
                CASE
                    WHEN w.temperature_celsius BETWEEN 20 AND 30 AND w.rainfall_mm > 1 THEN 8
                    ELSE 5
                END
            ELSE 5
        END AS weather_suitability_score,
        
        -- Vegetation suitability score (0-10)
        CASE
            WHEN v.ndvi_current > 0.7 AND v.soil_moisture_percent > 35 THEN 9
            WHEN v.ndvi_current > 0.5 AND v.soil_moisture_percent > 25 THEN 7
            WHEN v.ndvi_current > 0.3 AND v.soil_moisture_percent > 20 THEN 5
            ELSE 3
        END AS vegetation_suitability_score,
        
        -- Market opportunity score (0-10)
        CASE
            WHEN p.price_change_7days_pct > 10 THEN 9
            WHEN p.price_change_7days_pct > 5 THEN 8
            WHEN p.price_change_7days_pct > 0 THEN 6
            WHEN p.price_change_7days_pct > -5 THEN 4
            ELSE 2
        END AS market_opportunity_score,
        
        -- Pass through data
        w.temperature_celsius,
        w.rainfall_category,
        v.vegetation_health,
        v.soil_moisture_percent,
        p.current_price_ugx,
        p.price_trend
        
    FROM weather w
    CROSS JOIN prices p
    LEFT JOIN vegetation v ON w.district = v.district
    WHERE p.district = w.district
),

final_recommendations AS (
    SELECT
        district,
        crop_name,
        
        -- Calculate overall recommendation score
        ROUND(
            (weather_suitability_score * 0.4) +
            (vegetation_suitability_score * 0.35) +
            (market_opportunity_score * 0.25),
            1
        ) AS overall_recommendation_score,
        
        -- Individual scores
        weather_suitability_score,
        vegetation_suitability_score,
        market_opportunity_score,
        
        -- Recommendation category
        CASE
            WHEN (weather_suitability_score * 0.4 + vegetation_suitability_score * 0.35 + market_opportunity_score * 0.25) >= 7.5
                THEN 'Highly Recommended'
            WHEN (weather_suitability_score * 0.4 + vegetation_suitability_score * 0.35 + market_opportunity_score * 0.25) >= 6
                THEN 'Recommended'
            WHEN (weather_suitability_score * 0.4 + vegetation_suitability_score * 0.35 + market_opportunity_score * 0.25) >= 4
                THEN 'Acceptable'
            ELSE 'Not Recommended'
        END AS recommendation_category,
        
        -- Supporting data
        temperature_celsius,
        rainfall_category,
        vegetation_health,
        soil_moisture_percent,
        current_price_ugx,
        price_trend,
        
        -- Rank crops within each district
        ROW_NUMBER() OVER (PARTITION BY district ORDER BY 
            (weather_suitability_score * 0.4 + vegetation_suitability_score * 0.35 + market_opportunity_score * 0.25) DESC
        ) AS crop_rank,
        
        CURRENT_TIMESTAMP AS recommendation_generated_at
        
    FROM crop_weather_suitability
)

SELECT * FROM final_recommendations

/*
BUSINESS LOGIC:
================
1. Weather Suitability (40% weight):
   - Considers optimal temperature ranges per crop
   - Accounts for rainfall needs
   
2. Vegetation/Soil Suitability (35% weight):
   - NDVI indicates land health
   - Soil moisture readiness
   
3. Market Opportunity (25% weight):
   - Recent price trends
   - Selling potential

RECOMMENDATION FORMULA:
Overall Score = (Weather * 0.4) + (Vegetation * 0.35) + (Market * 0.25)

SCORING THRESHOLDS:
- 7.5+: Highly Recommended (plant now)
- 6-7.5: Recommended (good conditions)
- 4-6: Acceptable (proceed with caution)
- <4: Not Recommended (wait for better conditions)
*/
