"""
Dino Run Sprite Classes
Enhanced sprite system using pygame.sprite.Sprite
"""

import pygame
import random
from games.dino_run.settings import *
from games.dino_run.utils import create_placeholder_surface

class Obstacle(pygame.sprite.Sprite):
    """Base obstacle class using pygame sprite system"""
    
    def __init__(self, x, y, width, height, speed=0):
        super().__init__()
        
        # Sprite properties
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement properties
        self.speed = speed
        self.original_speed = speed
        
        # Visual properties
        self.width = width
        self.height = height
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.last_animation_update = pygame.time.get_ticks()
        
    def update(self):
        """Update obstacle position and animation"""
        # Move obstacle left
        self.rect.x -= self.speed
        
        # Update animation
        self.update_animation()
        
    def update_animation(self):
        """Update sprite animation"""
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > (1000 * self.animation_speed):
            self.animation_frame += 1
            self.last_animation_update = now
            self.update_image()
            
    def update_image(self):
        """Update the sprite image - override in subclasses"""
        pass
        
    def is_off_screen(self):
        """Check if obstacle is completely off screen"""
        return self.rect.right < 0
        
    def set_speed(self, speed):
        """Set obstacle movement speed"""
        self.speed = speed

class Cactus(Obstacle):
    """Cactus obstacle sprite"""
    
    def __init__(self, x, theme_manager=None, sprite_customizer=None, style="geometric"):
        super().__init__(x, GROUND_Y - CACTUS_HEIGHT, CACTUS_WIDTH, CACTUS_HEIGHT)
        
        self.theme_manager = theme_manager
        self.sprite_customizer = sprite_customizer
        self.style = style
        self.obstacle_type = "cactus"
        
        # Create initial image
        self.update_image()
        
    def update_image(self):
        """Update cactus sprite image"""
        if self.sprite_customizer and self.theme_manager:
            # Use custom sprite system
            self.image = self.sprite_customizer.get_sprite("cactus", "default", self.style)
        else:
            # Fallback to simple colored rectangle
            color = (200, 100, 100) if self.theme_manager else RED
            if self.theme_manager:
                color = self.theme_manager.get_sprite_color('cactus')
            self.image = create_placeholder_surface(self.width, self.height, color)
            
    def create_geometric_cactus(self):
        """Create geometric style cactus"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        color = self.theme_manager.get_sprite_color('cactus') if self.theme_manager else (0, 150, 0)
        
        # Main stem
        stem_width = self.width // 4
        stem_x = (self.width - stem_width) // 2
        pygame.draw.rect(surface, color, (stem_x, self.height//4, stem_width, 3*self.height//4))
        
        # Left arm
        arm_width = self.width // 3
        arm_height = self.height // 8
        pygame.draw.rect(surface, color, (stem_x - arm_width//2, self.height//3, arm_width, arm_height))
        
        # Right arm
        pygame.draw.rect(surface, color, (stem_x + stem_width//2, self.height//2, arm_width//2, arm_height))
        
        # Add spikes
        spike_color = tuple(max(0, c - 50) for c in color)  # Darker spikes
        for i in range(0, self.height - 10, 8):
            # Left spikes
            pygame.draw.line(surface, spike_color, (stem_x - 2, self.height//4 + i), (stem_x - 5, self.height//4 + i - 2), 2)
            # Right spikes
            pygame.draw.line(surface, spike_color, (stem_x + stem_width + 2, self.height//4 + i), (stem_x + stem_width + 5, self.height//4 + i - 2), 2)
            
        return surface

class Bird(Obstacle):
    """Flying bird obstacle sprite"""
    
    def __init__(self, x, theme_manager=None, sprite_customizer=None, style="geometric"):
        # Birds fly at different heights
        heights = [GROUND_Y - 150, GROUND_Y - 100, GROUND_Y - 200]
        y = random.choice(heights)
        
        super().__init__(x, y, BIRD_WIDTH, BIRD_HEIGHT)
        
        self.theme_manager = theme_manager
        self.sprite_customizer = sprite_customizer
        self.style = style
        self.obstacle_type = "bird"
        
        # Bird-specific animation
        self.wing_flap_speed = 0.05  # Faster animation for wing flapping
        self.animation_speed = self.wing_flap_speed
        
        # Create initial image
        self.update_image()
        
    def update_image(self):
        """Update bird sprite image with wing flapping animation"""
        if self.sprite_customizer and self.theme_manager:
            # Use custom sprite system
            self.image = self.sprite_customizer.get_sprite("bird", "default", self.style)
        else:
            # Create animated bird
            self.image = self.create_animated_bird()
            
    def create_animated_bird(self):
        """Create animated bird with flapping wings"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        color = self.theme_manager.get_sprite_color('bird') if self.theme_manager else (139, 69, 19)
        
        # Body (ellipse)
        body_rect = (self.width//4, self.height//3, self.width//2, self.height//3)
        pygame.draw.ellipse(surface, color, body_rect)
        
        # Wing animation based on frame
        wing_offset = 2 if self.animation_frame % 2 == 0 else -2
        
        # Left wing
        left_wing_points = [
            (self.width//4, self.height//2),
            (5, self.height//2 + wing_offset),
            (self.width//4, 2*self.height//3)
        ]
        pygame.draw.polygon(surface, color, left_wing_points)
        
        # Right wing
        right_wing_points = [
            (3*self.width//4, self.height//2),
            (self.width - 5, self.height//2 + wing_offset),
            (3*self.width//4, 2*self.height//3)
        ]
        pygame.draw.polygon(surface, color, right_wing_points)
        
        # Beak
        beak_color = (255, 200, 0)  # Yellow beak
        beak_points = [
            (3*self.width//4, self.height//2),
            (self.width - 2, self.height//2 - 2),
            (3*self.width//4, self.height//2 + 4)
        ]
        pygame.draw.polygon(surface, beak_color, beak_points)
        
        # Eye
        eye_pos = (self.width//2, self.height//2)
        pygame.draw.circle(surface, (255, 255, 255), eye_pos, 2)
        pygame.draw.circle(surface, (0, 0, 0), eye_pos, 1)
        
        return surface

class DinoSprite(pygame.sprite.Sprite):
    """Enhanced Dino player sprite"""
    
    def __init__(self, x, y, theme_manager=None, sprite_customizer=None):
        super().__init__()
        
        self.theme_manager = theme_manager
        self.sprite_customizer = sprite_customizer
        
        # Position and physics
        self.rect = pygame.Rect(x, y, DINO_WIDTH, DINO_HEIGHT)
        self.vel_y = 0
        self.ground_y = GROUND_Y - DINO_HEIGHT
        
        # State management
        self.state = "running"  # running, jumping, ducking
        self.is_jumping = False
        self.is_ducking = False
        
        # Animation
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.last_animation_update = pygame.time.get_ticks()
        
        # Style
        self.style = "geometric"
        
        # Create initial image
        self.update_image()
        
    def update(self):
        """Update dino physics and animation"""
        # Apply gravity
        if self.is_jumping:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            
            # Check if landed
            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.vel_y = 0
                self.is_jumping = False
                self.state = "running"
                
        # Update animation
        self.update_animation()
        
    def update_animation(self):
        """Update sprite animation"""
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > (1000 * self.animation_speed):
            self.animation_frame += 1
            self.last_animation_update = now
            self.update_image()
            
    def update_image(self):
        """Update dino sprite image"""
        if self.sprite_customizer and self.theme_manager:
            self.image = self.sprite_customizer.get_sprite("dino", self.state, self.style)
        else:
            # Fallback sprite creation
            self.image = self.create_simple_dino()
            
        # Handle ducking size change
        if self.is_ducking:
            old_bottom = self.rect.bottom
            self.rect.height = int(DINO_HEIGHT * DUCK_HEIGHT_REDUCTION)
            self.rect.bottom = old_bottom
        else:
            self.rect.height = DINO_HEIGHT
            
    def create_simple_dino(self):
        """Create simple fallback dino sprite"""
        height = int(DINO_HEIGHT * DUCK_HEIGHT_REDUCTION) if self.is_ducking else DINO_HEIGHT
        
        if self.state == "running":
            color = (0, 200, 0)
        elif self.state == "jumping":
            color = (0, 150, 255)
        else:  # ducking
            color = (0, 0, 200)
            
        return create_placeholder_surface(DINO_WIDTH, height, color)
        
    def jump(self):
        """Make the dino jump"""
        if not self.is_jumping:
            self.vel_y = JUMP_STRENGTH
            self.is_jumping = True
            self.state = "jumping"
            
    def duck(self):
        """Make the dino duck"""
        if not self.is_jumping:
            self.is_ducking = True
            self.state = "ducking"
            
    def stop_duck(self):
        """Stop ducking"""
        if self.is_ducking:
            self.is_ducking = False
            self.state = "running"
            
    def set_style(self, style):
        """Change sprite style"""
        self.style = style
        self.update_image()

class ObstacleGroup(pygame.sprite.Group):
    """Enhanced sprite group for obstacles"""
    
    def __init__(self, theme_manager=None, sprite_customizer=None):
        super().__init__()
        self.theme_manager = theme_manager
        self.sprite_customizer = sprite_customizer
        self.last_spawn_x = SCREEN_WIDTH
        
    def spawn_obstacle(self, game_speed):
        """Spawn a new obstacle"""
        spawn_x = SCREEN_WIDTH + 50
        
        # Check minimum distance
        if spawn_x - self.last_spawn_x >= MIN_OBSTACLE_DISTANCE:
            if random.random() < OBSTACLE_SPAWN_CHANCE:
                # Choose obstacle type
                if random.choice([True, False]):
                    obstacle = Cactus(spawn_x, self.theme_manager, self.sprite_customizer)
                else:
                    obstacle = Bird(spawn_x, self.theme_manager, self.sprite_customizer)
                
                obstacle.set_speed(game_speed)
                self.add(obstacle)
                self.last_spawn_x = spawn_x
                
    def update_speed(self, speed):
        """Update speed for all obstacles"""
        for obstacle in self.sprites():
            obstacle.set_speed(speed)
            
    def remove_off_screen(self):
        """Remove obstacles that are off screen"""
        for obstacle in self.sprites():
            if obstacle.is_off_screen():
                self.remove(obstacle)
                
    def update_style(self, style):
        """Update sprite style for all obstacles"""
        for obstacle in self.sprites():
            if hasattr(obstacle, 'style'):
                obstacle.style = style
                obstacle.update_image()
