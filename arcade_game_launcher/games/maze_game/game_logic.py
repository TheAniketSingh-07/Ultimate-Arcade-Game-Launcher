"""
Maze Game Logic
Main game logic with smooth gameplay and good graphics
"""

import pygame
import random
import math
from enum import Enum
from settings import *
from maze_generator import MazeGenerator
from player import Player

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"

class Collectible:
    """Animated collectible items"""
    
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * CELL_SIZE + CELL_SIZE // 2
        self.pixel_y = y * CELL_SIZE + CELL_SIZE // 2
        self.collected = False
        self.pulse = 0
        self.rotation = 0
        self.float_offset = 0
        
    def update(self):
        """Update collectible animations"""
        self.pulse += 0.15
        self.rotation += 3
        self.float_offset = math.sin(self.pulse) * 3
        
    def draw(self, screen):
        """Draw animated collectible"""
        if self.collected:
            return
            
        y_pos = self.pixel_y + self.float_offset
        
        # Glow effect
        glow_size = COLLECTIBLE_SIZE + 8 + math.sin(self.pulse) * 2
        glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        glow_color = (*COLLECTIBLE_COLOR, 50)
        pygame.draw.circle(glow_surface, glow_color, (int(glow_size), int(glow_size)), int(glow_size))
        screen.blit(glow_surface, (self.pixel_x - glow_size, y_pos - glow_size))
        
        # Main collectible
        pygame.draw.circle(screen, WHITE, (int(self.pixel_x), int(y_pos)), COLLECTIBLE_SIZE + 1)
        pygame.draw.circle(screen, COLLECTIBLE_COLOR, (int(self.pixel_x), int(y_pos)), COLLECTIBLE_SIZE)
        
        # Rotating inner star
        self._draw_star(screen, self.pixel_x, y_pos, COLLECTIBLE_SIZE - 3, self.rotation)
    
    def _draw_star(self, screen, x, y, size, rotation):
        """Draw rotating star inside collectible"""
        points = []
        for i in range(8):
            angle = math.radians(rotation + i * 45)
            if i % 2 == 0:
                px = x + math.cos(angle) * size
                py = y + math.sin(angle) * size
            else:
                px = x + math.cos(angle) * size * 0.5
                py = y + math.sin(angle) * size * 0.5
            points.append((px, py))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, YELLOW, points)

