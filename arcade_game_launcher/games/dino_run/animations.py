"""
Dino Run Animation System
Handles sprite animations and visual effects
"""

import pygame
import math
import random
from games.dino_run.settings import *
from games.dino_run.utils import load_image, create_placeholder_surface

class Animation:
    """Base animation class"""
    
    def __init__(self, frames, frame_duration=100):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.playing = True
        self.loop = True
        
    def update(self):
        """Update animation frame"""
        if not self.playing or not self.frames:
            return
            
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
                    
            self.last_update = now
            
    def get_current_frame(self):
        """Get current animation frame"""
        if self.frames and 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
        
    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.playing = True
        self.last_update = pygame.time.get_ticks()
        
    def play(self):
        """Start playing animation"""
        self.playing = True
        
    def pause(self):
        """Pause animation"""
        self.playing = False
        
    def stop(self):
        """Stop and reset animation"""
        self.playing = False
        self.current_frame = 0

class SpriteSheet:
    """Sprite sheet loader and manager"""
    
    def __init__(self, filename, sprite_width, sprite_height):
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sheet = load_image(filename)
        
        if not self.sheet:
            # Create placeholder sheet
            self.sheet = create_placeholder_surface(
                sprite_width * 4, sprite_height * 4, (255, 0, 255)
            )
            
    def get_sprite(self, x, y):
        """Get a single sprite from the sheet"""
        rect = pygame.Rect(
            x * self.sprite_width,
            y * self.sprite_height,
            self.sprite_width,
            self.sprite_height
        )
        
        sprite = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), rect)
        return sprite
        
    def get_sprites(self, positions):
        """Get multiple sprites from positions list"""
        sprites = []
        for x, y in positions:
            sprites.append(self.get_sprite(x, y))
        return sprites

class DinoAnimator:
    """Handles dino character animations"""
    
    def __init__(self):
        self.load_animations()
        self.current_state = "running"
        
    def load_animations(self):
        """Load all dino animations"""
        # Try to load sprite sheet
        sheet_path = os.path.join(IMAGES_DIR, 'dino_run_spritesheet.png')
        self.sprite_sheet = SpriteSheet(sheet_path, DINO_WIDTH, DINO_HEIGHT)
        
        # Create animations
        self.animations = {
            "running": Animation(
                self.create_running_frames(),
                frame_duration=150
            ),
            "jumping": Animation(
                self.create_jumping_frames(),
                frame_duration=200,
                loop=False
            ),
            "ducking": Animation(
                self.create_ducking_frames(),
                frame_duration=100
            ),
            "idle": Animation(
                self.create_idle_frames(),
                frame_duration=500
            )
        }
        
    def create_running_frames(self):
        """Create running animation frames"""
        # If sprite sheet is available, use it
        # Otherwise create placeholder frames
        frames = []
        for i in range(4):  # 4 running frames
            frame = create_placeholder_surface(DINO_WIDTH, DINO_HEIGHT, (0, 255, 0))
            # Add simple animation effect
            brightness = 200 + (i * 10)
            frame.fill((0, min(255, brightness), 0))
            frames.append(frame)
        return frames
        
    def create_jumping_frames(self):
        """Create jumping animation frames"""
        frames = []
        frame = create_placeholder_surface(DINO_WIDTH, DINO_HEIGHT, (0, 200, 255))
        frames.append(frame)
        return frames
        
    def create_ducking_frames(self):
        """Create ducking animation frames"""
        frames = []
        duck_height = int(DINO_HEIGHT * DUCK_HEIGHT_REDUCTION)
        for i in range(2):  # 2 ducking frames
            frame = create_placeholder_surface(DINO_WIDTH, duck_height, (0, 0, 255))
            frames.append(frame)
        return frames
        
    def create_idle_frames(self):
        """Create idle animation frames"""
        frames = []
        frame = create_placeholder_surface(DINO_WIDTH, DINO_HEIGHT, (100, 255, 100))
        frames.append(frame)
        return frames
        
    def set_state(self, state):
        """Set animation state"""
        if state in self.animations and state != self.current_state:
            self.current_state = state
            self.animations[state].reset()
            
    def update(self):
        """Update current animation"""
        if self.current_state in self.animations:
            self.animations[self.current_state].update()
            
    def get_current_frame(self):
        """Get current animation frame"""
        if self.current_state in self.animations:
            return self.animations[self.current_state].get_current_frame()
        return None

class ParticleSystem:
    """Simple particle system for effects"""
    
    def __init__(self):
        self.particles = []
        
    def add_particle(self, x, y, vel_x, vel_y, color, life_time=1000):
        """Add a new particle"""
        particle = {
            'x': x,
            'y': y,
            'vel_x': vel_x,
            'vel_y': vel_y,
            'color': color,
            'life_time': life_time,
            'max_life': life_time,
            'size': 3
        }
        self.particles.append(particle)
        
    def update(self, dt):
        """Update all particles"""
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            
            # Update life
            particle['life_time'] -= dt * 1000
            
            # Apply gravity
            particle['vel_y'] += 0.5
            
            # Remove dead particles
            if particle['life_time'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            alpha = int(255 * (particle['life_time'] / particle['max_life']))
            alpha = max(0, min(255, alpha))
            
            # Create surface with alpha
            size = max(1, int(particle['size'] * (particle['life_time'] / particle['max_life'])))
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            
            color_with_alpha = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, color_with_alpha, (size, size), size)
            
            screen.blit(particle_surface, (int(particle['x'] - size), int(particle['y'] - size)))
            
    def create_dust_effect(self, x, y):
        """Create dust particles for running effect"""
        for _ in range(3):
            self.add_particle(
                x + random.randint(-10, 10),
                y,
                random.uniform(-2, 2),
                random.uniform(-3, -1),
                (139, 69, 19),  # Brown dust color
                life_time=500
            )
            
    def create_impact_effect(self, x, y):
        """Create impact particles for collision"""
        for _ in range(8):
            self.add_particle(
                x,
                y,
                random.uniform(-5, 5),
                random.uniform(-8, -2),
                (255, 255, 0),  # Yellow impact
                life_time=800
            )

class BackgroundAnimator:
    """Handles parallax background animation"""
    
    def __init__(self):
        self.layers = []
        self.load_background_layers()
        
    def load_background_layers(self):
        """Load background layers for parallax effect"""
        layer_files = [
            ('background_layer1.png', 0.2),  # Far background, slow
            ('background_layer2.png', 0.5),  # Mid background, medium
            ('ground.png', 1.0)              # Ground, full speed
        ]
        
        for filename, speed in layer_files:
            layer_path = os.path.join(IMAGES_DIR, filename)
            image = load_image(layer_path)
            
            if not image:
                # Create placeholder layer
                if 'ground' in filename:
                    image = create_placeholder_surface(SCREEN_WIDTH, 100, (101, 67, 33))
                else:
                    image = create_placeholder_surface(SCREEN_WIDTH, SCREEN_HEIGHT, (135, 206, 235))
                    
            self.layers.append({
                'image': image,
                'speed': speed,
                'x': 0,
                'width': image.get_width()
            })
            
    def update(self, game_speed):
        """Update background layers"""
        for layer in self.layers:
            layer['x'] -= game_speed * layer['speed']
            
            # Reset position for seamless scrolling
            if layer['x'] <= -layer['width']:
                layer['x'] = 0
                
    def draw(self, screen):
        """Draw all background layers"""
        for layer in self.layers:
            # Draw main image
            screen.blit(layer['image'], (layer['x'], 0))
            
            # Draw second copy for seamless scrolling
            screen.blit(layer['image'], (layer['x'] + layer['width'], 0))
