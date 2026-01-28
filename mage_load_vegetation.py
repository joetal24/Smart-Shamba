"""
MAGE PIPELINE: Vegetation/NDVI Data Loader
===========================================
Purpose: Load vegetation health data (NDVI) and load into DuckDB raw layer
Author: Smart-Shamba Project

NOTE: This uses simulated NDVI data. In production, you'd use:
- Sentinel-2 satellite data (free via Copernicus)
- NASA MODIS data
- Google Earth Engine API
"""

import duckdb
import random
from datetime import datetime
from typing import Dict, List
import json
from mage_ai.data_preparation.decorators import data_loader

DB_PATH = './warehouse/duckdb/agri_analytics.db'

DISTRICTS = [
    {'name': 'Kampala', 'lat': 0.3476, 'lon': 32.5825},
    {'name': 'Mbale', 'lat': 1.0820, 'lon': 34.1754},
    {'name': 'Gulu', 'lat': 2.7747, 'lon': 32.2989},
    {'name': 'Mbarara', 'lat': -0.6103, 'lon': 30.6589},
]


def classify_vegetation_health(ndvi: float) -> str:
    """
    Classify vegetation health based on NDVI value.
    
    NDVI ranges:
    - Below 0.2: Bare soil / No vegetation
    - 0.2-0.5: Sparse vegetation
    - 0.5-0.7: Moderate vegetation
    - Above 0.7: Dense, healthy vegetation
    """
    if ndvi < 0.2:
        return 'Bare/Very Poor'
    elif ndvi < 0.5:
        return 'Sparse'
    elif ndvi < 0.7:
        return 'Moderate'
    else:
        return 'Dense/Healthy'


@data_loader
def load_vegetation_data(*args, **kwargs) -> Dict:
    """
    Load vegetation health (NDVI) data for districts.
    
    NDVI = Normalized Difference Vegetation Index
    - Measures photosynthetic activity
    - Range: -1 to 1 (higher = healthier vegetation)
    
    Returns:
        Dict: Contains status and data loaded
    """
    print("🌱 Starting vegetation data collection...")
    
    vegetation_records = []
    
    for district in DISTRICTS:
        try:
            # Simulate NDVI reading (0.1 to 0.9 for Uganda's range)
            # Uganda has two rainy seasons, so NDVI varies
            current_ndvi = random.uniform(0.3, 0.85)
            
            # Historical comparison (14 days ago)
            ndvi_14days_ago = current_ndvi * random.uniform(0.85, 1.05)
            ndvi_change = current_ndvi - ndvi_14days_ago
            
            # Soil moisture estimate (related to NDVI)
            soil_moisture_pct = random.uniform(15, 45)
            
            vegetation_record = {
                'district': district['name'],
                'latitude': district['lat'],
                'longitude': district['lon'],
                'ndvi_value': round(current_ndvi, 3),
                'ndvi_14days_ago': round(ndvi_14days_ago, 3),
                'ndvi_change': round(ndvi_change, 3),
                'vegetation_health': classify_vegetation_health(current_ndvi),
                'soil_moisture_pct': round(soil_moisture_pct, 1),
                'satellite_source': 'Simulated Sentinel-2',  # In production: actual source
                'timestamp': datetime.now().isoformat(),
                'raw_json': json.dumps({
                    'ndvi': current_ndvi,
                    'soil_moisture': soil_moisture_pct,
                    'data_quality': 'high'
                })
            }
            
            vegetation_records.append(vegetation_record)
            print(f"✅ Loaded vegetation data for {district['name']} (NDVI: {current_ndvi:.2f})")
            
        except Exception as e:
            print(f"❌ Error loading vegetation for {district['name']}: {str(e)}")
            continue
    
    # Load into DuckDB
    conn = duckdb.connect(DB_PATH)
    
    # Create raw table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_vegetation (
            district VARCHAR,
            latitude FLOAT,
            longitude FLOAT,
            ndvi_value FLOAT,
            ndvi_14days_ago FLOAT,
            ndvi_change FLOAT,
            vegetation_health VARCHAR,
            soil_moisture_pct FLOAT,
            satellite_source VARCHAR,
            timestamp TIMESTAMP,
            raw_json VARCHAR,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert records
    if vegetation_records:
        conn.executemany("""
            INSERT INTO raw_vegetation 
            (district, latitude, longitude, ndvi_value, ndvi_14days_ago, ndvi_change,
             vegetation_health, soil_moisture_pct, satellite_source, timestamp, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [(r['district'], r['latitude'], r['longitude'], r['ndvi_value'],
               r['ndvi_14days_ago'], r['ndvi_change'], r['vegetation_health'],
               r['soil_moisture_pct'], r['satellite_source'], r['timestamp'], r['raw_json']) 
              for r in vegetation_records])
        
        conn.commit()
        print(f"✅ Inserted {len(vegetation_records)} vegetation records into DuckDB")
    
    conn.close()
    
    return {
        'status': 'success',
        'records_loaded': len(vegetation_records),
        'timestamp': datetime.now().isoformat()
    }


if __name__ == '__main__':
    # For testing outside Mage
    result = load_vegetation_data()
    print(json.dumps(result, indent=2))
