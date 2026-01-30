# 📋 Streamlit Community Cloud - Reproducible Deployment Guide

## Quick Reference

**Deployment URL Format**: `https://[github-username]-smart-shamba.streamlit.app`

**Time to Deploy**: 2-3 minutes

---

## 🔑 Key Files for Deployment

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main dashboard application |
| `streamlit_requirements.txt` | Lightweight dependencies (dashboard only) |
| `.streamlit/config.toml` | Appearance and behavior settings |
| `.streamlit/secrets.toml` | Template for secrets (don't commit!) |
| `warehouse/duckdb/agri_analytics.db` | Pre-initialized database |
| `.env.template` | Environment variables template |
| `.gitignore` | Git ignore rules (includes `.env`) |
| `DEPLOYMENT.md` | Full deployment instructions |

---

## 🚀 Reproducible Steps (TL;DR)

### Step 1: Local Setup
```bash
# Clone or navigate to your repo
cd ~/Documents/GitHub/Data\ engineering\ projects/Smart\ shamba

# Copy environment template
cp .env.template .env

# Add your API key to .env
nano .env
# OPENWEATHER_API_KEY=your_actual_key_here

# Install dependencies
pip install -r streamlit_requirements.txt

# Test locally
streamlit run streamlit_app.py
# Visit http://localhost:8501
```

### Step 2: Push to GitHub
```bash
# Verify .env is in .gitignore
grep "^\.env$" .gitignore

# Commit and push
git add .
git commit -m "Configure for Streamlit Cloud deployment"
git push origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click **"Create App"**
3. Select your GitHub repo and `streamlit_app.py`
4. Click **"Deploy"**

### Step 4: Add Secrets
1. Once deployed, click **Settings** ⚙️
2. Go to **"Secrets"** tab
3. Paste this TOML (fill in your API key):
```toml
openweather_api_key = "your_actual_api_key_here"
db_path = "warehouse/duckdb/agri_analytics.db"
```
4. Save and wait for auto-refresh (~30 seconds)

### Step 5: Verify & Share
- Your app is live at: `https://[username]-smart-shamba.streamlit.app`
- Share the link!

---

## 🔄 Updating Your App (After Deployment)

### Update Code
```bash
# Make changes locally
nano streamlit_app.py

# Test it
streamlit run streamlit_app.py

# Push to GitHub
git add streamlit_app.py
git commit -m "Update feature/fix"
git push origin main
# Streamlit Cloud auto-deploys! (1-2 minutes)
```

### Update Database
```bash
# Refresh data locally
python setup_project.py
python mage_load_weather.py
python mage_load_prices.py
python mage_load_vegetation.py

# Or use dbt
cd dbt && dbt run

# Commit and push
git add warehouse/duckdb/agri_analytics.db
git commit -m "Update database"
git push origin main
# App redeploys with new data
```

### Update Dependencies
```bash
# Add to streamlit_requirements.txt
echo "new-package==1.0.0" >> streamlit_requirements.txt

# Update main requirements too
echo "new-package==1.0.0" >> requirements.txt

# Commit
git add streamlit_requirements.txt requirements.txt
git commit -m "Add new dependency"
git push origin main
```

---

## 🛠️ Configuration Details

### `.streamlit/config.toml`
- **Theme**: Green colors (agriculture theme)
- **Layout**: Wide (uses full page width)
- **Toolbar**: Visible in viewer mode
- **Upload limit**: 200MB

### `streamlit_requirements.txt`
Minimal dependencies for dashboard:
```
streamlit>=1.28.0      # Web framework
duckdb>=0.8.0          # Database
pandas>=1.5.0          # Data processing
plotly>=5.17.0         # Visualizations
folium>=0.14.0         # Maps
requests>=2.31.0       # HTTP requests
python-dotenv>=1.0.0   # Environment variables
pyyaml>=6.0            # Config files
```

**Why separate from requirements.txt?**
- Cloud doesn't need Mage.ai or dbt
- Smaller dependencies = faster deployment
- Cleaner environment

### `.streamlit/secrets.toml`
- **Never commit actual secrets**
- Only template goes in repo
- Real secrets set in Streamlit Cloud dashboard
- Format: TOML (key = "value")

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
# Verify file is named correctly
ls -la streamlit_requirements.txt

# Check package names (case-sensitive)
cat streamlit_requirements.txt
```

### "Database file not found"
```bash
# Database must be in git
git status warehouse/duckdb/agri_analytics.db

# If not tracked:
git add warehouse/duckdb/agri_analytics.db
git commit -m "Add database"
git push origin main
```

### "Secrets not recognized"
```
1. Go to Settings → Secrets
2. Check TOML syntax:
   - Keys use underscores: openweather_api_key
   - Values in quotes: "actual_value"
   - No comments with #
3. Save and wait 30 seconds
4. Hard refresh browser (Ctrl+F5)
```

### "App crashes at startup"
1. Check Streamlit Cloud logs (in dashboard)
2. Test locally: `streamlit run streamlit_app.py`
3. Look for errors in database connection
4. Ensure .env/.secrets have required keys

### "App runs slow"
1. Add caching:
   ```python
   @st.cache_data(ttl=3600)
   def load_data():
       ...
   ```
2. Optimize dbt queries
3. Limit displayed records
4. Reduce database file size (archive old data)

---

## 📊 Database Management

### Current Setup
- **Database**: DuckDB (embedded SQLite alternative)
- **Storage**: `warehouse/duckdb/agri_analytics.db`
- **File Size**: Should be <100MB for smooth deployment
- **Access**: Read-only from Streamlit app

### Refresh Data Workflow
```bash
# 1. Run local pipelines
mage run daily_agri_ingest

# 2. Transform with dbt
dbt run

# 3. Verify locally
streamlit run streamlit_app.py

# 4. Commit and push
git add warehouse/duckdb/agri_analytics.db
git commit -m "Update data: $(date +%Y-%m-%d)"
git push origin main
```

### If Database Gets Too Large
Options (in order of preference):
1. **Archive old data**: Keep only last 30-90 days
2. **Optimize tables**: Run `VACUUM` in DuckDB
3. **Use cloud database**: 
   - Supabase (PostgreSQL)
   - Neon (PostgreSQL)
   - Render (PostgreSQL/MySQL)
   - This requires app changes (no file path)

---

## 🔐 Security Checklist

- [ ] `.env` file in `.gitignore`
- [ ] No API keys in code
- [ ] No API keys in config files (except template)
- [ ] Secrets set in Streamlit Cloud dashboard
- [ ] Database file has no sensitive data
- [ ] Read-only database connection from app
- [ ] API key rotated regularly (every 3-6 months)

---

## 📱 Testing Checklist Before Deploying

```bash
# 1. Install fresh dependencies
pip install -r streamlit_requirements.txt

# 2. Test with .env file
streamlit run streamlit_app.py
# Verify all pages load
# Verify data displays correctly
# Try all interactive elements

# 3. Test with secrets simulation
# Edit .streamlit/secrets.toml with actual key
# Restart app: Ctrl+C then streamlit run streamlit_app.py

# 4. Check git status
git status
# Ensure .env and secrets.toml are NOT listed

# 5. Final push
git add -A
git commit -m "Ready for cloud deployment"
git push origin main
```

---

## 🎯 Common Deployment Commands

| Command | Purpose |
|---------|---------|
| `streamlit run streamlit_app.py` | Test locally |
| `git add -A && git commit -m "msg" && git push` | Deploy changes |
| `pip install -r streamlit_requirements.txt` | Install deps |
| `cp .env.template .env` | Setup environment |
| `python setup_project.py` | Initialize database |

---

## 📞 Getting Help

1. **Streamlit Docs**: https://docs.streamlit.io
2. **Cloud Deployment**: https://docs.streamlit.io/deploy/streamlit-cloud
3. **DuckDB Docs**: https://duckdb.org/docs/
4. **GitHub Issues**: Check your repo's issues tab

---

## ✨ Next Steps After Deployment

1. **Monitor Performance**: Check Streamlit Cloud dashboard
2. **Gather Feedback**: Share with users, collect feedback
3. **Optimize**: Add features based on feedback
4. **Automate Updates**: Setup GitHub Actions to refresh data automatically
5. **Scale Up**: If successful, move to self-hosted Streamlit or cloud database

---

**Last Updated**: January 30, 2026  
**Version**: 1.0  
**Status**: Production Ready
