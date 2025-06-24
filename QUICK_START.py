#!/usr/bin/env python3
"""
Quick Start Script for Ultimate Arcade Game Launcher
Downloads and runs the launcher automatically
"""

import subprocess
import sys
import os

def install_pygame():
    """Install pygame if not available"""
    try:
        import pygame
        print("✅ Pygame already installed")
        return True
    except ImportError:
        print("📦 Installing pygame...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("✅ Pygame installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pygame")
            return False

def main():
    """Main function"""
    print("🎮" + "="*60 + "🎮")
    print("    ULTIMATE ARCADE GAME LAUNCHER - QUICK START")
    print("🎮" + "="*60 + "🎮")
    
    print("\n🚀 Preparing your gaming experience...")
    
    # Install pygame if needed
    if not install_pygame():
        print("❌ Cannot proceed without pygame")
        return
    
    # Check if launcher exists
    if os.path.exists("ULTIMATE_LAUNCHER.py"):
        print("✅ Launcher found!")
        print("🎮 Starting Ultimate Arcade Game Launcher...")
        
        # Import and run launcher
        try:
            from ULTIMATE_LAUNCHER import main as launcher_main
            launcher_main()
        except Exception as e:
            print(f"❌ Error starting launcher: {e}")
    else:
        print("❌ ULTIMATE_LAUNCHER.py not found")
        print("Make sure you're in the correct directory")

if __name__ == "__main__":
    main()
