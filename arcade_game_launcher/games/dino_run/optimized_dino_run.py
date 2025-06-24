#!/usr/bin/env python3
"""
Optimized Dino Run - Lag-Free Endless Runner
Ultra-smooth performance with proper game speed control
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
WINDOW_HEIGHT = 400
TARGET_FPS = 60
GROUND_HEIGHT = 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

class OptimizedDino:
    """Optimized Dino with smooth animations"""
    def __init__(self):
        self.x = 80
        self.y = WINDOW_HEIGHT - GROUND_HEIGHT - 40
        self.width = 30
        self.height = 40
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.is_jumping = False
        self.is_ducking = False
        self.ground_y = WINDOW_HEIGHT - GROUND_HEIGHT - 40
        
        # Animation
        self.run_frame = 0
        self.animation_speed = 0.2
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_strength
            self.is_jumping = True
    
    def duck(self, ducking):
        self.is_ducking = ducking
        if ducking:
            self.height = 20
            self.y = self.ground_y + 20
        else:
            self.height = 40
            if not self.is_jumping:
                self.y = self.ground_y
    
    def update(self, dt):
        # Physics with delta time
        if self.is_jumping:
            self.vel_y += self.gravity
            self.y += self.vel_y
            
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.vel_y = 0
                self.is_jumping = False
        
        # Animation
        self.run_frame += self.animation_speed * dt * 60
        if self.run_frame >= 4:
            self.run_frame = 0
    
    def draw(self, screen):
        # Draw dino body
        color = GREEN
        if self.is_ducking:
            # Ducking pose
            pygame.draw.ellipse(screen, color, (self.x, self.y + 10, self.width, self.height))
        else:
            # Standing/jumping pose
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Draw eye
        eye_x = self.x + self.width - 8
        eye_y = self.y + 5 if not self.is_ducking else self.y + 15
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)
        
        # Draw legs (animated)
        if not self.is_ducking and not self.is_jumping:
            leg_offset = int(self.run_frame) % 2 * 4
            pygame.draw.rect(screen, color, (self.x + 5 + leg_offset, self.y + self.height, 6, 8))
            pygame.draw.rect(screen, color, (self.x + 15 - leg_offset, self.y + self.height, 6, 8))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class OptimizedObstacle:
    """Optimized obstacle with smooth movement"""
    def __init__(self, x, obstacle_type="cactus"):
        self.x = x
        self.type = obstacle_type
        self.speed = 6
        
        if obstacle_type == "cactus":
            self.width = 20
            self.height = 40
            self.y = WINDOW_HEIGHT - GROUND_HEIGHT - self.height
            self.color = GREEN
        elif obstacle_type == "bird":
            self.width = 25
            self.height = 15
            self.y = WINDOW_HEIGHT - GROUND_HEIGHT - 80
            self.color = GRAY
            self.flap_frame = 0
        else:  # rock
            self.width = 30
            self.height = 20
            self.y = WINDOW_HEIGHT - GROUND_HEIGHT - self.height
            self.color = GRAY
    
    def update(self, dt, game_speed):
        self.x -= self.speed * game_speed * dt * 60
        
        if self.type == "bird":
            self.flap_frame += 0.3 * dt * 60
    
    def draw(self, screen):
        if self.type == "cactus":
            # Draw cactus
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Cactus arms
            pygame.draw.rect(screen, self.color, (self.x - 8, self.y + 10, 8, 15))
            pygame.draw.rect(screen, self.color, (self.x + self.width, self.y + 15, 8, 10))
        elif self.type == "bird":
            # Draw bird with flapping animation
            wing_offset = int(self.flap_frame) % 2 * 3
            pygame.draw.ellipse(screen, self.color, (self.x, self.y - wing_offset, self.width, self.height))
            # Wings
            pygame.draw.ellipse(screen, self.color, (self.x - 5, self.y - wing_offset - 2, 10, 5))
            pygame.draw.ellipse(screen, self.color, (self.x + self.width - 5, self.y - wing_offset - 2, 10, 5))
        else:  # rock
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class OptimizedCloud:
    """Optimized background cloud"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.size = random.randint(30, 60)
    
    def update(self, dt, game_speed):
        self.x -= self.speed * game_speed * dt * 60
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.circle(screen, WHITE, (int(self.x + self.size // 3), int(self.y)), self.size // 3)
        pygame.draw.circle(screen, WHITE, (int(self.x - self.size // 3), int(self.y)), self.size // 3)
    
    def is_off_screen(self):
        return self.x + self.size < 0

class OptimizedDinoGame:
    """Ultra-optimized Dino Run game"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🦕 Optimized Dino Run - Ultra Smooth!")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.dino = OptimizedDino()
        self.obstacles = []
        self.clouds = []
        
        # Game state
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_speed = 1.0
        self.running = True
        self.game_over = False
        
        # Timers
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.speed_increase_timer = 0
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize clouds
        for i in range(3):
            cloud = OptimizedCloud(random.randint(0, WINDOW_WIDTH), random.randint(50, 150))
            self.clouds.append(cloud)
    
    def load_high_score(self):
        try:
            with open("dino_high_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0
    
    def save_high_score(self):
        try:
            with open("dino_high_score.txt", "w") as f:
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
                        self.dino.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        self.dino.duck(keys[pygame.K_DOWN] or keys[pygame.K_s])
    
    def spawn_obstacle(self):
        if self.obstacle_timer <= 0:
            obstacle_types = ["cactus", "bird", "rock"]
            obstacle_type = random.choice(obstacle_types)
            obstacle = OptimizedObstacle(WINDOW_WIDTH + 50, obstacle_type)
            self.obstacles.append(obstacle)
            
            # Dynamic spawn rate based on speed
            base_spawn_time = 90
            spawn_time = max(30, base_spawn_time - int(self.game_speed * 20))
            self.obstacle_timer = spawn_time + random.randint(-20, 20)
    
    def spawn_cloud(self):
        if self.cloud_timer <= 0:
            cloud = OptimizedCloud(WINDOW_WIDTH + 100, random.randint(50, 150))
            self.clouds.append(cloud)
            self.cloud_timer = random.randint(120, 300)
    
    def check_collisions(self):
        dino_rect = self.dino.get_rect()
        for obstacle in self.obstacles:
            obstacle_rect = obstacle.get_rect()
            if dino_rect.colliderect(obstacle_rect):
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                break
    
    def update(self, dt):
        if self.game_over:
            return
        
        # Update timers
        self.obstacle_timer -= 1
        self.cloud_timer -= 1
        self.speed_increase_timer += 1
        
        # Increase game speed gradually
        if self.speed_increase_timer >= 300:  # Every 5 seconds at 60 FPS
            self.game_speed += 0.1
            self.speed_increase_timer = 0
        
        # Update score
        self.score += int(self.game_speed * dt * 60)
        
        # Update game objects
        self.dino.update(dt)
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(dt, self.game_speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
        
        # Update clouds
        for cloud in self.clouds[:]:
            cloud.update(dt, self.game_speed)
            if cloud.is_off_screen():
                self.clouds.remove(cloud)
        
        # Spawn new objects
        self.spawn_obstacle()
        self.spawn_cloud()
        
        # Check collisions
        self.check_collisions()
    
    def draw_ground(self):
        # Ground
        ground_y = WINDOW_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(self.screen, GRAY, (0, ground_y, WINDOW_WIDTH, GROUND_HEIGHT))
        
        # Ground line
        pygame.draw.line(self.screen, BLACK, (0, ground_y), (WINDOW_WIDTH, ground_y), 2)
    
    def draw_ui(self):
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # High score
        high_score_text = self.small_font.render(f"High: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (10, 50))
        
        # Speed indicator
        speed_text = self.small_font.render(f"Speed: {self.game_speed:.1f}x", True, BLACK)
        self.screen.blit(speed_text, (WINDOW_WIDTH - 120, 10))
        
        # Controls
        if not self.game_over:
            controls = ["Space/↑: Jump", "↓/S: Duck", "ESC: Exit"]
            for i, control in enumerate(controls):
                control_text = self.small_font.render(control, True, BLACK)
                self.screen.blit(control_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 80 + i * 20))
    
    def draw_game_over(self):
        # Game over overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            new_high_text = self.small_font.render("NEW HIGH SCORE!", True, YELLOW)
            new_high_rect = new_high_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(new_high_text, new_high_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        self.dino = OptimizedDino()
        self.obstacles = []
        self.score = 0
        self.game_speed = 1.0
        self.game_over = False
        self.obstacle_timer = 0
        self.speed_increase_timer = 0
    
    def draw(self):
        # Clear screen with sky color
        self.screen.fill((135, 206, 235))  # Sky blue
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(self.screen)
        
        # Draw ground
        self.draw_ground()
        
        # Draw game objects
        self.dino.draw(self.screen)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        print("🦕 Optimized Dino Run Started!")
        print("🎮 Ultra-smooth performance with proper game speed!")
        print("🎯 Space/↑: Jump, ↓/S: Duck, ESC: Exit")
        
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
    game = OptimizedDinoGame()
    game.run()

if __name__ == "__main__":
    main()
