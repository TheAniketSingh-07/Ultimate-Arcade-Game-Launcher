yes run #!/usr/bin/env python3
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
    print("3. 🧪 Run Tests")
    print("4. ❌ Exit")
    print("=" * 30)
    
    while True:
        try:
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                print("🚀 Starting Game Launcher...")
                os.system("python3 launcher.py")
                break
            elif choice == '2':
                print("🦕 Starting Dino Run...")
                os.system("python3 games/dino_run/main.py")
                break
            elif choice == '3':
                print("🧪 Running Tests...")
                os.system("python3 test_game.py")
                break
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
