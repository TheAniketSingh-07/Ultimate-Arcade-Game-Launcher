#!/usr/bin/env python3
"""
🚀 EASY GITHUB UPLOAD SCRIPT
Automated upload for your Ultimate Arcade Game Launcher
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Run a command and show the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS!")
            if result.stdout.strip():
                print(f"📄 Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - FAILED!")
            print(f"🚨 Error: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("🎮 ULTIMATE ARCADE GAME LAUNCHER - GITHUB UPLOAD")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("ULTIMATE_LAUNCHER.py"):
        print("❌ Error: Please run this script from your project directory!")
        print("📁 Expected file: ULTIMATE_LAUNCHER.py")
        return
    
    print("✅ Project directory confirmed!")
    print("📁 Found: ULTIMATE_LAUNCHER.py")
    
    # Check git status
    print("\n📊 Checking project status...")
    run_command("git status --porcelain", "Git status check")
    
    # Add all files
    if not run_command("git add .", "Adding all files to git"):
        return
    
    # Commit changes
    commit_message = "🎮 Ultimate Arcade Game Launcher - Complete with 6 games"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        print("ℹ️  Note: No new changes to commit (this is normal if already committed)")
    
    # Show what will be uploaded
    print("\n📦 READY TO UPLOAD:")
    print("🎮 6 Complete Games:")
    print("   🦕 Dino Run - Endless runner")
    print("   🚀 Fighter Shoot - Space combat")
    print("   🥷 Gravity Ninja - Platformer")
    print("   🧩 Maze Explorer - Puzzle game")
    print("   🐍 Snake Classic - Classic snake")
    print("   ⭕ Tic Tac Toe - Strategy game")
    print("\n🚀 Ultra-smooth launcher with 120 FPS performance")
    print("📚 Complete documentation and guides")
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("🚀 Ready to upload to GitHub? (y/n): ").lower().strip()
    
    if response != 'y':
        print("❌ Upload cancelled.")
        return
    
    # Push to GitHub
    print("\n🚀 UPLOADING TO GITHUB...")
    print("🔐 You may be prompted for GitHub credentials:")
    print("   📧 Username: Your GitHub username")
    print("   🔑 Password: Your Personal Access Token (NOT your GitHub password)")
    print("\n💡 If you don't have a token, visit:")
    print("   https://github.com/settings/tokens")
    
    if run_command("git push origin main", "Uploading to GitHub"):
        print("\n" + "🎉" * 20)
        print("🎮 SUCCESS! Your Ultimate Arcade Game Launcher is now on GitHub!")
        print("🌐 Repository URL: https://github.com/TheAniketSingh-07/Arcade-game-with-Q-CLI")
        print("✨ Anyone can now clone and play your games!")
        print("🎯 To test: git clone https://github.com/TheAniketSingh-07/Arcade-game-with-Q-CLI.git")
        print("🎮 Then run: python3 ULTIMATE_LAUNCHER.py")
        print("🎉" * 20)
    else:
        print("\n❌ Upload failed. Please check your GitHub credentials.")
        print("💡 Make sure you're using a Personal Access Token as password")

if __name__ == "__main__":
    main()
