#!/usr/bin/env python3
"""
Quick Start Script for Optimized Game Launcher
Handles dependencies and launches the optimized launcher
"""

import sys
import os
import subprocess
import importlib.util

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_pygame():
    """Install pygame if not available"""
    print("Installing pygame...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        return True
    except subprocess.CalledProcessError:
        print("Failed to install pygame. Please install manually:")
        print("pip install pygame")
        return False

def main():
    """Main startup function"""
    print("🎮 Starting Optimized Game Launcher...")
    
    # Check pygame
    if not check_pygame():
        print("Pygame not found. Installing...")
        if not install_pygame():
            sys.exit(1)
    
    # Change to launcher directory
    launcher_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(launcher_dir)
    
    # Launch the optimized launcher
    try:
        from optimized_launcher import main as launcher_main
        launcher_main()
    except ImportError as e:
        print(f"Failed to import launcher: {e}")
        print("Make sure optimized_launcher.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"Launcher error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
