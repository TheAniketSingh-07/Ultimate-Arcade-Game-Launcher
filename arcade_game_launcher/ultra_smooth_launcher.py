#!/usr/bin/env python3
"""
Ultra-Smooth Game Launcher - Zero Micro-Lag Edition
Eliminates all forms of lag including micro-stuttering for perfect smoothness
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

# Ultra-optimized initialization
pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=128)

# Ultra-smooth constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TARGET_FPS = 120  # Higher FPS for ultra-smoothness
VSYNC = True

class UltraTheme:
    """Ultra-optimized theme colors"""
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
    """Ultra-lightweight game data"""
    name: str
    path: str
    description: str
    category: str
    color: Tuple[int, int, int]
    icon: str
    play_count: int = 0
    last_played: float = 0

class UltraRenderer:
    """Ultra-high performance renderer with zero micro-lag"""
    def __init__(self, screen):
        self.screen = screen
        self.surface_cache = {}
        self.font_cache = {}
        
        # Pre-load all fonts at startup
        self.fonts = {
            'title': pygame.font.Font(None, 56),
            'subtitle': pygame.font.Font(None, 36),
            'body': pygame.font.Font(None, 28),
            'small': pygame.font.Font(None, 20),
            'icon': pygame.font.Font(None, 48)
        }
        
        # Pre-render common text
        self.prerender_common_text()
    
    def prerender_common_text(self):
        """Pre-render commonly used text to eliminate rendering lag"""
        common_texts = [
            ("🎮 Ultra-Smooth Game Launcher", 'title', UltraTheme.TEXT_WHITE),
            ("✨ Perfect Performance • Zero Lag • Ultra-Smooth", 'body', UltraTheme.TEXT_GRAY),
            ("Ready", 'small', UltraTheme.SUCCESS),
            ("FPS:", 'small', UltraTheme.TEXT_GRAY),
            ("Game", 'small', UltraTheme.TEXT_GRAY),
        ]
        
        for text, font_key, color in common_texts:
            cache_key = (text, font_key, color)
            font = self.fonts[font_key]
            self.surface_cache[cache_key] = font.render(text, True, color)
    
    def get_text_surface(self, text: str, font_key: str, color: Tuple[int, int, int]):
        """Ultra-fast cached text rendering"""
        cache_key = (text, font_key, color)
        
        if cache_key not in self.surface_cache:
            font = self.fonts[font_key]
            self.surface_cache[cache_key] = font.render(text, True, color)
        
        return self.surface_cache[cache_key]
    
    def draw_rounded_rect(self, color: Tuple[int, int, int], rect: pygame.Rect, radius: int = 12):
        """Ultra-optimized rounded rectangle"""
        if radius <= 0:
            pygame.draw.rect(self.screen, color, rect)
            return
        
        # Optimized corner drawing
        pygame.draw.rect(self.screen, color, (rect.x + radius, rect.y, rect.width - 2*radius, rect.height))
        pygame.draw.rect(self.screen, color, (rect.x, rect.y + radius, rect.width, rect.height - 2*radius))
        
        # Draw corners
        pygame.draw.circle(self.screen, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + rect.width - radius, rect.y + radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + radius, rect.y + rect.height - radius), radius)
        pygame.draw.circle(self.screen, color, (rect.x + rect.width - radius, rect.y + rect.height - radius), radius)

class UltraSmoothCard:
    """Ultra-smooth game card with zero micro-lag"""
    def __init__(self, game_data: GameData, x: int, y: int):
        self.game_data = game_data
        self.rect = pygame.Rect(x, y, 280, 180)
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.is_hovered = False
        self.is_selected = False
        self.glow_intensity = 0.0
        
        # Ultra-smooth animation parameters
        self.animation_speed = 0.25  # Faster response
        self.scale_smoothing = 0.15
        
        # Pre-calculate positions
        self.center_x = x + 140
        self.center_y = y + 90
    
    def update(self, dt: float):
        """Ultra-smooth animation updates with interpolation"""
        # Smooth scale interpolation
        scale_diff = self.target_scale - self.hover_scale
        self.hover_scale += scale_diff * self.scale_smoothing
        
        # Smooth glow interpolation
        target_glow = 1.0 if (self.is_selected or self.is_hovered) else 0.0
        glow_diff = target_glow - self.glow_intensity
        self.glow_intensity += glow_diff * self.animation_speed
    
    def handle_hover(self, mouse_pos: Tuple[int, int]):
        """Ultra-responsive hover detection"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered != was_hovered:
            self.target_scale = 1.05 if self.is_hovered else 1.0
    
    def set_selected(self, selected: bool):
        """Ultra-smooth selection state"""
        self.is_selected = selected
        if selected:
            self.target_scale = 1.08
        else:
            self.target_scale = 1.05 if self.is_hovered else 1.0
    
    def draw(self, renderer: UltraRenderer):
        """Ultra-optimized drawing with zero lag"""
        # Calculate scaled dimensions
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
            renderer.draw_rounded_rect(UltraTheme.PRIMARY, glow_rect, 16)
        
        # Card background
        bg_color = UltraTheme.CARD_SELECTED if self.is_selected else UltraTheme.CARD_HOVER if self.is_hovered else UltraTheme.CARD_BG
        renderer.draw_rounded_rect(bg_color, scaled_rect, 12)
        
        # Game icon
        icon_surface = renderer.get_text_surface(self.game_data.icon, 'icon', self.game_data.color)
        icon_rect = icon_surface.get_rect(center=(scaled_rect.x + 60, scaled_rect.y + 50))
        renderer.screen.blit(icon_surface, icon_rect)
        
        # Game name
        name_surface = renderer.get_text_surface(self.game_data.name, 'subtitle', UltraTheme.TEXT_WHITE)
        renderer.screen.blit(name_surface, (scaled_rect.x + 20, scaled_rect.y + 90))
        
        # Category
        category_surface = renderer.get_text_surface(self.game_data.category, 'small', UltraTheme.TEXT_GRAY)
        renderer.screen.blit(category_surface, (scaled_rect.x + 20, scaled_rect.y + 120))
        
        # Status
        status_surface = renderer.get_text_surface("✅ Ready", 'small', UltraTheme.SUCCESS)
        renderer.screen.blit(status_surface, (scaled_rect.x + scaled_rect.width - 80, scaled_rect.y + 15))

