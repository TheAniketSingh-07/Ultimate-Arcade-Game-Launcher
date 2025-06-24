#!/usr/bin/env python3
"""
ULTIMATE ARCADE GAME LAUNCHER
Complete, self-contained launcher in the main directory
Ultra-smooth performance with all games included
"""

import pygame
import sys
import os
import subprocess
import json
import time
import threading
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Add arcade_game_launcher to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'arcade_game_launcher'))

# Ultra-optimized initialization
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=128)

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TARGET_FPS = 120

class UltimateTheme:
    """Ultimate theme colors"""
    BG_DARK = (8, 8, 15)
    BG_SURFACE = (15, 15, 25)
    PRIMARY = (70, 130, 255)
    SECONDARY = (130, 70, 255)
    ACCENT = (255, 130, 70)
    SUCCESS = (70, 255, 130)
    TEXT_WHITE = (255, 255, 255)
    TEXT_GRAY = (180, 180, 200)
    TEXT_DARK = (120, 120, 140)
    CARD_BG = (25, 25, 40)
    CARD_HOVER = (35, 35, 55)
    CARD_SELECTED = (70, 70, 120)
    BORDER = (60, 60, 80)

@dataclass
class GameData:
    """Game data structure"""
    name: str
    path: str
    description: str
    category: str
    color: Tuple[int, int, int]
    icon: str
    play_count: int = 0
    last_played: float = 0

class UltimateRenderer:
    """Ultimate high-performance renderer"""
    def __init__(self, screen):
        self.screen = screen
        self.surface_cache = {}
        
        # Pre-load fonts
        self.fonts = {
            'title': pygame.font.Font(None, 56),
            'subtitle': pygame.font.Font(None, 36),
            'body': pygame.font.Font(None, 28),
            'small': pygame.font.Font(None, 20),
            'icon': pygame.font.Font(None, 48)
        }
    
    def get_text_surface(self, text: str, font_key: str, color: Tuple[int, int, int]):
        """Cached text rendering"""
        cache_key = (text, font_key, color)
        if cache_key not in self.surface_cache:
            font = self.fonts[font_key]
            self.surface_cache[cache_key] = font.render(text, True, color)
        return self.surface_cache[cache_key]
    
    def draw_rounded_rect(self, color: Tuple[int, int, int], rect: pygame.Rect, radius: int = 12):
        """Optimized rounded rectangle"""
        if radius <= 0:
            pygame.draw.rect(self.screen, color, rect)
            return
        
        pygame.draw.rect(self.screen, color, (rect.x + radius, rect.y, rect.width - 2*radius, rect.height))
        pygame.draw.rect(self.screen, color, (rect.x, rect.y + radius, rect.width, rect.height - 2*radius))
        
        pygame.draw.circle(self.screen, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)

