#!/usr/bin/env python3
"""
Arcade Game Launcher
Main launcher for all arcade games
"""

import pygame
import sys
import os
from enum import Enum

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

class GameState(Enum):
    MAIN_MENU = "main_menu"
    GAME_SELECTION = "game_selection"
    SETTINGS = "settings"
    QUIT = "quit"

class ArcadeLauncher:
    """Main launcher application"""
    
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.screen_width = 1200
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("🎮 Arcade Game Launcher")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 200)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.GRAY = (128, 128, 128)
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Game state
        self.state = GameState.MAIN_MENU
        self.selected_option = 0
        self.clock = pygame.time.Clock()
        
        # Available games
        self.games = [
            {
                'name': '🦕 Dino Run',
                'description': 'Endless runner adventure',
                'module': 'games.dino_run.main',
                'status': 'Ready'
            },
            {
                'name': '🚀 Fighter Shoot',
                'description': 'Space shooter action',
                'module': 'games.fighter_shoot.main',
                'status': 'Coming Soon'
            },
            {
                'name': '⭕ Tic Tac Toe',
                'description': 'Classic strategy game',
                'module': 'games.tic_tac_toe.main',
                'status': 'Coming Soon'
            },
            {
                'name': '🌟 Maze Game',
                'description': 'Navigate the labyrinth',
                'module': 'games.maze_game.main',
                'status': 'Coming Soon'
            }
        ]
        
    def draw_text(self, text, font, color, x, y, center=False):
        """Draw text on screen"""
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, (x, y))
            
    def draw_main_menu(self):
        """Draw the main menu"""
        self.screen.fill(self.BLACK)
        
        # Title
        self.draw_text("🎮 ARCADE GAME LAUNCHER", self.font_large, self.WHITE,
                      self.screen_width // 2, 100, center=True)
        
        # Subtitle
        self.draw_text("Classic Games Collection", self.font_medium, self.GRAY,
                      self.screen_width // 2, 150, center=True)
        
        # Menu options
        menu_options = ["Play Games", "Settings", "Exit"]
        start_y = 250
        
        for i, option in enumerate(menu_options):
            color = self.GREEN if i == self.selected_option else self.WHITE
            self.draw_text(option, self.font_medium, color,
                          self.screen_width // 2, start_y + i * 60, center=True)
        
        # Instructions
        self.draw_text("Use UP/DOWN arrows to navigate, SPACE to select", 
                      self.font_small, self.GRAY,
                      self.screen_width // 2, 500, center=True)
                      
    def draw_game_selection(self):
        """Draw the game selection menu"""
        self.screen.fill(self.BLACK)
        
        # Title
        self.draw_text("🎮 SELECT GAME", self.font_large, self.WHITE,
                      self.screen_width // 2, 80, center=True)
        
        # Game list
        start_y = 150
        for i, game in enumerate(self.games):
            # Highlight selected game
            if i == self.selected_option:
                pygame.draw.rect(self.screen, self.BLUE, 
                               (100, start_y + i * 100 - 10, 
                                self.screen_width - 200, 80))
            
            # Game name
            color = self.WHITE if game['status'] == 'Ready' else self.GRAY
            self.draw_text(game['name'], self.font_medium, color,
                          120, start_y + i * 100)
            
            # Game description
            self.draw_text(game['description'], self.font_small, self.GRAY,
                          120, start_y + i * 100 + 30)
            
            # Status
            status_color = self.GREEN if game['status'] == 'Ready' else self.RED
            self.draw_text(game['status'], self.font_small, status_color,
                          self.screen_width - 200, start_y + i * 100 + 15)
        
        # Instructions
        self.draw_text("UP/DOWN: Navigate | SPACE: Play | ESC: Back", 
                      self.font_small, self.GRAY,
                      self.screen_width // 2, 550, center=True)
                      
    def draw_settings(self):
        """Draw the settings menu"""
        self.screen.fill(self.BLACK)
        
        # Title
        self.draw_text("⚙️ SETTINGS", self.font_large, self.WHITE,
                      self.screen_width // 2, 100, center=True)
        
        # Settings info
        settings_text = [
            "🔊 Audio: Enabled",
            "🖥️  Resolution: 1200x600",
            "🎮 Controls: Keyboard",
            "📁 Game Data: Local Storage"
        ]
        
        start_y = 200
        for i, setting in enumerate(settings_text):
            self.draw_text(setting, self.font_medium, self.WHITE,
                          self.screen_width // 2, start_y + i * 50, center=True)
        
        # Back instruction
        self.draw_text("Press ESC to go back", self.font_small, self.GRAY,
                      self.screen_width // 2, 500, center=True)
                      
    def handle_main_menu_input(self, event):
        """Handle main menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 3
            elif event.key == pygame.K_SPACE:
                if self.selected_option == 0:  # Play Games
                    self.state = GameState.GAME_SELECTION
                    self.selected_option = 0
                elif self.selected_option == 1:  # Settings
                    self.state = GameState.SETTINGS
                elif self.selected_option == 2:  # Exit
                    self.state = GameState.QUIT
                    
    def handle_game_selection_input(self, event):
        """Handle game selection input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.games)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.games)
            elif event.key == pygame.K_SPACE:
                game = self.games[self.selected_option]
                if game['status'] == 'Ready':
                    self.launch_game(game)
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MAIN_MENU
                self.selected_option = 0
                
    def handle_settings_input(self, event):
        """Handle settings input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MAIN_MENU
                self.selected_option = 0
                
    def launch_game(self, game):
        """Launch the selected game"""
        print(f"🚀 Launching {game['name']}...")
        
        try:
            if game['name'] == '🦕 Dino Run':
                # Close launcher window
                pygame.quit()
                
                # Launch Dino Run
                import subprocess
                subprocess.run([sys.executable, 'games/dino_run/main.py'], 
                             cwd=os.path.dirname(__file__))
                
                # Restart launcher after game closes
                pygame.init()
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                pygame.display.set_caption("🎮 Arcade Game Launcher")
                
        except Exception as e:
            print(f"❌ Failed to launch {game['name']}: {e}")
            
    def run(self):
        """Main launcher loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.state == GameState.MAIN_MENU:
                    self.handle_main_menu_input(event)
                elif self.state == GameState.GAME_SELECTION:
                    self.handle_game_selection_input(event)
                elif self.state == GameState.SETTINGS:
                    self.handle_settings_input(event)
                    
            # Check for quit state
            if self.state == GameState.QUIT:
                running = False
                
            # Draw current screen
            if self.state == GameState.MAIN_MENU:
                self.draw_main_menu()
            elif self.state == GameState.GAME_SELECTION:
                self.draw_game_selection()
            elif self.state == GameState.SETTINGS:
                self.draw_settings()
                
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    print("🎮 Starting Arcade Game Launcher...")
    launcher = ArcadeLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
