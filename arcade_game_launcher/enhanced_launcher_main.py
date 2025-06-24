#!/usr/bin/env python3
"""
Enhanced Game Launcher - Main Class
Complete launcher with keyboard controls, last game memory, and single-click launch
"""

from enhanced_launcher import *

class EnhancedGameLauncher:
    """Main launcher class with enhanced controls"""
    
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
                                            pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("Enhanced Game Launcher - Keyboard Controls")
        
        # Performance components
        self.clock = pygame.time.Clock()
        self.performance_monitor = PerformanceMonitor()
        self.renderer = OptimizedRenderer(self.screen)
        
        # Game data
        self.games = self.load_games()
        self.game_cards = []
        
        # Selection and navigation
        self.selected_index = 0
        self.last_game_index = -1
        
        # UI state
        self.scroll_offset = 0
        self.target_scroll = 0
        self.scroll_speed = 0.2
        
        # Statistics and settings
        self.stats = self.load_stats()
        self.settings = self.load_settings()
        
        # Control hints
        self.show_controls = True
        self.control_fade = 1.0
        
        self.setup_game_cards()
        self.load_last_game()
    
    def find_game_executable(self, game_dir: str) -> Optional[str]:
        """Find the main executable file for a game"""
        if not os.path.exists(game_dir):
            return None
        
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
        
        # Look for any .py file
        try:
            py_files = [f for f in os.listdir(game_dir) if f.endswith('.py') and not f.startswith('__')]
            if py_files:
                for py_file in py_files:
                    if any(keyword in py_file.lower() for keyword in ['main', 'game', 'run']):
                        return os.path.join(game_dir, py_file)
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
        
        game_configs = {
            "dino_run": {
                "name": "🦕 Dino Run",
                "description": "Jump over obstacles in endless runner!",
                "category": "Action",
                "color": (255, 100, 100)
            },
            "fighter_shoot": {
                "name": "🚀 Fighter Shoot",
                "description": "Epic space combat with aliens!",
                "category": "Shooter",
                "color": (100, 255, 100)
            },
            "gravity_flip_ninja": {
                "name": "🥷 Gravity Ninja",
                "description": "Flip gravity to navigate levels!",
                "category": "Platformer",
                "color": (100, 100, 255)
            },
            "maze_game": {
                "name": "🧩 Maze Explorer",
                "description": "Navigate through challenging mazes!",
                "category": "Puzzle",
                "color": (255, 255, 100)
            },
            "snake_game": {
                "name": "🐍 Snake Classic",
                "description": "Classic snake with modern graphics!",
                "category": "Classic",
                "color": (255, 100, 255)
            },
            "tic_tac_toe": {
                "name": "⭕ Tic Tac Toe",
                "description": "Strategic X's and O's gameplay!",
                "category": "Strategy",
                "color": (100, 255, 255)
            }
        }
        
        try:
            for game_dir in os.listdir(games_dir):
                game_path = os.path.join(games_dir, game_dir)
                if os.path.isdir(game_path):
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
        """Fallback games"""
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
    
    def load_settings(self) -> Dict:
        """Load launcher settings"""
        try:
            with open("launcher_settings.json", "r") as f:
                return json.load(f)
        except:
            return {"last_game": "", "show_controls": True}
    
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
    
    def save_settings(self):
        """Save launcher settings"""
        settings_data = {
            "last_game": self.games[self.last_game_index].name if self.last_game_index >= 0 else "",
            "show_controls": self.show_controls
        }
        
        try:
            with open("launcher_settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")
    
    def load_last_game(self):
        """Load and select the last played game"""
        last_game_name = self.settings.get("last_game", "")
        if last_game_name:
            for i, game in enumerate(self.games):
                if game.name == last_game_name:
                    self.last_game_index = i
                    self.selected_index = i
                    self.update_selection()
                    break
    
    def setup_game_cards(self):
        """Create game cards with optimized layout"""
        self.game_cards = []
        cards_per_row = 4
        card_width = 280
        card_height = 160
        margin = 20
        start_x = (WINDOW_WIDTH - (cards_per_row * card_width + (cards_per_row - 1) * margin)) // 2
        start_y = 140
        
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
    
    def update_selection(self):
        """Update card selection states"""
        for i, card in enumerate(self.game_cards):
            card.set_selected(i == self.selected_index)
    
    def navigate_selection(self, direction: str):
        """Navigate game selection with keyboard"""
        if not self.games:
            return
        
        cards_per_row = 4
        rows = (len(self.games) + cards_per_row - 1) // cards_per_row
        current_row = self.selected_index // cards_per_row
        current_col = self.selected_index % cards_per_row
        
        if direction == "up" and current_row > 0:
            self.selected_index = (current_row - 1) * cards_per_row + current_col
        elif direction == "down" and current_row < rows - 1:
            new_index = (current_row + 1) * cards_per_row + current_col
            if new_index < len(self.games):
                self.selected_index = new_index
        elif direction == "left" and current_col > 0:
            self.selected_index -= 1
        elif direction == "right" and current_col < cards_per_row - 1 and self.selected_index + 1 < len(self.games):
            self.selected_index += 1
        
        self.update_selection()
        self.ensure_visible()
    
    def ensure_visible(self):
        """Ensure selected card is visible"""
        if not self.game_cards or self.selected_index >= len(self.game_cards):
            return
        
        selected_card = self.game_cards[self.selected_index]
        card_top = selected_card.rect.y - self.scroll_offset
        card_bottom = selected_card.rect.bottom - self.scroll_offset
        
        if card_top < 140:  # Above visible area
            self.target_scroll = selected_card.rect.y - 140
        elif card_bottom > WINDOW_HEIGHT - 100:  # Below visible area
            self.target_scroll = selected_card.rect.bottom - WINDOW_HEIGHT + 100
        
        self.target_scroll = max(0, min(self.target_scroll, self.get_max_scroll()))
    
    def launch_selected_game(self):
        """Launch the currently selected game"""
        if 0 <= self.selected_index < len(self.games):
            game = self.games[self.selected_index]
            self.launch_game(game)
            self.last_game_index = self.selected_index
            self.save_settings()
    
    def launch_last_game(self):
        """Launch the last played game"""
        if self.last_game_index >= 0 and self.last_game_index < len(self.games):
            game = self.games[self.last_game_index]
            self.launch_game(game)
            print(f"🔄 Launched last game: {game.name}")
    
    def handle_events(self) -> bool:
        """Enhanced event handling with keyboard controls"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.launch_selected_game()
                elif event.key == pygame.K_UP:
                    self.navigate_selection("up")
                elif event.key == pygame.K_DOWN:
                    self.navigate_selection("down")
                elif event.key == pygame.K_LEFT:
                    self.navigate_selection("left")
                elif event.key == pygame.K_RIGHT:
                    self.navigate_selection("right")
                elif event.key == pygame.K_l:  # L for Last game
                    self.launch_last_game()
                elif event.key == pygame.K_h:  # H for Help/Controls
                    self.show_controls = not self.show_controls
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_r:  # R for Refresh
                    self.refresh_games()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - Single click launch
                    mouse_pos = pygame.mouse.get_pos()
                    adjusted_mouse_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
                    for i, card in enumerate(self.game_cards):
                        if card.rect.collidepoint(adjusted_mouse_pos):
                            self.selected_index = i
                            self.update_selection()
                            # Single click launch
                            self.launch_selected_game()
                            break
            
            elif event.type == pygame.MOUSEWHEEL:
                self.target_scroll += event.y * 30
                self.target_scroll = max(0, min(self.target_scroll, self.get_max_scroll()))
        
        return True
    
    def refresh_games(self):
        """Refresh game list"""
        print("🔄 Refreshing games...")
        self.games = self.load_games()
        self.setup_game_cards()
        self.selected_index = min(self.selected_index, len(self.games) - 1)
        self.update_selection()
    
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
        """Update game state"""
        # Smooth scrolling
        scroll_diff = self.target_scroll - self.scroll_offset
        self.scroll_offset += scroll_diff * self.scroll_speed
        
        # Update cards
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
        
        for card in self.game_cards:
            card.update(dt)
            card.handle_hover(adjusted_mouse_pos)
        
        # Control fade animation
        if self.show_controls:
            self.control_fade = min(1.0, self.control_fade + dt * 2)
        else:
            self.control_fade = max(0.0, self.control_fade - dt * 2)
    
    def draw(self):
        """Enhanced drawing with controls"""
        self.screen.fill(Theme.BG_DARK)
        
        # Draw header
        self.draw_header()
        
        # Draw game cards
        for card in self.game_cards:
            original_y = card.rect.y
            card.rect.y -= int(self.scroll_offset)
            
            if -200 < card.rect.y < WINDOW_HEIGHT + 200:
                card.draw(self.renderer)
            
            card.rect.y = original_y
        
        # Draw controls
        if self.control_fade > 0:
            self.draw_controls()
        
        # Draw performance info
        self.draw_performance_info()
        
        pygame.display.flip()
    
    def draw_header(self):
        """Draw enhanced header"""
        # Title
        title_surface = self.renderer.get_text_surface("🎮 Enhanced Game Launcher", 'title', Theme.TEXT_WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle with last game info
        if self.last_game_index >= 0:
            last_game_name = self.games[self.last_game_index].name
            subtitle_text = f"🚀 {len(self.games)} games • Last played: {last_game_name}"
        else:
            subtitle_text = f"🚀 {len(self.games)} games ready • Use arrow keys to navigate"
        
        subtitle_surface = self.renderer.get_text_surface(subtitle_text, 'body', Theme.TEXT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, 70))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Current selection indicator
        if 0 <= self.selected_index < len(self.games):
            selected_game = self.games[self.selected_index]
            selection_text = f"Selected: {selected_game.name}"
            selection_surface = self.renderer.get_text_surface(selection_text, 'small', Theme.ACCENT)
            selection_rect = selection_surface.get_rect(center=(WINDOW_WIDTH // 2, 95))
            self.screen.blit(selection_surface, selection_rect)
        
        # Separator
        pygame.draw.line(self.screen, Theme.BORDER, (50, 110), (WINDOW_WIDTH - 50, 110), 2)
    
    def draw_controls(self):
        """Draw control instructions"""
        if self.control_fade <= 0:
            return
        
        controls = [
            "🎮 CONTROLS:",
            "Arrow Keys: Navigate games",
            "Enter/Space: Launch selected game",
            "L: Launch last played game",
            "Mouse Click: Single-click launch",
            "Mouse Wheel: Scroll",
            "H: Toggle help",
            "R: Refresh games",
            "ESC: Exit"
        ]
        
        # Background panel
        panel_height = len(controls) * 25 + 20
        panel_rect = pygame.Rect(20, WINDOW_HEIGHT - panel_height - 20, 300, panel_height)
        panel_color = (*Theme.BG_SURFACE, int(200 * self.control_fade))
        
        # Create surface with alpha
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill(panel_color)
        self.screen.blit(panel_surface, panel_rect)
        
        # Draw controls text
        for i, control in enumerate(controls):
            color = Theme.TEXT_WHITE if i == 0 else Theme.TEXT_GRAY
            alpha_color = (*color, int(255 * self.control_fade))
            
            control_surface = self.renderer.get_text_surface(control, 'small', color)
            control_surface.set_alpha(int(255 * self.control_fade))
            
            y_pos = panel_rect.y + 10 + i * 25
            self.screen.blit(control_surface, (panel_rect.x + 10, y_pos))
    
    def draw_performance_info(self):
        """Draw performance and status info"""
        fps = self.performance_monitor.get_fps()
        fps_text = f"FPS: {fps:.1f}"
        fps_color = Theme.SUCCESS if fps > 60 else Theme.ACCENT if fps > 30 else Theme.TEXT_GRAY
        fps_surface = self.renderer.get_text_surface(fps_text, 'small', fps_color)
        self.screen.blit(fps_surface, (WINDOW_WIDTH - 100, 10))
        
        # Status info
        status_text = f"Game {self.selected_index + 1}/{len(self.games)}"
        status_surface = self.renderer.get_text_surface(status_text, 'small', Theme.TEXT_GRAY)
        self.screen.blit(status_surface, (WINDOW_WIDTH - 100, 30))
    
    def launch_game(self, game_data: GameData):
        """Launch game with enhanced feedback"""
        if not os.path.exists(game_data.path):
            print(f"❌ Game file not found: {game_data.path}")
            return
        
        try:
            # Update statistics
            game_data.play_count += 1
            game_data.last_played = time.time()
            self.save_stats()
            
            # Launch game
            game_dir = os.path.dirname(game_data.path)
            subprocess.Popen([sys.executable, os.path.basename(game_data.path)], 
                           cwd=game_dir)
            print(f"🚀 Launched: {game_data.name}")
            
        except Exception as e:
            print(f"❌ Failed to launch {game_data.name}: {e}")
    
    def run(self):
        """Main game loop"""
        running = True
        last_time = time.time()
        
        print("🚀 Enhanced Game Launcher Started!")
        print("📊 Performance monitoring enabled")
        print("🎮 Use arrow keys to navigate, Enter to launch!")
        print("💡 Press H to toggle help, L for last game")
        print(f"🎯 Found {len(self.games)} games ready to play!")
        
        while running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            self.performance_monitor.update()
            running = self.handle_events()
            self.update(dt)
            self.draw()
            self.clock.tick(TARGET_FPS)
        
        self.save_stats()
        self.save_settings()
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    try:
        launcher = EnhancedGameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Launcher error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