class UltimateGameCard:
    """Ultimate game card with smooth animations"""
    def __init__(self, game_data: GameData, x: int, y: int):
        self.game_data = game_data
        self.rect = pygame.Rect(x, y, 280, 180)
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.is_hovered = False
        self.is_selected = False
        self.glow_intensity = 0.0
        self.animation_speed = 0.25
        self.center_x = x + 140
        self.center_y = y + 90
    
    def update(self, dt: float):
        """Smooth animation updates"""
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * 0.15
        
        target_glow = 1.0 if (self.is_selected or self.is_hovered) else 0.0
        glow_diff = target_glow - self.glow_intensity
        self.glow_intensity += glow_diff * self.animation_speed
    
    def handle_hover(self, mouse_pos: Tuple[int, int]):
        """Handle hover state"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered != was_hovered:
            self.target_scale = 1.05 if self.is_hovered else 1.0
    
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        if selected:
            self.target_scale = 1.08
        else:
            self.target_scale = 1.05 if self.is_hovered else 1.0
    
    def draw(self, renderer: UltimateRenderer):
        """Draw the game card"""
        scale = self.hover_scale
        scaled_width = int(self.rect.width * scale)
        scaled_height = int(self.rect.height * scale)
        scaled_x = self.center_x - scaled_width // 2
        scaled_y = self.center_y - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw glow effect
        if self.glow_intensity > 0.1:
            glow_size = int(4 * self.glow_intensity)
            glow_rect = pygame.Rect(scaled_rect.x - glow_size, scaled_rect.y - glow_size,
                                  scaled_rect.width + 2*glow_size, scaled_rect.height + 2*glow_size)
            renderer.draw_rounded_rect(UltimateTheme.PRIMARY, glow_rect, 16)
        
        # Card background
        bg_color = UltimateTheme.CARD_SELECTED if self.is_selected else UltimateTheme.CARD_HOVER if self.is_hovered else UltimateTheme.CARD_BG
        renderer.draw_rounded_rect(bg_color, scaled_rect, 12)
        
        # Game icon
        icon_surface = renderer.get_text_surface(self.game_data.icon, 'icon', self.game_data.color)
        icon_rect = icon_surface.get_rect(center=(scaled_rect.x + 60, scaled_rect.y + 50))
        renderer.screen.blit(icon_surface, icon_rect)
        
        # Game name
        name_surface = renderer.get_text_surface(self.game_data.name, 'subtitle', UltimateTheme.TEXT_WHITE)
        renderer.screen.blit(name_surface, (scaled_rect.x + 20, scaled_rect.y + 90))
        
        # Category
        category_surface = renderer.get_text_surface(self.game_data.category, 'small', UltimateTheme.TEXT_GRAY)
        renderer.screen.blit(category_surface, (scaled_rect.x + 20, scaled_rect.y + 120))
        
        # Status
        status_surface = renderer.get_text_surface("✅ Ready", 'small', UltimateTheme.SUCCESS)
        renderer.screen.blit(status_surface, (scaled_rect.x + scaled_rect.width - 80, scaled_rect.y + 15))
        
        # Play count
        if self.game_data.play_count > 0:
            count_text = f"Played {self.game_data.play_count}x"
            count_surface = renderer.get_text_surface(count_text, 'small', UltimateTheme.ACCENT)
            renderer.screen.blit(count_surface, (scaled_rect.x + 20, scaled_rect.y + scaled_rect.height - 25))

class UltimateGameLauncher:
    """Ultimate game launcher with all features"""
    
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
                                            pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("🎮 Ultimate Arcade Game Launcher")
        
        # Components
        self.clock = pygame.time.Clock()
        self.renderer = UltimateRenderer(self.screen)
        
        # Game data
        self.games = self.load_games()
        self.game_cards = []
        self.selected_index = 0
        
        # Performance tracking
        self.frame_times = []
        self.fps_display = 120
        
        # Statistics
        self.stats = self.load_stats()
        
        self.setup_layout()
        self.load_game_stats()
    
    def load_games(self) -> List[GameData]:
        """Load all games with proper paths"""
        base_path = "arcade_game_launcher/games"
        
        games = [
            GameData("Dino Run", f"{base_path}/dino_run/main.py", 
                    "Ultra-smooth endless runner!", "Action", 
                    (255, 100, 100), "🦕"),
            GameData("Fighter Shoot", f"{base_path}/fighter_shoot/main.py",
                    "Epic space combat!", "Shooter", 
                    (100, 255, 100), "🚀"),
            GameData("Gravity Ninja", f"{base_path}/gravity_flip_ninja/gravity_flip_ninja.py",
                    "Flip gravity to survive!", "Platformer", 
                    (100, 100, 255), "🥷"),
            GameData("Maze Explorer", f"{base_path}/maze_game/main.py",
                    "Navigate through mazes!", "Puzzle", 
                    (255, 255, 100), "🧩"),
            GameData("Snake Classic", f"{base_path}/snake_game/snake_game.py",
                    "Classic snake gameplay!", "Classic", 
                    (255, 100, 255), "🐍"),
            GameData("Tic Tac Toe", f"{base_path}/tic_tac_toe/main.py",
                    "Strategic AI gameplay!", "Strategy", 
                    (100, 255, 255), "⭕")
        ]
        
        # Verify games exist
        verified_games = []
        for game in games:
            if os.path.exists(game.path):
                verified_games.append(game)
                print(f"✅ {game.name} - Ready to play!")
            else:
                print(f"⚠️  {game.name} - File not found: {game.path}")
        
        return verified_games
    
    def setup_layout(self):
        """Setup perfect 3-column layout"""
        self.game_cards = []
        
        cards_per_row = 3
        card_width = 280
        card_height = 180
        margin_x = 40
        margin_y = 30
        
        total_width = cards_per_row * card_width + (cards_per_row - 1) * margin_x
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 150
        
        for i, game in enumerate(self.games):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + margin_x)
            y = start_y + row * (card_height + margin_y)
            
            card = UltimateGameCard(game, x, y)
            self.game_cards.append(card)
    
    def load_stats(self) -> Dict:
        """Load game statistics"""
        try:
            stats_path = "arcade_game_launcher/game_stats.json"
            with open(stats_path, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def load_game_stats(self):
        """Load statistics for each game"""
        for game in self.games:
            if game.name in self.stats:
                game.play_count = self.stats[game.name].get("play_count", 0)
                game.last_played = self.stats[game.name].get("last_played", 0)
    
    def save_stats(self):
        """Save game statistics"""
        stats_data = {game.name: {"play_count": game.play_count, "last_played": game.last_played} 
                     for game in self.games}
        try:
            stats_path = "arcade_game_launcher/game_stats.json"
            with open(stats_path, "w") as f:
                json.dump(stats_data, f, indent=2)
        except:
            pass
    
    def handle_events(self) -> bool:
        """Handle all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.launch_selected_game()
                elif event.key == pygame.K_LEFT:
                    self.navigate_selection(-1)
                elif event.key == pygame.K_RIGHT:
                    self.navigate_selection(1)
                elif event.key == pygame.K_UP:
                    self.navigate_selection(-3)
                elif event.key == pygame.K_DOWN:
                    self.navigate_selection(3)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, card in enumerate(self.game_cards):
                        if card.rect.collidepoint(mouse_pos):
                            self.selected_index = i
                            self.update_selection()
                            self.launch_selected_game()
                            break
        return True
    
    def navigate_selection(self, direction: int):
        """Navigate game selection"""
        new_index = max(0, min(len(self.games) - 1, self.selected_index + direction))
        self.selected_index = new_index
        self.update_selection()
    
    def update_selection(self):
        """Update selection states"""
        for i, card in enumerate(self.game_cards):
            card.set_selected(i == self.selected_index)
    
    def launch_selected_game(self):
        """Launch the selected game"""
        if 0 <= self.selected_index < len(self.games):
            game = self.games[self.selected_index]
            self.launch_game(game)
    
    def launch_game(self, game: GameData):
        """Launch a game"""
        try:
            game.play_count += 1
            game.last_played = time.time()
            self.save_stats()
            
            # Launch in separate thread
            def launch_thread():
                game_dir = os.path.dirname(game.path)
                subprocess.Popen([sys.executable, os.path.basename(game.path)], 
                               cwd=game_dir)
            
            threading.Thread(target=launch_thread, daemon=True).start()
            print(f"🚀 Launched: {game.name}")
        except Exception as e:
            print(f"❌ Failed to launch {game.name}: {e}")
    
    def update(self, dt: float):
        """Update game state"""
        # Update performance tracking
        self.frame_times.append(dt)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        self.fps_display = int(1.0 / avg_frame_time) if avg_frame_time > 0 else 120
        
        # Update cards
        mouse_pos = pygame.mouse.get_pos()
        for card in self.game_cards:
            card.update(dt)
            card.handle_hover(mouse_pos)
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(UltimateTheme.BG_DARK)
        
        # Draw header
        self.draw_header()
        
        # Draw cards
        for card in self.game_cards:
            card.draw(self.renderer)
        
        # Draw footer
        self.draw_footer()
        
        pygame.display.flip()
    
    def draw_header(self):
        """Draw header"""
        # Title
        title_surface = self.renderer.get_text_surface("🎮 Ultimate Arcade Game Launcher", 'title', UltimateTheme.TEXT_WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_surface = self.renderer.get_text_surface("✨ Ultra-Smooth • Zero Lag • Perfect Performance", 'body', UltimateTheme.TEXT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, 75))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Selected game
        if 0 <= self.selected_index < len(self.games):
            selected_game = self.games[self.selected_index]
            selection_text = f"Selected: {selected_game.icon} {selected_game.name}"
            selection_surface = self.renderer.get_text_surface(selection_text, 'body', UltimateTheme.ACCENT)
            selection_rect = selection_surface.get_rect(center=(WINDOW_WIDTH // 2, 105))
            self.screen.blit(selection_surface, selection_rect)
        
        # Separator
        pygame.draw.line(self.screen, UltimateTheme.BORDER, (50, 130), (WINDOW_WIDTH - 50, 130), 2)
    
    def draw_footer(self):
        """Draw footer"""
        controls = [
            "🖱️ Single Click: Launch instantly • ⌨️ Arrow Keys: Navigate • Enter: Launch • ESC: Exit",
            f"🎯 Game {self.selected_index + 1}/{len(self.games)} • FPS: {self.fps_display} • Ultimate Performance"
        ]
        
        y_start = WINDOW_HEIGHT - 60
        for i, control in enumerate(controls):
            control_surface = self.renderer.get_text_surface(control, 'small', UltimateTheme.TEXT_GRAY)
            control_rect = control_surface.get_rect(center=(WINDOW_WIDTH // 2, y_start + i * 25))
            self.screen.blit(control_surface, control_rect)
    
    def run(self):
        """Main game loop"""
        print("🎮 Ultimate Arcade Game Launcher Started!")
        print("✨ Ultra-smooth performance with zero lag!")
        print("🚀 All games optimized and ready to play!")
        print(f"🎯 Found {len(self.games)} games in perfect condition!")
        
        running = True
        last_time = time.time()
        
        # Initial setup
        self.update_selection()
        
        while running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            dt = min(dt, 1/60)
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
            self.clock.tick(TARGET_FPS)
        
        self.save_stats()
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    try:
        launcher = UltimateGameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Launcher error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
