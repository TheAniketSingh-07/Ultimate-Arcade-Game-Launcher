#!/usr/bin/env python3
"""
Advanced Game Launcher with Beautiful UI Graphics
A comprehensive launcher for all your arcade games with visual previews and smooth navigation
"""

import pygame
import sys
import os
import math
import random
import subprocess
from enum import Enum
from typing import List, Dict, Tuple, Optional
import json

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS = 60

class Colors:
    # Modern color palette
    BACKGROUND = (15, 15, 25)
    SURFACE = (25, 25, 40)
    PRIMARY = (100, 150, 255)
    SECONDARY = (150, 100, 255)
    ACCENT = (255, 150, 100)
    SUCCESS = (100, 255, 150)
    WARNING = (255, 200, 100)
    DANGER = (255, 100, 100)
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (200, 200, 220)
    TEXT_MUTED = (150, 150, 170)
    CARD_BG = (35, 35, 55)
    CARD_HOVER = (45, 45, 65)
    CARD_SELECTED = (55, 55, 75)
    GLOW = (100, 150, 255, 100)

class GameInfo:
    def __init__(self, name: str, description: str, path: str, icon_color: Tuple[int, int, int], 
                 category: str = "Arcade", difficulty: str = "Medium", status: str = "Ready"):
        self.name = name
        self.description = description
        self.path = path
        self.icon_color = icon_color
        self.category = category
        self.difficulty = difficulty
        self.status = status
        self.last_played = None
        self.high_score = 0
        self.play_count = 0

