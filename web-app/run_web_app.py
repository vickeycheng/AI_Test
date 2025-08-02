#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fancy TODO Web Application Launcher
Run this script to start the beautiful web interface for your TODO app!
"""

import subprocess
import sys
import os

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
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Flask. Please install manually:")
        print("   pip install flask")
        return False

def main():
    print("🚀 Starting Vickey's Fancy TODO Web Application...")
    print("=" * 60)
    
    # Check Flask installation
    if not check_flask_installed():
        print("⚠️  Flask not found. Installing...")
        if not install_flask():
            sys.exit(1)
    
    # Start the web application
    try:
        print("🌟 Features of your Fancy UI:")
        print("   • Beautiful glass-morphism design")
        print("   • Real-time task statistics")
        print("   • Smooth animations and transitions")
        print("   • Mobile-responsive layout")
        print("   • Toast notifications")
        print("   • One-click task completion")
        print("   • Bulk task operations")
        print("")
        print("🌐 Starting web server...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using Vickey's Fancy TODO App!")
        print("💾 Your tasks have been saved automatically.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Make sure all files are in place and try again.")

if __name__ == "__main__":
    main()