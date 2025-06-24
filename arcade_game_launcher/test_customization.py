#!/usr/bin/env python3
"""
Test Customization Features
Demonstrates all customization options
"""

import os
import sys
import subprocess
import time

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

def test_theme(theme_name):
    """Test a specific theme"""
    print(f"🎨 Testing {theme_name} theme...")
    
    # Apply theme
    cmd = f"echo 'n' | python3 customize.py --theme {theme_name} --style geometric"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {theme_name.title()} theme applied successfully")
        
        # Test game startup
        game_cmd = "timeout 2 python3 games/dino_run/main.py"
        game_result = subprocess.run(game_cmd, shell=True, capture_output=True, text=True)
        
        if "Theme changed to:" in game_result.stdout:
            print(f"✅ {theme_name.title()} theme loaded in game")
            return True
        else:
            print(f"❌ {theme_name.title()} theme failed to load")
            return False
    else:
        print(f"❌ Failed to apply {theme_name} theme")
        return False

def test_sprite_style(style_name):
    """Test a specific sprite style"""
    print(f"✨ Testing {style_name} sprite style...")
    
    # Apply style
    cmd = f"echo 'n' | python3 customize.py --style {style_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {style_name.title()} style applied successfully")
        return True
    else:
        print(f"❌ Failed to apply {style_name} style")
        return False

def main():
    """Run all customization tests"""
    print("🎮 DINO RUN CUSTOMIZATION TESTS")
    print("=" * 50)
    
    # Test themes
    themes = ["light", "dark", "neon"]
    theme_results = []
    
    print("\n🎭 TESTING THEMES:")
    print("-" * 20)
    
    for theme in themes:
        success = test_theme(theme)
        theme_results.append(success)
        time.sleep(1)  # Brief pause between tests
    
    # Test sprite styles
    styles = ["default", "geometric", "pixel_art", "neon"]
    style_results = []
    
    print("\n✨ TESTING SPRITE STYLES:")
    print("-" * 25)
    
    for style in styles:
        success = test_sprite_style(style)
        style_results.append(success)
        time.sleep(0.5)
    
    # Test combination
    print("\n🎨 TESTING COMBINATION:")
    print("-" * 23)
    
    combo_cmd = "echo 'n' | python3 customize.py --theme neon --sprite dino --style neon"
    combo_result = subprocess.run(combo_cmd, shell=True, capture_output=True, text=True)
    combo_success = combo_result.returncode == 0
    
    if combo_success:
        print("✅ Combination customization successful")
    else:
        print("❌ Combination customization failed")
    
    # Results summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    print(f"\n🎭 Themes: {sum(theme_results)}/{len(themes)} passed")
    for i, theme in enumerate(themes):
        status = "✅" if theme_results[i] else "❌"
        print(f"   {status} {theme.title()}")
    
    print(f"\n✨ Styles: {sum(style_results)}/{len(styles)} passed")
    for i, style in enumerate(styles):
        status = "✅" if style_results[i] else "❌"
        print(f"   {status} {style.title()}")
    
    print(f"\n🎨 Combination: {'✅ Passed' if combo_success else '❌ Failed'}")
    
    total_tests = len(themes) + len(styles) + 1
    total_passed = sum(theme_results) + sum(style_results) + (1 if combo_success else 0)
    
    print(f"\n🏆 OVERALL: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL CUSTOMIZATION FEATURES WORKING!")
        print("\n🎮 Available commands:")
        print("   python3 customize.py --theme dark --sprite dino --style geometric")
        print("   python3 customize.py --theme neon --style neon")
        print("   python3 customize.py --show-options")
        print("\n🚀 In-game controls:")
        print("   T - Cycle themes")
        print("   S - Cycle sprite styles")
    else:
        print(f"\n⚠️  {total_tests - total_passed} tests failed")
    
    return total_passed == total_tests

if __name__ == "__main__":
    main()
