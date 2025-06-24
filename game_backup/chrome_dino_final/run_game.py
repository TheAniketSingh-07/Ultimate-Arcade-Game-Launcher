#!/usr/bin/env python3
"""
Chrome Dino Game - Standalone Runner
Run this file to play the saved Chrome Dino game
"""

import pygame
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Import game components
from game_logic import DinoGame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE

def main():
    """Run the Chrome Dino Game"""
    print("🦕 Starting Chrome Dino Game...")
    print("Controls: SPACEBAR/UP = Jump, DOWN = Duck, SPACEBAR = Restart")
    
    # Initialize Pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    
    # Set up clock
    clock = pygame.time.Clock()
    
    # Create game
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
        
        # Update and draw
        game.update()
        game.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()
    print("Thanks for playing Chrome Dino! 🎮")

if __name__ == "__main__":
    main()
