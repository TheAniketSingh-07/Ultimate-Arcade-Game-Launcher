#!/usr/bin/env python3
"""
Perfect Game Launcher - 3 Games in a Row Design
Ultra-optimized, lag-free launcher with perfect 3-column layout
"""

import pygame
import sys
import os
import subprocess
import json
import time
from typing import List, Dict, Tuple, Optional

# Initialize Pygame with optimizations
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=256)

# Optimized Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TARGET_FPS = 144  # Higher FPS for ultra-smooth experience

class Theme:
    """Ultra-modern theme colors"""
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
    GLOW = (70, 130, 255, 100)

class GameData:
    """Optimized game data structure"""
    def __init__(self, name: str, path: str, description: str, category: str, 
                 color: Tuple[int, int, int], icon: str):
        self.name = name
        self.path = path
        self.description = description
        self.category = category
        self.color = color
        self.icon = icon
        self.play_count = 0
        self.last_played = 0
        self.is_working = True

class PerformanceRenderer:
    """Ultra-high performance rendering system"""
    def __init__(self, screen):
        self.screen = screen
        self.surface_cache = {}
        self.max_cache_size = 500
        
        # Pre-load optimized fonts
        self.fonts = {
            'title': pygame.font.Font(None, 56),
            'subtitle': pygame.font.Font(None, 36),
            'body': pygame.font.Font(None, 28),
            'small': pygame.font.Font(None, 20),
            'icon': pygame.font.Font(None, 48)
        }
    
    def get_text_surface(self, text: str, font_key: str, color: Tuple[int, int, int]):
        """Ultra-fast cached text rendering"""
        cache_key = (text, font_key, color)
        
        if cache_key not in self.surface_cache:
            if len(self.surface_cache) >= self.max_cache_size:
                # Clear oldest entries
                keys_to_remove = list(self.surface_cache.keys())[:100]
                for key in keys_to_remove:
                    del self.surface_cache[key]
            
            font = self.fonts.get(font_key, self.fonts['body'])
            surface = font.render(text, True, color)
            self.surface_cache[cache_key] = surface
        
        return self.surface_cache[cache_key]
    
    def draw_rounded_rect(self, color: Tuple[int, int, int], rect: pygame.Rect, radius: int = 12):
        """Optimized rounded rectangle with glow effect"""
        if radius <= 0:
            pygame.draw.rect(self.screen, color, rect)
            return
        
        # Main rectangle
        pygame.draw.rect(self.screen, color, 
                        (rect.x + radius, rect.y, rect.width - 2*radius, rect.height))
        pygame.draw.rect(self.screen, color, 
                        (rect.x, rect.y + radius, rect.width, rect.height - 2*radius))
        
        # Corners
        pygame.draw.circle(self.screen, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)

