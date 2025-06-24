#!/usr/bin/env python3
"""
Quick run script for the arcade games
"""

import sys
import os

def main():
    print("🎮 ARCADE GAME LAUNCHER")
    print("=" * 35)
    print("1. 🚀 Launch Advanced Game Launcher (NEW!)")
    print("2. 📋 Launch Classic Game Launcher")
    print("3. 🦕 Run Dino Run Directly")
    print("4. 🐍 Run Snake Game Directly")
    print("5. 🥷 Run Gravity Flip Ninja Directly")
    print("6. 🧪 Run Tests")
    print("7. ❌ Exit")
    print("=" * 35)
    
    while True:
        try:
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                print("🚀 Starting Advanced Game Launcher...")
                print("✨ Features: Beautiful UI, Game Cards, Visual Previews")
                os.system("python3 advanced_launcher.py")
                break
            elif choice == '2':
                print("📋 Starting Classic Game Launcher...")
                os.system("python3 launcher.py")
                break
            elif choice == '3':
                print("🦕 Starting Dino Run...")
                os.system("python3 games/dino_run/main.py")
                break
            elif choice == '4':
                print("🐍 Starting Snake Game...")
                os.system("python3 games/snake_game/snake_game.py")
                break
            elif choice == '5':
                print("🥷 Starting Gravity Flip Ninja...")
                os.system("python3 games/gravity_flip_ninja/gravity_flip_ninja.py")
                break
            elif choice == '6':
                print("🧪 Running Tests...")
                os.system("python3 test_game.py")
                break
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
