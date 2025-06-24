"""
Smooth Player Character
Advanced player with smooth movement, animations, and effects
"""

import pygame
import math
import random
from settings import *

class Player:
    """Smooth-moving player character with visual effects"""
    
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * CELL_SIZE + CELL_SIZE // 2
        self.pixel_y = y * CELL_SIZE + CELL_SIZE // 2
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        
        # Movement and animation
        self.speed = PLAYER_SPEED
        self.is_moving = False
        self.move_progress = 0.0
        
        # Visual effects
        self.trail = []
        self.particles = []
        self.glow_radius = PLAYER_SIZE + 5
        self.glow_pulse = 0
        
        # Animation states
        self.bounce_offset = 0
        self.rotation = 0
        
    def move(self, dx, dy, maze):
        """Initiate smooth movement if path is clear"""
        if self.is_moving:
            return False
            
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy
        
        # Check if move is valid
        if (0 <= new_grid_x < len(maze[0]) and 
            0 <= new_grid_y < len(maze) and 
            maze[new_grid_y][new_grid_x] == 0):
            
            # Start smooth movement
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.target_x = new_grid_x * CELL_SIZE + CELL_SIZE // 2
            self.target_y = new_grid_y * CELL_SIZE + CELL_SIZE // 2
            self.is_moving = True
            self.move_progress = 0.0
            
            # Add trail point
            self.trail.append((self.pixel_x, self.pixel_y))
            if len(self.trail) > TRAIL_LENGTH:
                self.trail.pop(0)
                
            # Add movement particles
            self._add_particles()
            
            return True
        return False
    
    def update(self):
        """Update player position and animations"""
        if self.is_moving:
            # Smooth interpolation
            self.move_progress += self.speed * 0.1
            if self.move_progress >= 1.0:
                self.move_progress = 1.0
                self.is_moving = False
            
            # Easing function for smooth movement
            t = self._ease_in_out_cubic(self.move_progress)
            
            start_x = self.pixel_x
            start_y = self.pixel_y
            
            self.pixel_x = start_x + (self.target_x - start_x) * t
            self.pixel_y = start_y + (self.target_y - start_y) * t
        
        # Update animations
        self.glow_pulse += 0.1
        self.bounce_offset = math.sin(pygame.time.get_ticks() * 0.01) * 2
        self.rotation += 2
        
        # Update particles
        self._update_particles()
    
    def _ease_in_out_cubic(self, t):
        """Smooth easing function"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def _add_particles(self):
        """Add movement particles for visual effect"""
        for _ in range(PARTICLE_COUNT):
            particle = {
                'x': self.pixel_x + random.randint(-5, 5),
                'y': self.pixel_y + random.randint(-5, 5),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': 30,
                'max_life': 30,
                'color': PLAYER_TRAIL_COLOR
            }
            self.particles.append(particle)
    
    def _update_particles(self):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vx'] *= 0.98  # Friction
            particle['vy'] *= 0.98
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Draw player with all visual effects"""
        # Draw trail
        self._draw_trail(screen)
        
        # Draw particles
        self._draw_particles(screen)
        
        # Draw glow effect
        self._draw_glow(screen)
        
        # Draw main player
        self._draw_player(screen)
    
    def _draw_trail(self, screen):
        """Draw smooth trail behind player"""
        if len(self.trail) > 1:
            for i, (x, y) in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)) * 0.5)
                size = int(PLAYER_SIZE * 0.3 * (i / len(self.trail)))
                if size > 0:
                    trail_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                    color = (*PLAYER_TRAIL_COLOR, alpha)
                    pygame.draw.circle(trail_surface, color, (size, size), size)
                    screen.blit(trail_surface, (x - size, y - size))
    
    def _draw_particles(self, screen):
        """Draw particle effects"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            size = max(1, int(3 * (particle['life'] / particle['max_life'])))
            
            particle_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            color = (*particle['color'], alpha)
            pygame.draw.circle(particle_surface, color, (size, size), size)
            screen.blit(particle_surface, (particle['x'] - size, particle['y'] - size))
    
    def _draw_glow(self, screen):
        """Draw glow effect around player"""
        glow_size = self.glow_radius + math.sin(self.glow_pulse) * 3
        glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        
        # Create gradient glow
        for i in range(int(glow_size), 0, -2):
            alpha = int(30 * (i / glow_size))
            color = (*PLAYER_COLOR, alpha)
            pygame.draw.circle(glow_surface, color, (int(glow_size), int(glow_size)), i)
        
        screen.blit(glow_surface, (self.pixel_x - glow_size, self.pixel_y - glow_size + self.bounce_offset))
    
    def _draw_player(self, screen):
        """Draw the main player character"""
        # Main body with bounce animation
        y_pos = self.pixel_y + self.bounce_offset
        
        # Outer ring
        pygame.draw.circle(screen, WHITE, (int(self.pixel_x), int(y_pos)), PLAYER_SIZE + 2)
        
        # Main body
        pygame.draw.circle(screen, PLAYER_COLOR, (int(self.pixel_x), int(y_pos)), PLAYER_SIZE)
        
        # Inner highlight
        highlight_offset = 3
        pygame.draw.circle(screen, LIGHT_BLUE, 
                         (int(self.pixel_x - highlight_offset), int(y_pos - highlight_offset)), 
                         PLAYER_SIZE // 3)
        
        # Rotating inner element
        angle = math.radians(self.rotation)
        inner_x = self.pixel_x + math.cos(angle) * 5
        inner_y = y_pos + math.sin(angle) * 5
        pygame.draw.circle(screen, WHITE, (int(inner_x), int(inner_y)), 3)
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.pixel_x - PLAYER_SIZE//2, 
                          self.pixel_y - PLAYER_SIZE//2, 
                          PLAYER_SIZE, PLAYER_SIZE)
