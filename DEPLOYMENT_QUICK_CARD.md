# 🚀 Smart-Shamba Deployment - Quick Reference Card

**Print this page and keep it handy!**

---

## ⚡ Quick Deploy (Copy & Paste)

```bash
# 1. Verify (30 seconds)
python3 verify_deployment.py

# 2. Test (2 minutes)
pip install -r streamlit_requirements.txt
streamlit run streamlit_app.py

# 3. Setup (1 minute)
cp .env.template .env
nano .env  # Add your API key

# 4. Deploy (3 minutes)
git add -A
git commit -m "Deploy to Streamlit Cloud"
git push origin main

# 5. On Streamlit Cloud
# Go to https://share.streamlit.io
# Create App → repo → streamlit_app.py → Deploy

# 6. Add Secrets (1 minute)
# Settings → Secrets → Copy this:
# openweather_api_key = "your_actual_key_here"
# db_path = "warehouse/duckdb/agri_analytics.db"
```

---

## 📋 Critical Files to Know

| File | Why | What to Do |
|------|-----|-----------|
| `streamlit_app.py` | Main app | ✓ Already updated |
| `streamlit_requirements.txt` | Dependencies | ✓ Already created |
| `.env` | Local secrets | ⚠️ Create from template |
| `.streamlit/config.toml` | App settings | ✓ Already created |
| `.streamlit/secrets.toml` | Secrets template | ✓ Already created |
| `warehouse/duckdb/agri_analytics.db` | Database | ✓ Commit to git |

---

## 🔑 Essential Commands

```bash
# Verify
python3 verify_deployment.py

# Test locally
streamlit run streamlit_app.py

# Check git status
git status

# Commit everything
git add -A && git commit -m "Deploy to Streamlit Cloud"

# Push to GitHub
git push origin main
```

---

## 🌐 Deployment URLs

| Service | URL |
|---------|-----|
| Streamlit Cloud | https://share.streamlit.io |
| Your App | https://[username]-smart-shamba.streamlit.app |
| GitHub Repo | https://github.com/joetal24/Smart-Shamba |
| API Docs | https://openweathermap.org/api |

---

## 🔐 Security Reminders

✅ **DO**
- Keep `.env` in `.gitignore`
- Add API key to `.env` locally only
- Add secrets via Streamlit dashboard (not files)
- Rotate keys every 6 months

❌ **DON'T**
- Commit `.env` file
- Put API keys in code
- Share API keys in chat/email
- Use same key for dev and prod

---

## 🆘 If Something Goes Wrong

| Error | Fix |
|-------|-----|
| **Module not found** | Check `streamlit_requirements.txt` spelling |
| **Database not found** | Run: `git add warehouse/duckdb/agri_analytics.db && git push` |
| **Secrets error** | Go to Settings → Secrets → Check syntax |
| **App crashes** | Check logs in Streamlit Cloud dashboard |
| **Still stuck?** | Read `DEPLOYMENT_GUIDE.md` for details |

---

## 📞 Getting Help

**Quick Help**:
```bash
python3 verify_deployment.py
```

**Need Details?**:
- Quick: `DEPLOYMENT_QUICK_START.md`
- Guide: `DEPLOYMENT_GUIDE.md`
- Checklist: `DEPLOYMENT_CHECKLIST.md`

---

## 📊 Deployment Checklist

- [ ] Ran `python3 verify_deployment.py` (all ✓)
- [ ] Tested locally: `streamlit run streamlit_app.py`
- [ ] `.env` created from template
- [ ] Added API key to `.env`
- [ ] `.env` NOT in git
- [ ] All changes committed: `git status` is clean
- [ ] Pushed to GitHub: `git push origin main`
- [ ] App deployed on Streamlit Cloud
- [ ] Secrets added to dashboard
- [ ] Live app tested at public URL

---

## 🎯 What You Get

✅ Free hosting (Streamlit Community Cloud)
✅ Live dashboard at public URL
✅ Auto-deploys when you push to GitHub
✅ HTTPS/SSL security
✅ Shareable link for stakeholders

---

## 📈 Next Steps (After Deploying)

1. **Share**: Give the URL to stakeholders
2. **Monitor**: Check logs in Streamlit Cloud
3. **Update**: Push code changes → auto-deploys
4. **Refresh**: Update database → push → auto-deploys
5. **Optimize**: Add caching, optimize queries

---

## 🎓 Documentation Files

| File | Read When |
|------|-----------|
| `DEPLOYMENT_INDEX.md` | Starting out |
| `DEPLOYMENT_GUIDE.md` | First deployment |
| `DEPLOYMENT_QUICK_START.md` | Updating later |
| `DEPLOYMENT_CHECKLIST.md` | Before deploying |
| `DEPLOYMENT.md` | Need details |
| `DEPLOYMENT_SUMMARY.md` | Understanding changes |

---

## 🚀 Go Deploy!

```bash
python3 verify_deployment.py
# Then follow the 6 steps above
```

**Time**: ~15 minutes  
**Result**: Live dashboard for your stakeholders  
**Status**: ✅ Ready to go!

---

**Bookmark this page or save to your notes!**

For more details, open: [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)
