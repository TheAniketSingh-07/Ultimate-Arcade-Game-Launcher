#!/usr/bin/env python3
"""
Enhanced Game Launcher with Keyboard Controls
Features: Arrow key navigation, Enter to launch, Last game memory, Single-click launch
"""

import pygame
import sys
import os
import subprocess
import json
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Initialize Pygame
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
TARGET_FPS = 120

class Theme:
    """Enhanced color theme"""
    BG_DARK = (12, 12, 20)
    BG_SURFACE = (20, 20, 32)
    PRIMARY = (64, 128, 255)
    SECONDARY = (128, 64, 255)
    ACCENT = (255, 128, 64)
    SUCCESS = (64, 255, 128)
    TEXT_WHITE = (255, 255, 255)
    TEXT_GRAY = (180, 180, 200)
    TEXT_DARK = (120, 120, 140)
    CARD_BG = (28, 28, 44)
    CARD_HOVER = (36, 36, 52)
    CARD_SELECTED = (64, 64, 128)  # New selected state
    CARD_ACTIVE = (44, 44, 60)
    BORDER = (60, 60, 80)
    LAST_GAME = (255, 200, 100)  # Highlight for last played game

@dataclass
class GameData:
    """Game data structure with enhanced features"""
    name: str
    path: str
    description: str
    category: str
    color: Tuple[int, int, int]
    executable: str
    last_played: float = 0
    play_count: int = 0
    is_favorite: bool = False

class PerformanceMonitor:
    """Performance monitoring system"""
    def __init__(self):
        self.frame_times = []
        self.max_samples = 60
        self.last_time = time.time()
    
    def update(self):
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
    
    def get_fps(self) -> float:
        if not self.frame_times:
            return 0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0

class OptimizedRenderer:
    """High-performance rendering system"""
    def __init__(self, screen):
        self.screen = screen
        self.surface_cache = {}
        
        # Pre-load fonts
        self.fonts = {
            'title': pygame.font.Font(None, 48),
            'subtitle': pygame.font.Font(None, 32),
            'body': pygame.font.Font(None, 24),
            'small': pygame.font.Font(None, 18),
            'controls': pygame.font.Font(None, 20)
        }
    
    def get_text_surface(self, text: str, font_key: str, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cached text rendering"""
        cache_key = (text, font_key, color)
        if cache_key not in self.surface_cache:
            font = self.fonts.get(font_key, self.fonts['body'])
            surface = font.render(text, True, color)
            self.surface_cache[cache_key] = surface
        return self.surface_cache[cache_key]
    
    def draw_rounded_rect(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                         rect: pygame.Rect, radius: int = 8):
        """Optimized rounded rectangle drawing"""
        if radius <= 0:
            pygame.draw.rect(surface, color, rect)
            return
        
        # Draw main rectangle
        pygame.draw.rect(surface, color, (rect.x + radius, rect.y, rect.width - 2*radius, rect.height))
        pygame.draw.rect(surface, color, (rect.x, rect.y + radius, rect.width, rect.height - 2*radius))
        
        # Draw corners
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)

class GameCard:
    """Enhanced game card with selection states"""
    def __init__(self, game_data: GameData, x: int, y: int, width: int = 280, height: int = 160):
        self.game_data = game_data
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.animation_speed = 0.15
        self.is_hovered = False
        self.is_selected = False
        self.click_animation = 0.0
        self.selection_glow = 0.0
    
    def update(self, dt: float):
        """Smooth animation updates"""
        # Scale animation
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * self.animation_speed
        
        # Click animation decay
        if self.click_animation > 0:
            self.click_animation = max(0, self.click_animation - dt * 3)
        
        # Selection glow animation
        if self.is_selected:
            self.selection_glow = min(1.0, self.selection_glow + dt * 4)
        else:
            self.selection_glow = max(0.0, self.selection_glow - dt * 4)
    
    def handle_hover(self, mouse_pos: Tuple[int, int]):
        """Handle hover state"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered and not was_hovered:
            self.target_scale = 1.05
        elif not self.is_hovered and was_hovered:
            self.target_scale = 1.0
    
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        if selected:
            self.target_scale = 1.08
        else:
            self.target_scale = 1.05 if self.is_hovered else 1.0
    
    def handle_click(self):
        """Handle click animation"""
        self.click_animation = 1.0
        return self.game_data
    
    def draw(self, renderer: OptimizedRenderer):
        """Enhanced drawing with selection states"""
        # Calculate animated position and size
        scale = self.hover_scale - self.click_animation * 0.05
        scaled_width = int(self.rect.width * scale)
        scaled_height = int(self.rect.height * scale)
        scaled_x = self.rect.x + (self.rect.width - scaled_width) // 2
        scaled_y = self.rect.y + (self.rect.height - scaled_height) // 2
        
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Background color based on state
        if self.is_selected:
            bg_color = Theme.CARD_SELECTED
        elif self.is_hovered:
            bg_color = Theme.CARD_HOVER
        else:
            bg_color = Theme.CARD_BG
        
        # Draw background
        renderer.draw_rounded_rect(renderer.screen, bg_color, scaled_rect, 12)
        
        # Draw selection glow
        if self.selection_glow > 0:
            glow_color = (*Theme.PRIMARY, int(100 * self.selection_glow))
            glow_rect = pygame.Rect(scaled_rect.x - 2, scaled_rect.y - 2, 
                                  scaled_rect.width + 4, scaled_rect.height + 4)
            renderer.draw_rounded_rect(renderer.screen, Theme.PRIMARY, glow_rect, 14)
            renderer.draw_rounded_rect(renderer.screen, bg_color, scaled_rect, 12)
        
        # Last played indicator
        if self.game_data.last_played > 0:
            last_played_time = time.time() - self.game_data.last_played
            if last_played_time < 3600:  # Last hour
                pygame.draw.circle(renderer.screen, Theme.LAST_GAME, 
                                 (scaled_rect.x + scaled_rect.width - 15, scaled_rect.y + 15), 8)
        
        # Game icon (colored circle)
        icon_radius = 24
        icon_center = (scaled_rect.x + 40, scaled_rect.y + 40)
        pygame.draw.circle(renderer.screen, self.game_data.color, icon_center, icon_radius)
        
        # Game name
        name_surface = renderer.get_text_surface(self.game_data.name, 'subtitle', Theme.TEXT_WHITE)
        name_pos = (scaled_rect.x + 80, scaled_rect.y + 20)
        renderer.screen.blit(name_surface, name_pos)
        
        # Category
        category_surface = renderer.get_text_surface(self.game_data.category, 'small', Theme.TEXT_GRAY)
        category_pos = (scaled_rect.x + 80, scaled_rect.y + 50)
        renderer.screen.blit(category_surface, category_pos)
        
        # Description
        desc_lines = self.wrap_text(self.game_data.description, 30)
        for i, line in enumerate(desc_lines[:2]):
            desc_surface = renderer.get_text_surface(line, 'small', Theme.TEXT_DARK)
            desc_pos = (scaled_rect.x + 20, scaled_rect.y + 80 + i * 20)
            renderer.screen.blit(desc_surface, desc_pos)
        
        # Play count indicator
        if self.game_data.play_count > 0:
            count_text = f"Played {self.game_data.play_count}x"
            count_surface = renderer.get_text_surface(count_text, 'small', Theme.ACCENT)
            count_pos = (scaled_rect.x + scaled_rect.width - 80, scaled_rect.y + scaled_rect.height - 25)
            renderer.screen.blit(count_surface, count_pos)
    
    def wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
