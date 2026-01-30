#!/usr/bin/env python3
"""
Pre-deployment Verification Script
===================================
Verifies all required files and configurations for Streamlit Cloud deployment.

Usage: python verify_deployment.py
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

PROJECT_ROOT = Path(__file__).parent

def check_file_exists(filepath, critical=True):
    """Check if a file exists."""
    exists = filepath.exists()
    status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
    criticality = "CRITICAL" if critical else "Optional"
    print(f"{status} {filepath.relative_to(PROJECT_ROOT)} ({criticality})")
    return exists

def check_content(filepath, search_text):
    """Check if file contains specific text."""
    if not filepath.exists():
        return False
    with open(filepath) as f:
        return search_text in f.read()

def main():
    print(f"\n{BOLD}Smart-Shamba Streamlit Cloud Deployment Verification{RESET}\n")
    
    all_good = True
    
    # Critical files
    print(f"{BOLD}Critical Files:{RESET}")
    critical_files = [
        PROJECT_ROOT / "streamlit_app.py",
        PROJECT_ROOT / "streamlit_requirements.txt",
        PROJECT_ROOT / ".streamlit" / "config.toml",
        PROJECT_ROOT / "warehouse" / "duckdb" / "agri_analytics.db",
        PROJECT_ROOT / ".env.template",
    ]
    
    for f in critical_files:
        if not check_file_exists(f, critical=True):
            all_good = False
    
    # Optional but recommended
    print(f"\n{BOLD}Recommended Files:{RESET}")
    optional_files = [
        PROJECT_ROOT / ".streamlit" / "secrets.toml",
        PROJECT_ROOT / "DEPLOYMENT.md",
        PROJECT_ROOT / "DEPLOYMENT_QUICK_START.md",
    ]
    
    for f in optional_files:
        check_file_exists(f, critical=False)
    
    # Check content
    print(f"\n{BOLD}Configuration Checks:{RESET}")
    
    # Check .gitignore
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if check_content(gitignore_path, ".env"):
        print(f"{GREEN}✓{RESET} .env is in .gitignore")
    else:
        print(f"{RED}✗{RESET} .env NOT in .gitignore (SECURITY RISK!)")
        all_good = False
    
    # Check streamlit_app.py uses secrets
    app_path = PROJECT_ROOT / "streamlit_app.py"
    if check_content(app_path, "st.secrets"):
        print(f"{GREEN}✓{RESET} streamlit_app.py uses st.secrets")
    else:
        print(f"{YELLOW}⚠{RESET} streamlit_app.py doesn't use st.secrets (consider updating)")
    
    # Check requirements files
    reqs_path = PROJECT_ROOT / "streamlit_requirements.txt"
    if reqs_path.exists():
        with open(reqs_path) as f:
            content = f.read()
            has_streamlit = "streamlit" in content
            has_duckdb = "duckdb" in content
            
        if has_streamlit and has_duckdb:
            print(f"{GREEN}✓{RESET} streamlit_requirements.txt has core dependencies")
        else:
            print(f"{RED}✗{RESET} streamlit_requirements.txt missing dependencies")
            all_good = False
    
    # Summary
    print(f"\n{BOLD}Deployment Summary:{RESET}")
    if all_good:
        print(f"{GREEN}✓ All critical checks passed!{RESET}")
        print(f"{BOLD}Next steps:{RESET}")
        print("1. Commit all changes: git add -A && git commit -m 'Prepare for deployment'")
        print("2. Push to GitHub: git push origin main")
        print("3. Go to https://share.streamlit.io and deploy")
        print("4. Add secrets in Streamlit Cloud dashboard")
        return 0
    else:
        print(f"{RED}✗ Some critical checks failed. Fix issues above before deploying.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
