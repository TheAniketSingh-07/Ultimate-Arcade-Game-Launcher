#!/usr/bin/env python3
"""
Fighter Shoot - Space Combat Game
Epic space shooter with aliens and power-ups!
"""

import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 60
        self.width = 40
        self.height = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < WINDOW_HEIGHT - self.height:
            self.y += self.speed
    
    def draw(self, screen):
        # Draw player ship
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 4, self.y + self.height - 5),
            (self.x + 3 * self.width // 4, self.y + self.height - 5),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, CYAN, points)
        
        # Draw health bar
        health_width = 60
        health_height = 8
        health_x = self.x + (self.width - health_width) // 2
        health_y = self.y - 15
        
        pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
        health_fill = int((self.health / self.max_health) * health_width)
        pygame.draw.rect(screen, GREEN, (health_x, health_y, health_fill, health_height))

class Bullet:
    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.speed = 8 * direction
        self.color = YELLOW if direction > 0 else RED
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def is_off_screen(self):
        return self.y < -self.height or self.y > WINDOW_HEIGHT

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH - 30)
        self.y = random.randint(-100, -30)
        self.width = 30
        self.height = 25
        self.speed = random.uniform(1, 3)
        self.health = 2
        self.shoot_timer = random.randint(60, 180)
        
    def update(self):
        self.y += self.speed
        self.shoot_timer -= 1
        
    def draw(self, screen):
        # Draw enemy ship
        points = [
            (self.x + self.width // 2, self.y + self.height),
            (self.x, self.y),
            (self.x + self.width // 4, self.y + 5),
            (self.x + 3 * self.width // 4, self.y + 5),
            (self.x + self.width, self.y)
        ]
        pygame.draw.polygon(screen, RED, points)
        
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT
        
    def should_shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(120, 240)
            return True
        return False

class PowerUp:
    def __init__(self):
        self.x = random.randint(20, WINDOW_WIDTH - 20)
        self.y = random.randint(-50, -20)
        self.width = 20
        self.height = 20
        self.speed = 2
        self.type = random.choice(['health', 'rapid_fire'])
        self.color = GREEN if self.type == 'health' else ORANGE
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
        if self.type == 'health':
            pygame.draw.rect(screen, WHITE, (self.x + 8, self.y + 6, 4, 8))
            pygame.draw.rect(screen, WHITE, (self.x + 6, self.y + 8, 8, 4))
        else:
            pygame.draw.circle(screen, WHITE, (self.x + self.width // 2, self.y + self.height // 2), 3)
            
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT

class FighterShootGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🚀 Fighter Shoot - Space Combat!")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.player = Player()
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.powerups = []
        
        # Game state
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.rapid_fire_timer = 0
        self.shoot_cooldown = 0
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.shoot_cooldown <= 0:
                    self.shoot()
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Continuous shooting with space
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
            
        return True
    
    def shoot(self):
        bullet = Bullet(self.player.x + self.player.width // 2 - 2, self.player.y)
        self.bullets.append(bullet)
        
        if self.rapid_fire_timer > 0:
            self.shoot_cooldown = 5  # Rapid fire
        else:
            self.shoot_cooldown = 15  # Normal fire rate
    
    def spawn_enemy(self):
        if self.enemy_spawn_timer <= 0:
            enemy = Enemy()
            self.enemies.append(enemy)
            spawn_rate = max(30, 90 - self.level * 5)
            self.enemy_spawn_timer = spawn_rate
    
    def spawn_powerup(self):
        if self.powerup_spawn_timer <= 0 and random.randint(1, 100) <= 2:
            powerup = PowerUp()
            self.powerups.append(powerup)
            self.powerup_spawn_timer = 300
    
    def check_collisions(self):
        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    self.bullets.remove(bullet)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 10
                    break
        
        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if (bullet.x < self.player.x + self.player.width and
                bullet.x + bullet.width > self.player.x and
                bullet.y < self.player.y + self.player.height and
                bullet.y + bullet.height > self.player.y):
                
                self.enemy_bullets.remove(bullet)
                self.player.health -= 10
        
        # Player vs enemies (collision damage)
        for enemy in self.enemies[:]:
            if (self.player.x < enemy.x + enemy.width and
                self.player.x + self.player.width > enemy.x and
                self.player.y < enemy.y + enemy.height and
                self.player.y + self.player.height > enemy.y):
                
                self.enemies.remove(enemy)
                self.player.health -= 20
        
        # Player vs powerups
        for powerup in self.powerups[:]:
            if (self.player.x < powerup.x + powerup.width and
                self.player.x + self.player.width > powerup.x and
                self.player.y < powerup.y + powerup.height and
                self.player.y + self.player.height > powerup.y):
                
                self.powerups.remove(powerup)
                if powerup.type == 'health':
                    self.player.health = min(self.player.max_health, self.player.health + 30)
                elif powerup.type == 'rapid_fire':
                    self.rapid_fire_timer = 300
    
    def update(self):
        # Update timers
        self.enemy_spawn_timer -= 1
        self.powerup_spawn_timer -= 1
        self.shoot_cooldown -= 1
        self.rapid_fire_timer -= 1
        
        # Update game objects
        self.player.update()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
            elif enemy.should_shoot():
                enemy_bullet = Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.height, -1)
                self.enemy_bullets.append(enemy_bullet)
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.is_off_screen():
                self.powerups.remove(powerup)
        
        # Spawn enemies and powerups
        self.spawn_enemy()
        self.spawn_powerup()
        
        # Check collisions
        self.check_collisions()
        
        # Level progression
        if self.score > 0 and self.score % 100 == 0:
            self.level = self.score // 100 + 1
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars background
        for i in range(50):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw game objects
        self.player.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 50))
        
        # Draw rapid fire indicator
        if self.rapid_fire_timer > 0:
            rapid_text = self.small_font.render("RAPID FIRE!", True, ORANGE)
            self.screen.blit(rapid_text, (WINDOW_WIDTH - 120, 10))
        
        # Draw controls
        controls = [
            "Arrow Keys: Move",
            "Space: Shoot",
            "ESC: Exit"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, WHITE)
            self.screen.blit(control_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 80 + i * 20))
        
        pygame.display.flip()
    
    def run(self):
        print("🚀 Fighter Shoot - Space Combat Game Started!")
        print("🎮 Use arrow keys to move, Space to shoot!")
        
        running = True
        while running and self.player.health > 0:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Game over screen
        if self.player.health <= 0:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(final_score_text, score_rect)
            pygame.display.flip()
            
            pygame.time.wait(3000)
        
        pygame.quit()
        sys.exit()

def main():
    game = FighterShootGame()
    game.run()

if __name__ == "__main__":
    main()
