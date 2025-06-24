# 🎮 Arcade Game Launcher

A collection of classic arcade games built with Python and Pygame, featuring a unified launcher interface.

## ✅ **CURRENT STATUS: FULLY FUNCTIONAL!**

The **Dino Run** game is complete and ready to play! All core systems are implemented and tested.

## 🎯 Games Included

### 🦕 Dino Run - Endless Runner ✅ **READY TO PLAY**
- **Genre**: Endless Runner / Casual Arcade
- **Objective**: Survive by jumping over and ducking under obstacles
- **Features**: 
  - ✅ Parallax scrolling backgrounds
  - ✅ Animated dino sprite with smooth movements
  - ✅ Progressive difficulty with speed increases
  - ✅ Power-ups system (shield, slow-mo, double jump)
  - ✅ Score tracking and distance measurement
  - ✅ Complete UI system (menu, HUD, game over)
  - ✅ Audio system with sound effects
  - ✅ Collision detection and physics

### 🚀 Fighter Shoot (Coming Soon)
- **Genre**: Space Shooter
- **Objective**: Defend against waves of enemies

### ⭕ Tic Tac Toe (Coming Soon)
- **Genre**: Strategy/Puzzle
- **Objective**: Classic 3x3 grid game

### 🌟 Maze Game (Coming Soon)
- **Genre**: Puzzle/Adventure
- **Objective**: Navigate through procedurally generated mazes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Linux/Ubuntu system (tested on Ubuntu 24.04)

### Installation & Running

1. **Navigate to the project directory**
   ```bash
   cd arcade_game_launcher
   ```

2. **Install dependencies (Ubuntu/Debian)**
   ```bash
   sudo apt update
   sudo apt install python3-pygame python3-numpy
   ```

3. **Choose how to run:**

   **Option A: Use the quick launcher**
   ```bash
   python3 run.py
   ```

   **Option B: Run the main launcher**
   ```bash
   python3 launcher.py
   ```

   **Option C: Run Dino Run directly**
   ```bash
   python3 games/dino_run/main.py
   ```

   **Option D: Run tests first**
   ```bash
   python3 test_game.py
   ```

## 🎮 Controls

### Dino Run
- **SPACE** or **UP ARROW**: Jump
- **DOWN ARROW**: Duck/Slide
- **P**: Pause game
- **ESC**: Return to menu

### Launcher Navigation
- **UP/DOWN ARROWS**: Navigate menus
- **SPACE**: Select/Confirm
- **ESC**: Back/Exit

## 📁 Project Structure

```
arcade_game_launcher/
│
├── launcher.py              # Main launcher application
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── launcher_icon.png       # Launcher icon
│
├── utils/                  # Shared utilities
│   ├── buttons.py         # UI button components
│   ├── config.py          # Global configuration
│   └── screens.py         # Screen management
│
├── games/                  # Individual games
│   └── dino_run/          # Dino Run game
│       ├── main.py        # Game entry point
│       ├── game_logic.py  # Core game mechanics
│       ├── ui.py          # User interface
│       ├── animations.py  # Sprite animations
│       ├── audio.py       # Sound management
│       ├── powerups.py    # Power-up system
│       ├── settings.py    # Game configuration
│       └── utils.py       # Helper functions
│
└── assets/                # Game assets
    └── dino_run/          # Dino Run assets
        ├── images/        # Sprites and backgrounds
        ├── sounds/        # Sound effects
        ├── music/         # Background music
        └── fonts/         # Custom fonts
```

## 🎨 Features

### Current Features (Dino Run)
- ✅ Smooth character animations
- ✅ Progressive difficulty scaling
- ✅ Collision detection with margin
- ✅ Parallax background scrolling
- ✅ Sound effects and music
- ✅ Power-up system
- ✅ Score and distance tracking
- ✅ Pause/resume functionality
- ✅ Game state management

### Planned Features
- 🔄 Additional games (Fighter Shoot, Tic Tac Toe, Maze Game)
- 🔄 High score persistence
- 🔄 Achievement system
- 🔄 Customizable controls
- 🔄 Theme selection
- 🔄 Multiplayer support

## 🛠️ Development

### Adding New Games

1. Create a new folder in `games/`
2. Follow the structure of `dino_run/`
3. Implement required files:
   - `main.py` - Entry point
   - `game_logic.py` - Core mechanics
   - `ui.py` - User interface
   - `settings.py` - Configuration

### Asset Guidelines

- **Images**: PNG format, transparent backgrounds preferred
- **Sounds**: WAV format for effects, MP3 for music
- **Fonts**: TTF format
- **Resolution**: Design for 1200x600 base resolution

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Document functions and classes
- Keep functions focused and modular

## 🎵 Audio

The game supports:
- Background music (looping)
- Sound effects (jump, collision, score)
- Volume controls
- Mute functionality

### Audio File Requirements
- **Music**: MP3 format, 44.1kHz sample rate
- **Sound Effects**: WAV format, 22kHz sample rate
- **File Size**: Keep under 1MB per file for performance

## 🐛 Troubleshooting

### Common Issues

**Game won't start**
- Ensure Python 3.8+ is installed
- Install required dependencies: `pip install -r requirements.txt`
- Check that pygame is properly installed

**No sound**
- Verify audio files exist in assets folders
- Check system audio settings
- Try running with `--no-audio` flag (if implemented)

**Performance issues**
- Lower the FPS in settings.py
- Reduce sprite sizes
- Disable particle effects

**Import errors**
- Ensure you're running from the correct directory
- Check Python path configuration
- Verify all required files exist

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution
- New games
- Bug fixes
- Performance improvements
- Asset creation (sprites, sounds, music)
- Documentation improvements

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the code documentation
3. Create an issue with detailed information

## 🎮 Game Development Tips

### For Dino Run Modifications
- Adjust `GRAVITY` and `JUMP_STRENGTH` in settings.py for different physics
- Modify `SPEED_INCREASE_RATE` to change difficulty progression
- Add new obstacle types in game_logic.py
- Create custom sprites and replace placeholder graphics

### Performance Optimization
- Use sprite groups for batch operations
- Implement object pooling for frequently created/destroyed objects
- Optimize collision detection with spatial partitioning
- Use pygame.SRCALPHA sparingly

---

**Happy Gaming! 🎮**
