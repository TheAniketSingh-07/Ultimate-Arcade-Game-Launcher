#!/usr/bin/env python3
"""
START LAUNCHER - Main Directory
Quick start script for the Ultimate Arcade Game Launcher
"""

import sys
import os

def main():
    """Start the ultimate launcher"""
    print("🎮" + "=" * 70 + "🎮")
    print("              ULTIMATE ARCADE GAME LAUNCHER")
    print("        Complete Package • Ultra-Smooth • Zero Lag")
    print("🎮" + "=" * 70 + "🎮")
    
    print("\n🚀 Starting Ultimate Gaming Experience...")
    print("✨ Features:")
    print("   • Ultra-smooth 120 FPS performance")
    print("   • Zero lag elimination")
    print("   • Perfect 3-games-in-a-row layout")
    print("   • Single-click game launching")
    print("   • All 6 games optimized")
    print("   • Professional UI design")
    
    try:
        # Import and run the ultimate launcher
        from ULTIMATE_LAUNCHER import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure ULTIMATE_LAUNCHER.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
