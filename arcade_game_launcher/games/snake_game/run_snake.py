#!/usr/bin/env python3
"""
Quick launcher for Snake Game
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🐍 SNAKE GAME LAUNCHER")
    print("=" * 25)
    print("Starting Snake Game...")
    print("Use arrow keys to move, P to pause, ESC to quit")
    print("=" * 25)
    
    try:
        from snake_game import main as snake_main
        snake_main()
    except ImportError as e:
        print(f"Error importing snake game: {e}")
        print("Make sure pygame is installed: pip install pygame")
    except Exception as e:
        print(f"Error running snake game: {e}")

if __name__ == "__main__":
    main()
