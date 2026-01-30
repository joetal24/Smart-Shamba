# 🌾 Smart-Shamba: Complete Streamlit Cloud Deployment Guide

**Status**: ✅ Ready for Production  
**Last Updated**: January 30, 2026  
**Version**: 1.0

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [What Was Configured](#what-was-configured)
3. [Directory Structure](#directory-structure)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Reproducible Setup Steps](#reproducible-setup-steps)
6. [Files Reference](#files-reference)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Smart-Shamba is now fully configured for deployment on **Streamlit Community Cloud**—a free platform for hosting Streamlit apps.

**Key Benefits**:
- ✅ Free hosting (no server costs)
- ✅ Automatic deployments from GitHub
- ✅ HTTPS/SSL included
- ✅ Shareable public URL
- ✅ Auto-scaling for traffic
- ✅ Built-in secret management

**Deployment Time**: ~2-3 minutes after pushing to GitHub

---

## What Was Configured

### 1. **Streamlit Configuration** (`.streamlit/config.toml`)
- Theme colors (green for agriculture)
- Page layout set to wide
- Toolbar mode set to viewer
- Server optimized for cloud deployment
- File upload limit: 200MB

### 2. **Secrets Management** (`.streamlit/secrets.toml`)
- Template for sensitive data (API keys)
- Never commits real secrets
- Secrets managed via Streamlit Cloud dashboard
- Format: TOML (key = "value")

### 3. **Lightweight Dependencies** (`streamlit_requirements.txt`)
- Streamlit, DuckDB, Pandas, Plotly, Folium
- **Excludes**: Mage.ai and dbt (not needed for dashboard)
- All versions pinned for reproducibility
- ~50MB total size (small, fast deployment)

### 4. **Updated App Code** (`streamlit_app.py`)
- Modified to read config from `st.secrets`
- Fallback to environment variables for local development
- Read-only database connections (safety)

### 5. **Environment Management** (`.env.template`)
- Template for local development
- `.env` added to `.gitignore` (security)
- Instructions for adding API key

### 6. **Verification Script** (`verify_deployment.py`)
- Checks all required files exist
- Verifies security settings
- Confirms dependencies are correct
- **Run before deploying**: `python3 verify_deployment.py`

### 7. **Comprehensive Documentation**
- `DEPLOYMENT.md` - Full deployment guide
- `DEPLOYMENT_QUICK_START.md` - Quick reference
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment checklist
- `DEPLOYMENT_GUIDE.md` - This file

---

## Directory Structure

```
Smart-Shamba/
│
├── streamlit_app.py                    # Main dashboard app ✨
├── streamlit_requirements.txt           # Cloud dependencies ✨
├── requirements.txt                     # All project dependencies
├── verify_deployment.py                 # Verification script ✨
│
├── .streamlit/                          # Streamlit config directory ✨
│   ├── config.toml                     # App settings
│   └── secrets.toml                    # Secrets template (don't commit real ones)
│
├── .env                                # Local secrets (NOT in git)
├── .env.template                       # Template (in git) ✨
├── .gitignore                          # Git ignore rules (updated) ✨
│
├── warehouse/duckdb/                    # Database directory
│   └── agri_analytics.db               # DuckDB database ✨
│
├── DEPLOYMENT.md                        # Full guide ✨
├── DEPLOYMENT_QUICK_START.md           # Quick start ✨
├── DEPLOYMENT_CHECKLIST.md             # Pre-deploy checklist ✨
│
├── mage/                               # (Not needed for cloud)
├── dbt/                                # (Not needed for cloud)
├── mage_load_*.py                      # (Not needed for cloud)
│
└── [other project files]
```

**✨** = New or updated for cloud deployment

---

## Step-by-Step Deployment

### Phase 1: Local Verification (5 minutes)

#### 1.1 Run Verification Script
```bash
cd ~/Documents/GitHub/Data\ engineering\ projects/Smart\ shamba
python3 verify_deployment.py
```

**Expected Output**:
```
✓ All critical checks passed!
```

#### 1.2 Test App Locally
```bash
pip install -r streamlit_requirements.txt
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` and verify:
- [ ] Dashboard loads
- [ ] All pages work
- [ ] Data displays correctly
- [ ] Visualizations render
- [ ] No console errors

Press `Ctrl+C` to stop.

---

### Phase 2: GitHub Preparation (2 minutes)

#### 2.1 Update .env (Local Only)
```bash
# Copy template
cp .env.template .env

# Edit with your API key
nano .env
# OPENWEATHER_API_KEY=your_actual_key_here
```

#### 2.2 Verify .gitignore
```bash
# Make sure .env is listed
grep -n "^\.env$" .gitignore

# You should see:
# [line number]: .env
```

#### 2.3 Commit and Push
```bash
# Check status (should not show .env)
git status

# Commit all changes
git add -A
git commit -m "Configure for Streamlit Cloud deployment

- Add .streamlit/config.toml for app settings
- Add streamlit_requirements.txt for cloud dependencies
- Update streamlit_app.py to use st.secrets
- Add verify_deployment.py script
- Add comprehensive deployment guides
- Update .env.template and .gitignore"

# Push to GitHub
git push origin main
```

**Verify on GitHub**: Visit your repo, confirm files are there (except `.env`).

---

### Phase 3: Streamlit Cloud Deployment (3 minutes)

#### 3.1 Create App on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in (or create free account)
3. Click **"Create App"**
4. Fill in the form:
   - **GitHub repository**: `joetal24/Smart-Shamba` (select from dropdown)
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Click **"Deploy"**

**What happens**:
- Streamlit clones your repo
- Installs `streamlit_requirements.txt`
- Starts the app
- Gives you a public URL

**Wait**: 2-3 minutes for deployment to complete.

#### 3.2 Add Secrets

Once deployed, add your API key:

1. Click **⚙️ Settings** (top-right)
2. Click **"Secrets"** tab
3. Paste this text:
```toml
openweather_api_key = "your_actual_api_key_here"
db_path = "warehouse/duckdb/agri_analytics.db"
```
4. Replace `your_actual_api_key_here` with your real OpenWeatherMap API key
5. Click **"Save"**

**Wait**: ~30 seconds for app to refresh

#### 3.3 Verify Deployment

Your app is live at:
```
https://[your-github-username]-smart-shamba.streamlit.app
```

Visit this URL and check:
- [ ] Dashboard loads
- [ ] No "missing secret" errors
- [ ] Data displays correctly
- [ ] All features work

**Celebrate! 🎉** Your app is now live!

---

## Reproducible Setup Steps

### For Future Reference or Setting Up Again

If you need to reproduce this setup on another machine:

```bash
# 1. Clone the repository
git clone https://github.com/joetal24/Smart-Shamba.git
cd Smart-Shamba

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.template .env
nano .env  # Add your actual API key

# 5. Verify setup (optional)
python3 setup_project.py

# 6. Test the app
streamlit run streamlit_app.py
# Visit http://localhost:8501

# 7. Deploy (follow Phase 3 above)
```

### Updating After Deployment

**Update Code**:
```bash
# Make changes locally
nano streamlit_app.py

# Test
streamlit run streamlit_app.py

# Push to GitHub (auto-deploys)
git add streamlit_app.py
git commit -m "Fix feature"
git push origin main
# Wait 1-2 minutes for cloud to redeploy
```

**Update Database**:
```bash
# Refresh data locally
python3 setup_project.py

# Or use Mage/dbt
mage run daily_agri_ingest

# Commit and push
git add warehouse/duckdb/agri_analytics.db
git commit -m "Update data: $(date +%Y-%m-%d)"
git push origin main
# App redeploys with new data
```

---

## Files Reference

### New/Modified Files for Deployment

| File | Purpose | Type | Must Commit? |
|------|---------|------|--------------|
| `.streamlit/config.toml` | Streamlit settings | Config | ✅ Yes |
| `.streamlit/secrets.toml` | Secrets template | Config | ✅ Yes |
| `streamlit_requirements.txt` | Cloud dependencies | Config | ✅ Yes |
| `streamlit_app.py` | Updated for secrets | Code | ✅ Yes |
| `.env` | Your actual secrets | Secret | ❌ NO |
| `.env.template` | Secrets template | Template | ✅ Yes |
| `.gitignore` | Updated | Config | ✅ Yes |
| `verify_deployment.py` | Verification script | Script | ✅ Yes |
| `DEPLOYMENT.md` | Full guide | Doc | ✅ Yes |
| `DEPLOYMENT_QUICK_START.md` | Quick reference | Doc | ✅ Yes |
| `DEPLOYMENT_CHECKLIST.md` | Pre-deploy checklist | Doc | ✅ Yes |

---

## Troubleshooting

### Deployment Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **"Module not found"** | Wrong package name or missing from requirements | Check `streamlit_requirements.txt`, try installing locally first |
| **"Database not found"** | File not committed to git | Run `git add warehouse/duckdb/agri_analytics.db && git push` |
| **"Secrets not working"** | Syntax error or not saved | Check TOML syntax in dashboard, hard refresh (Ctrl+F5) |
| **"App crashes on startup"** | Check logs | Click "Logs" in Streamlit Cloud, look for error messages |
| **"Slow deployment"** | Large file size | Check `warehouse/duckdb/agri_analytics.db` size (should be <100MB) |

### Runtime Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **"API key error"** | Key not in secrets or wrong format | Go to Settings → Secrets, verify key value |
| **"No data displayed"** | Database connection failed | Ensure `db_path` secret is set correctly |
| **"Slow queries"** | Large dataset or no caching | Add `@st.cache_data(ttl=3600)` to functions |
| **"Memory error"** | Loading too much data | Limit queries (e.g., last 30 days only) |

### Common Fixes

**App won't deploy**:
```bash
# 1. Check file names
ls -la streamlit_requirements.txt

# 2. Verify syntax
python3 -m py_compile streamlit_app.py

# 3. Test locally
pip install -r streamlit_requirements.txt
streamlit run streamlit_app.py
```

**Secrets don't work**:
```
1. Go to Settings → Secrets in Streamlit Cloud
2. Check TOML syntax:
   - Good: openweather_api_key = "abc123"
   - Bad: openweather_api_key = abc123 (missing quotes)
3. Save and hard refresh (Ctrl+F5)
```

**Database too large**:
```bash
# Check size
ls -lh warehouse/duckdb/agri_analytics.db

# If >100MB, archive old data:
# - Delete records older than 6 months
# - Run VACUUM in DuckDB
# - Commit and push the smaller database
```

---

## Security Best Practices

✅ **Do**:
- ✅ Keep `.env` in `.gitignore`
- ✅ Use Streamlit Secrets dashboard for sensitive data
- ✅ Rotate API keys every 3-6 months
- ✅ Review `.gitignore` regularly
- ✅ Use read-only database connections
- ✅ Monitor app logs for unusual activity

❌ **Don't**:
- ❌ Commit `.env` file
- ❌ Put API keys in code
- ❌ Put API keys in config files
- ❌ Share secrets in chat/email
- ❌ Use the same key for production and dev
- ❌ Grant write access to database

---

## Performance Tips

1. **Cache Data Aggressively**:
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def load_data():
       return pd.read_sql(query, conn)
   ```

2. **Optimize Queries**:
   - Use `LIMIT` for large datasets
   - Filter by date range (e.g., last 30 days)
   - Use indexed columns in WHERE clauses

3. **Limit Display Size**:
   ```python
   st.dataframe(df.head(100))  # Show first 100 rows only
   ```

4. **Precompute Results**:
   - Use dbt to create summary tables
   - Store aggregations in database
   - Query summaries instead of raw data

5. **Monitor Logs**:
   - Check Streamlit Cloud logs regularly
   - Look for slow queries
   - Monitor resource usage

---

## Next Steps

1. **Deploy**: Follow Phase 1-3 above
2. **Monitor**: Check logs in Streamlit Cloud dashboard
3. **Share**: Give stakeholders the URL
4. **Update**: Push changes to GitHub (auto-deploys)
5. **Optimize**: Add caching, optimize queries
6. **Scale**: If needed, migrate to cloud database

---

## Quick Commands Reference

```bash
# Verify setup
python3 verify_deployment.py

# Test locally
streamlit run streamlit_app.py

# Deploy changes
git add -A && git commit -m "msg" && git push origin main

# Check status
git status
git log --oneline | head -5

# File checks
ls -la .streamlit/
ls -lh warehouse/duckdb/agri_analytics.db
cat streamlit_requirements.txt | head -10
```

---

## Useful Links

| Resource | Link |
|----------|------|
| Streamlit Documentation | https://docs.streamlit.io |
| Cloud Deployment Guide | https://docs.streamlit.io/deploy/streamlit-cloud |
| DuckDB Documentation | https://duckdb.org/docs/ |
| OpenWeatherMap API | https://openweathermap.org/api |
| Streamlit Community Forum | https://discuss.streamlit.io |

---

## Support

If you encounter issues:

1. **Check logs**: Streamlit Cloud dashboard → Logs tab
2. **Read guides**: 
   - `DEPLOYMENT.md` (full details)
   - `DEPLOYMENT_QUICK_START.md` (quick reference)
   - `DEPLOYMENT_CHECKLIST.md` (verification)
3. **Test locally**: `streamlit run streamlit_app.py`
4. **Verify files**: `python3 verify_deployment.py`
5. **Check GitHub**: Look for issues in your repo

---

## Summary

Your Smart-Shamba project is **fully configured and ready for Streamlit Community Cloud deployment**.

**What's been done**:
- ✅ Streamlit configuration files created
- ✅ Dependencies organized for cloud
- ✅ App code updated for cloud deployment
- ✅ Secrets management configured
- ✅ Security best practices implemented
- ✅ Verification script created
- ✅ Comprehensive documentation written

**Next action**: Follow the **Step-by-Step Deployment** section above to deploy!

---

**Happy Deploying! 🚀**

---

*Last Updated: January 30, 2026*  
*Status: Production Ready*  
*Verified: ✅ All checks passed*
