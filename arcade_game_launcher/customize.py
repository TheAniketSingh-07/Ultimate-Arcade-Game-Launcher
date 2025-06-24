#!/usr/bin/env python3
"""
Dino Run Customization Tool
Command-line tool for customizing the game
"""

import sys
import os
import argparse

# Add the project root to the path for imports
sys.path.append(os.path.dirname(__file__))

def customize_game(sprite=None, theme=None, style=None):
    """Apply customizations to the game"""
    
    print("🎨 DINO RUN CUSTOMIZATION TOOL")
    print("=" * 40)
    
    # Update settings file with customizations
    settings_path = os.path.join("games", "dino_run", "settings.py")
    
    if not os.path.exists(settings_path):
        print("❌ Game settings file not found!")
        return False
    
    customizations = []
    
    if theme:
        print(f"🎨 Setting theme to: {theme}")
        customizations.append(f"DEFAULT_THEME = '{theme}'")
        
    if sprite:
        print(f"🦕 Setting sprite type to: {sprite}")
        customizations.append(f"DEFAULT_SPRITE = '{sprite}'")
        
    if style:
        print(f"✨ Setting sprite style to: {style}")
        customizations.append(f"DEFAULT_STYLE = '{style}'")
    
    # Read current settings
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Add customization settings
    if customizations:
        custom_section = "\n# Customization Settings\n" + "\n".join(customizations) + "\n"
        
        # Remove existing customization section if present
        lines = content.split('\n')
        filtered_lines = []
        skip_section = False
        
        for line in lines:
            if line.strip() == "# Customization Settings":
                skip_section = True
                continue
            elif skip_section and (line.startswith("DEFAULT_") or line.strip() == ""):
                continue
            else:
                skip_section = False
                filtered_lines.append(line)
        
        content = '\n'.join(filtered_lines) + custom_section
        
        # Write updated settings
        with open(settings_path, 'w') as f:
            f.write(content)
            
        print("✅ Customizations applied successfully!")
        print("\n🚀 Run the game to see your changes:")
        print("   python3 games/dino_run/main.py")
        
        return True
    else:
        print("❌ No customizations specified!")
        return False

def show_options():
    """Show available customization options"""
    print("🎨 AVAILABLE CUSTOMIZATION OPTIONS")
    print("=" * 40)
    
    print("\n🎭 THEMES:")
    print("  • light  - Default bright theme")
    print("  • dark   - Dark mode theme")
    print("  • neon   - Cyberpunk neon theme")
    
    print("\n🦕 SPRITE TYPES:")
    print("  • dino   - Classic dinosaur")
    print("  • robot  - Futuristic robot")
    print("  • ninja  - Stealthy ninja")
    
    print("\n✨ SPRITE STYLES:")
    print("  • default    - Simple colored shapes")
    print("  • geometric  - Clean geometric design")
    print("  • pixel_art  - Retro pixel art style")
    print("  • neon       - Glowing neon effects")
    
    print("\n💡 EXAMPLE USAGE:")
    print("  python3 customize.py --theme dark --sprite dino --style geometric")

def main():
    """Main customization function"""
    parser = argparse.ArgumentParser(description="Customize Dino Run game")
    parser.add_argument("--sprite", choices=["dino", "robot", "ninja"], 
                       help="Choose sprite type")
    parser.add_argument("--theme", choices=["light", "dark", "neon"], 
                       help="Choose game theme")
    parser.add_argument("--style", choices=["default", "geometric", "pixel_art", "neon"], 
                       help="Choose sprite style")
    parser.add_argument("--show-options", action="store_true", 
                       help="Show all available options")
    
    args = parser.parse_args()
    
    if args.show_options:
        show_options()
        return
    
    if not any([args.sprite, args.theme, args.style]):
        print("🎨 No customizations specified!")
        print("Use --help to see available options or --show-options for details")
        return
    
    success = customize_game(
        sprite=args.sprite,
        theme=args.theme,
        style=args.style
    )
    
    if success:
        print("\n🎮 Your customized game is ready!")
        
        # Offer to run the game
        try:
            response = input("\n🚀 Would you like to run the game now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                print("🎮 Starting Dino Run...")
                os.system("python3 games/dino_run/main.py")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
