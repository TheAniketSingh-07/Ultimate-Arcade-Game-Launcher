"""
Enhanced Dino Run Game Logic with Sprite System
Improved version using pygame.sprite.Sprite classes
"""

import pygame
import random
from enum import Enum
from games.dino_run.settings import *
from games.dino_run.ui import GameUI
from games.dino_run.audio import AudioManager
from games.dino_run.utils import check_collision
from games.dino_run.themes import ThemeManager
from games.dino_run.sprite_customizer import SpriteCustomizer
from games.dino_run.sprites import DinoSprite, ObstacleGroup, Cactus, Bird

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class EnhancedDinoGame:
    """Enhanced game class using sprite system"""
    
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.MENU
        self.clock = pygame.time.Clock()
        
        # Theme and customization system
        self.theme_manager = ThemeManager()
        self.sprite_customizer = SpriteCustomizer(self.theme_manager)
        
        # Apply default customizations from settings
        try:
            from games.dino_run.settings import DEFAULT_THEME, DEFAULT_STYLE
            self.theme_manager.set_theme(DEFAULT_THEME)
            self.sprite_style = DEFAULT_STYLE
        except ImportError:
            # Fallback to defaults
            self.theme_manager.set_theme('dark')
            self.sprite_style = 'geometric'
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = ObstacleGroup(self.theme_manager, self.sprite_customizer)
        
        # Player sprite
        self.dino = DinoSprite(100, GROUND_Y - DINO_HEIGHT, self.theme_manager, self.sprite_customizer)
        self.dino.set_style(self.sprite_style)
        self.all_sprites.add(self.dino)
        
        # Game variables
        self.score = 0
        self.distance = 0
        self.speed = INITIAL_SPEED
        
        # UI and Audio
        self.ui = GameUI(screen, self.theme_manager)
        self.audio = AudioManager()
        
        # Input handling
        self.keys_pressed = set()
        
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(pygame.key.name(event.key).upper())
            
            if self.state == GameState.MENU:
                if event.key == pygame.K_SPACE:
                    self.start_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_t:  # Theme toggle
                    self.cycle_theme()
                elif event.key == pygame.K_s:  # Sprite style toggle
                    self.cycle_sprite_style()
                    
            elif self.state == GameState.PLAYING:
                if pygame.key.name(event.key).upper() in JUMP_KEYS:
                    self.dino.jump()
                    self.audio.play_sound('jump')
                elif pygame.key.name(event.key).upper() == PAUSE_KEY.upper():
                    self.state = GameState.PAUSED
                elif event.key == pygame.K_t:  # Theme toggle during gameplay
                    self.cycle_theme()
                elif event.key == pygame.K_s:  # Sprite style toggle during gameplay
                    self.cycle_sprite_style()
                    
            elif self.state == GameState.PAUSED:
                if pygame.key.name(event.key).upper() == PAUSE_KEY.upper():
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_t:
                    self.cycle_theme()
                elif event.key == pygame.K_s:
                    self.cycle_sprite_style()
                    
            elif self.state == GameState.GAME_OVER:
                if event.key == pygame.K_SPACE:
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    
        elif event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key).upper()
            if key_name in self.keys_pressed:
                self.keys_pressed.remove(key_name)
                
            if key_name in DUCK_KEYS:
                self.dino.stop_duck()
                
        return True
        
    def cycle_theme(self):
        """Cycle through available themes"""
        themes = self.theme_manager.list_themes()
        current_index = themes.index(self.theme_manager.current_theme.name.lower())
        next_index = (current_index + 1) % len(themes)
        self.theme_manager.set_theme(themes[next_index])
        
        # Update all sprites with new theme
        self.dino.update_image()
        for obstacle in self.obstacles.sprites():
            obstacle.update_image()
        
    def cycle_sprite_style(self):
        """Cycle through sprite styles"""
        styles = ["default", "geometric", "pixel_art", "neon"]
        current_index = styles.index(self.sprite_style)
        next_index = (current_index + 1) % len(styles)
        self.sprite_style = styles[next_index]
        print(f"🎨 Sprite style changed to: {self.sprite_style}")
        
        # Update all sprites with new style
        self.dino.set_style(self.sprite_style)
        self.obstacles.update_style(self.sprite_style)
        
        # Clear sprite cache to regenerate with new style
        self.sprite_customizer.custom_sprites.clear()
        
    def start_game(self):
        """Start a new game"""
        self.state = GameState.PLAYING
        self.score = 0
        self.distance = 0
        self.speed = INITIAL_SPEED
        
        # Clear obstacles
        self.obstacles.empty()
        
        # Reset dino
        self.dino.rect.x = 100
        self.dino.rect.y = GROUND_Y - DINO_HEIGHT
        self.dino.vel_y = 0
        self.dino.is_jumping = False
        self.dino.is_ducking = False
        self.dino.state = "running"
        
        self.audio.play_music()
        
    def restart_game(self):
        """Restart the game"""
        self.start_game()
        
    def update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            self.update_gameplay()
        elif self.state == GameState.MENU:
            self.ui.update_menu()
        elif self.state == GameState.GAME_OVER:
            self.ui.update_game_over()
            
    def update_gameplay(self):
        """Update gameplay mechanics"""
        # Handle continuous input
        if 'DOWN' in self.keys_pressed:
            self.dino.duck()
        else:
            self.dino.stop_duck()
            
        # Update all sprites
        self.all_sprites.update()
        self.obstacles.update()
        
        # Update distance and score
        self.distance += self.speed
        self.score = int(self.distance * SCORE_MULTIPLIER / 100)
        
        # Increase speed gradually
        if self.speed < MAX_SPEED:
            self.speed += SPEED_INCREASE_RATE
            
        # Update obstacle speeds
        self.obstacles.update_speed(self.speed)
        
        # Spawn new obstacles
        self.obstacles.spawn_obstacle(self.speed)
        
        # Remove off-screen obstacles
        self.obstacles.remove_off_screen()
        
        # Check collisions using sprite collision detection
        collisions = pygame.sprite.spritecollide(self.dino, self.obstacles, False)
        if collisions:
            self.game_over()
            
    def game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER
        self.audio.play_sound('hit')
        self.audio.stop_music()
        
    def draw(self):
        """Draw everything"""
        # Fill background with theme color
        bg_color = self.theme_manager.get_color('background')
        self.screen.fill(bg_color)
        
        # Draw theme-specific background effects
        self.theme_manager.draw_background_effects(self.screen)
        
        if self.state == GameState.MENU:
            self.ui.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_gameplay()
            self.ui.draw_hud(self.score, self.distance, self.speed)
        elif self.state == GameState.PAUSED:
            self.draw_gameplay()
            self.ui.draw_pause_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_gameplay()
            self.ui.draw_game_over(self.score, self.distance)
            
    def draw_gameplay(self):
        """Draw gameplay elements using sprite system"""
        # Draw ground line with theme color
        ground_color = self.theme_manager.get_sprite_color('ground_line')
        pygame.draw.line(self.screen, ground_color, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
        
        # Draw all sprites with theme effects
        for sprite in self.all_sprites:
            if self.theme_manager.has_effect('glow'):
                self.theme_manager.apply_glow_effect(self.screen, sprite.image, sprite.rect.topleft)
            else:
                self.screen.blit(sprite.image, sprite.rect)
                
        for obstacle in self.obstacles:
            if self.theme_manager.has_effect('glow'):
                self.theme_manager.apply_glow_effect(self.screen, obstacle.image, obstacle.rect.topleft)
            else:
                self.screen.blit(obstacle.image, obstacle.rect)
                
        # Draw customization info
        self.draw_customization_info()
        
    def draw_customization_info(self):
        """Draw current customization settings"""
        if self.state == GameState.PLAYING:
            font = pygame.font.Font(None, 24)
            text_color = self.theme_manager.get_color('text_secondary')
            
            # Theme info
            theme_text = f"Theme: {self.theme_manager.current_theme.name} (T to change)"
            theme_surface = font.render(theme_text, True, text_color)
            self.screen.blit(theme_surface, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 60))
            
            # Sprite style info
            style_text = f"Style: {self.sprite_style} (S to change)"
            style_surface = font.render(style_text, True, text_color)
            self.screen.blit(style_surface, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 35))

# Create a wrapper function to use the enhanced game
def create_enhanced_game(screen):
    """Create enhanced game instance"""
    return EnhancedDinoGame(screen)
