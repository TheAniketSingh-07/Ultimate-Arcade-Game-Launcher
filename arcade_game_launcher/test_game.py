#!/usr/bin/env python3
"""
Test script to verify game components work
"""

import os
import sys

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test that all game modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from games.dino_run.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
        print("✅ Settings imported successfully")
        print(f"   Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}, FPS: {FPS}")
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        return False
    
    try:
        from games.dino_run.game_logic import Dino, Cactus, Bird
        print("✅ Game logic imported successfully")
    except Exception as e:
        print(f"❌ Game logic import failed: {e}")
        return False
    
    try:
        from games.dino_run.utils import check_collision, clamp, lerp
        print("✅ Utils imported successfully")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_game_objects():
    """Test game object creation and basic functionality"""
    print("\n🎮 Testing game objects...")
    
    try:
        from games.dino_run.game_logic import Dino, Cactus, Bird
        from games.dino_run.settings import GROUND_Y, DINO_HEIGHT
        
        # Test Dino creation
        dino = Dino(100, GROUND_Y - DINO_HEIGHT)
        print(f"✅ Dino created at position ({dino.x}, {dino.y})")
        
        # Test Dino jump
        dino.jump()
        print(f"✅ Dino jump initiated, velocity: {dino.vel_y}")
        
        # Test obstacle creation
        cactus = Cactus(800)
        bird = Bird(900)
        print(f"✅ Obstacles created - Cactus at {cactus.x}, Bird at {bird.x}")
        
        # Test collision detection
        from games.dino_run.utils import check_collision
        collision = check_collision(dino.get_rect(), cactus.get_rect())
        print(f"✅ Collision detection works: {collision}")
        
        return True
    except Exception as e:
        print(f"❌ Game objects test failed: {e}")
        return False

def test_audio_system():
    """Test audio system initialization"""
    print("\n🔊 Testing audio system...")
    
    try:
        import pygame
        pygame.mixer.init()
        
        from games.dino_run.audio import AudioManager
        audio = AudioManager()
        print("✅ Audio manager created successfully")
        print(f"   Sounds loaded: {list(audio.sounds.keys())}")
        print(f"   Music loaded: {audio.music_loaded}")
        
        return True
    except Exception as e:
        print(f"❌ Audio system test failed: {e}")
        return False

def test_power_ups():
    """Test power-up system"""
    print("\n⚡ Testing power-up system...")
    
    try:
        from games.dino_run.powerups import PowerUpManager, PowerUpType
        from games.dino_run.audio import AudioManager
        
        audio = AudioManager()
        powerup_manager = PowerUpManager(audio)
        
        # Test power-up activation
        powerup_manager.activate_power_up(PowerUpType.SHIELD)
        shield_active = powerup_manager.is_power_up_active(PowerUpType.SHIELD)
        print(f"✅ Power-up system works - Shield active: {shield_active}")
        
        return True
    except Exception as e:
        print(f"❌ Power-up system test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎮 DINO RUN - GAME COMPONENT TESTS")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_game_objects,
        test_audio_system,
        test_power_ups
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"🏆 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The game is ready to run!")
        print("\n🚀 To run the game:")
        print("   python3 games/dino_run/main.py")
        print("\n🎮 Controls:")
        print("   SPACE/UP - Jump")
        print("   DOWN - Duck")
        print("   P - Pause")
        print("   ESC - Menu/Exit")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
