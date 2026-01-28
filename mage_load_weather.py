"""
MAGE PIPELINE: Weather Data Loader
===================================
Purpose: Fetch weather data from OpenWeatherMap API and load into DuckDB raw layer
Author: Smart-Shamba Project
"""

import requests
import json
import duckdb
from datetime import datetime
from typing import Dict, List
import os
from mage_ai.data_preparation.decorators import data_loader
from dotenv import load_dotenv

# Configuration
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
DISTRICTS = [
    {'name': 'Kampala', 'lat': 0.3476, 'lon': 32.5825},
    {'name': 'Mbale', 'lat': 1.0820, 'lon': 34.1754},
    {'name': 'Gulu', 'lat': 2.7747, 'lon': 32.2989},
    {'name': 'Mbarara', 'lat': -0.6103, 'lon': 30.6589},
]

DB_PATH = './warehouse/duckdb/agri_analytics.db'


@data_loader
def load_weather_data(*args, **kwargs) -> Dict:
    """
    Load weather data from OpenWeatherMap API for Ugandan districts.
    
    Returns:
        Dict: Contains status and data loaded
    """
    print("🌦️  Starting weather data collection...")
    
    weather_records = []
    
    for district in DISTRICTS:
        try:
            # Fetch current weather
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={district['lat']}&lon={district['lon']}&appid={API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Structure the data
            weather_record = {
                'district': district['name'],
                'latitude': district['lat'],
                'longitude': district['lon'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather_condition': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'rainfall': data.get('rain', {}).get('1h', 0),  # Rain in last hour
                'timestamp': datetime.now().isoformat(),
                'raw_json': json.dumps(data)
            }
            
            weather_records.append(weather_record)
            print(f"✅ Loaded weather for {district['name']}")
            
        except Exception as e:
            print(f"❌ Error loading weather for {district['name']}: {str(e)}")
            continue
    
    # Load into DuckDB
    conn = duckdb.connect(DB_PATH)
    
    # Create raw table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            district VARCHAR,
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            humidity FLOAT,
            pressure FLOAT,
            weather_condition VARCHAR,
            weather_description VARCHAR,
            wind_speed FLOAT,
            clouds INTEGER,
            rainfall FLOAT,
            timestamp TIMESTAMP,
            raw_json VARCHAR,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert records
    if weather_records:
        conn.executemany("""
            INSERT INTO raw_weather 
            (district, latitude, longitude, temperature, humidity, pressure, 
             weather_condition, weather_description, wind_speed, clouds, rainfall, timestamp, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [(r['district'], r['latitude'], r['longitude'], r['temperature'], 
               r['humidity'], r['pressure'], r['weather_condition'], 
               r['weather_description'], r['wind_speed'], r['clouds'], 
               r['rainfall'], r['timestamp'], r['raw_json']) 
              for r in weather_records])
        
        conn.commit()
        print(f"✅ Inserted {len(weather_records)} weather records into DuckDB")
    
    conn.close()
    
    return {
        'status': 'success',
        'records_loaded': len(weather_records),
        'timestamp': datetime.now().isoformat()
    }


if __name__ == '__main__':
    # For testing outside Mage
    result = load_weather_data()
    print(json.dumps(result, indent=2))
