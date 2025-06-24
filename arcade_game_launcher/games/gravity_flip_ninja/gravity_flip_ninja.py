#!/usr/bin/env python3
"""
Gravity Flip Ninja - Advanced Arcade Game
A stylish ninja game with gravity flipping mechanics, particle effects, and smooth animations
"""

import pygame
import math
import random
import sys
import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame and mixer for better audio
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()

# Game Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors with alpha support
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 50, 50)
    BLUE = (50, 150, 255)
    GREEN = (50, 255, 50)
    PURPLE = (150, 50, 255)
    ORANGE = (255, 150, 50)
    YELLOW = (255, 255, 50)
    DARK_BLUE = (20, 30, 60)
    NINJA_BLUE = (64, 128, 255)
    SHADOW = (0, 0, 0, 128)
    PARTICLE_COLORS = [(255, 100, 100), (100, 255, 100), (100, 100, 255), 
                      (255, 255, 100), (255, 100, 255), (100, 255, 255)]

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    size: float

class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
    
    def add_explosion(self, x: float, y: float, count: int = 15):
        """Add explosion particles"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(30, 60),
                max_life=60,
                color=random.choice(Colors.PARTICLE_COLORS),
                size=random.uniform(2, 5)
            ))
    
    def add_trail(self, x: float, y: float, color: Tuple[int, int, int]):
        """Add trail particles for ninja movement"""
        for _ in range(3):
            self.particles.append(Particle(
                x=x + random.uniform(-5, 5),
                y=y + random.uniform(-5, 5),
                vx=random.uniform(-1, 1),
                vy=random.uniform(-1, 1),
                life=random.uniform(15, 25),
                max_life=25,
                color=color,
                size=random.uniform(1, 3)
            ))
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.x += particle.vx
            particle.y += particle.vy
            particle.life -= 1
            particle.vy += 0.1  # Gravity effect on particles
            
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw all particles with alpha blending"""
        for particle in self.particles:
            alpha = int(255 * (particle.life / particle.max_life))
            color = (*particle.color, alpha)
            
            # Create a surface for alpha blending
            particle_surf = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, 
                             (particle.size, particle.size), particle.size)
            screen.blit(particle_surf, (particle.x - particle.size, particle.y - particle.size))

