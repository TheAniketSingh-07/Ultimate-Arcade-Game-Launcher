#!/usr/bin/env python3
"""
Obstacle Class Demonstration
Shows how to use the new pygame.sprite.Sprite based obstacle system
"""

import pygame
import sys
import os

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

from games.dino_run.sprites import Obstacle, Cactus, Bird, DinoSprite, ObstacleGroup
from games.dino_run.themes import ThemeManager
from games.dino_run.sprite_customizer import SpriteCustomizer
from games.dino_run.settings import *

class ObstacleDemo:
    """Demonstration of the obstacle class system"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 Obstacle Class Demo")
        self.clock = pygame.time.Clock()
        
        # Theme and customization
        self.theme_manager = ThemeManager()
        self.sprite_customizer = SpriteCustomizer(self.theme_manager)
        self.theme_manager.set_theme('dark')
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = ObstacleGroup(self.theme_manager, self.sprite_customizer)
        
        # Create demo sprites
        self.create_demo_sprites()
        
        # Demo variables
        self.current_style = "geometric"
        self.demo_speed = 3
        
    def create_demo_sprites(self):
        """Create demonstration sprites"""
        # Create various obstacles
        cactus1 = Cactus(200, self.theme_manager, self.sprite_customizer, "geometric")
        cactus2 = Cactus(400, self.theme_manager, self.sprite_customizer, "pixel_art")
        cactus3 = Cactus(600, self.theme_manager, self.sprite_customizer, "neon")
        
        bird1 = Bird(300, self.theme_manager, self.sprite_customizer, "geometric")
        bird2 = Bird(500, self.theme_manager, self.sprite_customizer, "pixel_art")
        bird3 = Bird(700, self.theme_manager, self.sprite_customizer, "neon")
        
        # Set speeds
        for obstacle in [cactus1, cactus2, cactus3, bird1, bird2, bird3]:
            obstacle.set_speed(self.demo_speed)
            
        # Add to groups
        self.obstacles.add(cactus1, cactus2, cactus3, bird1, bird2, bird3)
        self.all_sprites.add(cactus1, cactus2, cactus3, bird1, bird2, bird3)
        
        # Create dino sprite
        self.dino = DinoSprite(50, GROUND_Y - DINO_HEIGHT, self.theme_manager, self.sprite_customizer)
        self.all_sprites.add(self.dino)
        
    def handle_events(self):
        """Handle demo events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.dino.jump()
                elif event.key == pygame.K_DOWN:
                    self.dino.duck()
                elif event.key == pygame.K_t:
                    self.cycle_theme()
                elif event.key == pygame.K_s:
                    self.cycle_style()
                elif event.key == pygame.K_r:
                    self.reset_demo()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.dino.stop_duck()
                    
        return True
        
    def cycle_theme(self):
        """Cycle through themes"""
        themes = self.theme_manager.list_themes()
        current_index = themes.index(self.theme_manager.current_theme.name.lower())
        next_index = (current_index + 1) % len(themes)
        self.theme_manager.set_theme(themes[next_index])
        
        # Update all sprites
        for sprite in self.all_sprites:
            if hasattr(sprite, 'update_image'):
                sprite.update_image()
                
    def cycle_style(self):
        """Cycle through sprite styles"""
        styles = ["default", "geometric", "pixel_art", "neon"]
        current_index = styles.index(self.current_style)
        next_index = (current_index + 1) % len(styles)
        self.current_style = styles[next_index]
        
        # Update all sprites
        self.obstacles.update_style(self.current_style)
        self.dino.set_style(self.current_style)
        
    def reset_demo(self):
        """Reset demonstration"""
        # Clear all sprites
        self.all_sprites.empty()
        self.obstacles.empty()
        
        # Recreate sprites
        self.create_demo_sprites()
        
    def update(self):
        """Update demo"""
        # Update all sprites
        self.all_sprites.update()
        
        # Respawn obstacles that go off screen
        for obstacle in self.obstacles.sprites():
            if obstacle.is_off_screen():
                obstacle.rect.x = SCREEN_WIDTH + 100
                
        # Check collisions
        collisions = pygame.sprite.spritecollide(self.dino, self.obstacles, False)
        if collisions:
            print("💥 Collision detected!")
            
    def draw(self):
        """Draw demo"""
        # Background
        bg_color = self.theme_manager.get_color('background')
        self.screen.fill(bg_color)
        
        # Background effects
        self.theme_manager.draw_background_effects(self.screen)
        
        # Ground line
        ground_color = self.theme_manager.get_sprite_color('ground_line')
        pygame.draw.line(self.screen, ground_color, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
        
        # Draw all sprites
        for sprite in self.all_sprites:
            if self.theme_manager.has_effect('glow'):
                self.theme_manager.apply_glow_effect(self.screen, sprite.image, sprite.rect.topleft)
            else:
                self.screen.blit(sprite.image, sprite.rect)
                
        # Draw info
        self.draw_info()
        
    def draw_info(self):
        """Draw demonstration info"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        text_color = self.theme_manager.get_color('text')
        
        # Title
        title = font.render("🎮 Obstacle Class Demo", True, text_color)
        self.screen.blit(title, (20, 20))
        
        # Instructions
        instructions = [
            "SPACE - Dino Jump",
            "DOWN - Dino Duck", 
            "T - Cycle Themes",
            "S - Cycle Styles",
            "R - Reset Demo",
            "ESC - Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, text_color)
            self.screen.blit(text, (20, 70 + i * 25))
            
        # Current settings
        theme_text = small_font.render(f"Theme: {self.theme_manager.current_theme.name}", True, text_color)
        style_text = small_font.render(f"Style: {self.current_style}", True, text_color)
        
        self.screen.blit(theme_text, (SCREEN_WIDTH - 200, 20))
        self.screen.blit(style_text, (SCREEN_WIDTH - 200, 45))
        
        # Obstacle info
        info_y = 250
        obstacle_info = small_font.render("Obstacle Classes:", True, text_color)
        self.screen.blit(obstacle_info, (20, info_y))
        
        class_info = [
            "• Cactus(pygame.sprite.Sprite)",
            "• Bird(pygame.sprite.Sprite)", 
            "• DinoSprite(pygame.sprite.Sprite)",
            "• ObstacleGroup(pygame.sprite.Group)"
        ]
        
        for i, info in enumerate(class_info):
            text = small_font.render(info, True, text_color)
            self.screen.blit(text, (40, info_y + 30 + i * 20))
            
    def run(self):
        """Run the demonstration"""
        print("🎮 Starting Obstacle Class Demo...")
        print("Controls:")
        print("  SPACE - Dino Jump")
        print("  DOWN - Dino Duck")
        print("  T - Cycle Themes")
        print("  S - Cycle Styles")
        print("  R - Reset Demo")
        print("  ESC - Exit")
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()

def main():
    """Main function"""
    print("🎮 OBSTACLE CLASS DEMONSTRATION")
    print("=" * 40)
    print("This demo shows the new pygame.sprite.Sprite based obstacle system")
    print()
    
    try:
        demo = ObstacleDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
