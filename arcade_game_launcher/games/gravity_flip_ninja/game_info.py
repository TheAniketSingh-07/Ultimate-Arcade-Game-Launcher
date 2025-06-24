"""
Gravity Flip Ninja Game Information
An advanced ninja game with gravity flipping mechanics, particle effects, and smooth animations
"""

GAME_INFO = {
    "name": "Gravity Flip Ninja",
    "description": "Master the art of gravity manipulation as a ninja warrior! Flip gravity to navigate through deadly obstacles in this stylish action game with stunning particle effects and smooth animations.",
    "controls": {
        "SPACE": "Jump / Start Game / Menu",
        "G or UP Arrow": "Flip Gravity (with cooldown)",
        "LEFT/RIGHT Arrows or A/D": "Move ninja left/right",
        "ESC": "Pause/Resume game",
        "R": "Restart game (when game over)"
    },
    "features": [
        "🎨 Advanced particle effects and animations",
        "🌟 Smooth 60 FPS gameplay",
        "🎯 Progressive difficulty system",
        "💫 Screen shake and visual effects",
        "🏆 High score tracking",
        "🎮 Responsive controls with cooldown system",
        "🌈 Dynamic background and lighting",
        "⚡ Gravity flip mechanics with visual feedback"
    ],
    "objective": "Survive as long as possible by avoiding obstacles! Use your gravity flip ability strategically to navigate through spikes and platforms. The longer you survive, the higher your score!",
    "difficulty": "Medium to Hard",
    "category": "Action/Arcade",
    "main_file": "gravity_flip_ninja.py",
    "requirements": ["pygame"],
    "tips": [
        "Time your gravity flips carefully - there's a cooldown!",
        "Use momentum to your advantage when moving",
        "Watch for the purple glow when gravity is flipped",
        "The game gets faster as your score increases",
        "Practice makes perfect - learn the obstacle patterns!"
    ]
}

def get_game_info():
    """Return game information dictionary"""
    return GAME_INFO