class GameCard:
    def __init__(self, game_info: GameInfo, x: float, y: float, width: float, height: float):
        self.game_info = game_info
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hover = False
        self.selected = False
        self.animation_offset = 0
        self.glow_intensity = 0
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, mouse_pos: Tuple[int, int], dt: float):
        """Update card animations and hover state"""
        rect = self.get_rect()
        was_hover = self.hover
        self.hover = rect.collidepoint(mouse_pos)
        
        # Smooth hover animation
        if self.hover:
            self.animation_offset = min(self.animation_offset + dt * 300, 10)
            self.glow_intensity = min(self.glow_intensity + dt * 500, 100)
        else:
            self.animation_offset = max(self.animation_offset - dt * 300, 0)
            self.glow_intensity = max(self.glow_intensity - dt * 500, 0)
    
    def draw(self, screen: pygame.Surface, font_large: pygame.font.Font, 
             font_medium: pygame.font.Font, font_small: pygame.font.Font):
        """Draw the game card with animations"""
        # Card position with hover animation
        card_y = self.y - self.animation_offset
        
        # Glow effect
        if self.glow_intensity > 0:
            glow_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            glow_color = (*Colors.GLOW[:3], int(self.glow_intensity))
            pygame.draw.rect(glow_surf, glow_color, 
                           (0, 0, self.width + 20, self.height + 20), border_radius=15)
            screen.blit(glow_surf, (self.x - 10, card_y - 10))
        
        # Card background
        card_color = Colors.CARD_SELECTED if self.selected else (
            Colors.CARD_HOVER if self.hover else Colors.CARD_BG
        )
        pygame.draw.rect(screen, card_color, 
                        (self.x, card_y, self.width, self.height), border_radius=12)
        
        # Card border
        border_color = Colors.PRIMARY if self.selected else (
            Colors.SECONDARY if self.hover else Colors.SURFACE
        )
        pygame.draw.rect(screen, border_color, 
                        (self.x, card_y, self.width, self.height), width=2, border_radius=12)
        
        # Game icon (colored circle with emoji-style icon)
        icon_size = 60
        icon_x = self.x + 20
        icon_y = card_y + 20
        
        # Icon background
        pygame.draw.circle(screen, self.game_info.icon_color, 
                          (icon_x + icon_size//2, icon_y + icon_size//2), icon_size//2)
        
        # Icon symbol based on game type
        icon_symbols = {
            "Snake Game": "🐍",
            "Gravity Flip Ninja": "🥷",
            "Dino Run": "🦕",
            "Fighter Shoot": "⚔️",
            "Maze Game": "🧩",
            "Tic Tac Toe": "⭕"
        }
        
        icon_text = icon_symbols.get(self.game_info.name, "🎮")
        icon_surface = font_large.render(icon_text, True, Colors.TEXT_PRIMARY)
        icon_rect = icon_surface.get_rect(center=(icon_x + icon_size//2, icon_y + icon_size//2))
        screen.blit(icon_surface, icon_rect)
        
        # Game title
        title_x = icon_x + icon_size + 15
        title_y = card_y + 15
        title_surface = font_medium.render(self.game_info.name, True, Colors.TEXT_PRIMARY)
        screen.blit(title_surface, (title_x, title_y))
        
        # Game description
        desc_y = title_y + 35
        desc_words = self.game_info.description.split()
        desc_lines = []
        current_line = ""
        max_width = self.width - (title_x - self.x) - 20
        
        for word in desc_words:
            test_line = current_line + (" " if current_line else "") + word
            if font_small.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    desc_lines.append(current_line)
                current_line = word
        if current_line:
            desc_lines.append(current_line)
        
        for i, line in enumerate(desc_lines[:2]):  # Max 2 lines
            desc_surface = font_small.render(line, True, Colors.TEXT_SECONDARY)
            screen.blit(desc_surface, (title_x, desc_y + i * 20))
        
        # Game stats
        stats_y = card_y + self.height - 60
        
        # Category badge
        category_surface = font_small.render(self.game_info.category, True, Colors.TEXT_PRIMARY)
        category_rect = category_surface.get_rect()
        category_bg = pygame.Rect(title_x, stats_y, category_rect.width + 16, 24)
        pygame.draw.rect(screen, Colors.PRIMARY, category_bg, border_radius=12)
        screen.blit(category_surface, (title_x + 8, stats_y + 4))
        
        # Difficulty
        diff_x = title_x + category_bg.width + 10
        diff_colors = {
            "Easy": Colors.SUCCESS,
            "Medium": Colors.WARNING,
            "Hard": Colors.DANGER
        }
        diff_color = diff_colors.get(self.game_info.difficulty, Colors.TEXT_MUTED)
        diff_surface = font_small.render(f"● {self.game_info.difficulty}", True, diff_color)
        screen.blit(diff_surface, (diff_x, stats_y + 4))
        
        # Status
        status_y = stats_y + 30
        status_surface = font_small.render(f"Status: {self.game_info.status}", True, Colors.TEXT_MUTED)
        screen.blit(status_surface, (title_x, status_y))

class AdvancedGameLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🎮 Advanced Arcade Game Launcher - Ultimate Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_title = pygame.font.Font(None, 64)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game data
        self.games = self.load_games()
        self.game_cards: List[GameCard] = []
        self.selected_game_index = 0
        
        # UI state
        self.scroll_offset = 0
        self.target_scroll = 0
        self.sidebar_width = 300
        
        # Animations
        self.background_animation = 0
        self.particles = []
        
        # Initialize UI
        self.setup_game_cards()
        self.create_background_particles()
    
    def load_games(self) -> List[GameInfo]:
        """Load game information"""
        games = [
            GameInfo(
                name="Snake Game",
                description="Classic snake game with modern graphics. Eat food, grow longer, avoid walls and your own tail!",
                path="games/snake_game/snake_game.py",
                icon_color=Colors.SUCCESS,
                category="Classic",
                difficulty="Easy",
                status="Ready"
            ),
            GameInfo(
                name="Gravity Flip Ninja",
                description="Advanced ninja game with gravity flipping mechanics, particle effects, and smooth animations. Master the art of gravity manipulation!",
                path="games/gravity_flip_ninja/gravity_flip_ninja.py",
                icon_color=Colors.SECONDARY,
                category="Action",
                difficulty="Hard",
                status="Ready"
            ),
            GameInfo(
                name="Dino Run",
                description="Endless runner game where you control a dinosaur jumping over obstacles. Simple yet addictive gameplay!",
                path="games/dino_run/main.py",
                icon_color=Colors.WARNING,
                category="Runner",
                difficulty="Medium",
                status="Ready"
            ),
            GameInfo(
                name="Fighter Shoot",
                description="Action-packed shooting game with combat mechanics. Fight your way through enemies and challenges!",
                path="games/fighter_shoot/main.py",
                icon_color=Colors.DANGER,
                category="Shooter",
                difficulty="Hard",
                status="Ready"
            ),
            GameInfo(
                name="Maze Game",
                description="Navigate through challenging mazes and find your way to the exit. Test your problem-solving skills!",
                path="games/maze_game/main.py",
                icon_color=Colors.PRIMARY,
                category="Puzzle",
                difficulty="Medium",
                status="Ready"
            ),
            GameInfo(
                name="Tic Tac Toe",
                description="Classic strategy game for two players. Get three in a row to win! Simple rules, strategic gameplay.",
                path="games/tic_tac_toe/main.py",
                icon_color=Colors.ACCENT,
                category="Strategy",
                difficulty="Easy",
                status="Ready"
            )
        ]
        
        # Load additional stats if available
        self.load_game_stats(games)
        return games
    
    def load_game_stats(self, games: List[GameInfo]):
        """Load game statistics from file"""
        try:
            if os.path.exists("game_stats.json"):
                with open("game_stats.json", "r") as f:
                    stats = json.load(f)
                    for game in games:
                        if game.name in stats:
                            game_stats = stats[game.name]
                            game.high_score = game_stats.get("high_score", 0)
                            game.play_count = game_stats.get("play_count", 0)
                            game.last_played = game_stats.get("last_played")
        except Exception as e:
            print(f"Could not load game stats: {e}")
    
    def save_game_stats(self):
        """Save game statistics to file"""
        try:
            stats = {}
            for game in self.games:
                stats[game.name] = {
                    "high_score": game.high_score,
                    "play_count": game.play_count,
                    "last_played": game.last_played
                }
            with open("game_stats.json", "w") as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"Could not save game stats: {e}")
    
    def setup_game_cards(self):
        """Setup game cards layout"""
        self.game_cards.clear()
        
        # Grid layout
        cards_per_row = 2
        card_width = 400
        card_height = 180
        margin = 20
        start_x = self.sidebar_width + margin
        start_y = 120
        
        for i, game in enumerate(self.games):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            
            card = GameCard(game, x, y, card_width, card_height)
            self.game_cards.append(card)
    
    def create_background_particles(self):
        """Create animated background particles"""
        self.particles.clear()
        for _ in range(50):
            self.particles.append({
                'x': random.uniform(0, WINDOW_WIDTH),
                'y': random.uniform(0, WINDOW_HEIGHT),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.uniform(1, 3),
                'alpha': random.uniform(50, 150)
            })
    
    def handle_events(self):
        """Handle input events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.launch_selected_game()
                elif event.key == pygame.K_UP:
                    self.navigate_games(-1)
                elif event.key == pygame.K_DOWN:
                    self.navigate_games(1)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for i, card in enumerate(self.game_cards):
                        if card.get_rect().collidepoint(mouse_pos):
                            self.selected_game_index = i
                            self.launch_selected_game()
                            break
            
            if event.type == pygame.MOUSEWHEEL:
                self.target_scroll += event.y * 30
                self.target_scroll = max(0, min(self.target_scroll, 
                                              max(0, len(self.games) * 100 - WINDOW_HEIGHT + 200)))
        
        return True
    
    def navigate_games(self, direction: int):
        """Navigate through games with keyboard"""
        self.selected_game_index = (self.selected_game_index + direction) % len(self.games)
        
        # Update card selection
        for i, card in enumerate(self.game_cards):
            card.selected = (i == self.selected_game_index)
    
    def launch_selected_game(self):
        """Launch the selected game"""
        if 0 <= self.selected_game_index < len(self.games):
            game = self.games[self.selected_game_index]
            print(f"🚀 Launching {game.name}...")
            
            # Update stats
            game.play_count += 1
            import datetime
            game.last_played = datetime.datetime.now().isoformat()
            self.save_game_stats()
            
            try:
                # Launch the game
                subprocess.run([sys.executable, game.path], cwd=os.path.dirname(__file__))
            except Exception as e:
                print(f"Error launching {game.name}: {e}")
    
    def update(self, dt: float):
        """Update launcher state"""
        # Update background animation
        self.background_animation += dt
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = WINDOW_WIDTH
            elif particle['x'] > WINDOW_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = WINDOW_HEIGHT
            elif particle['y'] > WINDOW_HEIGHT:
                particle['y'] = 0
        
        # Update scroll
        self.scroll_offset += (self.target_scroll - self.scroll_offset) * dt * 5
        
        # Update game cards
        mouse_pos = pygame.mouse.get_pos()
        for i, card in enumerate(self.game_cards):
            card.selected = (i == self.selected_game_index)
            card.update(mouse_pos, dt)
    
    def draw_background(self):
        """Draw animated background"""
        # Gradient background
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(Colors.BACKGROUND[0] + ratio * 10)
            g = int(Colors.BACKGROUND[1] + ratio * 10)
            b = int(Colors.BACKGROUND[2] + ratio * 15)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
        
        # Animated particles
        for particle in self.particles:
            alpha = int(particle['alpha'] + 50 * math.sin(self.background_animation + particle['x'] * 0.01))
            alpha = max(0, min(255, alpha))
            
            particle_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (*Colors.PRIMARY, alpha), 
                             (particle['size'], particle['size']), particle['size'])
            self.screen.blit(particle_surf, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def draw_sidebar(self):
        """Draw sidebar with launcher info"""
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, Colors.SURFACE, sidebar_rect)
        pygame.draw.line(self.screen, Colors.PRIMARY, 
                        (self.sidebar_width, 0), (self.sidebar_width, WINDOW_HEIGHT), 2)
        
        # Title
        title_text = self.font_title.render("🎮", True, Colors.PRIMARY)
        title_rect = title_text.get_rect(center=(self.sidebar_width // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_medium.render("Game Launcher", True, Colors.TEXT_PRIMARY)
        subtitle_rect = subtitle_text.get_rect(center=(self.sidebar_width // 2, 110))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Game count
        count_text = self.font_small.render(f"{len(self.games)} Games Available", True, Colors.TEXT_SECONDARY)
        count_rect = count_text.get_rect(center=(self.sidebar_width // 2, 140))
        self.screen.blit(count_text, count_rect)
        
        # Selected game info
        if 0 <= self.selected_game_index < len(self.games):
            selected_game = self.games[self.selected_game_index]
            
            info_y = 200
            
            # Selected game title
            selected_title = self.font_medium.render("Selected:", True, Colors.TEXT_MUTED)
            self.screen.blit(selected_title, (20, info_y))
            
            game_title = self.font_medium.render(selected_game.name, True, Colors.TEXT_PRIMARY)
            self.screen.blit(game_title, (20, info_y + 30))
            
            # Game stats
            stats_y = info_y + 80
            stats = [
                f"Category: {selected_game.category}",
                f"Difficulty: {selected_game.difficulty}",
                f"Status: {selected_game.status}",
                f"Played: {selected_game.play_count} times"
            ]
            
            for i, stat in enumerate(stats):
                stat_text = self.font_small.render(stat, True, Colors.TEXT_SECONDARY)
                self.screen.blit(stat_text, (20, stats_y + i * 25))
        
        # Controls
        controls_y = WINDOW_HEIGHT - 200
        controls_title = self.font_small.render("Controls:", True, Colors.TEXT_MUTED)
        self.screen.blit(controls_title, (20, controls_y))
        
        controls = [
            "↑↓ - Navigate",
            "Enter/Space - Launch",
            "Mouse - Click to play",
            "Esc - Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font_small.render(control, True, Colors.TEXT_SECONDARY)
            self.screen.blit(control_text, (20, controls_y + 25 + i * 20))
    
    def draw_header(self):
        """Draw main header"""
        header_y = 20
        header_x = self.sidebar_width + 40
        
        # Main title
        title_text = self.font_large.render("Your Arcade Collection", True, Colors.TEXT_PRIMARY)
        self.screen.blit(title_text, (header_x, header_y))
        
        # Subtitle
        subtitle_text = self.font_small.render("Choose a game to play", True, Colors.TEXT_SECONDARY)
        self.screen.blit(subtitle_text, (header_x, header_y + 50))
    
    def draw_game_cards(self):
        """Draw all game cards"""
        for card in self.game_cards:
            card.draw(self.screen, self.font_large, self.font_medium, self.font_small)
    
    def draw(self):
        """Main draw function"""
        self.draw_background()
        self.draw_sidebar()
        self.draw_header()
        self.draw_game_cards()
        
        pygame.display.flip()
    
    def run(self):
        """Main launcher loop"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

def main():
    """Main function"""
    try:
        launcher = AdvancedGameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error running Advanced Game Launcher: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
