#!/usr/bin/env python3
"""
Ultra-Smooth Launcher Startup Script
Starts the ultimate zero-lag gaming experience
"""

import sys
import os

def main():
    """Start the ultra-smooth launcher"""
    print("🎮" + "=" * 70 + "🎮")
    print("              ULTRA-SMOOTH GAME LAUNCHER")
    print("        Zero Micro-Lag • Perfect Smoothness • 120 FPS")
    print("🎮" + "=" * 70 + "🎮")
    
    print("\n🚀 Starting Ultra-Smooth Experience...")
    print("✨ Features:")
    print("   • Zero micro-lag elimination")
    print("   • Ultra-smooth 120 FPS performance")
    print("   • Perfect frame timing")
    print("   • Instant response controls")
    print("   • Thread-based game launching")
    print("   • Hardware acceleration")
    
    try:
        # Import and run the ultra-smooth launcher
        from ultra_smooth_launcher import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure ultra_smooth_launcher.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
