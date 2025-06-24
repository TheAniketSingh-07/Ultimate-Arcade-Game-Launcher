"""
Simple Chrome Dino Game Settings
"""

import os

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Game info
GAME_TITLE = "Chrome Dino - Simple Runner"

# Colors (RGB) - Simple Chrome style
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Sprite dimensions - Simple Chrome style
DINO_WIDTH = 40
DINO_HEIGHT = 40
CACTUS_WIDTH = 20
CACTUS_HEIGHT = 40

# Ground level
GROUND_Y = SCREEN_HEIGHT - 100

# Game physics - Intermediate and comfortable
GRAVITY = 0.9
JUMP_STRENGTH = -15
DUCK_HEIGHT_REDUCTION = 0.6

# Game mechanics - Intermediate level (slower and more manageable)
INITIAL_SPEED = 6
MAX_SPEED = 14
SPEED_INCREASE_RATE = 0.015
SCORE_MULTIPLIER = 10

# Controls
JUMP_KEYS = ['SPACE', 'UP']
DUCK_KEYS = ['DOWN']
PAUSE_KEY = 'p'

# Obstacle spawn settings - Intermediate spacing (more room to react)
MIN_OBSTACLE_DISTANCE = 300
MAX_OBSTACLE_DISTANCE = 500
OBSTACLE_SPAWN_CHANCE = 0.07

# Asset paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'dino_run')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# UI settings
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# Sound settings
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.8

# Customization Settings - Simple
DEFAULT_THEME = 'light'
DEFAULT_SPRITE = 'simple'
DEFAULT_STYLE = 'simple'