class Ninja:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.vx = 0
        self.vy = 0
        self.gravity = 0.8
        self.gravity_flipped = False
        self.jump_power = 15
        self.max_speed = 8
        self.on_ground = False
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        
        # Effects
        self.trail_timer = 0
        self.flip_cooldown = 0
        
    def update(self, particle_system: ParticleSystem):
        """Update ninja physics and animation"""
        # Apply gravity
        if self.gravity_flipped:
            self.vy -= self.gravity
        else:
            self.vy += self.gravity
        
        # Limit fall speed
        self.vy = max(-20, min(20, self.vy))
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Friction
        self.vx *= 0.95
        
        # Animation
        self.animation_timer += 1
        if self.animation_timer > 8:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
        
        # Trail effect
        self.trail_timer += 1
        if self.trail_timer > 3:
            self.trail_timer = 0
            particle_system.add_trail(self.x + self.width//2, self.y + self.height//2, 
                                    Colors.NINJA_BLUE)
        
        # Update cooldowns
        if self.flip_cooldown > 0:
            self.flip_cooldown -= 1
        
        # Keep ninja on screen horizontally
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
        
        # Check ground collision (simplified)
        if not self.gravity_flipped and self.y > WINDOW_HEIGHT - self.height - 50:
            self.y = WINDOW_HEIGHT - self.height - 50
            self.vy = 0
            self.on_ground = True
        elif self.gravity_flipped and self.y < 50:
            self.y = 50
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def jump(self):
        """Make ninja jump"""
        if self.on_ground:
            if self.gravity_flipped:
                self.vy = self.jump_power
            else:
                self.vy = -self.jump_power
            self.on_ground = False
    
    def move_left(self):
        """Move ninja left"""
        self.vx = max(-self.max_speed, self.vx - 1)
        self.facing_right = False
    
    def move_right(self):
        """Move ninja right"""
        self.vx = min(self.max_speed, self.vx + 1)
        self.facing_right = True
    
    def flip_gravity(self, particle_system: ParticleSystem):
        """Flip gravity with cooldown and effects"""
        if self.flip_cooldown <= 0:
            self.gravity_flipped = not self.gravity_flipped
            self.flip_cooldown = 30  # 0.5 second cooldown at 60 FPS
            self.vy *= 0.5  # Reduce velocity during flip
            
            # Add particle effect
            particle_system.add_explosion(self.x + self.width//2, self.y + self.height//2, 20)
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen: pygame.Surface):
        """Draw ninja with advanced graphics"""
        # Shadow effect
        shadow_surf = pygame.Surface((self.width + 4, self.height + 4), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, Colors.SHADOW, 
                          (0, 0, self.width + 4, self.height + 4))
        screen.blit(shadow_surf, (self.x - 2, self.y - 2))
        
        # Main ninja body
        ninja_color = Colors.NINJA_BLUE
        if self.gravity_flipped:
            ninja_color = Colors.PURPLE
        
        # Body
        pygame.draw.ellipse(screen, ninja_color, 
                          (self.x, self.y, self.width, self.height))
        
        # Eyes
        eye_size = 6
        eye_y = self.y + 10
        if self.facing_right:
            pygame.draw.circle(screen, Colors.WHITE, (int(self.x + 25), int(eye_y)), eye_size)
            pygame.draw.circle(screen, Colors.BLACK, (int(self.x + 27), int(eye_y)), 3)
        else:
            pygame.draw.circle(screen, Colors.WHITE, (int(self.x + 15), int(eye_y)), eye_size)
            pygame.draw.circle(screen, Colors.BLACK, (int(self.x + 13), int(eye_y)), 3)
        
        # Gravity indicator
        if self.gravity_flipped:
            # Up arrow
            points = [(self.x + self.width//2, self.y - 10),
                     (self.x + self.width//2 - 5, self.y - 5),
                     (self.x + self.width//2 + 5, self.y - 5)]
            pygame.draw.polygon(screen, Colors.PURPLE, points)
        
        # Cooldown indicator
        if self.flip_cooldown > 0:
            cooldown_width = int((self.flip_cooldown / 30) * self.width)
            pygame.draw.rect(screen, Colors.YELLOW, 
                           (self.x, self.y - 5, cooldown_width, 3))

class Obstacle:
    def __init__(self, x: float, y: float, width: float, height: float, obstacle_type: str = "spike"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type
        self.animation_offset = random.uniform(0, 2 * math.pi)
    
    def update(self):
        """Update obstacle (move left)"""
        self.x -= 5
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen: pygame.Surface):
        """Draw obstacle with effects"""
        if self.type == "spike":
            # Animated spikes
            points = []
            spike_count = int(self.width // 20)
            for i in range(spike_count + 1):
                base_x = self.x + i * 20
                if i < spike_count:
                    # Spike points
                    points.extend([
                        (base_x, self.y + self.height),
                        (base_x + 10, self.y),
                        (base_x + 20, self.y + self.height)
                    ])
            
            if points:
                pygame.draw.polygon(screen, Colors.RED, points)
                # Glow effect
                glow_surf = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
                pygame.draw.polygon(glow_surf, (*Colors.RED, 50), 
                                  [(p[0] - self.x + 5, p[1] - self.y + 5) for p in points])
                screen.blit(glow_surf, (self.x - 5, self.y - 5))
        
        elif self.type == "platform":
            # Moving platform
            pygame.draw.rect(screen, Colors.GREEN, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, Colors.WHITE, (self.x, self.y, self.width, self.height), 2)

class GravityFlipNinja:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🥷 Gravity Flip Ninja - Ultimate Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.high_score = self.load_high_score()
        
        # Game objects
        self.ninja = Ninja(100, WINDOW_HEIGHT - 100)
        self.obstacles: List[Obstacle] = []
        self.particle_system = ParticleSystem()
        
        # Background
        self.bg_stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) 
                        for _ in range(100)]
        self.bg_scroll = 0
        
        # Timing
        self.obstacle_timer = 0
        self.score_timer = 0
        
        # Effects
        self.screen_shake = 0
        self.flash_timer = 0
    
    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def reset_game(self):
        """Reset game to initial state"""
        self.ninja = Ninja(100, WINDOW_HEIGHT - 100)
        self.obstacles.clear()
        self.particle_system = ParticleSystem()
        self.score = 0
        self.obstacle_timer = 0
        self.score_timer = 0
        self.screen_shake = 0
        self.flash_timer = 0
    
    def handle_events(self):
        """Handle input events"""
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    else:
                        return False
                
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING
                        self.reset_game()
                
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.ninja.jump()
                    elif event.key == pygame.K_g or event.key == pygame.K_UP:
                        self.ninja.flip_gravity(self.particle_system)
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.MENU
                    elif event.key == pygame.K_r:
                        self.state = GameState.PLAYING
                        self.reset_game()
        
        # Continuous input for movement
        if self.state == GameState.PLAYING:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.ninja.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.ninja.move_right()
        
        return True
    
    def update(self):
        """Update game logic"""
        if self.state != GameState.PLAYING:
            return
        
        # Update ninja
        self.ninja.update(self.particle_system)
        
        # Update particles
        self.particle_system.update()
        
        # Spawn obstacles
        self.obstacle_timer += 1
        if self.obstacle_timer > max(60 - self.score // 100, 30):  # Increase difficulty
            self.obstacle_timer = 0
            self.spawn_obstacle()
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
        
        # Check collisions
        ninja_rect = self.ninja.get_rect()
        for obstacle in self.obstacles:
            if ninja_rect.colliderect(obstacle.get_rect()):
                self.game_over()
                return
        
        # Check if ninja falls off screen
        if self.ninja.y > WINDOW_HEIGHT + 100 or self.ninja.y < -100:
            self.game_over()
            return
        
        # Update score
        self.score_timer += 1
        if self.score_timer > 10:
            self.score_timer = 0
            self.score += 1
        
        # Update effects
        if self.screen_shake > 0:
            self.screen_shake -= 1
        if self.flash_timer > 0:
            self.flash_timer -= 1
        
        # Update background
        self.bg_scroll += 2
        if self.bg_scroll > WINDOW_WIDTH:
            self.bg_scroll = 0
    
    def spawn_obstacle(self):
        """Spawn a new obstacle"""
        obstacle_type = random.choice(["spike", "platform"])
        
        if obstacle_type == "spike":
            height = random.randint(40, 80)
            if random.choice([True, False]):
                # Ground spikes
                y = WINDOW_HEIGHT - height - 50
            else:
                # Ceiling spikes
                y = 50
            
            self.obstacles.append(Obstacle(WINDOW_WIDTH, y, 60, height, "spike"))
        
        elif obstacle_type == "platform":
            width = random.randint(80, 120)
            height = 20
            y = random.randint(200, WINDOW_HEIGHT - 200)
            self.obstacles.append(Obstacle(WINDOW_WIDTH, y, width, height, "platform"))
    
    def game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER
        self.screen_shake = 30
        self.flash_timer = 10
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        # Add explosion effect
        self.particle_system.add_explosion(self.ninja.x + self.ninja.width//2, 
                                         self.ninja.y + self.ninja.height//2, 30)
    
    def draw_background(self):
        """Draw animated background"""
        # Gradient background
        for y in range(WINDOW_HEIGHT):
            color_ratio = y / WINDOW_HEIGHT
            r = int(20 + color_ratio * 40)
            g = int(30 + color_ratio * 60)
            b = int(60 + color_ratio * 100)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
        
        # Animated stars
        for i, (x, y) in enumerate(self.bg_stars):
            brightness = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.01 + i))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), 1)
    
    def draw_ui(self):
        """Draw user interface"""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, Colors.WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # High score
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, Colors.YELLOW)
        self.screen.blit(high_score_text, (20, 70))
        
        # Controls hint
        if self.score < 100:  # Show for new players
            controls_text = self.font_small.render("SPACE: Jump | G/↑: Flip Gravity | ←→: Move", True, Colors.WHITE)
            self.screen.blit(controls_text, (20, WINDOW_HEIGHT - 40))
    
    def draw_menu(self):
        """Draw main menu"""
        self.draw_background()
        
        # Title with glow effect
        title_text = self.font_large.render("GRAVITY FLIP NINJA", True, Colors.WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        
        # Glow effect
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_text = self.font_large.render("GRAVITY FLIP NINJA", True, Colors.NINJA_BLUE)
            glow_rect = glow_text.get_rect(center=(WINDOW_WIDTH//2 + offset[0], WINDOW_HEIGHT//2 - 100 + offset[1]))
            self.screen.blit(glow_text, glow_rect)
        
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Press SPACE to Start",
            "Use ARROW KEYS or WASD to move",
            "Press SPACE to jump",
            "Press G or UP ARROW to flip gravity",
            "Avoid obstacles and survive as long as possible!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = Colors.WHITE if i == 0 else Colors.YELLOW
            font = self.font_medium if i == 0 else self.font_small
            text = font.render(instruction, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + i * 40))
            self.screen.blit(text, text_rect)
        
        # High score display
        if self.high_score > 0:
            high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, Colors.GREEN)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 100))
            self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.draw_background()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.BLACK, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, Colors.RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, Colors.WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            new_record_text = self.font_medium.render("NEW HIGH SCORE!", True, Colors.YELLOW)
            new_record_rect = new_record_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(new_record_text, new_record_rect)
        else:
            high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, Colors.YELLOW)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Options
        restart_text = self.font_small.render("Press R to Restart or SPACE for Menu", True, Colors.WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_paused(self):
        """Draw pause screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*Colors.BLACK, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, Colors.BLUE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
        # Resume instruction
        resume_text = self.font_small.render("Press ESC to Resume", True, Colors.WHITE)
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        self.screen.blit(resume_text, resume_rect)
    
    def draw(self):
        """Main draw function"""
        # Screen shake effect
        shake_x = shake_y = 0
        if self.screen_shake > 0:
            shake_x = random.randint(-5, 5)
            shake_y = random.randint(-5, 5)
        
        # Clear screen
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        else:
            # Game screen
            self.draw_background()
            
            # Draw game objects with shake
            temp_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            temp_surface.fill(Colors.BLACK)
            self.draw_background()
            
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            # Draw ninja
            self.ninja.draw(self.screen)
            
            # Draw particles
            self.particle_system.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Apply screen shake
            if self.screen_shake > 0:
                self.screen.blit(temp_surface, (shake_x, shake_y))
            
            # Flash effect
            if self.flash_timer > 0:
                flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                flash_surface.fill((*Colors.WHITE, 100))
                self.screen.blit(flash_surface, (0, 0))
            
            # Pause overlay
            if self.state == GameState.PAUSED:
                self.draw_paused()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    """Main function"""
    try:
        game = GravityFlipNinja()
        game.run()
    except Exception as e:
        print(f"Error running Gravity Flip Ninja: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
