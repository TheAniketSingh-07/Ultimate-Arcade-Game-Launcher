"""
Dino Run Utility Functions
Helper functions for collision detection, math, and other utilities
"""

import pygame
import math
import random

def check_collision(rect1, rect2):
    """
    Check if two rectangles collide
    Returns True if collision detected, False otherwise
    """
    return rect1.colliderect(rect2)

def check_collision_with_margin(rect1, rect2, margin=5):
    """
    Check collision with a margin for more forgiving gameplay
    """
    # Shrink rectangles by margin amount
    shrunk_rect1 = pygame.Rect(
        rect1.x + margin,
        rect1.y + margin,
        rect1.width - 2 * margin,
        rect1.height - 2 * margin
    )
    
    shrunk_rect2 = pygame.Rect(
        rect2.x + margin,
        rect2.y + margin,
        rect2.width - 2 * margin,
        rect2.height - 2 * margin
    )
    
    return shrunk_rect1.colliderect(shrunk_rect2)

def distance_between_points(x1, y1, x2, y2):
    """Calculate distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def clamp(value, min_value, max_value):
    """Clamp a value between min and max"""
    return max(min_value, min(value, max_value))

def lerp(start, end, factor):
    """Linear interpolation between start and end"""
    return start + (end - start) * factor

def ease_in_out(t):
    """Ease in-out function for smooth animations"""
    return t * t * (3.0 - 2.0 * t)

def random_range(min_val, max_val):
    """Generate random float between min and max"""
    return random.uniform(min_val, max_val)

def random_choice_weighted(choices, weights):
    """Choose random item from list with weights"""
    return random.choices(choices, weights=weights)[0]

def load_image(path, scale=None, convert_alpha=True):
    """
    Load and optionally scale an image
    Returns pygame Surface or None if failed
    """
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
            
        if scale:
            image = pygame.transform.scale(image, scale)
            
        return image
    except pygame.error as e:
        print(f"Could not load image {path}: {e}")
        return None

def create_placeholder_surface(width, height, color=(255, 0, 255)):
    """Create a colored rectangle as placeholder for missing images"""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface

def wrap_text(text, font, max_width):
    """
    Wrap text to fit within max_width
    Returns list of text lines
    """
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                
    if current_line:
        lines.append(' '.join(current_line))
        
    return lines

def format_time(milliseconds):
    """Format milliseconds into MM:SS format"""
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def format_score(score):
    """Format score with commas for readability"""
    return f"{score:,}"

def get_high_score():
    """Get high score from file (placeholder implementation)"""
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(score):
    """Save high score to file (placeholder implementation)"""
    try:
        current_high = get_high_score()
        if score > current_high:
            with open('high_score.txt', 'w') as f:
                f.write(str(score))
            return True
    except:
        pass
    return False

def create_gradient_surface(width, height, start_color, end_color, vertical=True):
    """Create a gradient surface"""
    surface = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            ratio = y / height
            color = [
                int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                for i in range(3)
            ]
            pygame.draw.line(surface, color, (0, y), (width, y))
    else:
        for x in range(width):
            ratio = x / width
            color = [
                int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                for i in range(3)
            ]
            pygame.draw.line(surface, color, (x, 0), (x, height))
            
    return surface

def shake_screen(intensity, duration):
    """Generate screen shake offset values"""
    if duration <= 0:
        return 0, 0
        
    shake_x = random.randint(-intensity, intensity)
    shake_y = random.randint(-intensity, intensity)
    
    return shake_x, shake_y
