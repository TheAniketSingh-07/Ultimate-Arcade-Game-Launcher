"""
Advanced Visual Effects for Gravity Flip Ninja
Additional effects and utilities for enhanced graphics
"""

import pygame
import math
import random
from typing import List, Tuple

class AdvancedEffects:
    """Collection of advanced visual effects"""
    
    @staticmethod
    def create_glow_surface(size: Tuple[int, int], color: Tuple[int, int, int], intensity: float = 1.0):
        """Create a glowing surface with radial gradient"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        center_x, center_y = size[0] // 2, size[1] // 2
        max_radius = min(center_x, center_y)
        
        for radius in range(max_radius, 0, -1):
            alpha = int(255 * (1 - radius / max_radius) * intensity)
            glow_color = (*color, alpha)
            
            # Create temporary surface for alpha blending
            temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, glow_color, (radius, radius), radius)
            
            # Blit to main surface
            surface.blit(temp_surf, (center_x - radius, center_y - radius))
        
        return surface
    
    @staticmethod
    def create_lightning_effect(start: Tuple[int, int], end: Tuple[int, int], 
                               segments: int = 10, deviation: float = 20.0):
        """Create lightning bolt points between two positions"""
        points = [start]
        
        for i in range(1, segments):
            progress = i / segments
            
            # Linear interpolation
            x = start[0] + (end[0] - start[0]) * progress
            y = start[1] + (end[1] - start[1]) * progress
            
            # Add random deviation
            x += random.uniform(-deviation, deviation)
            y += random.uniform(-deviation, deviation)
            
            points.append((int(x), int(y)))
        
        points.append(end)
        return points
    
    @staticmethod
    def draw_energy_field(surface: pygame.Surface, center: Tuple[int, int], 
                         radius: float, color: Tuple[int, int, int], time: float):
        """Draw animated energy field around a point"""
        num_rays = 12
        for i in range(num_rays):
            angle = (i / num_rays) * 2 * math.pi + time * 0.05
            
            # Inner and outer points
            inner_radius = radius * 0.7
            outer_radius = radius * (1.0 + 0.3 * math.sin(time * 0.1 + i))
            
            inner_x = center[0] + math.cos(angle) * inner_radius
            inner_y = center[1] + math.sin(angle) * inner_radius
            outer_x = center[0] + math.cos(angle) * outer_radius
            outer_y = center[1] + math.sin(angle) * outer_radius
            
            # Draw energy ray
            pygame.draw.line(surface, color, (inner_x, inner_y), (outer_x, outer_y), 2)
    
    @staticmethod
    def create_ripple_effect(surface: pygame.Surface, center: Tuple[int, int], 
                           radius: float, color: Tuple[int, int, int], thickness: int = 3):
        """Create ripple effect at specified position"""
        if radius > 0:
            pygame.draw.circle(surface, color, center, int(radius), thickness)
            
            # Inner ripple
            if radius > 10:
                inner_radius = radius * 0.6
                inner_color = (*color[:3], max(0, color[3] // 2) if len(color) > 3 else 128)
                pygame.draw.circle(surface, inner_color, center, int(inner_radius), thickness // 2)

class ParticleEffects:
    """Advanced particle effect systems"""
    
    @staticmethod
    def create_spiral_particles(center: Tuple[float, float], count: int = 20):
        """Create particles in a spiral pattern"""
        particles = []
        for i in range(count):
            angle = (i / count) * 4 * math.pi  # Two full rotations
            radius = i * 2
            
            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius
            
            # Velocity pointing outward
            vx = math.cos(angle) * 3
            vy = math.sin(angle) * 3
            
            particles.append({
                'x': x, 'y': y, 'vx': vx, 'vy': vy,
                'life': 60, 'max_life': 60,
                'color': (100 + i * 5, 150, 255 - i * 3),
                'size': 3 - i * 0.1
            })
        
        return particles
    
    @staticmethod
    def create_gravity_particles(center: Tuple[float, float], gravity_up: bool = False):
        """Create particles that respond to gravity direction"""
        particles = []
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            
            particles.append({
                'x': center[0] + random.uniform(-10, 10),
                'y': center[1] + random.uniform(-10, 10),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'gravity': -0.2 if gravity_up else 0.2,
                'life': 45,
                'max_life': 45,
                'color': (150, 50, 255) if gravity_up else (50, 150, 255),
                'size': random.uniform(2, 4)
            })
        
        return particles

class AnimationHelpers:
    """Helper functions for smooth animations"""
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """Smooth easing function (0 to 1)"""
        return t * t * (3.0 - 2.0 * t)
    
    @staticmethod
    def bounce_ease(t: float) -> float:
        """Bouncing easing function"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)
    
    @staticmethod
    def elastic_ease(t: float) -> float:
        """Elastic easing function"""
        if t == 0 or t == 1:
            return t
        
        p = 0.3
        s = p / 4
        return -(2 ** (10 * (t - 1))) * math.sin((t - 1 - s) * (2 * math.pi) / p)
    
    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """Linear interpolation"""
        return start + (end - start) * t
    
    @staticmethod
    def lerp_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Interpolate between two colors"""
        return (
            int(AnimationHelpers.lerp(color1[0], color2[0], t)),
            int(AnimationHelpers.lerp(color1[1], color2[1], t)),
            int(AnimationHelpers.lerp(color1[2], color2[2], t))
        )

class SoundEffectHooks:
    """Placeholder for sound effect integration"""
    
    @staticmethod
    def play_jump_sound():
        """Hook for jump sound effect"""
        # Placeholder for sound implementation
        pass
    
    @staticmethod
    def play_gravity_flip_sound():
        """Hook for gravity flip sound effect"""
        # Placeholder for sound implementation
        pass
    
    @staticmethod
    def play_collision_sound():
        """Hook for collision sound effect"""
        # Placeholder for sound implementation
        pass
    
    @staticmethod
    def play_score_sound():
        """Hook for score increase sound effect"""
        # Placeholder for sound implementation
        pass
