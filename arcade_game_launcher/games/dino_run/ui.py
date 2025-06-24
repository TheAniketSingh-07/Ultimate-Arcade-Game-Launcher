"""
Dino Run UI Components
Handles menus, HUD, and screen transitions
"""

import pygame
from games.dino_run.settings import *

class GameUI:
    """UI manager for the game"""
    
    def __init__(self, screen, theme_manager=None):
        self.screen = screen
        self.theme_manager = theme_manager
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.load_fonts()
        
    def load_fonts(self):
        """Load game fonts"""
        try:
            # Try to load custom font
            font_path = os.path.join(FONTS_DIR, 'pixel_font.ttf')
            if os.path.exists(font_path) and os.path.getsize(font_path) > 0:
                self.font_large = pygame.font.Font(font_path, FONT_SIZE_LARGE)
                self.font_medium = pygame.font.Font(font_path, FONT_SIZE_MEDIUM)
                self.font_small = pygame.font.Font(font_path, FONT_SIZE_SMALL)
            else:
                raise FileNotFoundError("Custom font not available")
        except Exception as e:
            print(f"Loading custom font failed: {e}")
            # Fallback to system fonts
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
            
    def get_theme_color(self, color_name, fallback=BLACK):
        """Get color from theme manager or use fallback"""
        if self.theme_manager:
            return self.theme_manager.get_color(color_name)
        return fallback
        
    def draw_text(self, text, font, color, x, y, center=False):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, (x, y))
            
    def draw_menu(self):
        """Draw main menu"""
        # Title
        title_color = self.get_theme_color('text', BLACK)
        self.draw_text("DINO RUN", self.font_large, title_color, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, center=True)
        
        # Subtitle
        subtitle_color = self.get_theme_color('text_secondary', GRAY)
        self.draw_text("Endless Runner Adventure", self.font_medium, subtitle_color, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        
        # Instructions
        primary_color = self.get_theme_color('ui_primary', BLUE)
        self.draw_text("Press SPACE to Start", self.font_medium, primary_color, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
        
        self.draw_text("Press ESC to Exit", self.font_small, subtitle_color, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True)
        
        # Controls
        controls_y = SCREEN_HEIGHT // 2 + 120
        self.draw_text("Controls:", self.font_small, title_color, 
                      SCREEN_WIDTH // 2, controls_y, center=True)
        
        self.draw_text("SPACE/UP - Jump", self.font_small, subtitle_color, 
                      SCREEN_WIDTH // 2, controls_y + 30, center=True)
        
        self.draw_text("DOWN - Duck", self.font_small, subtitle_color, 
                      SCREEN_WIDTH // 2, controls_y + 55, center=True)
        
        self.draw_text("P - Pause | T - Theme | S - Style", self.font_small, subtitle_color, 
                      SCREEN_WIDTH // 2, controls_y + 80, center=True)
                      
    def draw_hud(self, score, distance, speed):
        """Draw heads-up display during gameplay"""
        text_color = self.get_theme_color('text', BLACK)
        
        # Score
        self.draw_text(f"Score: {score}", self.font_medium, text_color, 20, 20)
        
        # Distance
        distance_km = distance / 100  # Convert to km
        self.draw_text(f"Distance: {distance_km:.1f}km", self.font_medium, text_color, 20, 60)
        
        # Speed
        self.draw_text(f"Speed: {speed:.1f}", self.font_medium, text_color, 20, 100)
        
        # Speed indicator bar
        speed_percentage = min(speed / MAX_SPEED, 1.0)
        bar_width = 200
        bar_height = 10
        bar_x = SCREEN_WIDTH - bar_width - 20
        bar_y = 20
        
        # Background bar
        bg_color = self.get_theme_color('text_secondary', GRAY)
        pygame.draw.rect(self.screen, bg_color, (bar_x, bar_y, bar_width, bar_height))
        
        # Speed bar
        speed_bar_width = int(bar_width * speed_percentage)
        if speed_percentage < 0.7:
            speed_color = self.get_theme_color('ui_secondary', GREEN)
        elif speed_percentage < 0.9:
            speed_color = (255, 165, 0)  # Orange
        else:
            speed_color = self.get_theme_color('danger', RED)
        pygame.draw.rect(self.screen, speed_color, (bar_x, bar_y, speed_bar_width, bar_height))
        
        # Speed label
        self.draw_text("Speed", self.font_small, text_color, bar_x, bar_y - 25)
        
    def draw_pause_menu(self):
        """Draw pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        self.draw_text("PAUSED", self.font_large, WHITE, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        
        self.draw_text("Press P to Resume", self.font_medium, WHITE, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
                      
    def draw_game_over(self, score, distance):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over title
        self.draw_text("GAME OVER", self.font_large, RED, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, center=True)
        
        # Final score
        self.draw_text(f"Final Score: {score}", self.font_medium, WHITE, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, center=True)
        
        # Final distance
        distance_km = distance / 100
        self.draw_text(f"Distance Traveled: {distance_km:.1f}km", self.font_medium, WHITE, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        
        # Instructions
        self.draw_text("Press SPACE to Retry", self.font_medium, GREEN, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True)
        
        self.draw_text("Press ESC for Main Menu", self.font_small, GRAY, 
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, center=True)
                      
    def update_menu(self):
        """Update menu animations (if any)"""
        pass
        
    def update_game_over(self):
        """Update game over screen animations (if any)"""
        pass
