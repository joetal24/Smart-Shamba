# 🌾 Smart-Shamba: Local Analytics Lakehouse for Agricultural Decisions

A complete, local-first analytics lakehouse that provides data-driven crop planting recommendations for Ugandan smallholder farmers.

---

## 📖 Project Overview

**Problem:** Farmers make planting decisions based on intuition, leading to losses from weather volatility and market fluctuations.

**Solution:** Smart-Shamba integrates weather, vegetation health (NDVI), and market price data to generate explainable, district-level crop recommendations.

**Tech Stack:** 100% free-tier tools running locally
- **Orchestration:** Mage.ai
- **Storage:** DuckDB
- **Transformation:** dbt Core
- **Visualization:** Streamlit
- **Language:** Python & SQL

---

## 🏗️ Architecture

```
External APIs → Mage.ai → DuckDB (Raw) → dbt (Transform) → Streamlit
                              ↓
                         Business Logic
                              ↓
                    Crop Recommendations
```

### Data Flow (ELT Pattern)

1. **Extract & Load:** Mage pipelines pull data from APIs and load into DuckDB raw tables
2. **Transform:** dbt models clean data (staging) and apply business rules (marts)
3. **Analyze:** Streamlit dashboard visualizes recommendations

---

## 📂 Project Structure

```
smart-shamba-lakehouse/
│
├── requirements.txt              # Python dependencies
├── setup_project.py             # Automated setup script
├── .env.template                # Environment variables template
│
├── mage_load_weather.py         # Weather data loader
├── mage_load_prices.py          # Price data loader
├── mage_load_vegetation.py      # Vegetation data loader
│
├── warehouse/
│   └── duckdb/
│       └── agri_analytics.db    # DuckDB database file
│
├── dbt/
│   ├── dbt_project.yml          # dbt configuration
│   ├── profiles.yml             # Database connection config
│   ├── dbt_sources.yml          # Raw data sources
│   │
│   └── models/
│       ├── staging/
│       │   ├── dbt_stg_weather.sql      # Clean weather data
│       │   ├── dbt_stg_prices.sql       # Clean price data
│       │   └── dbt_stg_vegetation.sql   # Clean vegetation data
│       │
│       └── marts/
│           └── dbt_mart_planting_advice.sql  # Final recommendations
│
└── streamlit_app.py             # Interactive dashboard
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Setup Script
```bash
python setup_project.py
```
This will:
- Create directory structure
- Initialize DuckDB database
- Create raw tables
- Generate .env template

### 3. Configure Environment
```bash
cp .env.template .env
```
Edit `.env` and add your OpenWeatherMap API key (free at https://openweathermap.org/api)

### 4. Load Data
```bash
# Run each loader
python mage_load_weather.py
python mage_load_prices.py
python mage_load_vegetation.py
```

### 5. Run dbt Transformations
```bash
# Create staging and mart models
dbt run

# Optional: Run tests
dbt test
```

### 6. Launch Dashboard
```bash
streamlit run streamlit_app.py
```

---

## 📊 How It Works

### Data Pipeline Explained

#### Step 1: Data Loading (Mage)
- **`mage_load_weather.py`**: Fetches weather data from OpenWeatherMap API for 4 Ugandan districts
- **`mage_load_prices.py`**: Simulates market price data (in production, would scrape real sources)
- **`mage_load_vegetation.py`**: Simulates NDVI satellite data (in production, would use Sentinel-2)

All raw data is preserved in DuckDB with full JSON payloads for audit trails.

#### Step 2: Data Cleaning (dbt Staging)
- **`dbt_stg_weather.sql`**: 
  - Standardizes district names
  - Categorizes rainfall (Heavy/Moderate/Light)
  - Calculates heat index
  
- **`dbt_stg_prices.sql`**:
  - Calculates price trends (Rising/Stable/Falling)
  - Generates selling advice
  - Measures price volatility
  
- **`dbt_stg_vegetation.sql`**:
  - Validates NDVI ranges (-1 to 1)
  - Classifies vegetation health
  - Calculates planting readiness scores

#### Step 3: Business Logic (dbt Mart)
**`dbt_mart_planting_advice.sql`** combines all data to generate recommendations:

**Scoring System:**
- **Weather Suitability (40%)**: Temperature + rainfall requirements per crop
- **Vegetation Suitability (35%)**: NDVI + soil moisture readiness
- **Market Opportunity (25%)**: Recent price trends

**Recommendation Formula:**
```
Overall Score = (Weather × 0.4) + (Vegetation × 0.35) + (Market × 0.25)
```

**Thresholds:**
- 7.5+: **Highly Recommended** (plant now)
- 6-7.5: **Recommended** (good conditions)
- 4-6: **Acceptable** (proceed with caution)
- <4: **Not Recommended** (wait)

#### Step 4: Visualization (Streamlit)
Dashboard provides:
- Top crop recommendations per district
- Market price trends
- Current weather conditions
- District comparisons with heatmaps

---

## 💡 Key Features

### 1. **Explainable Recommendations**
No black-box ML. Farmers see exactly why a crop is recommended:
- Weather conditions
- Soil health
- Market prices

### 2. **Local-First Architecture**
Runs entirely on your laptop. No cloud dependencies, no costs.

### 3. **Auditable Data**
Raw JSON preserved in database. Can trace any recommendation back to source data.

### 4. **Modular Design**
Each component (load, transform, visualize) is independent and testable.

---

## 🧪 Testing the System

### Verify Data Loading
```bash
# Check DuckDB directly
duckdb warehouse/duckdb/agri_analytics.db

