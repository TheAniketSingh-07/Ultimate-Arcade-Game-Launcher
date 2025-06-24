"""
Dino Run Power-ups System
Optional power-up mechanics for enhanced gameplay
"""

import pygame
import random
from enum import Enum
from games.dino_run.settings import *
from games.dino_run.utils import create_placeholder_surface

class PowerUpType(Enum):
    SHIELD = "shield"
    SLOW_MOTION = "slow_motion"
    DOUBLE_JUMP = "double_jump"
    SCORE_MULTIPLIER = "score_multiplier"
    INVINCIBILITY = "invincibility"

class PowerUp:
    """Base power-up class"""
    
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.power_type = power_type
        self.speed = 0
        self.collected = False
        
        # Visual effects
        self.bob_offset = 0
        self.bob_speed = 0.1
        self.rotation = 0
        self.rotation_speed = 2
        
        # Load sprite
        self.sprite = self.load_sprite()
        
    def load_sprite(self):
        """Load power-up sprite"""
        # Create placeholder sprites with different colors for each type
        colors = {
            PowerUpType.SHIELD: (0, 255, 255),      # Cyan
            PowerUpType.SLOW_MOTION: (255, 255, 0), # Yellow
            PowerUpType.DOUBLE_JUMP: (255, 0, 255), # Magenta
            PowerUpType.SCORE_MULTIPLIER: (0, 255, 0), # Green
            PowerUpType.INVINCIBILITY: (255, 165, 0)   # Orange
        }
        
        color = colors.get(self.power_type, (255, 255, 255))
        return create_placeholder_surface(self.width, self.height, color)
        
    def update(self):
        """Update power-up position and effects"""
        # Move with game speed
        self.x -= self.speed
        
        # Bobbing animation
        self.bob_offset = math.sin(pygame.time.get_ticks() * self.bob_speed) * 5
        
        # Rotation animation
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation = 0
            
    def draw(self, screen):
        """Draw power-up with effects"""
        if self.collected:
            return
            
        # Apply bobbing and rotation
        y_pos = self.y + self.bob_offset
        
        # Rotate sprite
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        rect = rotated_sprite.get_rect(center=(self.x + self.width // 2, y_pos + self.height // 2))
        
        # Draw glow effect
        glow_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        glow_color = (*self.sprite.get_at((0, 0))[:3], 50)
        pygame.draw.circle(glow_surface, glow_color, 
                         (glow_surface.get_width() // 2, glow_surface.get_height() // 2), 
                         self.width // 2 + 5)
        
        glow_rect = glow_surface.get_rect(center=rect.center)
        screen.blit(glow_surface, glow_rect)
        
        # Draw main sprite
        screen.blit(rotated_sprite, rect)
        
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y + self.bob_offset, self.width, self.height)
        
    def is_off_screen(self):
        """Check if power-up is off screen"""
        return self.x + self.width < 0
        
    def collect(self):
        """Mark power-up as collected"""
        self.collected = True

class PowerUpManager:
    """Manages all power-ups in the game"""
    
    def __init__(self, audio_manager):
        self.power_ups = []
        self.active_effects = {}
        self.audio_manager = audio_manager
        
        # Spawn settings
        self.spawn_chance = 0.005  # Very low chance per frame
        self.min_spawn_distance = 800
        self.last_spawn_x = 0
        
    def update(self, game_speed, dino_rect):
        """Update all power-ups"""
        # Update existing power-ups
        for power_up in self.power_ups[:]:
            power_up.speed = game_speed
            power_up.update()
            
            # Check collision with dino
            if not power_up.collected and power_up.get_rect().colliderect(dino_rect):
                self.collect_power_up(power_up)
                
            # Remove off-screen power-ups
            if power_up.is_off_screen():
                self.power_ups.remove(power_up)
                
        # Update active effects
        self.update_active_effects()
        
        # Spawn new power-ups
        self.try_spawn_power_up()
        
    def try_spawn_power_up(self):
        """Try to spawn a new power-up"""
        if random.random() < self.spawn_chance:
            # Check if enough distance from last spawn
            spawn_x = SCREEN_WIDTH + 50
            if spawn_x - self.last_spawn_x >= self.min_spawn_distance:
                self.spawn_power_up(spawn_x)
                self.last_spawn_x = spawn_x
                
    def spawn_power_up(self, x):
        """Spawn a random power-up"""
        # Choose random power-up type
        power_type = random.choice(list(PowerUpType))
        
        # Spawn at different heights
        y_positions = [GROUND_Y - 150, GROUND_Y - 100, GROUND_Y - 200]
        y = random.choice(y_positions)
        
        power_up = PowerUp(x, y, power_type)
        self.power_ups.append(power_up)
        
    def collect_power_up(self, power_up):
        """Handle power-up collection"""
        power_up.collect()
        self.activate_power_up(power_up.power_type)
        
        # Play collection sound
        if self.audio_manager:
            self.audio_manager.play_sound('score')
            
    def activate_power_up(self, power_type):
        """Activate a power-up effect"""
        current_time = pygame.time.get_ticks()
        
        self.active_effects[power_type] = {
            'start_time': current_time,
            'duration': POWERUP_DURATION,
            'active': True
        }
        
        # Apply immediate effects
        if power_type == PowerUpType.SHIELD:
            print("Shield activated!")
        elif power_type == PowerUpType.SLOW_MOTION:
            print("Slow motion activated!")
        elif power_type == PowerUpType.DOUBLE_JUMP:
            print("Double jump activated!")
        elif power_type == PowerUpType.SCORE_MULTIPLIER:
            print("Score multiplier activated!")
        elif power_type == PowerUpType.INVINCIBILITY:
            print("Invincibility activated!")
            
    def update_active_effects(self):
        """Update and expire active power-up effects"""
        current_time = pygame.time.get_ticks()
        
        for power_type, effect in list(self.active_effects.items()):
            if effect['active']:
                elapsed = current_time - effect['start_time']
                if elapsed >= effect['duration']:
                    effect['active'] = False
                    self.deactivate_power_up(power_type)
                    
    def deactivate_power_up(self, power_type):
        """Deactivate a power-up effect"""
        if power_type in self.active_effects:
            del self.active_effects[power_type]
            
        # Remove effects
        if power_type == PowerUpType.SHIELD:
            print("Shield deactivated!")
        elif power_type == PowerUpType.SLOW_MOTION:
            print("Slow motion deactivated!")
        elif power_type == PowerUpType.DOUBLE_JUMP:
            print("Double jump deactivated!")
        elif power_type == PowerUpType.SCORE_MULTIPLIER:
            print("Score multiplier deactivated!")
        elif power_type == PowerUpType.INVINCIBILITY:
            print("Invincibility deactivated!")
            
    def is_power_up_active(self, power_type):
        """Check if a specific power-up is active"""
        return (power_type in self.active_effects and 
                self.active_effects[power_type]['active'])
                
    def get_remaining_time(self, power_type):
        """Get remaining time for a power-up effect"""
        if not self.is_power_up_active(power_type):
            return 0
            
        effect = self.active_effects[power_type]
        elapsed = pygame.time.get_ticks() - effect['start_time']
        remaining = max(0, effect['duration'] - elapsed)
        return remaining
        
    def draw(self, screen):
        """Draw all power-ups"""
        for power_up in self.power_ups:
            power_up.draw(screen)
            
    def draw_active_effects_ui(self, screen):
        """Draw UI indicators for active power-ups"""
        y_offset = 150
        
        for power_type, effect in self.active_effects.items():
            if effect['active']:
                remaining = self.get_remaining_time(power_type)
                seconds = remaining // 1000
                
                # Draw power-up icon
                icon_size = 24
                icon_x = 20
                icon_y = y_offset
                
                colors = {
                    PowerUpType.SHIELD: (0, 255, 255),
                    PowerUpType.SLOW_MOTION: (255, 255, 0),
                    PowerUpType.DOUBLE_JUMP: (255, 0, 255),
                    PowerUpType.SCORE_MULTIPLIER: (0, 255, 0),
                    PowerUpType.INVINCIBILITY: (255, 165, 0)
                }
                
                color = colors.get(power_type, (255, 255, 255))
                pygame.draw.rect(screen, color, (icon_x, icon_y, icon_size, icon_size))
                
                # Draw timer
                font = pygame.font.Font(None, 20)
                timer_text = font.render(f"{seconds}s", True, BLACK)
                screen.blit(timer_text, (icon_x + icon_size + 5, icon_y + 2))
                
                y_offset += 30
                
    def apply_shield_effect(self, collision_detected):
        """Apply shield effect to collision detection"""
        if self.is_power_up_active(PowerUpType.SHIELD):
            return False  # Ignore collision
        return collision_detected
        
    def apply_slow_motion_effect(self, game_speed):
        """Apply slow motion effect to game speed"""
        if self.is_power_up_active(PowerUpType.SLOW_MOTION):
            return game_speed * SLOWMO_FACTOR
        return game_speed
        
    def apply_score_multiplier_effect(self, score_gain):
        """Apply score multiplier effect"""
        if self.is_power_up_active(PowerUpType.SCORE_MULTIPLIER):
            return score_gain * 2
        return score_gain
        
    def can_double_jump(self):
        """Check if double jump is available"""
        return self.is_power_up_active(PowerUpType.DOUBLE_JUMP)
        
    def is_invincible(self):
        """Check if player is invincible"""
        return self.is_power_up_active(PowerUpType.INVINCIBILITY)
