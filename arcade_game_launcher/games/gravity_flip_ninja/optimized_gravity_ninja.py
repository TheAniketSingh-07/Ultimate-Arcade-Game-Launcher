#!/usr/bin/env python3
"""
Optimized Gravity Flip Ninja - Lag-Free Platformer
Ultra-smooth performance with proper physics and game speed
"""

import pygame
import sys
import random
import math

# Initialize Pygame with optimizations
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=256)

# Optimized Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TARGET_FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (64, 128, 255)
RED = (255, 64, 64)
GREEN = (64, 255, 64)
PURPLE = (128, 64, 255)
ORANGE = (255, 128, 64)
GRAY = (128, 128, 128)
DARK_BLUE = (32, 64, 128)

class OptimizedNinja:
    """Optimized ninja with smooth gravity flipping"""
    def __init__(self):
        self.x = 100
        self.y = WINDOW_HEIGHT // 2
        self.width = 20
        self.height = 30
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.gravity_direction = 1  # 1 for down, -1 for up
        self.speed = 5
        self.on_ground = False
        self.trail = []
        self.max_trail_length = 10
        
        # Animation
        self.rotation = 0
        self.target_rotation = 0
        self.flip_cooldown = 0
    
    def flip_gravity(self):
        if self.flip_cooldown <= 0:
            self.gravity_direction *= -1
            self.target_rotation += 180
            self.flip_cooldown = 10
            self.vel_y *= 0.5  # Reduce velocity on flip for smoother transition
    
    def update(self, dt):
        # Update cooldown
        self.flip_cooldown = max(0, self.flip_cooldown - 1)
        
        # Smooth rotation
        rotation_diff = self.target_rotation - self.rotation
        if abs(rotation_diff) > 180:
            if rotation_diff > 0:
                rotation_diff -= 360
            else:
                rotation_diff += 360
        self.rotation += rotation_diff * 0.2
        
        # Physics with delta time
        self.vel_y += self.gravity * self.gravity_direction * dt * 60
        
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        else:
            self.vel_x *= 0.8  # Friction
        
        # Apply velocity
        self.x += self.vel_x * dt * 60
        self.y += self.vel_y * dt * 60
        
        # Boundary collision
        if self.y <= 0:
            self.y = 0
            self.vel_y = 0
            self.on_ground = True if self.gravity_direction == -1 else False
        elif self.y >= WINDOW_HEIGHT - self.height:
            self.y = WINDOW_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True if self.gravity_direction == 1 else False
        else:
            self.on_ground = False
        
        # Keep ninja on screen horizontally
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
        
        # Update trail
        self.trail.append((self.x + self.width // 2, self.y + self.height // 2))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def draw(self, screen):
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            trail_color = (*BLUE, alpha)
            trail_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            trail_surface.fill(trail_color)
            screen.blit(trail_surface, (trail_x - 3, trail_y - 3))
        
        # Draw ninja body
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Create ninja surface for rotation
        ninja_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        
        # Draw ninja on surface
        pygame.draw.rect(ninja_surface, BLUE, (5, 5, self.width, self.height))
        
        # Draw ninja eyes
        eye_y = 8 if self.gravity_direction == 1 else self.height - 3
        pygame.draw.circle(ninja_surface, WHITE, (8, eye_y), 2)
        pygame.draw.circle(ninja_surface, WHITE, (self.width - 3, eye_y), 2)
        
        # Rotate and blit
        rotated_surface = pygame.transform.rotate(ninja_surface, self.rotation)
        rotated_rect = rotated_surface.get_rect(center=(center_x, center_y))
        screen.blit(rotated_surface, rotated_rect)
        
        # Draw gravity indicator
        indicator_y = center_y - 40 if self.gravity_direction == 1 else center_y + 40
        arrow_points = [
            (center_x, indicator_y),
            (center_x - 5, indicator_y + (10 * self.gravity_direction)),
            (center_x + 5, indicator_y + (10 * self.gravity_direction))
        ]
        pygame.draw.polygon(screen, ORANGE, arrow_points)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class OptimizedObstacle:
    """Optimized obstacle with smooth movement"""
    def __init__(self, x, y, width, height, obstacle_type="static"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type
        self.speed = 3
        self.original_y = y
        self.time_offset = random.random() * math.pi * 2
        
        if obstacle_type == "moving":
            self.color = RED
        elif obstacle_type == "spike":
            self.color = PURPLE
        else:
            self.color = GRAY
    
    def update(self, dt, game_speed):
        self.x -= self.speed * game_speed * dt * 60
        
        if self.type == "moving":
            # Smooth vertical movement
            self.time_offset += 2 * dt * 60
            self.y = self.original_y + math.sin(self.time_offset / 30) * 50
    
    def draw(self, screen):
        if self.type == "spike":
            # Draw spikes
            points = [
                (self.x, self.y + self.height),
                (self.x + self.width // 2, self.y),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, self.color, points)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # Add some detail
            if self.type == "moving":
                pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class OptimizedParticle:
    """Optimized particle system"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.color = color
        self.life = 30
        self.max_life = 30
    
    def update(self, dt):
        self.x += self.vel_x * dt * 60
        self.y += self.vel_y * dt * 60
        self.life -= 1
        self.vel_x *= 0.98
        self.vel_y *= 0.98
    
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        particle_color = (*self.color, alpha)
        particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        particle_surface.fill(particle_color)
        screen.blit(particle_surface, (self.x, self.y))
    
    def is_dead(self):
        return self.life <= 0

class OptimizedGravityNinja:
    """Ultra-optimized Gravity Ninja game"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🥷 Optimized Gravity Ninja - Ultra Smooth!")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.ninja = OptimizedNinja()
        self.obstacles = []
        self.particles = []
        
        # Game state
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_speed = 1.0
        self.running = True
        self.game_over = False
        self.level = 1
        
        # Timers
        self.obstacle_timer = 0
        self.speed_increase_timer = 0
        self.particle_timer = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Background stars
        self.stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(50)]
    
    def load_high_score(self):
        try:
            with open("gravity_ninja_high_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open("gravity_ninja_high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.game_over:
                        self.restart_game()
                    else:
                        self.ninja.flip_gravity()
                        # Add flip particles
                        for _ in range(5):
                            particle = OptimizedParticle(
                                self.ninja.x + self.ninja.width // 2,
                                self.ninja.y + self.ninja.height // 2,
                                ORANGE
                            )
                            self.particles.append(particle)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def spawn_obstacle(self):
        if self.obstacle_timer <= 0:
            obstacle_types = ["static", "moving", "spike"]
            obstacle_type = random.choice(obstacle_types)
            
            if obstacle_type == "spike":
                width = 30
                height = 40
                y = random.choice([0, WINDOW_HEIGHT - height])
            else:
                width = random.randint(20, 60)
                height = random.randint(30, 80)
                y = random.randint(50, WINDOW_HEIGHT - height - 50)
            
            obstacle = OptimizedObstacle(WINDOW_WIDTH + 50, y, width, height, obstacle_type)
            self.obstacles.append(obstacle)
            
            # Dynamic spawn rate
            base_spawn_time = 80
            spawn_time = max(30, base_spawn_time - int(self.level * 5))
            self.obstacle_timer = spawn_time + random.randint(-20, 20)
    
    def check_collisions(self):
        ninja_rect = self.ninja.get_rect()
        for obstacle in self.obstacles:
            obstacle_rect = obstacle.get_rect()
            if ninja_rect.colliderect(obstacle_rect):
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                
                # Add explosion particles
                for _ in range(20):
                    particle = OptimizedParticle(
                        self.ninja.x + self.ninja.width // 2,
                        self.ninja.y + self.ninja.height // 2,
                        RED
                    )
                    self.particles.append(particle)
                break
    
    def update(self, dt):
        if self.game_over:
            # Update particles even when game over
            for particle in self.particles[:]:
                particle.update(dt)
                if particle.is_dead():
                    self.particles.remove(particle)
            return
        
        # Update timers
        self.obstacle_timer -= 1
        self.speed_increase_timer += 1
        self.particle_timer += 1
        
        # Increase difficulty
        if self.speed_increase_timer >= 600:  # Every 10 seconds at 60 FPS
            self.game_speed += 0.1
            self.level += 1
            self.speed_increase_timer = 0
        
        # Update score
        self.score += int(self.game_speed * dt * 60)
        
        # Update game objects
        self.ninja.update(dt)
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(dt, self.game_speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)
        
        # Add ambient particles
        if self.particle_timer >= 10:
            if random.random() < 0.3:
                particle = OptimizedParticle(
                    WINDOW_WIDTH,
                    random.randint(0, WINDOW_HEIGHT),
                    random.choice([BLUE, PURPLE, GREEN])
                )
                particle.vel_x = -2
                self.particles.append(particle)
            self.particle_timer = 0
        
        # Spawn obstacles
        self.spawn_obstacle()
        
        # Check collisions
        self.check_collisions()
    
    def draw_background(self):
        # Gradient background
        for y in range(WINDOW_HEIGHT):
            color_ratio = y / WINDOW_HEIGHT
            r = int(DARK_BLUE[0] * (1 - color_ratio) + BLACK[0] * color_ratio)
            g = int(DARK_BLUE[1] * (1 - color_ratio) + BLACK[1] * color_ratio)
            b = int(DARK_BLUE[2] * (1 - color_ratio) + BLACK[2] * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
        
        # Draw stars
        for star_x, star_y in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star_x, star_y), 1)
    
    def draw_ui(self):
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # High score
        high_score_text = self.small_font.render(f"High: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (10, 50))
        
        # Level and speed
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 75))
        
        speed_text = self.small_font.render(f"Speed: {self.game_speed:.1f}x", True, WHITE)
        self.screen.blit(speed_text, (WINDOW_WIDTH - 120, 10))
        
        # Controls
        if not self.game_over:
            controls = ["Space/↑: Flip Gravity", "A/D or ←/→: Move", "ESC: Exit"]
            for i, control in enumerate(controls):
                control_text = self.small_font.render(control, True, WHITE)
                self.screen.blit(control_text, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 80 + i * 20))
    
    def draw_game_over(self):
        # Game over overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Level reached
        level_text = self.small_font.render(f"Level Reached: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        self.screen.blit(level_text, level_rect)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            new_high_text = self.small_font.render("NEW HIGH SCORE!", True, GREEN)
            new_high_rect = new_high_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(new_high_text, new_high_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        self.ninja = OptimizedNinja()
        self.obstacles = []
        self.particles = []
        self.score = 0
        self.game_speed = 1.0
        self.level = 1
        self.game_over = False
        self.obstacle_timer = 0
        self.speed_increase_timer = 0
    
    def draw(self):
        # Draw background
        self.draw_background()
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw ninja
        self.ninja.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        print("🥷 Optimized Gravity Ninja Started!")
        print("🎮 Ultra-smooth performance with proper physics!")
        print("🎯 Space/↑: Flip Gravity, A/D: Move, ESC: Exit")
        
        last_time = pygame.time.get_ticks()
        
        while self.running:
            # Calculate delta time for smooth gameplay
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Cap delta time to prevent large jumps
            dt = min(dt, 1/30)  # Max 30 FPS equivalent
            
            self.handle_events()
            self.update(dt)
            self.draw()
            self.clock.tick(TARGET_FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = OptimizedGravityNinja()
    game.run()

if __name__ == "__main__":
    main()
