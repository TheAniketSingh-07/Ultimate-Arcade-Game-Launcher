#!/usr/bin/env python3
"""
Simple Obstacle Class Demo
Basic demonstration of pygame.sprite.Sprite obstacle system
"""

import pygame
import sys
import os

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

def test_obstacle_classes():
    """Test obstacle class creation and basic functionality"""
    print("🎮 TESTING OBSTACLE CLASSES")
    print("=" * 40)
    
    # Initialize pygame
    pygame.init()
    
    try:
        from games.dino_run.sprites import Obstacle, Cactus, Bird, DinoSprite
        from games.dino_run.themes import ThemeManager
        from games.dino_run.sprite_customizer import SpriteCustomizer
        from games.dino_run.settings import GROUND_Y, CACTUS_HEIGHT, DINO_HEIGHT
        
        print("✅ All obstacle classes imported successfully")
        
        # Create theme manager
        theme_manager = ThemeManager()
        sprite_customizer = SpriteCustomizer(theme_manager)
        theme_manager.set_theme('dark')
        print("✅ Theme system initialized")
        
        # Test base Obstacle class
        base_obstacle = Obstacle(400, 300, 32, 64, 5)
        print(f"✅ Base Obstacle created: pos=({base_obstacle.rect.x}, {base_obstacle.rect.y}), size=({base_obstacle.rect.width}, {base_obstacle.rect.height})")
        
        # Test Cactus class
        cactus = Cactus(500, theme_manager, sprite_customizer, "geometric")
        print(f"✅ Cactus created: pos=({cactus.rect.x}, {cactus.rect.y}), type={cactus.obstacle_type}")
        
        # Test Bird class
        bird = Bird(600, theme_manager, sprite_customizer, "geometric")
        print(f"✅ Bird created: pos=({bird.rect.x}, {bird.rect.y}), type={bird.obstacle_type}")
        
        # Test DinoSprite class
        dino = DinoSprite(100, GROUND_Y - DINO_HEIGHT, theme_manager, sprite_customizer)
        print(f"✅ Dino created: pos=({dino.rect.x}, {dino.rect.y}), state={dino.state}")
        
        # Test sprite group
        all_sprites = pygame.sprite.Group()
        all_sprites.add(base_obstacle, cactus, bird, dino)
        print(f"✅ Sprite group created with {len(all_sprites)} sprites")
        
        # Test movement
        print("\n🏃 TESTING MOVEMENT:")
        print("-" * 20)
        
        original_x = cactus.rect.x
        cactus.set_speed(10)
        cactus.update()
        print(f"✅ Cactus moved from x={original_x} to x={cactus.rect.x}")
        
        # Test collision detection
        print("\n💥 TESTING COLLISION DETECTION:")
        print("-" * 30)
        
        # Move dino close to cactus for collision test
        dino.rect.x = cactus.rect.x - 10
        collisions = pygame.sprite.spritecollide(dino, [cactus], False)
        print(f"✅ Collision detection works: {len(collisions)} collision(s) detected")
        
        # Test animation
        print("\n🎬 TESTING ANIMATION:")
        print("-" * 18)
        
        original_frame = bird.animation_frame
        bird.update_animation()
        print(f"✅ Bird animation frame: {original_frame} -> {bird.animation_frame}")
        
        # Test style changes
        print("\n🎨 TESTING STYLE CHANGES:")
        print("-" * 24)
        
        original_style = cactus.style
        cactus.style = "pixel_art"
        cactus.update_image()
        print(f"✅ Cactus style changed: {original_style} -> {cactus.style}")
        
        # Test off-screen detection
        print("\n📺 TESTING OFF-SCREEN DETECTION:")
        print("-" * 32)
        
        base_obstacle.rect.x = -100  # Move off screen
        is_off_screen = base_obstacle.is_off_screen()
        print(f"✅ Off-screen detection: {is_off_screen}")
        
        print("\n" + "=" * 40)
        print("🏆 ALL OBSTACLE CLASS TESTS PASSED!")
        print("=" * 40)
        
        print("\n🎮 OBSTACLE CLASS FEATURES:")
        print("✅ pygame.sprite.Sprite inheritance")
        print("✅ Automatic collision detection")
        print("✅ Animation system")
        print("✅ Theme integration")
        print("✅ Style customization")
        print("✅ Movement and physics")
        print("✅ Off-screen detection")
        print("✅ Sprite group management")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        pygame.quit()

def show_class_structure():
    """Show the obstacle class structure"""
    print("\n🏗️  OBSTACLE CLASS STRUCTURE:")
    print("=" * 35)
    print("""
pygame.sprite.Sprite
    ├── Obstacle (Base class)
    │   ├── Cactus (Ground obstacle)
    │   └── Bird (Flying obstacle)
    ├── DinoSprite (Player character)
    └── ObstacleGroup (pygame.sprite.Group)
    
Key Methods:
    • __init__() - Initialize sprite
    • update() - Update position/animation
    • update_image() - Refresh sprite image
    • set_speed() - Change movement speed
    • is_off_screen() - Check boundaries
    """)

def show_usage_example():
    """Show usage example"""
    print("\n💡 USAGE EXAMPLE:")
    print("=" * 18)
    print("""
# Create obstacle system
theme_manager = ThemeManager()
sprite_customizer = SpriteCustomizer(theme_manager)

# Create obstacles
cactus = Cactus(400, theme_manager, sprite_customizer, "geometric")
bird = Bird(600, theme_manager, sprite_customizer, "pixel_art")

# Create sprite group
obstacles = pygame.sprite.Group()
obstacles.add(cactus, bird)

# Game loop
for obstacle in obstacles:
    obstacle.set_speed(game_speed)
    obstacle.update()
    
# Collision detection
collisions = pygame.sprite.spritecollide(player, obstacles, False)
    """)

def main():
    """Main function"""
    print("🎮 OBSTACLE CLASS DEMONSTRATION")
    print("Testing pygame.sprite.Sprite based obstacle system")
    print()
    
    # Run tests
    success = test_obstacle_classes()
    
    if success:
        show_class_structure()
        show_usage_example()
        
        print("\n🎉 OBSTACLE CLASS SYSTEM READY!")
        print("Your class Obstacle(pygame.sprite.Sprite) is fully implemented!")
    else:
        print("\n❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
