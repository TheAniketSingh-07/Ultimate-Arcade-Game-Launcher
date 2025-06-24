#!/usr/bin/env python3
"""
Enhanced Launcher Startup Script
Combines all files and starts the enhanced launcher
"""

import sys
import os

def main():
    """Start the enhanced launcher"""
    print("🎮 Starting Enhanced Game Launcher...")
    print("✨ Features: Keyboard controls, Last game memory, Single-click launch")
    
    try:
        # Import and run the enhanced launcher
        from enhanced_launcher_main import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all launcher files are in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
