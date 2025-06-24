"""
Maze Game Settings
Configuration for the maze game with good graphics
"""

import pygame

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

# Game info
GAME_TITLE = "Maze Adventure - Smooth Explorer"

# Colors - Good graphics palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
PURPLE = (138, 43, 226)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Maze settings
CELL_SIZE = 30
MAZE_WIDTH = 25
MAZE_HEIGHT = 20
WALL_THICKNESS = 3

# Player settings - Smooth character
PLAYER_SIZE = 20
PLAYER_SPEED = 4
PLAYER_COLOR = BLUE
PLAYER_TRAIL_COLOR = LIGHT_BLUE

# Game elements
GOAL_COLOR = GOLD
GOAL_SIZE = 18
COLLECTIBLE_COLOR = GREEN
COLLECTIBLE_SIZE = 12

# Animation settings for smooth movement
ANIMATION_SPEED = 0.3
TRAIL_LENGTH = 8
PARTICLE_COUNT = 5

# UI settings
FONT_SIZE_LARGE = 36
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 18

# Sound settings
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
