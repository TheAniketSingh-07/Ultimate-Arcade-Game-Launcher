#!/usr/bin/env python3
"""
Quick launcher for Advanced Game Launcher
"""

import sys
import os

def main():
    print("🎮 ADVANCED GAME LAUNCHER - ULTIMATE EDITION")
    print("=" * 50)
    print("🚀 Starting Beautiful Game Launcher...")
    print("✨ Features:")
    print("   • Visual game cards with hover effects")
    print("   • Smooth animations and particle backgrounds")
    print("   • Game statistics and information")
    print("   • Mouse and keyboard navigation")
    print("   • Modern UI with beautiful graphics")
    print("=" * 50)
    
    try:
        from advanced_launcher import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"❌ Error importing advanced launcher: {e}")
        print("💡 Make sure pygame is installed: pip install pygame")
    except Exception as e:
        print(f"❌ Error running advanced launcher: {e}")
        print("💡 Check that all launcher files are present")

if __name__ == "__main__":
    main()
