#!/usr/bin/env python3
"""
Maze Adventure - Smooth Explorer
Advanced maze game with smooth character movement and good graphics
"""

import pygame
import sys
import os

# Add the project root to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from games.maze_game.game_logic import MazeGame
from games.maze_game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE

def main():
    """Main entry point for Maze Adventure game"""
    
    print("🎮 Starting Maze Adventure - Smooth Explorer...")
    print("Controls: WASD or Arrow Keys to move, SPACE to start/continue")
    
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    
    # Set up the clock for FPS control
    clock = pygame.time.Clock()
    
    # Create game instance
    game = MazeGame(screen)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    print("Thanks for playing Maze Adventure! 🏆")
    sys.exit()

if __name__ == "__main__":
    main()
