#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web TODO Application Launcher
Run this script to start the beautiful web interface
"""

import os
import sys
import subprocess

def check_flask_installed():
    """Check if Flask is installed"""
    try:
        import flask
        return True
    except ImportError:
        return False

def install_flask():
    """Install Flask if not present"""
    print("📦 Installing Flask...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "flask"])
        print("✅ Flask installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Flask. Please install manually:")
        print("   python3 -m pip install --user flask")
        return False

if __name__ == "__main__":
    print("🚀 Starting Web TODO Application...")
    print("🌐 Beautiful web interface with light gray theme")
    print("📱 Mobile responsive design")
    print("💾 Shared data with CLI interface")
    print("=" * 50)
    
    # Check Flask installation
    if not check_flask_installed():
        print("⚠️  Flask not found. Installing...")
        if not install_flask():
            sys.exit(1)
    
    # Import and run the web app
    from todo_web import app
    app.run(debug=True, host='0.0.0.0', port=5000)