# Run queries
SELECT COUNT(*) FROM raw_weather;
SELECT COUNT(*) FROM raw_prices;
SELECT COUNT(*) FROM raw_vegetation;
```

### Verify dbt Models
```bash
# Run dbt tests
dbt test

# Generate and view documentation
dbt docs generate
dbt docs serve
```

### Verify Dashboard
```bash
# Launch Streamlit
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
```

---

## 🇺🇬 Ugandan Context

### Districts Covered
- **Kampala**: Central region, urban agriculture
- **Mbale**: Eastern region, coffee and maize
- **Gulu**: Northern region, cassava and beans
- **Mbarara**: Western region, banana (matoke) and livestock

### Crops Evaluated
- **Maize**: Staple grain crop
- **Beans**: Protein-rich legume
- **Cassava**: Drought-resistant tuber
- **Sweet Potato**: Nutritious tuber
- **Coffee**: Major export crop
- **Banana (Matoke)**: Cooking banana, staple food

### Seasonal Considerations
Uganda has two rainy seasons:
1. March-May
2. September-November

The system adapts recommendations based on current rainfall patterns and soil moisture.

---

## 📈 Example Outputs

### Sample Recommendation
```
District: Mbale
Crop: Maize
Overall Score: 8.2/10
Category: Highly Recommended

Breakdown:
- Weather Suitability: 8/10 (optimal temp, good rainfall)
- Vegetation Suitability: 9/10 (healthy NDVI, moist soil)
- Market Opportunity: 7/10 (prices rising 12%)

Advice: Plant now. Conditions are ideal and market trends favorable.
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
OPENWEATHER_API_KEY=your_key_here
DB_PATH=warehouse/duckdb/agri_analytics.db
```

### dbt Profile (profiles.yml)
```yaml
smart_shamba:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: '../warehouse/duckdb/agri_analytics.db'
      threads: 4
```

---

## 🧠 Technical Concepts Demonstrated

### 1. **ELT Pattern**
Extract → Load → Transform (not ETL)
- Raw data preserved
- Transformations version-controlled
- Business logic explicit

### 2. **Analytics Engineering**
Using dbt to treat data transformation like software development:
- Version control (SQL in Git)
- Testing (dbt tests)
- Documentation (dbt docs)
- Dependency management (ref() function)

### 3. **Local Lakehouse**
DuckDB provides lakehouse capabilities locally:
- Columnar storage
- ACID transactions
- SQL analytics
- No server needed

### 4. **Business Rule Modeling**
Recommendations based on explicit, understandable rules:
- Transparent decision logic
- Domain expert input (agricultural best practices)
- Easy to audit and update

---

## 📚 Next Steps

### Enhancements
1. **Real Data Sources**
   - Connect to actual market APIs
   - Use Sentinel-2 satellite data via Google Earth Engine
   - Integrate weather forecasts (not just current)

2. **Geospatial Features**
   - Interactive maps with district boundaries
   - Crop suitability heatmaps
   - Transportation/market proximity analysis

3. **Historical Analysis**
   - Track recommendation accuracy over time
   - Seasonal trend analysis
   - Price forecasting

4. **User Features**
   - SMS/WhatsApp alerts for farmers
   - Multi-language support (English, Luganda, Swahili)
   - Mobile-first interface

---

## 🤝 Contributing

This is a portfolio/learning project, but improvements welcome!

Areas for contribution:
- Ugandan agricultural domain knowledge
- Additional data sources
- Mobile interface design
- Translation to local languages

---

## 📄 License

MIT License - Free to use for learning and non-commercial purposes.

---

## 🙏 Acknowledgments

- OpenWeatherMap API for weather data
- dbt Community for analytics engineering best practices
- Ugandan agricultural extension services for domain knowledge

---

**Made with ❤️ for smallholder farmers in Uganda**

🌾 Smart-Shamba | Data-Driven Agriculture
# Smart-Shamba
