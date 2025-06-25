#!/usr/bin/env python3
"""
🚀 Quick Upload Script for Arcade Game Launcher
Helps you upload your project to GitHub with proper authentication
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Failed!")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    print("🎮 Ultimate Arcade Game Launcher - GitHub Upload Helper")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("ULTIMATE_LAUNCHER.py"):
        print("❌ Error: Please run this script from your project directory")
        print("   (The directory containing ULTIMATE_LAUNCHER.py)")
        sys.exit(1)
    
    print("✅ Project directory confirmed!")
    
    # Check git status
    print("\n📊 Checking project status...")
    run_command("git status --porcelain", "Checking for uncommitted changes")
    
    # Show what will be uploaded
    print("\n📁 Your project contains:")
    print("   🎮 ULTIMATE_LAUNCHER.py - Main launcher")
    print("   📚 README.md - Professional documentation")
    print("   📂 arcade_game_launcher/ - Complete game package")
    print("      ├── 🦕 dino_run/")
    print("      ├── 🚀 fighter_shoot/")
    print("      ├── 🥷 gravity_flip_ninja/")
    print("      ├── 🧩 maze_game/")
    print("      ├── 🐍 snake_game/")
    print("      └── ⭕ tic_tac_toe/")
    
    # Authentication guide
    print("\n🔐 AUTHENTICATION REQUIRED:")
    print("   GitHub removed password authentication in 2021.")
    print("   You need a Personal Access Token:")
    print()
    print("   1. Go to: https://github.com/settings/tokens")
    print("   2. Click 'Generate new token (classic)'")
    print("   3. Select 'repo' scope")
    print("   4. Copy the generated token")
    print()
    print("   When prompted for password, use your TOKEN instead!")
    
    # Ask user if ready
    response = input("\n❓ Do you have your Personal Access Token ready? (y/n): ").lower()
    
    if response != 'y':
        print("\n📖 Please get your token first, then run this script again.")
        print("   Guide: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
        sys.exit(0)
    
    # Attempt upload
    print("\n🚀 Attempting to upload to GitHub...")
    print("   Repository: https://github.com/TheAniketSingh-07/Arcade-game-with-Q-CLI")
    print()
    print("   When prompted:")
    print("   Username: TheAniketSingh-07")
    print("   Password: [paste your token here]")
    print()
    
    success = run_command("git push origin main", "Uploading to GitHub")
    
    if success:
        print("\n🎉 SUCCESS! Your Arcade Game Launcher is now on GitHub!")
        print("   🔗 View at: https://github.com/TheAniketSingh-07/Arcade-game-with-Q-CLI")
        print("   📱 Share with: git clone https://github.com/TheAniketSingh-07/Arcade-game-with-Q-CLI.git")
        print("\n✨ Your project is now:")
        print("   ✅ Publicly available")
        print("   ✅ Professionally documented")
        print("   ✅ Ready for contributions")
        print("   ✅ Portfolio-ready!")
    else:
        print("\n❌ Upload failed. Common solutions:")
        print("   1. Check your Personal Access Token")
        print("   2. Make sure token has 'repo' permissions")
        print("   3. Use token as password, not your GitHub password")
        print("   4. Check internet connection")
        print("\n📖 Full guide available in: COMPLETE_GITHUB_UPLOAD_GUIDE.md")

if __name__ == "__main__":
    main()
