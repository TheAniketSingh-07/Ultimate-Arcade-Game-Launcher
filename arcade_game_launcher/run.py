#!/usr/bin/env python3
"""
Quick run script for the arcade games
"""

import sys
import os

def main():
    print("🎮 ARCADE GAME LAUNCHER")
    print("=" * 30)
    print("1. 🚀 Launch Game Launcher")
    print("2. 🦕 Run Dino Run Directly")
    print("3. 🐍 Run Snake Game Directly")
    print("4. 🧪 Run Tests")
    print("5. ❌ Exit")
    print("=" * 30)
    
    while True:
        try:
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                print("🚀 Starting Game Launcher...")
                os.system("python3 launcher.py")
                break
            elif choice == '2':
                print("🦕 Starting Dino Run...")
                os.system("python3 games/dino_run/main.py")
                break
            elif choice == '3':
                print("🐍 Starting Snake Game...")
                os.system("python3 games/snake_game/snake_game.py")
                break
            elif choice == '4':
                print("🧪 Running Tests...")
                os.system("python3 test_game.py")
                break
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
