# Smart-Shamba Quick Start

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
