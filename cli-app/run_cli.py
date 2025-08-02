#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI TODO Application Launcher
Run this script to start the command-line interface
"""

import os
import sys

if __name__ == "__main__":
    print("🚀 Starting CLI TODO Application...")
    print("📝 Command-line interface with Chinese menus")
    print("💾 Shared data with web interface")
    print("=" * 50)
    
    # Import and run the CLI app
    from todo_cli import main
    main()