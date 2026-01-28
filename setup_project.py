#!/usr/bin/env python3
"""
Setup Script for Smart-Shamba Project
======================================
This script initializes the database and runs initial data loads.

Usage: python setup_project.py
"""

import os
import sys
import duckdb
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
DB_DIR = PROJECT_ROOT / 'warehouse' / 'duckdb'
DB_PATH = DB_DIR / 'agri_analytics.db'

def create_directories():
    """Create necessary directory structure."""
    print("📁 Creating directory structure...")
    
    directories = [
        'warehouse/duckdb',
        'mage/pipelines/daily_agri_ingest',
        'dbt/models/staging',
        'dbt/models/marts',
        'dbt/tests',
        'data_samples',
        'architecture'
    ]
    
    for directory in directories:
        dir_path = PROJECT_ROOT / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {directory}")
    
    print("✅ Directory structure created\n")


def initialize_database():
    """Initialize DuckDB database with raw tables."""
    print("🗄️  Initializing DuckDB database...")
    
    # Ensure directory exists
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Connect and create tables
    conn = duckdb.connect(str(DB_PATH))
    
    # Create raw tables
    print("  Creating raw_weather table...")
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
    
    print("  Creating raw_prices table...")
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
    
    print("  Creating raw_vegetation table...")
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
    
    conn.close()
    print("✅ Database initialized\n")


def run_data_loaders():
    """Run the data loader scripts to populate initial data."""
    print("🔄 Running data loaders...")
    
    try:
        # Import and run loaders
        sys.path.insert(0, str(PROJECT_ROOT))
        
        print("  Loading weather data...")
        from mage_load_weather import load_weather_data
        weather_result = load_weather_data()
        print(f"  ✓ Loaded {weather_result['records_loaded']} weather records")
        
        print("  Loading price data...")
        from mage_load_prices import load_price_data
        price_result = load_price_data()
        print(f"  ✓ Loaded {price_result['records_loaded']} price records")
        
        print("  Loading vegetation data...")
        from mage_load_vegetation import load_vegetation_data
        veg_result = load_vegetation_data()
        print(f"  ✓ Loaded {veg_result['records_loaded']} vegetation records")
        
        print("✅ Data loading complete\n")
        
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        print("Note: Make sure you have the required API keys set up")
        return False
    
    return True


def create_env_template():
    """Create a .env template file."""
    print("📝 Creating .env template...")
    
    env_template = """# Smart-Shamba Environment Variables
# ====================================

# OpenWeatherMap API Key (get free key from https://openweathermap.org/api)
OPENWEATHER_API_KEY=your_api_key_here

# Database path (default is fine for local development)
DB_PATH=warehouse/duckdb/agri_analytics.db
"""
    
    env_path = PROJECT_ROOT / '.env.template'
    with open(env_path, 'w') as f:
        f.write(env_template)
    
    print(f"  ✓ Created .env.template")
    print("  ⚠️  Copy this to .env and add your actual API keys")
    print("✅ Environment template created\n")


def create_readme():
    """Create a quick start README."""
    print("📖 Creating README...")
    
    readme = """# Smart-Shamba Quick Start

## Setup Complete! 🎉

Your project structure is ready. Here's what to do next:

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up Environment
```bash
cp .env.template .env
# Edit .env and add your OpenWeatherMap API key
```

### 3️⃣ Run Data Pipelines
```bash
# Run individual loaders
python mage_load_weather.py
python mage_load_prices.py
python mage_load_vegetation.py
```

### 4️⃣ Run dbt Transformations
```bash
cd dbt
dbt run
dbt test
```

### 5️⃣ Launch Dashboard
```bash
streamlit run streamlit_app.py
```

## Project Structure
```
smart-shamba-lakehouse/
├── warehouse/duckdb/          # DuckDB database
├── mage/                      # Data loading pipelines
├── dbt/                       # Data transformations
├── streamlit_app.py          # Dashboard
└── requirements.txt          # Python dependencies
```

## Need Help?
- Check DuckDB: `duckdb warehouse/duckdb/agri_analytics.db`
- Run dbt docs: `dbt docs generate && dbt docs serve`

Happy farming! 🌾
"""
    
    readme_path = PROJECT_ROOT / 'QUICKSTART.md'
    with open(readme_path, 'w') as f:
        f.write(readme)
    
    print("  ✓ Created QUICKSTART.md")
    print("✅ Documentation created\n")


def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("🌾 SMART-SHAMBA PROJECT SETUP")
    print("="*60 + "\n")
    
    create_directories()
    initialize_database()
    create_env_template()
    create_readme()
    
    print("="*60)
    print("✅ Setup complete!")
    print("="*60 + "\n")
    
    print("📋 Next steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Set up API keys in .env file")
    print("  3. Run data loaders: python mage_load_weather.py")
    print("  4. Check QUICKSTART.md for detailed instructions")
    print("\n🚀 Ready to go!\n")


if __name__ == '__main__':
    main()
