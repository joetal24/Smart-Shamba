# 🚀 Smart-Shamba Streamlit Cloud Deployment Checklist

Complete this checklist to ensure your project is ready for Streamlit Community Cloud deployment.

## ✅ Pre-Deployment Checklist

### 1. Files and Structure
- [ ] `streamlit_app.py` exists in root directory
- [ ] `streamlit_requirements.txt` exists with core dependencies
- [ ] `.streamlit/config.toml` exists with theme configuration
- [ ] `.streamlit/secrets.toml` exists (template only, no real keys)
- [ ] `warehouse/duckdb/agri_analytics.db` committed to git
- [ ] `.env.template` exists in root
- [ ] `DEPLOYMENT.md` exists with full instructions
- [ ] `verify_deployment.py` exists for verification

### 2. Security
- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in `streamlit_app.py`
- [ ] No API keys in `.streamlit/config.toml`
- [ ] All secrets use template in `.streamlit/secrets.toml`
- [ ] `.gitignore` blocks: `.env`, `*.db`, `venv/`, `__pycache__/`

### 3. Dependencies
- [ ] `streamlit_requirements.txt` includes:
  - `streamlit>=1.28.0`
  - `duckdb>=0.8.0`
  - `pandas>=1.5.0`
  - `plotly>=5.17.0`
  - `python-dotenv>=1.0.0`
- [ ] No Mage.ai or dbt in `streamlit_requirements.txt`
- [ ] All versions pinned (e.g., `package==1.0.0`)

### 4. Code Updates
- [ ] `streamlit_app.py` uses `st.secrets` for configuration:
  ```python
  api_key = st.secrets.get("openweather_api_key")
  db_path = st.secrets.get("db_path", "./warehouse/duckdb/agri_analytics.db")
  ```
- [ ] Database connections use read-only mode
- [ ] All imports are available in `streamlit_requirements.txt`
- [ ] No `sys.path` hacks or relative imports that won't work in cloud

### 5. Database
- [ ] DuckDB database is <100MB (for reasonable deployment times)
- [ ] Database file is tracked in git: `git ls-files warehouse/duckdb/agri_analytics.db`
- [ ] Database has been tested locally with Streamlit app
- [ ] Database initialization script exists: `setup_project.py`

### 6. Configuration Files
- [ ] `.streamlit/config.toml`:
  ```toml
  [theme]
  primaryColor = "#2E7D32"
  
  [server]
  headless = true
  runOnSave = true
  ```
- [ ] `.streamlit/secrets.toml` (template):
  ```toml
  openweather_api_key = ""
  db_path = "warehouse/duckdb/agri_analytics.db"
  ```

### 7. Git and GitHub
- [ ] All changes committed: `git status` shows clean
- [ ] Latest changes pushed: `git push origin main`
- [ ] GitHub repository is public (or owned by deployer)
- [ ] `.gitignore` prevents committing secrets

### 8. Documentation
- [ ] `README.md` includes deployment instructions
- [ ] `DEPLOYMENT.md` has step-by-step guide
- [ ] `DEPLOYMENT_QUICK_START.md` has quick reference
- [ ] Comments in code explain critical sections

### 9. Testing (Local)
- [ ] App runs without errors: `streamlit run streamlit_app.py`
- [ ] Dashboard loads all pages
- [ ] Data displays correctly
- [ ] No errors in terminal console
- [ ] Interactive elements respond (filters, buttons, etc.)
- [ ] Maps/visualizations render properly

