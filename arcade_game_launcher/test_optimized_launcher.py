#!/usr/bin/env python3
"""
Test script for the optimized launcher
Validates functionality without opening the full GUI
"""

import sys
import os
import pygame

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from optimized_launcher import OptimizedGameLauncher, GameData, Theme, PerformanceMonitor
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_pygame_init():
    """Test pygame initialization"""
    try:
        pygame.init()
        print("✅ Pygame initialized successfully")
        pygame.quit()
        return True
    except Exception as e:
        print(f"❌ Pygame init error: {e}")
        return False

def test_game_data():
    """Test GameData creation"""
    try:
        from optimized_launcher import GameData
        game = GameData("Test Game", "test.py", "A test game", "Test", (255, 0, 0), "test.py")
        print(f"✅ GameData created: {game.name}")
        return True
    except Exception as e:
        print(f"❌ GameData error: {e}")
        return False

def test_performance_monitor():
    """Test performance monitoring"""
    try:
        from optimized_launcher import PerformanceMonitor
        monitor = PerformanceMonitor()
        monitor.update()
        fps = monitor.get_fps()
        print(f"✅ Performance monitor working, FPS: {fps}")
        return True
    except Exception as e:
        print(f"❌ Performance monitor error: {e}")
        return False

def test_file_structure():
    """Test if required files exist"""
    required_files = [
        "optimized_launcher.py",
        "start_launcher.py",
        "performance_config.json"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 Testing Optimized Game Launcher")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Pygame Init", test_pygame_init),
        ("GameData", test_game_data),
        ("Performance Monitor", test_performance_monitor)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Launcher is ready to use.")
        print("\n🚀 To start the launcher, run:")
        print("   python3 start_launcher.py")
        print("   or")
        print("   python3 optimized_launcher.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
