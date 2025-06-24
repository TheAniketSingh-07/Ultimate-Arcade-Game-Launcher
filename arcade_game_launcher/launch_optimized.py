#!/usr/bin/env python3
"""
Ultimate Game Launcher - Optimized Edition
Complete launcher with automatic optimization and error handling
"""

import sys
import os
import subprocess
import time

def print_banner():
    """Print startup banner"""
    print("🎮" + "=" * 60 + "🎮")
    print("    OPTIMIZED ARCADE GAME LAUNCHER")
    print("    High Performance • Lag-Free • Smooth")
    print("🎮" + "=" * 60 + "🎮")

def check_dependencies():
    """Check and install required dependencies"""
    dependencies = ["pygame"]
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} is available")
        except ImportError:
            missing.append(dep)
            print(f"❌ {dep} is missing")
    
    if missing:
        print(f"\n📦 Installing missing dependencies: {', '.join(missing)}")
        for dep in missing:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ {dep} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {dep}")
                return False
    
    return True

def run_performance_check():
    """Run performance optimization if available"""
    try:
        print("\n🔧 Running performance optimization...")
        from performance_optimizer import PerformanceOptimizer
        optimizer = PerformanceOptimizer()
        
        # Quick optimization without full output
        config = optimizer.load_config()
        optimized_config = optimizer.optimize_config(config)
        
        if config != optimized_config:
            optimizer.save_config(optimized_config)
            print("✅ Performance optimizations applied")
        else:
            print("✅ Performance is already optimized")
            
    except ImportError:
        print("⚠️  Performance optimizer not available (psutil missing)")
    except Exception as e:
        print(f"⚠️  Performance check failed: {e}")

def launch_game_launcher():
    """Launch the optimized game launcher"""
    try:
        print("\n🚀 Starting Optimized Game Launcher...")
        
        # Change to launcher directory
        launcher_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(launcher_dir)
        
        # Import and run launcher
        from optimized_launcher import OptimizedGameLauncher
        launcher = OptimizedGameLauncher()
        launcher.run()
        
    except ImportError as e:
        print(f"❌ Failed to import launcher: {e}")
        print("Make sure optimized_launcher.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        return False
    
    return True

def main():
    """Main launch function"""
    print_banner()
    
    # Step 1: Check dependencies
    print("\n📋 Checking dependencies...")
    if not check_dependencies():
        print("❌ Dependency check failed. Please install manually.")
        input("Press Enter to exit...")
        return
    
    # Step 2: Performance optimization
    run_performance_check()
    
    # Step 3: Launch the game launcher
    print("\n" + "=" * 60)
    success = launch_game_launcher()
    
    if not success:
        print("\n❌ Failed to start launcher")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Python 3.7+ is installed")
        print("2. Install pygame: pip install pygame")
        print("3. Run from the correct directory")
        print("4. Check file permissions")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