### 10. API Keys and Secrets
- [ ] OpenWeatherMap API key obtained (free from https://openweathermap.org/api)
- [ ] API key NOT in any code files
- [ ] API key stored in `.env` locally (for testing)
- [ ] Ready to add to Streamlit Cloud secrets dashboard

---

## 🚀 Deployment Steps

### Step 1: Verify Everything
```bash
python verify_deployment.py
```
Should show all ✓ marks.

### Step 2: Test Locally
```bash
# Install dependencies
pip install -r streamlit_requirements.txt

# Test with .env
streamlit run streamlit_app.py
# Check http://localhost:8501
```

### Step 3: Push to GitHub
```bash
git add -A
git commit -m "Configure for Streamlit Cloud deployment"
git push origin main
```

### Step 4: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click **"Create App"**
3. Select your GitHub repo
4. Select `streamlit_app.py` as main file
5. Click **"Deploy"**

Wait 2-3 minutes for deployment.

### Step 5: Add Secrets
1. Once deployed, click **⚙️ Settings**
2. Go to **"Secrets"** tab
3. Add (in TOML format):
   ```toml
   openweather_api_key = "your_actual_api_key_here"
   db_path = "warehouse/duckdb/agri_analytics.db"
   ```
4. Save and wait ~30 seconds for auto-refresh

### Step 6: Verify Deployment
- [ ] App loads at `https://[username]-smart-shamba.streamlit.app`
- [ ] All pages load without errors
- [ ] Data displays correctly
- [ ] No error messages in browser console
- [ ] Check logs in Streamlit Cloud dashboard for warnings

---

## 🔄 After Deployment

### Regular Updates
```bash
# Make changes locally
# Test: streamlit run streamlit_app.py
# Commit and push
git add -A
git commit -m "Update description"
git push origin main
# Streamlit Cloud auto-deploys in 1-2 minutes
```

### Refresh Data
```bash
# Run local data pipelines
python setup_project.py
python mage_load_weather.py
python mage_load_prices.py
python mage_load_vegetation.py

# Commit and push
git add warehouse/duckdb/agri_analytics.db
git commit -m "Update data: $(date +%Y-%m-%d)"
git push origin main
# App redeploys with new data
```

### Monitor
- Check Streamlit Cloud dashboard regularly
- Review app logs for errors
- Monitor resource usage
- Get user feedback

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Module not found"** | Check `streamlit_requirements.txt` file name and packages |
| **"Database not found"** | Commit: `git add warehouse/duckdb/agri_analytics.db` |
| **"Secrets not working"** | Verify TOML syntax in Secrets dashboard, hard refresh browser |
| **App crashes** | Check Streamlit Cloud logs, test locally first |
| **Slow performance** | Add `@st.cache_data` decorators, optimize queries |
| **Too large deployment** | Reduce database size, consider cloud database instead |

---

## 📋 Files Reference

| File | Purpose | Commit? |
|------|---------|---------|
| `streamlit_app.py` | Main app | Yes |
| `streamlit_requirements.txt` | Dependencies | Yes |
| `.streamlit/config.toml` | Settings | Yes |
| `.streamlit/secrets.toml` | Template (empty values) | Yes |
| `.env` | Local secrets | **NO** (.gitignore) |
| `.env.template` | Template | Yes |
| `warehouse/duckdb/agri_analytics.db` | Database | Yes |
| `.gitignore` | Git ignore rules | Yes |
| `verify_deployment.py` | Verification script | Yes |
| `DEPLOYMENT.md` | Full guide | Yes |
| `DEPLOYMENT_QUICK_START.md` | Quick reference | Yes |

---

## 🔐 Security Reminders

1. **Never commit `.env`** - It's in `.gitignore` for a reason
2. **Never commit actual secrets** - Use Streamlit Cloud dashboard
3. **Rotate API keys** - Every 3-6 months
4. **Review .gitignore** - Make sure sensitive files are listed
5. **Use read-only database** - Prevent accidental writes from cloud app
6. **Monitor logs** - Watch for unusual activity

---

## ✨ Success Criteria

Your deployment is successful when:
- ✅ App accessible at public URL
- ✅ All pages load without errors
- ✅ Data displays correctly
- ✅ Interactive elements work
- ✅ No sensitive data in logs
- ✅ Performance is acceptable
- ✅ Can update via git push

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Cloud Deployment**: https://docs.streamlit.io/deploy/streamlit-cloud
- **Troubleshooting**: https://docs.streamlit.io/streamlit-cloud/troubleshooting
- **GitHub Issues**: Check your repo's issues
- **Community**: https://discuss.streamlit.io

---

## 🎯 Quick Command Reference

```bash
# Verify setup
python verify_deployment.py

# Test locally
streamlit run streamlit_app.py

# Deploy
git add -A && git commit -m "msg" && git push origin main

# Check git
git status
git log --oneline | head -5

# File checks
ls -la .streamlit/
ls -lh warehouse/duckdb/agri_analytics.db
cat streamlit_requirements.txt
```

---

**Last Updated**: January 30, 2026  
**Status**: Ready for Production  
**Version**: 1.0
