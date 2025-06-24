"""
Simple Chrome Dino Game Logic
"""

import pygame
import random
from enum import Enum
from games.dino_run.settings import *
from games.dino_run.sprite_customizer import SpriteCustomizer

class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"

class Dino:
    """Simple dino player"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.ground_y = GROUND_Y - self.height
        
    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_STRENGTH
            self.is_jumping = True
            
    def duck(self):
        if not self.is_jumping:
            self.is_ducking = True
            self.height = int(DINO_HEIGHT * DUCK_HEIGHT_REDUCTION)
            
    def stop_duck(self):
        self.is_ducking = False
        self.height = DINO_HEIGHT
        
    def update(self):
        # Apply gravity
        if self.is_jumping:
            self.vel_y += GRAVITY
            self.y += self.vel_y
            
            # Land on ground
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.vel_y = 0
                self.is_jumping = False
                
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Cactus:
    """Simple cactus obstacle"""
    
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - CACTUS_HEIGHT
        self.width = CACTUS_WIDTH
        self.height = CACTUS_HEIGHT
        self.speed = 0
        
    def update(self):
        self.x -= self.speed
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def is_off_screen(self):
        return self.x + self.width < 0

class DinoGame:
    """Simple Chrome Dino Game"""
    
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.PLAYING
        
        # Game objects
        self.dino = Dino(100, GROUND_Y - DINO_HEIGHT)
        self.obstacles = []
        
        # Game variables
        self.score = 0
        self.speed = INITIAL_SPEED
        self.font = pygame.font.Font(None, 36)
        
        # Sprite customizer
        self.sprite_customizer = SpriteCustomizer(None)
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == GameState.PLAYING:
                if event.key in [pygame.K_SPACE, pygame.K_UP]:
                    self.dino.jump()
                elif event.key == pygame.K_DOWN:
                    self.dino.duck()
            elif self.state == GameState.GAME_OVER:
                if event.key == pygame.K_SPACE:
                    self.restart_game()
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.dino.stop_duck()
                
    def update(self):
        if self.state == GameState.PLAYING:
            # Update dino
            self.dino.update()
            
            # Update score
            self.score += 1
            
            # Increase speed
            if self.speed < MAX_SPEED:
                self.speed += SPEED_INCREASE_RATE
                
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.speed = self.speed
                obstacle.update()
                
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
                    
            # Spawn obstacles
            self.spawn_obstacles()
            
            # Check collisions
            self.check_collisions()
            
    def spawn_obstacles(self):
        if not self.obstacles or self.obstacles[-1].x < SCREEN_WIDTH - random.randint(MIN_OBSTACLE_DISTANCE, MAX_OBSTACLE_DISTANCE):
            if random.random() < OBSTACLE_SPAWN_CHANCE:
                obstacle = Cactus(SCREEN_WIDTH)
                self.obstacles.append(obstacle)
                
    def check_collisions(self):
        dino_rect = self.dino.get_rect()
        for obstacle in self.obstacles:
            if dino_rect.colliderect(obstacle.get_rect()):
                self.state = GameState.GAME_OVER
                break
                
    def restart_game(self):
        self.state = GameState.PLAYING
        self.score = 0
        self.speed = INITIAL_SPEED
        self.obstacles.clear()
        self.dino = Dino(100, GROUND_Y - DINO_HEIGHT)
        
    def draw(self):
        # White background
        self.screen.fill(WHITE)
        
        # Draw ground line
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        
        # Draw dino
        if self.dino.is_ducking:
            dino_sprite = self.sprite_customizer.get_sprite("dino", "ducking")
        elif self.dino.is_jumping:
            dino_sprite = self.sprite_customizer.get_sprite("dino", "jumping")
        else:
            dino_sprite = self.sprite_customizer.get_sprite("dino", "running")
        self.screen.blit(dino_sprite, (self.dino.x, self.dino.y))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            cactus_sprite = self.sprite_customizer.get_sprite("cactus")
            self.screen.blit(cactus_sprite, (obstacle.x, obstacle.y))
            
        # Draw score
        score_text = self.font.render(f"Score: {self.score//10}", True, BLACK)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 50))
        
        # Draw game over
        if self.state == GameState.GAME_OVER:
            game_over_text = self.font.render("GAME OVER - Press SPACE to restart", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
