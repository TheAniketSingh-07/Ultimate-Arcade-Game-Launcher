"""
Simple Chrome Dino Sprite Customizer
"""

import pygame
from games.dino_run.settings import *

class SpriteCustomizer:
    """Simple sprite customizer for Chrome-style game"""
    
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.custom_sprites = {}
        
    def create_simple_dino(self, state="running"):
        """Create simple box-style dino like Chrome"""
        width, height = DINO_WIDTH, DINO_HEIGHT
        if state == "ducking":
            height = int(height * DUCK_HEIGHT_REDUCTION)
            
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Simple black box dino
        if state == "running":
            # Main body - simple rectangle
            pygame.draw.rect(surface, BLACK, (5, 8, 30, 25))
            # Simple eye - white dot
            pygame.draw.circle(surface, WHITE, (12, 15), 2)
            # Simple legs
            pygame.draw.rect(surface, BLACK, (10, 33, 4, 6))
            pygame.draw.rect(surface, BLACK, (20, 33, 4, 6))
            
        elif state == "jumping":
            # Same as running but legs tucked
            pygame.draw.rect(surface, BLACK, (5, 8, 30, 25))
            pygame.draw.circle(surface, WHITE, (12, 15), 2)
            pygame.draw.rect(surface, BLACK, (12, 30, 4, 4))
            pygame.draw.rect(surface, BLACK, (18, 30, 4, 4))
            
        elif state == "ducking":
            # Flattened box
            pygame.draw.rect(surface, BLACK, (5, 15, 30, 15))
            pygame.draw.circle(surface, WHITE, (12, 20), 1)
            
        return surface
        
    def create_simple_cactus(self):
        """Create simple cactus like Chrome"""
        width, height = CACTUS_WIDTH, CACTUS_HEIGHT
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Simple cactus - just rectangles
        # Main stem
        pygame.draw.rect(surface, BLACK, (8, 10, 4, 30))
        # Left arm
        pygame.draw.rect(surface, BLACK, (4, 20, 8, 3))
        # Right arm
        pygame.draw.rect(surface, BLACK, (8, 25, 8, 3))
        
        return surface
        
    def get_sprite(self, sprite_type, state="default", style="simple"):
        """Get sprite - simplified"""
        if sprite_type == "dino":
            return self.create_simple_dino(state)
        elif sprite_type == "cactus":
            return self.create_simple_cactus()
        else:
            # Fallback
            surface = pygame.Surface((20, 20))
            surface.fill(BLACK)
            return surface
