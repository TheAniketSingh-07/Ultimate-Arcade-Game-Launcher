#!/usr/bin/env python3
"""
GitHub Upload Script - Upload Ultimate Arcade Game Launcher
Prepares and uploads the complete launcher package to GitHub
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error: {e.stderr}")
        return None

def check_git_installed():
    """Check if git is installed"""
    result = run_command("git --version", "Checking Git installation")
    return result is not None

def initialize_repository():
    """Initialize git repository and prepare for upload"""
    print("🚀 Preparing Ultimate Arcade Game Launcher for GitHub...")
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first:")
        print("   - Windows: https://git-scm.com/download/win")
        print("   - Mac: brew install git")
        print("   - Linux: sudo apt install git")
        return False
    
    # Initialize git repository
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
    
    # Configure git (if not already configured)
    run_command('git config user.name "Ultimate Launcher Creator"', "Setting Git username")
    run_command('git config user.email "launcher@example.com"', "Setting Git email")
    
    # Add all files
    run_command("git add .", "Adding all files to Git")
    
    # Create initial commit
    commit_message = "🎮 Initial upload - Ultimate Arcade Game Launcher with 6 games\n\nFeatures:\n- Ultra-smooth 120 FPS performance\n- Zero lag gaming experience\n- 6 amazing arcade games\n- Perfect 3-games-in-a-row design\n- Single-click game launching\n- Professional UI design"
    
    run_command(f'git commit -m "{commit_message}"', "Creating initial commit")
    
    return True

def create_repository_info():
    """Create repository information file"""
    repo_info = """# 🎮 Repository Information

## 📍 **Repository Details**

**Name**: Ultimate-Arcade-Game-Launcher
**Description**: Ultra-smooth arcade game launcher with 6 games - Zero lag, 120 FPS performance
**Type**: Public Repository
**License**: MIT License

## 🚀 **Quick Start for Users**

### **Download and Run**
1. Download ZIP from GitHub
2. Extract files
3. Run: `python3 ULTIMATE_LAUNCHER.py`
4. Enjoy ultra-smooth gaming!

### **Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/Ultimate-Arcade-Game-Launcher.git
cd Ultimate-Arcade-Game-Launcher
python3 ULTIMATE_LAUNCHER.py
```

## 🎯 **What's Included**

- ✅ Ultra-smooth 120 FPS launcher
- ✅ 6 amazing arcade games
- ✅ Zero lag performance
- ✅ Professional UI design
- ✅ Complete documentation
- ✅ Cross-platform compatibility

## 🌟 **Features**

- **🦕 Dino Run** - Ultra-smooth endless runner
- **🚀 Fighter Shoot** - Epic space combat
- **🥷 Gravity Ninja** - Gravity-flipping platformer
- **🧩 Maze Explorer** - Smooth maze navigation
- **🐍 Snake Classic** - Classic snake perfected
- **⭕ Tic Tac Toe** - Strategic AI opponent

---

**Your ultimate arcade gaming experience awaits! 🎮✨**
"""
    
    with open("REPOSITORY_INFO.md", "w") as f:
        f.write(repo_info)
    
    print("✅ Created repository information file")

def show_upload_instructions():
    """Show instructions for uploading to GitHub"""
    print("\n" + "="*80)
    print("🎮 GITHUB UPLOAD INSTRUCTIONS")
    print("="*80)
    
    print("\n🚀 **METHOD 1: GitHub Web Interface (Recommended)**")
    print("1. Go to: https://github.com")
    print("2. Sign in to your account")
    print("3. Click 'New Repository'")
    print("4. Repository name: Ultimate-Arcade-Game-Launcher")
    print("5. Description: Ultra-smooth arcade game launcher with 6 games - Zero lag, 120 FPS performance")
    print("6. Make it Public ✅")
    print("7. DON'T add README or .gitignore (we have them)")
    print("8. Click 'Create repository'")
    print("9. Click 'uploading an existing file'")
    print("10. Drag and drop ALL files from this folder")
    print("11. Commit message: 'Initial upload - Ultimate Arcade Game Launcher'")
    print("12. Click 'Commit changes'")
    
    print("\n🔗 **METHOD 2: Git Commands (Advanced)**")
    print("After creating empty repository on GitHub:")
    print("git remote add origin https://github.com/YOUR_USERNAME/Ultimate-Arcade-Game-Launcher.git")
    print("git branch -M main")
    print("git push -u origin main")
    
    print("\n🎯 **Your Repository Links Will Be:**")
    print("Repository: https://github.com/YOUR_USERNAME/Ultimate-Arcade-Game-Launcher")
    print("Download: https://github.com/YOUR_USERNAME/Ultimate-Arcade-Game-Launcher/archive/refs/heads/main.zip")
    print("Clone: git clone https://github.com/YOUR_USERNAME/Ultimate-Arcade-Game-Launcher.git")
    
    print("\n✨ **Replace YOUR_USERNAME with your actual GitHub username!**")

def create_quick_start_script():
    """Create a quick start script for users"""
    quick_start = """#!/usr/bin/env python3
\"\"\"
Quick Start Script for Ultimate Arcade Game Launcher
Downloads and runs the launcher automatically
\"\"\"

import subprocess
import sys
import os

def install_pygame():
    \"\"\"Install pygame if not available\"\"\"
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
    \"\"\"Main function\"\"\"
    print("🎮" + "="*60 + "🎮")
    print("    ULTIMATE ARCADE GAME LAUNCHER - QUICK START")
    print("🎮" + "="*60 + "🎮")
    
    print("\\n🚀 Preparing your gaming experience...")
    
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
"""
    
    with open("QUICK_START.py", "w") as f:
        f.write(quick_start)
    
    print("✅ Created quick start script for users")

def main():
    """Main function"""
    print("🎮" + "="*80 + "🎮")
    print("              GITHUB UPLOAD PREPARATION")
    print("         Ultimate Arcade Game Launcher")
    print("🎮" + "="*80 + "🎮")
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Create additional files
    create_repository_info()
    create_quick_start_script()
    
    # Initialize repository
    if initialize_repository():
        print("\n✅ Repository prepared successfully!")
    else:
        print("\n❌ Repository preparation failed")
        return
    
    # Show upload instructions
    show_upload_instructions()
    
    print("\n" + "="*80)
    print("🎉 READY FOR GITHUB UPLOAD!")
    print("="*80)
    print("Your Ultimate Arcade Game Launcher is ready to be uploaded to GitHub!")
    print("Follow the instructions above to make it available to the world!")
    print("🎮✨ Happy Gaming! ✨🎮")

if __name__ == "__main__":
    main()
