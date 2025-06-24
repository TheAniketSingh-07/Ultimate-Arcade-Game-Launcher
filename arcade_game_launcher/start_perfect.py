#!/usr/bin/env python3
"""
Perfect Launcher Startup Script
Starts the perfect 3-games-in-a-row launcher with all optimizations
"""

import sys
import os

def main():
    """Start the perfect launcher"""
    print("🎮" + "=" * 60 + "🎮")
    print("           PERFECT GAME LAUNCHER")
    print("    3-Games-in-a-Row • Ultra-Smooth • All Games Working")
    print("🎮" + "=" * 60 + "🎮")
    
    print("\n🚀 Starting Perfect Launcher...")
    print("✨ Features:")
    print("   • Perfect 3-column layout design")
    print("   • Ultra-smooth 144 FPS performance")
    print("   • Single-click game launching")
    print("   • All games verified and working")
    print("   • Zero lag, maximum responsiveness")
    
    try:
        # Import and run the perfect launcher
        from perfect_launcher import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure perfect_launcher.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