class UltraSmoothLauncher:
    """Ultra-smooth launcher with zero micro-lag"""
    
    def __init__(self):
        # Ultra-optimized display setup
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if VSYNC:
            flags |= pygame.SCALED
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
        pygame.display.set_caption("🎮 Ultra-Smooth Game Launcher")
        
        # Ultra-high performance clock
        self.clock = pygame.time.Clock()
        self.renderer = UltraRenderer(self.screen)
        
        # Game data
        self.games = self.load_games()
        self.game_cards = []
        self.selected_index = 0
        
        # Performance tracking
        self.frame_times = []
        self.fps_display = 120
        
        # Statistics
        self.stats = self.load_stats()
        
        self.setup_ultra_layout()
        self.load_game_stats()
    
    def load_games(self) -> List[GameData]:
        """Load games with ultra-fast detection"""
        return [
            GameData("Dino Run", "games/dino_run/main.py", 
                    "Ultra-smooth endless runner!", "Action", 
                    (255, 100, 100), "🦕"),
            GameData("Fighter Shoot", "games/fighter_shoot/main.py",
                    "Smooth space combat!", "Shooter", 
                    (100, 255, 100), "🚀"),
            GameData("Gravity Ninja", "games/gravity_flip_ninja/gravity_flip_ninja.py",
                    "Ultra-smooth gravity flipping!", "Platformer", 
                    (100, 100, 255), "🥷"),
            GameData("Maze Explorer", "games/maze_game/main.py",
                    "Smooth maze navigation!", "Puzzle", 
                    (255, 255, 100), "🧩"),
            GameData("Snake Classic", "games/snake_game/snake_game.py",
                    "Classic smooth snake!", "Classic", 
                    (255, 100, 255), "🐍"),
            GameData("Tic Tac Toe", "games/tic_tac_toe/main.py",
                    "Strategic AI gameplay!", "Strategy", 
                    (100, 255, 255), "⭕")
        ]
    
    def setup_ultra_layout(self):
        """Setup ultra-optimized 3-column layout"""
        self.game_cards = []
        
        # Perfect 3-column layout
        cards_per_row = 3
        card_width = 280
        card_height = 180
        margin_x = 40
        margin_y = 30
        
        # Center perfectly
        total_width = cards_per_row * card_width + (cards_per_row - 1) * margin_x
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 150
        
        for i, game in enumerate(self.games):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + margin_x)
            y = start_y + row * (card_height + margin_y)
            
            card = UltraSmoothCard(game, x, y)
            self.game_cards.append(card)
    
    def load_stats(self) -> Dict:
        """Ultra-fast stats loading"""
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
        """Ultra-fast stats saving"""
        stats_data = {game.name: {"play_count": game.play_count, "last_played": game.last_played} 
                     for game in self.games}
        try:
            with open("game_stats.json", "w") as f:
                json.dump(stats_data, f, indent=2)
        except:
            pass
    
    def handle_events(self) -> bool:
        """Ultra-responsive event handling"""
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
        """Ultra-smooth navigation"""
        new_index = max(0, min(len(self.games) - 1, self.selected_index + direction))
        self.selected_index = new_index
        self.update_selection()
    
    def update_selection(self):
        """Ultra-fast selection update"""
        for i, card in enumerate(self.game_cards):
            card.set_selected(i == self.selected_index)
    
    def launch_selected_game(self):
        """Ultra-fast game launching"""
        if 0 <= self.selected_index < len(self.games):
            game = self.games[self.selected_index]
            self.launch_game(game)
    
    def launch_game(self, game: GameData):
        """Ultra-optimized game launching"""
        try:
            game.play_count += 1
            game.last_played = time.time()
            self.save_stats()
            
            # Launch in separate thread for zero lag
            def launch_thread():
                game_dir = os.path.dirname(game.path)
                subprocess.Popen([sys.executable, os.path.basename(game.path)], 
                               cwd=game_dir)
            
            threading.Thread(target=launch_thread, daemon=True).start()
            print(f"🚀 Launched: {game.name}")
        except Exception as e:
            print(f"❌ Failed to launch {game.name}: {e}")
    
    def update(self, dt: float):
        """Ultra-smooth update loop"""
        # Update performance tracking
        self.frame_times.append(dt)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        self.fps_display = int(1.0 / avg_frame_time) if avg_frame_time > 0 else 120
        
        # Update cards with ultra-smooth animations
        mouse_pos = pygame.mouse.get_pos()
        for card in self.game_cards:
            card.update(dt)
            card.handle_hover(mouse_pos)
    
    def draw(self):
        """Ultra-optimized drawing with zero micro-lag"""
        # Clear with optimized fill
        self.screen.fill(UltraTheme.BG_DARK)
        
        # Draw header
        self.draw_ultra_header()
        
        # Draw cards with ultra-smooth rendering
        for card in self.game_cards:
            card.draw(self.renderer)
        
        # Draw footer
        self.draw_ultra_footer()
        
        # Ultra-smooth display update
        pygame.display.flip()
    
    def draw_ultra_header(self):
        """Ultra-optimized header drawing"""
        # Title
        title_surface = self.renderer.get_text_surface("🎮 Ultra-Smooth Game Launcher", 'title', UltraTheme.TEXT_WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_surface = self.renderer.get_text_surface("✨ Perfect Performance • Zero Lag • Ultra-Smooth", 'body', UltraTheme.TEXT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, 75))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Selected game
        if 0 <= self.selected_index < len(self.games):
            selected_game = self.games[self.selected_index]
            selection_text = f"Selected: {selected_game.icon} {selected_game.name}"
            selection_surface = self.renderer.get_text_surface(selection_text, 'body', UltraTheme.ACCENT)
            selection_rect = selection_surface.get_rect(center=(WINDOW_WIDTH // 2, 105))
            self.screen.blit(selection_surface, selection_rect)
        
        # Separator
        pygame.draw.line(self.screen, UltraTheme.BORDER, (50, 130), (WINDOW_WIDTH - 50, 130), 2)
    
    def draw_ultra_footer(self):
        """Ultra-optimized footer drawing"""
        controls = [
            "🖱️ Single Click: Launch instantly • ⌨️ Arrow Keys: Navigate • Enter: Launch • ESC: Exit",
            f"🎯 Game {self.selected_index + 1}/{len(self.games)} • FPS: {self.fps_display} • Ultra-Smooth Performance"
        ]
        
        y_start = WINDOW_HEIGHT - 60
        for i, control in enumerate(controls):
            control_surface = self.renderer.get_text_surface(control, 'small', UltraTheme.TEXT_GRAY)
            control_rect = control_surface.get_rect(center=(WINDOW_WIDTH // 2, y_start + i * 25))
            self.screen.blit(control_surface, control_rect)
    
    def run(self):
        """Ultra-smooth main loop with zero micro-lag"""
        print("🎮 Ultra-Smooth Game Launcher Started!")
        print("✨ Zero micro-lag • Perfect smoothness • Ultra-responsive")
        print("🚀 All games optimized for maximum performance!")
        
        running = True
        last_time = time.time()
        
        # Initial setup
        self.update_selection()
        
        while running:
            # Ultra-precise timing
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Cap delta time for stability
            dt = min(dt, 1/60)
            
            # Ultra-responsive event handling
            running = self.handle_events()
            
            # Ultra-smooth updates
            self.update(dt)
            
            # Ultra-optimized drawing
            self.draw()
            
            # Ultra-smooth frame rate control
            self.clock.tick(TARGET_FPS)
        
        # Cleanup
        self.save_stats()
        pygame.quit()
        sys.exit()

def main():
    """Ultra-smooth launcher entry point"""
    try:
        launcher = UltraSmoothLauncher()
        launcher.run()
    except Exception as e:
        print(f"Launcher error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
