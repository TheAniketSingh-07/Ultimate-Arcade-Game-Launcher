#!/usr/bin/env python3
"""
Fixed Optimized Game Launcher - High Performance Edition
Correctly detects and launches all games with proper file paths
"""

import pygame
import sys
import os
import subprocess
import json
import threading
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import time

# Performance optimizations
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)

# Optimized constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
TARGET_FPS = 120
VSYNC = True

class Theme:
    """Optimized color theme with pre-calculated values"""
    BG_DARK = (12, 12, 20)
    BG_SURFACE = (20, 20, 32)
    PRIMARY = (64, 128, 255)
    SECONDARY = (128, 64, 255)
    ACCENT = (255, 128, 64)
    SUCCESS = (64, 255, 128)
    TEXT_WHITE = (255, 255, 255)
    TEXT_GRAY = (180, 180, 200)
    TEXT_DARK = (120, 120, 140)
    CARD_BG = (28, 28, 44)
    CARD_HOVER = (36, 36, 52)
    CARD_ACTIVE = (44, 44, 60)
    BORDER = (60, 60, 80)

@dataclass
class GameData:
    """Lightweight game data structure"""
    name: str
    path: str
    description: str
    category: str
    color: Tuple[int, int, int]
    executable: str
    last_played: float = 0
    play_count: int = 0

class PerformanceMonitor:
    """Monitor and optimize performance"""
    def __init__(self):
        self.frame_times = []
        self.max_samples = 60
        self.last_time = time.time()
    
    def update(self):
        current_time = time.time()
        frame_time = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
    
    def get_fps(self) -> float:
        if not self.frame_times:
            return 0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0

