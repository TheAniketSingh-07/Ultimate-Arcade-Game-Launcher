#!/usr/bin/env python3
"""
Demo script to showcase the Advanced Game Launcher features
"""

import sys
import os

def main():
    print("🎮 ADVANCED GAME LAUNCHER DEMO")
    print("=" * 50)
    print()
    print("🌟 FEATURES SHOWCASE:")
    print("   ✨ Beautiful UI with modern design")
    print("   🎨 Visual game cards with hover effects")
    print("   🎮 Complete game collection display")
    print("   📊 Game statistics and information")
    print("   🖱️  Mouse and keyboard navigation")
    print("   💫 Smooth animations and particle effects")
    print()
    print("🎯 YOUR GAME COLLECTION:")
    print("   🐍 Snake Game - Classic arcade fun")
    print("   🥷 Gravity Flip Ninja - Advanced action")
    print("   🦕 Dino Run - Endless runner")
    print("   ⚔️  Fighter Shoot - Combat action")
    print("   🧩 Maze Game - Puzzle challenge")
    print("   ⭕ Tic Tac Toe - Strategy classic")
    print()
    print("🚀 LAUNCHING ADVANCED LAUNCHER...")
    print("=" * 50)
    
    try:
        # Import and run the advanced launcher
        from advanced_launcher import main as launcher_main
        launcher_main()
    except Exception as e:
        print(f"Demo Error: {e}")
        print("💡 Make sure pygame is installed for the full experience!")

if __name__ == "__main__":
    main()
