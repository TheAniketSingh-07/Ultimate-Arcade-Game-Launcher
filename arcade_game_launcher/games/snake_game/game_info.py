"""
Snake Game Information
A classic arcade game where you control a snake to eat food and grow longer.
"""

GAME_INFO = {
    "name": "Snake Game",
    "description": "Control a snake to eat food and grow longer while avoiding walls and your own tail",
    "controls": {
        "Arrow Keys": "Move the snake",
        "P": "Pause/Resume game",
        "SPACE": "Restart game (when game over)",
        "ESC": "Quit game",
        "Q": "Quit game (when game over)"
    },
    "objective": "Eat red food blocks to grow your snake and increase your score. Avoid hitting walls or your own tail!",
    "difficulty": "Easy to Medium",
    "category": "Classic Arcade",
    "main_file": "snake_game.py",
    "requirements": ["pygame"]
}

def get_game_info():
    """Return game information dictionary"""
    return GAME_INFO
