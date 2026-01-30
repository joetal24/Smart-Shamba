# 🚀 Smart-Shamba Streamlit Community Cloud Deployment Guide

This guide provides step-by-step instructions to deploy the Smart-Shamba dashboard to Streamlit Community Cloud.

---

## 📋 Prerequisites

Before deploying, ensure you have:

1. **GitHub Repository**: Push your code to GitHub
2. **Streamlit Account**: Create a free account at https://streamlit.io
3. **OpenWeatherMap API Key**: Get a free key from https://openweathermap.org/api
4. **Pre-initialized Database**: Your DuckDB database with data loaded

---

## 🔄 Complete Deployment Checklist

### Step 1: Prepare Your Repository

```bash
# 1a. Ensure all files are committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main

# 1b. Verify these files exist in your repo:
# - streamlit_app.py (main app)
# - streamlit_requirements.txt (dependencies)
# - .streamlit/config.toml (Streamlit configuration)
# - .env.template (template for secrets)
# - warehouse/duckdb/agri_analytics.db (pre-populated database)
```

### Step 2: Configure Environment Variables

**Local Development:**
```bash
# Copy the template
cp .env.template .env

# Edit .env and add your actual API key
nano .env
# OPENWEATHER_API_KEY=your_actual_api_key
# DB_PATH=warehouse/duckdb/agri_analytics.db
```

**Streamlit Cloud:**
- Do NOT commit `.env` file
- Secrets are managed in the Streamlit Cloud dashboard (see Step 4)

### Step 3: Test Locally Before Deploying

```bash
# Install dependencies
pip install -r streamlit_requirements.txt

# Run the app locally
streamlit run streamlit_app.py

# Visit http://localhost:8501 in your browser
# Verify all features work correctly
```

### Step 4: Deploy to Streamlit Community Cloud

#### 4a. Create App on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **"Create App"**
3. Fill in the form:
   - **GitHub repository**: Select your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
4. Click **"Deploy"**

The app will start deploying. This may take 2-3 minutes.

#### 4b. Add Secrets to Streamlit Cloud

After deployment:

1. Click **"⋯"** (three dots) → **"Settings"** in the top-right
2. Go to **"Secrets"** tab
3. Add your secrets in TOML format:

```toml
openweather_api_key = "your_actual_api_key_here"
db_path = "warehouse/duckdb/agri_analytics.db"
```

4. Save and the app will auto-refresh

### Step 5: Access Your Deployed App

Your app will be available at:
```
https://[your-github-username]-smart-shamba.streamlit.app
```

Share this link with stakeholders!

---

## 🔧 Configuration Files Explained

### `.streamlit/config.toml`
Controls Streamlit app appearance and behavior:
- Theme colors (green for agriculture)
- Page layout and toolbar
- Logging levels
- File upload limits

### `.streamlit/secrets.toml`
Template for sensitive data. **Never commit actual secrets here.**
Streamlit Cloud secrets are managed separately in the dashboard.

### `streamlit_requirements.txt`
Lightweight dependencies for the dashboard only (no Mage.ai, no dbt).
- Streamlit for UI
- DuckDB for database access
- Plotly for visualizations
- Folium for maps

---

## 📊 Updating Your App

### To Update Code:
```bash
# Make changes locally
# Test with: streamlit run streamlit_app.py

# Commit and push
git add .
git commit -m "Update feature/fix bug"
git push origin main

# Streamlit Cloud automatically redeploys on push!
```

### To Update Database:
```bash
# Run data loading scripts locally
python setup_project.py
python mage_load_weather.py
python mage_load_prices.py
python mage_load_vegetation.py

# Or run dbt transformation
cd dbt
dbt run

# Commit updated database
git add warehouse/duckdb/agri_analytics.db
git commit -m "Update database with latest data"
git push origin main
```

---

## 🐛 Troubleshooting

### App Won't Deploy

**Error: "Module not found"**
- Ensure `streamlit_requirements.txt` is in the root directory
- Check spelling of package names

**Error: "File not found: warehouse/duckdb/agri_analytics.db"**
- Database must be committed to GitHub
- Run `python setup_project.py` locally first
- Then: `git add warehouse/duckdb/agri_analytics.db && git push`

### Secrets Not Working

- Click **"Settings"** → **"Secrets"**
- Check TOML syntax (quotes around values)
- Save and wait for auto-refresh (30 seconds)

### Database Size Issues

DuckDB files can be large. If deployment fails:
```bash
# Check file size
ls -lh warehouse/duckdb/agri_analytics.db

# If >100MB, consider:
# 1. Archiving old data
# 2. Using a cloud database (Supabase, Render, etc.)
# 3. Loading data on-demand from APIs
```

### Performance Issues

- Use `@st.cache_data` decorators to cache queries
- Limit data to recent records (e.g., last 30 days)
- Optimize dbt queries for speed

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use Streamlit Secrets** for sensitive data in cloud
3. **Rotate API keys** regularly
4. **Limit database access** - Use read-only connections where possible
5. **Monitor app logs** in Streamlit Cloud dashboard

---

## 📈 Performance Tips

1. **Cache data aggressively**:
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def load_data():
       ...
   ```

2. **Optimize dbt queries** for speed

3. **Use summary tables** instead of raw data

4. **Limit displayed records**:
   ```python
   st.dataframe(df.head(100))  # Show first 100 only
   ```

---

## 🔗 Useful Links

- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Cloud Docs: https://docs.streamlit.io/deploy/streamlit-cloud
- DuckDB Guide: https://duckdb.org/docs/
- OpenWeatherMap API: https://openweathermap.org/api

---

## 📞 Support & Troubleshooting

If you encounter issues:

1. Check Streamlit Cloud **Logs** tab
2. Review this guide's troubleshooting section
3. Check GitHub Issues in the Smart-Shamba repo
4. Review Streamlit documentation

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `streamlit_app.py` is main entry point
- [ ] `streamlit_requirements.txt` exists and is up-to-date
- [ ] `.streamlit/config.toml` configured
- [ ] `.env` added to `.gitignore`
- [ ] `warehouse/duckdb/agri_analytics.db` committed to repo
- [ ] App deployed to Streamlit Cloud
- [ ] API key added to Secrets in dashboard
- [ ] App tested and working at public URL
- [ ] Shared with stakeholders

---

**Last Updated**: January 30, 2026
**Status**: Ready for Production Deployment
