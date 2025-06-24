"""
Configuration file for Gravity Flip Ninja
Easily customize game settings, colors, and mechanics
"""

# Display Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60
FULLSCREEN = False

# Game Mechanics
NINJA_SPEED = 8
NINJA_JUMP_POWER = 15
GRAVITY_STRENGTH = 0.8
GRAVITY_FLIP_COOLDOWN = 30  # frames
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_RATE = 60  # frames between spawns
DIFFICULTY_INCREASE_RATE = 100  # score points per difficulty increase

# Visual Effects
PARTICLE_COUNT_EXPLOSION = 20
PARTICLE_COUNT_TRAIL = 3
SCREEN_SHAKE_INTENSITY = 5
SCREEN_SHAKE_DURATION = 30
FLASH_DURATION = 10

# Colors (RGB)
class GameColors:
    # Background
    SKY_TOP = (20, 30, 60)
    SKY_BOTTOM = (60, 90, 140)
    
    # Ninja
    NINJA_NORMAL = (64, 128, 255)
    NINJA_FLIPPED = (150, 50, 255)
    NINJA_EYES = (255, 255, 255)
    NINJA_PUPILS = (0, 0, 0)
    
    # UI
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (255, 255, 100)
    TEXT_SCORE = (100, 255, 100)
    TEXT_DANGER = (255, 100, 100)
    
    # Obstacles
    SPIKE_COLOR = (255, 50, 50)
    PLATFORM_COLOR = (50, 255, 50)
    
    # Effects
    PARTICLE_COLORS = [
        (255, 100, 100),  # Red
        (100, 255, 100),  # Green
        (100, 100, 255),  # Blue
        (255, 255, 100),  # Yellow
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Cyan
    ]
    
    # Special Effects
    GLOW_COLOR = (255, 255, 255, 100)
    SHADOW_COLOR = (0, 0, 0, 128)
    FLASH_COLOR = (255, 255, 255, 100)

# Audio Settings (for future implementation)
class AudioSettings:
    MASTER_VOLUME = 0.7
    SFX_VOLUME = 0.8
    MUSIC_VOLUME = 0.6
    
    # Sound file paths (when implemented)
    SOUNDS = {
        'jump': 'assets/sounds/jump.wav',
        'gravity_flip': 'assets/sounds/gravity_flip.wav',
        'collision': 'assets/sounds/collision.wav',
        'score': 'assets/sounds/score.wav',
        'menu_select': 'assets/sounds/menu_select.wav',
    }
    
    MUSIC = {
        'menu': 'assets/sounds/menu_music.ogg',
        'game': 'assets/sounds/game_music.ogg',
    }

# Input Settings
class InputSettings:
    # Key mappings
    JUMP_KEYS = ['space']
    GRAVITY_FLIP_KEYS = ['g', 'up']
    MOVE_LEFT_KEYS = ['left', 'a']
    MOVE_RIGHT_KEYS = ['right', 'd']
    PAUSE_KEYS = ['escape', 'p']
    
    # Input sensitivity
    MOVEMENT_ACCELERATION = 1.0
    MOVEMENT_FRICTION = 0.95

# Performance Settings
class PerformanceSettings:
    # Particle limits
    MAX_PARTICLES = 200
    PARTICLE_CLEANUP_THRESHOLD = 250
    
    # Effect quality
    HIGH_QUALITY_EFFECTS = True
    ENABLE_SCREEN_SHAKE = True
    ENABLE_PARTICLES = True
    ENABLE_GLOW_EFFECTS = True
    
    # Optimization
    VSYNC = True
    HARDWARE_ACCELERATION = True

# Debug Settings
class DebugSettings:
    SHOW_FPS = False
    SHOW_COLLISION_BOXES = False
    SHOW_PARTICLE_COUNT = False
    ENABLE_DEBUG_KEYS = False
    LOG_PERFORMANCE = False

# Game Balance
class GameBalance:
    # Scoring
    POINTS_PER_FRAME = 1
    POINTS_PER_OBSTACLE = 10
    BONUS_MULTIPLIER = 1.5
    
    # Difficulty scaling
    MAX_OBSTACLE_SPEED = 12
    MIN_SPAWN_RATE = 20
    SPEED_INCREASE_RATE = 0.1
    
    # Power-ups (for future implementation)
    POWERUP_SPAWN_CHANCE = 0.05
    POWERUP_DURATION = 300  # frames

# File Paths
class FilePaths:
    HIGH_SCORE_FILE = "high_score.txt"
    CONFIG_FILE = "user_config.json"
    ASSETS_DIR = "assets"
    IMAGES_DIR = "assets/images"
    SOUNDS_DIR = "assets/sounds"
    FONTS_DIR = "assets/fonts"

def load_user_config():
    """Load user configuration from file (if exists)"""
    import json
    import os
    
    try:
        if os.path.exists(FilePaths.CONFIG_FILE):
            with open(FilePaths.CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                
                # Apply user settings (example)
                if 'master_volume' in user_config:
                    AudioSettings.MASTER_VOLUME = user_config['master_volume']
                if 'high_quality_effects' in user_config:
                    PerformanceSettings.HIGH_QUALITY_EFFECTS = user_config['high_quality_effects']
                
                return user_config
    except Exception as e:
        print(f"Could not load user config: {e}")
    
    return {}

def save_user_config(config_dict):
    """Save user configuration to file"""
    import json
    
    try:
        with open(FilePaths.CONFIG_FILE, 'w') as f:
            json.dump(config_dict, f, indent=2)
    except Exception as e:
        print(f"Could not save user config: {e}")

# Initialize user config on import
user_config = load_user_config()