class MazeGame:
    """Main maze game with smooth graphics and gameplay"""
    
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.MENU
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.maze_generator = MazeGenerator()
        self.maze = []
        self.player = None
        self.collectibles = []
        self.goal_pos = None
        
        # Game state
        self.level = 1
        self.score = 0
        self.collected_items = 0
        self.total_items = 0
        
        # Visual effects
        self.background_particles = []
        self.screen_shake = 0
        
        # Fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Initialize first level
        self.start_new_level()
        
    def start_new_level(self):
        """Start a new level with generated maze"""
        # Generate new maze
        self.maze = self.maze_generator.generate_maze()
        
        # Create player at start position
        self.player = Player(1, 1)
        
        # Set goal position
        self.goal_pos = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
        
        # Create collectibles
        self._create_collectibles()
        
        # Create background particles
        self._create_background_particles()
        
        self.state = GameState.PLAYING
    
    def _create_collectibles(self):
        """Create collectible items throughout the maze"""
        self.collectibles = []
        valid_positions = self.maze_generator.get_valid_positions()
        
        # Remove start and goal positions
        valid_positions = [pos for pos in valid_positions 
                          if pos != (1, 1) and pos != self.goal_pos]
        
        # Create collectibles (about 20% of valid positions)
        num_collectibles = max(3, len(valid_positions) // 5)
        collectible_positions = random.sample(valid_positions, 
                                            min(num_collectibles, len(valid_positions)))
        
        for x, y in collectible_positions:
            self.collectibles.append(Collectible(x, y))
        
        self.total_items = len(self.collectibles)
        self.collected_items = 0
    
    def _create_background_particles(self):
        """Create ambient background particles"""
        self.background_particles = []
        for _ in range(20):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'color': random.choice([LIGHT_BLUE, WHITE, SILVER]),
                'alpha': random.randint(30, 100)
            }
            self.background_particles.append(particle)
    
    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            if self.state == GameState.MENU:
                if event.key == pygame.K_SPACE:
                    self.state = GameState.PLAYING
            
            elif self.state == GameState.PLAYING:
                # Player movement
                moved = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    moved = self.player.move(0, -1, self.maze)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moved = self.player.move(0, 1, self.maze)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moved = self.player.move(-1, 0, self.maze)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moved = self.player.move(1, 0, self.maze)
                
                if moved:
                    self._check_collectibles()
                    self._check_goal()
            
            elif self.state == GameState.LEVEL_COMPLETE:
                if event.key == pygame.K_SPACE:
                    self.level += 1
                    self.start_new_level()
    
    def _check_collectibles(self):
        """Check if player collected any items"""
        player_grid_pos = (self.player.grid_x, self.player.grid_y)
        
        for collectible in self.collectibles:
            if not collectible.collected and (collectible.grid_x, collectible.grid_y) == player_grid_pos:
                collectible.collected = True
                self.collected_items += 1
                self.score += 100
                self.screen_shake = 5  # Screen shake effect
    
    def _check_goal(self):
        """Check if player reached the goal"""
        if (self.player.grid_x, self.player.grid_y) == self.goal_pos:
            # Bonus points for remaining collectibles
            bonus = (self.total_items - self.collected_items) * 50
            self.score += bonus + 500  # Level completion bonus
            self.state = GameState.LEVEL_COMPLETE
    
    def update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            self.player.update()
            
            # Update collectibles
            for collectible in self.collectibles:
                collectible.update()
            
            # Update background particles
            self._update_background_particles()
            
            # Update screen shake
            if self.screen_shake > 0:
                self.screen_shake -= 1
    
    def _update_background_particles(self):
        """Update ambient background particles"""
        for particle in self.background_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def draw(self):
        """Draw everything"""
        # Apply screen shake
        shake_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        shake_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        # Clear screen with gradient background
        self._draw_background()
        
        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.PLAYING:
            self._draw_game(shake_x, shake_y)
        elif self.state == GameState.LEVEL_COMPLETE:
            self._draw_level_complete()
    
    def _draw_background(self):
        """Draw gradient background with particles"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(20 + (40 - 20) * color_ratio)
            g = int(25 + (50 - 25) * color_ratio)
            b = int(40 + (80 - 40) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Background particles
        for particle in self.background_particles:
            particle_surface = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
            color = (*particle['color'], particle['alpha'])
            pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
            self.screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def _draw_game(self, shake_x, shake_y):
        """Draw the main game"""
        # Calculate maze offset to center it
        maze_pixel_width = MAZE_WIDTH * CELL_SIZE
        maze_pixel_height = MAZE_HEIGHT * CELL_SIZE
        offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2 + shake_x
        offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2 + shake_y
        
        # Draw maze
        self._draw_maze(offset_x, offset_y)
        
        # Draw goal
        self._draw_goal(offset_x, offset_y)
        
        # Draw collectibles
        for collectible in self.collectibles:
            if not collectible.collected:
                # Adjust collectible position for screen offset
                original_x = collectible.pixel_x
                original_y = collectible.pixel_y
                collectible.pixel_x = original_x + offset_x
                collectible.pixel_y = original_y + offset_y
                collectible.draw(self.screen)
                collectible.pixel_x = original_x
                collectible.pixel_y = original_y
        
        # Draw player
        original_x = self.player.pixel_x
        original_y = self.player.pixel_y
        self.player.pixel_x = original_x + offset_x
        self.player.pixel_y = original_y + offset_y
        self.player.draw(self.screen)
        self.player.pixel_x = original_x
        self.player.pixel_y = original_y
        
        # Draw UI
        self._draw_ui()
    
    def _draw_maze(self, offset_x, offset_y):
        """Draw the maze with good graphics"""
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                pixel_x = x * CELL_SIZE + offset_x
                pixel_y = y * CELL_SIZE + offset_y
                
                if self.maze[y][x] == 1:  # Wall
                    # Draw wall with gradient effect
                    wall_rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
                    
                    # Main wall
                    pygame.draw.rect(self.screen, DARK_GREEN, wall_rect)
                    
                    # Highlight edges
                    pygame.draw.rect(self.screen, GREEN, wall_rect, WALL_THICKNESS)
                    
                    # Inner highlight
                    inner_rect = pygame.Rect(pixel_x + 3, pixel_y + 3, 
                                           CELL_SIZE - 6, CELL_SIZE - 6)
                    pygame.draw.rect(self.screen, (0, 120, 0), inner_rect, 1)
    
    def _draw_goal(self, offset_x, offset_y):
        """Draw animated goal"""
        goal_x = self.goal_pos[0] * CELL_SIZE + CELL_SIZE // 2 + offset_x
        goal_y = self.goal_pos[1] * CELL_SIZE + CELL_SIZE // 2 + offset_y
        
        # Pulsing glow
        pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5
        glow_size = GOAL_SIZE + 10 + pulse
        
        glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        glow_color = (*GOAL_COLOR, 80)
        pygame.draw.circle(glow_surface, glow_color, (int(glow_size), int(glow_size)), int(glow_size))
        self.screen.blit(glow_surface, (goal_x - glow_size, goal_y - glow_size))
        
        # Main goal
        pygame.draw.circle(self.screen, WHITE, (int(goal_x), int(goal_y)), GOAL_SIZE + 2)
        pygame.draw.circle(self.screen, GOAL_COLOR, (int(goal_x), int(goal_y)), GOAL_SIZE)
        
        # Inner pattern
        for i in range(3):
            size = GOAL_SIZE - (i * 4)
            if size > 0:
                alpha = 255 - (i * 60)
                color = (*YELLOW, alpha) if i % 2 == 0 else (*WHITE, alpha)
                goal_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(goal_surface, color, (size, size), size)
                self.screen.blit(goal_surface, (goal_x - size, goal_y - size))
    
    def _draw_ui(self):
        """Draw user interface"""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (20, 50))
        
        # Collectibles
        items_text = self.font_medium.render(f"Items: {self.collected_items}/{self.total_items}", True, WHITE)
        self.screen.blit(items_text, (20, 80))
        
        # Controls hint
        controls_text = self.font_small.render("WASD or Arrow Keys to move", True, LIGHT_BLUE)
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def _draw_menu(self):
        """Draw main menu"""
        title_text = self.font_large.render("MAZE ADVENTURE", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_medium.render("Smooth Explorer Edition", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        start_text = self.font_medium.render("Press SPACE to Start", True, LIGHT_BLUE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(start_text, start_rect)
    
    def _draw_level_complete(self):
        """Draw level complete screen"""
        complete_text = self.font_large.render("LEVEL COMPLETE!", True, GOLD)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(complete_text, complete_rect)
        
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        next_text = self.font_medium.render("Press SPACE for Next Level", True, LIGHT_BLUE)
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(next_text, next_rect)
