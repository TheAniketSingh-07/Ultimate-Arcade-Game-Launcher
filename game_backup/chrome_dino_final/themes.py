"""
Dino Run Theme System
Handles different visual themes for the game
"""

import pygame
from games.dino_run.settings import *

class Theme:
    """Base theme class"""
    
    def __init__(self, name):
        self.name = name
        self.colors = {}
        self.sprites = {}
        self.effects = {}
        
    def get_color(self, color_name):
        """Get theme color"""
        return self.colors.get(color_name, WHITE)
        
    def get_sprite_color(self, sprite_name):
        """Get sprite color for this theme"""
        return self.sprites.get(sprite_name, GREEN)

class LightTheme(Theme):
    """Default light theme"""
    
    def __init__(self):
        super().__init__("Light")
        self.colors = {
            'background': (135, 206, 235),  # Sky blue
            'ground': (101, 67, 33),        # Brown
            'text': BLACK,
            'text_secondary': GRAY,
            'ui_primary': BLUE,
            'ui_secondary': GREEN,
            'danger': RED
        }
        self.sprites = {
            'dino_running': (0, 200, 0),    # Green
            'dino_jumping': (0, 150, 255),  # Blue
            'dino_ducking': (0, 0, 200),    # Dark blue
            'cactus': (0, 150, 0),          # Dark green
            'bird': (139, 69, 19),          # Brown
            'ground_line': BLACK
        }

class DarkTheme(Theme):
    """Dark theme for night mode"""
    
    def __init__(self):
        super().__init__("Dark")
        self.colors = {
            'background': (25, 25, 40),     # Dark blue-gray
            'ground': (40, 40, 40),         # Dark gray
            'text': (220, 220, 220),        # Light gray
            'text_secondary': (150, 150, 150),  # Medium gray
            'ui_primary': (100, 150, 255),  # Light blue
            'ui_secondary': (100, 255, 100), # Light green
            'danger': (255, 100, 100)       # Light red
        }
        self.sprites = {
            'dino_running': (100, 255, 100),    # Bright green
            'dino_jumping': (100, 200, 255),    # Bright blue
            'dino_ducking': (150, 100, 255),    # Purple
            'cactus': (200, 100, 100),          # Red-orange
            'bird': (255, 200, 100),            # Orange
            'ground_line': (150, 150, 150)      # Gray
        }
        self.effects = {
            'glow': True,
            'particles': 'neon',
            'background_stars': True
        }

class NeonTheme(Theme):
    """Neon cyberpunk theme"""
    
    def __init__(self):
        super().__init__("Neon")
        self.colors = {
            'background': (10, 10, 20),     # Very dark
            'ground': (20, 20, 30),         # Dark purple
            'text': (0, 255, 255),          # Cyan
            'text_secondary': (255, 0, 255), # Magenta
            'ui_primary': (0, 255, 255),    # Cyan
            'ui_secondary': (255, 0, 255),  # Magenta
            'danger': (255, 0, 100)         # Hot pink
        }
        self.sprites = {
            'dino_running': (0, 255, 255),      # Cyan
            'dino_jumping': (255, 0, 255),      # Magenta
            'dino_ducking': (255, 255, 0),      # Yellow
            'cactus': (255, 0, 100),            # Hot pink
            'bird': (100, 255, 0),              # Lime green
            'ground_line': (0, 255, 255)        # Cyan
        }
        self.effects = {
            'glow': True,
            'particles': 'electric',
            'background_grid': True,
            'neon_outlines': True
        }

class ThemeManager:
    """Manages game themes"""
    
    def __init__(self):
        self.themes = {
            'light': LightTheme(),
            'dark': DarkTheme(),
            'neon': NeonTheme()
        }
        self.current_theme = self.themes['light']
        
    def set_theme(self, theme_name):
        """Set the current theme"""
        if theme_name.lower() in self.themes:
            self.current_theme = self.themes[theme_name.lower()]
            print(f"🎨 Theme changed to: {self.current_theme.name}")
            return True
        else:
            print(f"❌ Theme '{theme_name}' not found")
            return False
            
    def get_current_theme(self):
        """Get the current theme"""
        return self.current_theme
        
    def list_themes(self):
        """List available themes"""
        return list(self.themes.keys())
        
    def get_color(self, color_name):
        """Get color from current theme"""
        return self.current_theme.get_color(color_name)
        
    def get_sprite_color(self, sprite_name):
        """Get sprite color from current theme"""
        return self.current_theme.get_sprite_color(sprite_name)
        
    def has_effect(self, effect_name):
        """Check if current theme has a specific effect"""
        return self.current_theme.effects.get(effect_name, False)
        
    def draw_background_effects(self, screen):
        """Draw theme-specific background effects"""
        if self.has_effect('background_stars'):
            self.draw_stars(screen)
        elif self.has_effect('background_grid'):
            self.draw_grid(screen)
            
    def draw_stars(self, screen):
        """Draw starfield for dark theme"""
        import random
        import math
        
        # Static stars (pseudo-random but consistent)
        random.seed(42)  # Fixed seed for consistent star positions
        
        for i in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            
            # Twinkling effect
            brightness = 150 + int(50 * math.sin(pygame.time.get_ticks() * 0.001 + i))
            color = (brightness, brightness, brightness)
            
            pygame.draw.circle(screen, color, (x, y), 1)
            
    def draw_grid(self, screen):
        """Draw grid for neon theme"""
        grid_color = (0, 50, 50)
        grid_size = 50
        
        # Vertical lines
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
            
        # Horizontal lines
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
            
    def apply_glow_effect(self, screen, surface, pos, glow_color=None):
        """Apply glow effect to a surface"""
        if not self.has_effect('glow'):
            screen.blit(surface, pos)
            return
            
        if glow_color is None:
            glow_color = self.get_color('ui_primary')
            
        # Create glow effect
        glow_surface = pygame.Surface((surface.get_width() + 10, surface.get_height() + 10), pygame.SRCALPHA)
        
        # Draw multiple layers for glow
        for i in range(3):
            alpha = 50 - (i * 15)
            glow_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            glow_layer.fill((*glow_color, alpha))
            
            offset = i + 1
            glow_surface.blit(glow_layer, (offset, offset))
            
        # Draw glow then original surface
        screen.blit(glow_surface, (pos[0] - 5, pos[1] - 5))
        screen.blit(surface, pos)