class OptimizedRenderer:
    """High-performance rendering system"""
    def __init__(self, screen):
        self.screen = screen
        self.surface_cache = {}
        self.font_cache = {}
        self.dirty_rects = []
        
        # Pre-load fonts
        self.fonts = {
            'title': pygame.font.Font(None, 48),
            'subtitle': pygame.font.Font(None, 32),
            'body': pygame.font.Font(None, 24),
            'small': pygame.font.Font(None, 18)
        }
    
    def get_text_surface(self, text: str, font_key: str, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cached text rendering"""
        cache_key = (text, font_key, color)
        if cache_key not in self.surface_cache:
            font = self.fonts.get(font_key, self.fonts['body'])
            surface = font.render(text, True, color)
            self.surface_cache[cache_key] = surface
        return self.surface_cache[cache_key]
    
    def draw_rounded_rect(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                         rect: pygame.Rect, radius: int = 8):
        """Optimized rounded rectangle drawing"""
        if radius <= 0:
            pygame.draw.rect(surface, color, rect)
            return
        
        # Draw main rectangle
        pygame.draw.rect(surface, color, (rect.x + radius, rect.y, rect.width - 2*radius, rect.height))
        pygame.draw.rect(surface, color, (rect.x, rect.y + radius, rect.width, rect.height - 2*radius))
        
        # Draw corners
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(surface, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)

class GameCard:
    """Optimized game card with smooth animations"""
    def __init__(self, game_data: GameData, x: int, y: int, width: int = 280, height: int = 160):
        self.game_data = game_data
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.animation_speed = 0.15
        self.is_hovered = False
        self.click_animation = 0.0
    
    def update(self, dt: float):
        """Smooth animation updates"""
        # Scale animation
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * self.animation_speed
        
        # Click animation decay
        if self.click_animation > 0:
            self.click_animation = max(0, self.click_animation - dt * 3)
    
    def handle_hover(self, mouse_pos: Tuple[int, int]):
        """Handle hover state"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered and not was_hovered:
            self.target_scale = 1.05
        elif not self.is_hovered and was_hovered:
            self.target_scale = 1.0
    
    def handle_click(self):
        """Handle click animation"""
        self.click_animation = 1.0
        return self.game_data
    
    def draw(self, renderer: OptimizedRenderer):
        """Optimized drawing"""
        # Calculate animated position and size
        scale = self.hover_scale - self.click_animation * 0.05
        scaled_width = int(self.rect.width * scale)
        scaled_height = int(self.rect.height * scale)
        scaled_x = self.rect.x + (self.rect.width - scaled_width) // 2
        scaled_y = self.rect.y + (self.rect.height - scaled_height) // 2
        
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Background
        bg_color = Theme.CARD_HOVER if self.is_hovered else Theme.CARD_BG
        renderer.draw_rounded_rect(renderer.screen, bg_color, scaled_rect, 12)
        
        # Game icon (colored circle)
        icon_radius = 24
        icon_center = (scaled_rect.x + 40, scaled_rect.y + 40)
        pygame.draw.circle(renderer.screen, self.game_data.color, icon_center, icon_radius)
        
        # Game name
        name_surface = renderer.get_text_surface(self.game_data.name, 'subtitle', Theme.TEXT_WHITE)
        name_pos = (scaled_rect.x + 80, scaled_rect.y + 20)
        renderer.screen.blit(name_surface, name_pos)
        
        # Category
        category_surface = renderer.get_text_surface(self.game_data.category, 'small', Theme.TEXT_GRAY)
        category_pos = (scaled_rect.x + 80, scaled_rect.y + 50)
        renderer.screen.blit(category_surface, category_pos)
        
        # Description
        desc_lines = self.wrap_text(self.game_data.description, 30)
        for i, line in enumerate(desc_lines[:2]):  # Max 2 lines
            desc_surface = renderer.get_text_surface(line, 'small', Theme.TEXT_DARK)
            desc_pos = (scaled_rect.x + 20, scaled_rect.y + 80 + i * 20)
            renderer.screen.blit(desc_surface, desc_pos)
        
        # Play count indicator
        if self.game_data.play_count > 0:
            count_text = f"Played {self.game_data.play_count}x"
            count_surface = renderer.get_text_surface(count_text, 'small', Theme.ACCENT)
            count_pos = (scaled_rect.x + scaled_rect.width - 80, scaled_rect.y + scaled_rect.height - 25)
            renderer.screen.blit(count_surface, count_pos)
    
    def wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

class FixedOptimizedGameLauncher:
    """Main launcher class with fixed game detection"""
    
    def __init__(self):
        # Initialize display with optimizations
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
                                            pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("Fixed Optimized Game Launcher")
        
        # Performance components
        self.clock = pygame.time.Clock()
        self.performance_monitor = PerformanceMonitor()
        self.renderer = OptimizedRenderer(self.screen)
        
        # Game data
        self.games = self.load_games()
        self.game_cards = []
        self.selected_game = None
        
        # UI state
        self.scroll_offset = 0
        self.target_scroll = 0
        self.scroll_speed = 0.2
        
        # Statistics
        self.stats = self.load_stats()
        
        self.setup_game_cards()
    
    def find_game_executable(self, game_dir: str) -> Optional[str]:
        """Find the main executable file for a game"""
        if not os.path.exists(game_dir):
            return None
        
        # Common main file names to check
        possible_mains = [
            "main.py",
            f"{os.path.basename(game_dir)}.py",
            f"run_{os.path.basename(game_dir)}.py",
            "game.py",
            "run.py"
        ]
        
        for main_file in possible_mains:
            full_path = os.path.join(game_dir, main_file)
            if os.path.exists(full_path):
                return full_path
        
        # If no standard main file found, look for any .py file
        try:
            py_files = [f for f in os.listdir(game_dir) if f.endswith('.py') and not f.startswith('__')]
            if py_files:
                # Prefer files with 'main', 'game', or 'run' in the name
                for py_file in py_files:
                    if any(keyword in py_file.lower() for keyword in ['main', 'game', 'run']):
                        return os.path.join(game_dir, py_file)
                # Otherwise return the first .py file
                return os.path.join(game_dir, py_files[0])
        except OSError:
            pass
        
        return None
    
    def load_games(self) -> List[GameData]:
        """Load game data with proper file detection"""
        games = []
        games_dir = "games"
        
        if not os.path.exists(games_dir):
            return self.get_default_games()
        
        # Game configurations with proper descriptions and colors
        game_configs = {
            "dino_run": {
                "name": "Dino Run",
                "description": "Jump over obstacles in this endless runner!",
                "category": "Action",
                "color": (255, 100, 100)
            },
            "fighter_shoot": {
                "name": "Fighter Shoot",
                "description": "Epic space combat with alien enemies!",
                "category": "Shooter",
                "color": (100, 255, 100)
            },
            "gravity_flip_ninja": {
                "name": "Gravity Ninja",
                "description": "Flip gravity to navigate through levels!",
                "category": "Platformer",
                "color": (100, 100, 255)
            },
            "maze_game": {
                "name": "Maze Explorer",
                "description": "Navigate through challenging mazes!",
                "category": "Puzzle",
                "color": (255, 255, 100)
            },
            "snake_game": {
                "name": "Snake Classic",
                "description": "Classic snake game with modern graphics!",
                "category": "Classic",
                "color": (255, 100, 255)
            },
            "tic_tac_toe": {
                "name": "Tic Tac Toe",
                "description": "Strategic X's and O's gameplay!",
                "category": "Strategy",
                "color": (100, 255, 255)
            }
        }
        
        try:
            for game_dir in os.listdir(games_dir):
                game_path = os.path.join(games_dir, game_dir)
                if os.path.isdir(game_path):
                    # Find the executable file
                    executable_path = self.find_game_executable(game_path)
                    if executable_path:
                        config = game_configs.get(game_dir, {
                            "name": game_dir.replace('_', ' ').title(),
                            "description": f"Play {game_dir.replace('_', ' ')}!",
                            "category": "Game",
                            "color": (128, 128, 255)
                        })
                        
                        game_data = GameData(
                            name=config["name"],
                            path=executable_path,
                            description=config["description"],
                            category=config["category"],
                            color=config["color"],
                            executable=os.path.basename(executable_path)
                        )
                        games.append(game_data)
                        print(f"✅ Found game: {config['name']} -> {executable_path}")
        except Exception as e:
            print(f"Error loading games: {e}")
        
        return games if games else self.get_default_games()
    
    def get_default_games(self) -> List[GameData]:
        """Fallback games if directory is empty"""
        return [
            GameData("Demo Game", "demo_game.py", "A demonstration game", "Demo", (128, 128, 255), "demo_game.py")
        ]
    
    def load_stats(self) -> Dict:
        """Load game statistics"""
        try:
            with open("game_stats.json", "r") as f:
                return json.load(f)
        except:
            return {}
    
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
    
    def setup_game_cards(self):
        """Create game cards with optimized layout"""
        self.game_cards = []
        cards_per_row = 4
        card_width = 280
        card_height = 160
        margin = 20
        start_x = (WINDOW_WIDTH - (cards_per_row * card_width + (cards_per_row - 1) * margin)) // 2
        start_y = 120
        
        for i, game in enumerate(self.games):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            
            # Load stats for this game
            if game.name in self.stats:
                game.play_count = self.stats[game.name].get("play_count", 0)
                game.last_played = self.stats[game.name].get("last_played", 0)
            
            card = GameCard(game, x, y, card_width, card_height)
            self.game_cards.append(card)
    
    def handle_events(self) -> bool:
        """Optimized event handling"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    adjusted_mouse_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
                    for card in self.game_cards:
                        if card.rect.collidepoint(adjusted_mouse_pos):
                            selected_game = card.handle_click()
                            self.launch_game(selected_game)
                            break
            
            elif event.type == pygame.MOUSEWHEEL:
                # Smooth scrolling
                self.target_scroll += event.y * 30
                self.target_scroll = max(0, min(self.target_scroll, self.get_max_scroll()))
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
        
        return True
    
    def get_max_scroll(self) -> int:
        """Calculate maximum scroll offset"""
        if not self.game_cards:
            return 0
        
        max_y = max(card.rect.bottom for card in self.game_cards)
        return max(0, max_y - WINDOW_HEIGHT + 100)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        pygame.display.toggle_fullscreen()
    
    def update(self, dt: float):
        """Update game state with delta time"""
        # Smooth scrolling
        scroll_diff = self.target_scroll - self.scroll_offset
        self.scroll_offset += scroll_diff * self.scroll_speed
        
        # Update cards
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
        
        for card in self.game_cards:
            card.update(dt)
            card.handle_hover(adjusted_mouse_pos)
    
    def draw(self):
        """Optimized drawing with minimal redraws"""
        # Clear screen
        self.screen.fill(Theme.BG_DARK)
        
        # Draw header
        self.draw_header()
        
        # Draw game cards with scroll offset
        for card in self.game_cards:
            # Adjust card position for scrolling
            original_y = card.rect.y
            card.rect.y -= int(self.scroll_offset)
            
            # Only draw visible cards
            if -200 < card.rect.y < WINDOW_HEIGHT + 200:
                card.draw(self.renderer)
            
            # Restore original position
            card.rect.y = original_y
        
        # Draw performance info
        self.draw_performance_info()
        
        # Update display
        pygame.display.flip()
    
    def draw_header(self):
        """Draw the header section"""
        # Title
        title_surface = self.renderer.get_text_surface("🎮 Optimized Arcade Launcher", 'title', Theme.TEXT_WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = f"🚀 {len(self.games)} games ready • Lag-free • Smooth performance"
        subtitle_surface = self.renderer.get_text_surface(subtitle_text, 'body', Theme.TEXT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, 70))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Separator line
        pygame.draw.line(self.screen, Theme.BORDER, (50, 90), (WINDOW_WIDTH - 50, 90), 2)
    
    def draw_performance_info(self):
        """Draw performance information"""
        fps = self.performance_monitor.get_fps()
        fps_text = f"FPS: {fps:.1f}"
        fps_color = Theme.SUCCESS if fps > 60 else Theme.ACCENT if fps > 30 else Theme.TEXT_GRAY
        fps_surface = self.renderer.get_text_surface(fps_text, 'small', fps_color)
        self.screen.blit(fps_surface, (WINDOW_WIDTH - 100, 10))
        
        # Controls hint
        controls_text = "Mouse wheel: scroll • ESC: exit • F11: fullscreen"
        controls_surface = self.renderer.get_text_surface(controls_text, 'small', Theme.TEXT_DARK)
        self.screen.blit(controls_surface, (10, WINDOW_HEIGHT - 25))
    
    def launch_game(self, game_data: GameData):
        """Launch selected game with error handling"""
        if not os.path.exists(game_data.path):
            print(f"❌ Game file not found: {game_data.path}")
            return
        
        try:
            # Update statistics
            game_data.play_count += 1
            game_data.last_played = time.time()
            self.save_stats()
            
            # Launch game in separate process
            game_dir = os.path.dirname(game_data.path)
            subprocess.Popen([sys.executable, os.path.basename(game_data.path)], 
                           cwd=game_dir)
            print(f"🚀 Launched: {game_data.name}")
            
        except Exception as e:
            print(f"❌ Failed to launch {game_data.name}: {e}")
    
    def run(self):
        """Main game loop with performance optimizations"""
        running = True
        last_time = time.time()
        
        print("🚀 Fixed Optimized Game Launcher Started!")
        print("📊 Performance monitoring enabled")
        print("🎮 Use mouse wheel to scroll, ESC to exit, F11 for fullscreen")
        print(f"🎯 Found {len(self.games)} games ready to play!")
        
        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Update performance monitor
            self.performance_monitor.update()
            
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update(dt)
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(TARGET_FPS)
        
        # Cleanup
        self.save_stats()
        pygame.quit()
        sys.exit()

def main():
    """Entry point with error handling"""
    try:
        launcher = FixedOptimizedGameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Launcher error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
