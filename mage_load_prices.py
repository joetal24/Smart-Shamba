"""
MAGE PIPELINE: Market Price Data Loader
========================================
Purpose: Scrape/load market prices for crops and load into DuckDB raw layer
Author: Smart-Shamba Project

NOTE: This uses simulated data. In production, you'd scrape from actual market websites.
"""

import duckdb
import random
from datetime import datetime, timedelta
from typing import Dict, List
import json
from mage_ai.data_preparation.decorators import data_loader

DB_PATH = './warehouse/duckdb/agri_analytics.db'

# Ugandan crops with typical price ranges (UGX per kg)
CROPS = {
    'Maize': {'min': 800, 'max': 1500},
    'Beans': {'min': 2000, 'max': 3500},
    'Cassava': {'min': 500, 'max': 1000},
    'Sweet Potato': {'min': 600, 'max': 1200},
    'Coffee': {'min': 3000, 'max': 5000},
    'Banana (Matoke)': {'min': 300, 'max': 800},
}

DISTRICTS = ['Kampala', 'Mbale', 'Gulu', 'Mbarara']


@data_loader
def load_price_data(*args, **kwargs) -> Dict:
    """
    Load market price data for various crops across districts.
    
    In production, this would scrape from:
    - Uganda Bureau of Statistics
    - Local market websites
    - Agricultural ministry data
    
    Returns:
        Dict: Contains status and data loaded
    """
    print("💰 Starting market price collection...")
    
    price_records = []
    
    for district in DISTRICTS:
        for crop, price_range in CROPS.items():
            try:
                # Simulate price with some variation
                base_price = random.uniform(price_range['min'], price_range['max'])
                
                # Add seasonal variation (±20%)
                seasonal_factor = random.uniform(0.8, 1.2)
                current_price = base_price * seasonal_factor
                
                # Calculate 7-day trend (simulated)
                price_7days_ago = current_price * random.uniform(0.9, 1.1)
                price_change_pct = ((current_price - price_7days_ago) / price_7days_ago) * 100
                
                price_record = {
                    'district': district,
                    'crop': crop,
                    'price_ugx_per_kg': round(current_price, 2),
                    'price_7days_ago': round(price_7days_ago, 2),
                    'price_change_pct': round(price_change_pct, 2),
                    'market_source': 'Simulated Market Data',  # In production: actual source
                    'timestamp': datetime.now().isoformat(),
                    'raw_json': json.dumps({
                        'crop': crop,
                        'current_price': current_price,
                        'historical': {
                            '7_days_ago': price_7days_ago
                        }
                    })
                }
                
                price_records.append(price_record)
                
            except Exception as e:
                print(f"❌ Error loading price for {crop} in {district}: {str(e)}")
                continue
    
    print(f"✅ Generated {len(price_records)} price records")
    
    # Load into DuckDB
    conn = duckdb.connect(DB_PATH)
    
    # Create raw table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_prices (
            district VARCHAR,
            crop VARCHAR,
            price_ugx_per_kg FLOAT,
            price_7days_ago FLOAT,
            price_change_pct FLOAT,
            market_source VARCHAR,
            timestamp TIMESTAMP,
            raw_json VARCHAR,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert records
    if price_records:
        conn.executemany("""
            INSERT INTO raw_prices 
            (district, crop, price_ugx_per_kg, price_7days_ago, price_change_pct, 
             market_source, timestamp, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [(r['district'], r['crop'], r['price_ugx_per_kg'], r['price_7days_ago'],
               r['price_change_pct'], r['market_source'], r['timestamp'], r['raw_json']) 
              for r in price_records])
        
        conn.commit()
        print(f"✅ Inserted {len(price_records)} price records into DuckDB")
    
    conn.close()
    
    return {
        'status': 'success',
        'records_loaded': len(price_records),
        'timestamp': datetime.now().isoformat()
    }


if __name__ == '__main__':
    # For testing outside Mage
    result = load_price_data()
    print(json.dumps(result, indent=2))
