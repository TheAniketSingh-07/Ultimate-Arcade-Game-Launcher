#!/usr/bin/env python3
"""
Quick launcher for Gravity Flip Ninja
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🥷 GRAVITY FLIP NINJA - ULTIMATE EDITION")
    print("=" * 45)
    print("🎮 Starting Advanced Ninja Game...")
    print("✨ Features: Particle Effects, Smooth Animation, Advanced Graphics")
    print("🎯 Controls: SPACE=Jump, G/↑=Flip Gravity, ←→=Move, ESC=Pause")
    print("=" * 45)
    
    try:
        from gravity_flip_ninja import main as ninja_main
        ninja_main()
    except ImportError as e:
        print(f"❌ Error importing ninja game: {e}")
        print("💡 Make sure pygame is installed: pip install pygame")
        print("💡 For best experience: pip install pygame numpy")
    except Exception as e:
        print(f"❌ Error running ninja game: {e}")
        print("💡 Check that all game files are present")

if __name__ == "__main__":
    main()