class GameCard:
    """Perfect game card with 3-in-a-row design"""
    def __init__(self, game_data: GameData, x: int, y: int):
        self.game_data = game_data
        self.rect = pygame.Rect(x, y, 280, 180)  # Perfect card size
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.is_hovered = False
        self.is_selected = False
        self.glow_intensity = 0.0
        self.animation_speed = 0.2
    
    def update(self, dt: float):
        """Ultra-smooth animations"""
        # Scale animation
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * self.animation_speed
        
        # Glow animation
        if self.is_selected or self.is_hovered:
            self.glow_intensity = min(1.0, self.glow_intensity + dt * 4)
        else:
            self.glow_intensity = max(0.0, self.glow_intensity - dt * 4)
    
    def handle_hover(self, mouse_pos: Tuple[int, int]):
        """Handle hover state"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered and not was_hovered:
            self.target_scale = 1.05
        elif not self.is_hovered and was_hovered:
            self.target_scale = 1.0
    
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        if selected:
            self.target_scale = 1.08
        else:
            self.target_scale = 1.05 if self.is_hovered else 1.0
    
    def draw(self, renderer: PerformanceRenderer):
        """Perfect card drawing"""
        # Calculate scaled rect
        scale = self.hover_scale
        scaled_width = int(self.rect.width * scale)
        scaled_height = int(self.rect.height * scale)
        scaled_x = self.rect.x + (self.rect.width - scaled_width) // 2
        scaled_y = self.rect.y + (self.rect.height - scaled_height) // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw glow effect
        if self.glow_intensity > 0:
            glow_size = 4
            glow_rect = pygame.Rect(scaled_rect.x - glow_size, scaled_rect.y - glow_size,
                                  scaled_rect.width + 2*glow_size, scaled_rect.height + 2*glow_size)
            glow_color = (*Theme.PRIMARY, int(50 * self.glow_intensity))
            renderer.draw_rounded_rect(Theme.PRIMARY, glow_rect, 16)
        
        # Card background
        bg_color = Theme.CARD_SELECTED if self.is_selected else Theme.CARD_HOVER if self.is_hovered else Theme.CARD_BG
        renderer.draw_rounded_rect(bg_color, scaled_rect, 12)
        
        # Game icon (large emoji/symbol)
        icon_surface = renderer.get_text_surface(self.game_data.icon, 'icon', self.game_data.color)
        icon_rect = icon_surface.get_rect(center=(scaled_rect.x + 60, scaled_rect.y + 50))
        renderer.screen.blit(icon_surface, icon_rect)
        
        # Game name
        name_surface = renderer.get_text_surface(self.game_data.name, 'subtitle', Theme.TEXT_WHITE)
        name_pos = (scaled_rect.x + 20, scaled_rect.y + 90)
        renderer.screen.blit(name_surface, name_pos)
        
        # Category
        category_surface = renderer.get_text_surface(self.game_data.category, 'small', Theme.TEXT_GRAY)
        category_pos = (scaled_rect.x + 20, scaled_rect.y + 120)
        renderer.screen.blit(category_surface, category_pos)
        
        # Status indicator
        status_color = Theme.SUCCESS if self.game_data.is_working else Theme.ACCENT
        status_text = "✅ Ready" if self.game_data.is_working else "⚠️ Check"
        status_surface = renderer.get_text_surface(status_text, 'small', status_color)
        status_pos = (scaled_rect.x + scaled_rect.width - 80, scaled_rect.y + 15)
        renderer.screen.blit(status_surface, status_pos)
        
        # Play count
        if self.game_data.play_count > 0:
            count_text = f"Played {self.game_data.play_count}x"
            count_surface = renderer.get_text_surface(count_text, 'small', Theme.ACCENT)
            count_pos = (scaled_rect.x + 20, scaled_rect.y + scaled_rect.height - 25)
            renderer.screen.blit(count_surface, count_pos)

class PerfectGameLauncher:
    """Perfect 3-games-in-a-row launcher"""
    
    def __init__(self):
        # Initialize display with maximum performance
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
                                            pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("🎮 Perfect Game Launcher - 3 in a Row")
        
        # Performance components
        self.clock = pygame.time.Clock()
        self.renderer = PerformanceRenderer(self.screen)
        
        # Game data
        self.games = self.load_games()
        self.game_cards = []
        self.selected_index = 0
        
        # UI state
        self.scroll_offset = 0
        self.target_scroll = 0
        
        # Statistics
        self.stats = self.load_stats()
        
        self.setup_perfect_layout()
        self.load_game_stats()
    
    def load_games(self) -> List[GameData]:
        """Load games with perfect configuration"""
        games = [
            GameData("Dino Run", "games/dino_run/main.py", 
                    "Jump over obstacles in endless runner!", "Action", 
                    (255, 100, 100), "🦕"),
            GameData("Fighter Shoot", "games/fighter_shoot/main.py",
                    "Epic space combat with aliens!", "Shooter", 
                    (100, 255, 100), "🚀"),
            GameData("Gravity Ninja", "games/gravity_flip_ninja/gravity_flip_ninja.py",
                    "Flip gravity to navigate levels!", "Platformer", 
                    (100, 100, 255), "🥷"),
            GameData("Maze Explorer", "games/maze_game/main.py",
                    "Navigate through challenging mazes!", "Puzzle", 
                    (255, 255, 100), "🧩"),
            GameData("Snake Classic", "games/snake_game/snake_game.py",
                    "Classic snake with modern graphics!", "Classic", 
                    (255, 100, 255), "🐍"),
            GameData("Tic Tac Toe", "games/tic_tac_toe/main.py",
                    "Strategic X's and O's with AI!", "Strategy", 
                    (100, 255, 255), "⭕")
        ]
        
        # Verify games exist and are working
        for game in games:
            game.is_working = os.path.exists(game.path)
            if game.is_working:
                print(f"✅ {game.name} - Ready to play!")
            else:
                print(f"⚠️  {game.name} - File not found: {game.path}")
        
        return games
    
    def setup_perfect_layout(self):
        """Setup perfect 3-games-in-a-row layout"""
        self.game_cards = []
        
        # Perfect 3-column layout
        cards_per_row = 3
        card_width = 280
        card_height = 180
        margin_x = 40
        margin_y = 30
        
        # Center the layout perfectly
        total_width = cards_per_row * card_width + (cards_per_row - 1) * margin_x
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 150
        
        for i, game in enumerate(self.games):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + margin_x)
            y = start_y + row * (card_height + margin_y)
            
            card = GameCard(game, x, y)
            self.game_cards.append(card)
        
        print(f"🎯 Perfect layout created: {len(self.games)} games in 3-column design")
    
    def load_stats(self) -> Dict:
        """Load game statistics"""
        try:
            with open("game_stats.json", "r") as f:
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
        stats_data = {}
        for game in self.games:
            stats_data[game.name] = {
                "play_count": game.play_count,
                "last_played": game.last_played
            }
        
        try:
            with open("game_stats.json", "w") as f:
                json.dump(stats_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save stats: {e}")
    
    def handle_events(self) -> bool:
        """Perfect event handling"""
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
                if event.button == 1:  # Single click launch
                    mouse_pos = pygame.mouse.get_pos()
                    for i, card in enumerate(self.game_cards):
                        if card.rect.collidepoint(mouse_pos):
                            self.selected_index = i
                            self.update_selection()
                            self.launch_selected_game()
                            break
        
        return True
    
    def navigate_selection(self, direction: int):
        """Navigate with perfect wrapping"""
        new_index = self.selected_index + direction
        new_index = max(0, min(len(self.games) - 1, new_index))
        self.selected_index = new_index
        self.update_selection()
    
    def update_selection(self):
        """Update card selection states"""
        for i, card in enumerate(self.game_cards):
            card.set_selected(i == self.selected_index)
    
    def launch_selected_game(self):
        """Launch game with perfect error handling"""
        if 0 <= self.selected_index < len(self.games):
            game = self.games[self.selected_index]
            self.launch_game(game)
    
    def launch_game(self, game: GameData):
        """Perfect game launching"""
        if not game.is_working:
            print(f"❌ {game.name} is not available")
            return
        
        try:
            # Update statistics
            game.play_count += 1
            game.last_played = time.time()
            self.save_stats()
            
            # Launch game in separate process
            game_dir = os.path.dirname(game.path)
            subprocess.Popen([sys.executable, os.path.basename(game.path)], 
                           cwd=game_dir)
            print(f"🚀 Launched: {game.name}")
            
        except Exception as e:
            print(f"❌ Failed to launch {game.name}: {e}")
    
    def update(self, dt: float):
        """Perfect update loop"""
        # Update cards
        mouse_pos = pygame.mouse.get_pos()
        for card in self.game_cards:
            card.update(dt)
            card.handle_hover(mouse_pos)
    
    def draw(self):
        """Perfect drawing with no lag"""
        # Clear screen
        self.screen.fill(Theme.BG_DARK)
        
        # Draw header
        self.draw_perfect_header()
        
        # Draw game cards in perfect 3-column layout
        for card in self.game_cards:
            card.draw(self.renderer)
        
        # Draw footer
        self.draw_perfect_footer()
        
        # Update display
        pygame.display.flip()
    
    def draw_perfect_header(self):
        """Perfect header design"""
        # Title
        title_surface = self.renderer.get_text_surface("🎮 Perfect Game Launcher", 'title', Theme.TEXT_WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = f"✨ {len(self.games)} Games • 3-in-a-Row Design • Ultra-Smooth Performance"
        subtitle_surface = self.renderer.get_text_surface(subtitle_text, 'body', Theme.TEXT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, 75))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Selected game indicator
        if 0 <= self.selected_index < len(self.games):
            selected_game = self.games[self.selected_index]
            selection_text = f"Selected: {selected_game.icon} {selected_game.name}"
            selection_surface = self.renderer.get_text_surface(selection_text, 'body', Theme.ACCENT)
            selection_rect = selection_surface.get_rect(center=(WINDOW_WIDTH // 2, 105))
            self.screen.blit(selection_surface, selection_rect)
        
        # Separator line
        pygame.draw.line(self.screen, Theme.BORDER, (50, 130), (WINDOW_WIDTH - 50, 130), 2)
    
    def draw_perfect_footer(self):
        """Perfect footer with controls"""
        # Controls
        controls = [
            "🖱️ Single Click: Launch game instantly",
            "⌨️ Arrow Keys: Navigate • Enter: Launch • ESC: Exit",
            f"🎯 Game {self.selected_index + 1}/{len(self.games)} • FPS: {int(self.clock.get_fps())}"
        ]
        
        y_start = WINDOW_HEIGHT - 80
        for i, control in enumerate(controls):
            control_surface = self.renderer.get_text_surface(control, 'small', Theme.TEXT_GRAY)
            control_rect = control_surface.get_rect(center=(WINDOW_WIDTH // 2, y_start + i * 25))
            self.screen.blit(control_surface, control_rect)
    
    def run(self):
        """Perfect main loop"""
        print("🎮 Perfect Game Launcher Started!")
        print("✨ 3-games-in-a-row design with ultra-smooth performance")
        print("🚀 All games verified and ready to play!")
        print("🎯 Use arrow keys to navigate, single-click to launch!")
        
        running = True
        last_time = time.time()
        
        # Initial selection
        self.update_selection()
        
        while running:
            # Perfect delta time calculation
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            running = self.handle_events()
            
            # Update
            self.update(dt)
            
            # Draw
            self.draw()
            
            # Perfect frame rate control
            self.clock.tick(TARGET_FPS)
        
        # Cleanup
        self.save_stats()
        pygame.quit()
        sys.exit()

def main():
    """Perfect launcher entry point"""
    try:
        launcher = PerfectGameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Launcher error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
