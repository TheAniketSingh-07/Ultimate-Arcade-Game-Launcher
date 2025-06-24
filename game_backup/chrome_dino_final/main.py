#!/usr/bin/env python3
"""
Dino Run - Endless Runner Game
Entry point for the dino run arcade game
"""

import pygame
import sys
import os

# Add the project root to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from games.dino_run.game_logic import DinoGame
from games.dino_run.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE

def main():
    """Main entry point for Dino Run game"""
    
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    
    # Set up the clock for FPS control
    clock = pygame.time.Clock()
    
    # Create game instance
    game = DinoGame(screen)
    
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
    sys.exit()

if __name__ == "__main__":
    main()
