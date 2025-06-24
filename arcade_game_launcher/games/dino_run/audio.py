"""
Dino Run Audio Manager
Handles music and sound effects
"""

import pygame
import os
from games.dino_run.settings import *

class AudioManager:
    """Manages all audio for the game"""
    
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Sound storage
        self.sounds = {}
        self.music_loaded = False
        
        # Volume settings
        self.master_volume = MASTER_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        
        # Load audio files
        self.load_sounds()
        self.load_music()
        
    def load_sounds(self):
        """Load all sound effects"""
        sound_files = {
            'jump': 'jump.wav',
            'hit': 'hit.wav',
            'score': 'score_ping.wav',
            'button': 'button_click.wav'
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join(SOUNDS_DIR, filename)
            try:
                if os.path.exists(sound_path) and os.path.getsize(sound_path) > 100:  # Check file has content
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.sfx_volume * self.master_volume)
                    self.sounds[sound_name] = sound
                else:
                    # Create a placeholder sound (short beep)
                    self.sounds[sound_name] = self.create_placeholder_sound()
            except pygame.error as e:
                print(f"Could not load sound {filename}: {e}")
                self.sounds[sound_name] = self.create_placeholder_sound()
                
    def load_music(self):
        """Load background music"""
        music_path = os.path.join(MUSIC_DIR, 'background_theme.mp3')
        try:
            if os.path.exists(music_path) and os.path.getsize(music_path) > 100:  # Check file has content
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                self.music_loaded = True
            else:
                print(f"Music file not found or empty: {music_path}")
                self.music_loaded = False
        except pygame.error as e:
            print(f"Could not load music: {e}")
            self.music_loaded = False
            
    def create_placeholder_sound(self):
        """Create a simple placeholder sound"""
        # Create a short sine wave sound using pygame
        duration = 0.1  # seconds
        sample_rate = 22050
        frequency = 440  # A note
        
        frames = int(duration * sample_rate)
        
        # Create simple beep sound without numpy
        sound_array = []
        for i in range(frames):
            # Simple sine wave
            import math
            wave = math.sin(2 * math.pi * frequency * i / sample_rate)
            # Convert to 16-bit integer
            sample = int(wave * 16383)  # Half of max 16-bit value for safety
            sound_array.extend([sample, sample])  # Stereo
        
        # Convert to bytes
        sound_bytes = b''.join(sample.to_bytes(2, byteorder='little', signed=True) for sample in sound_array)
        
        try:
            sound = pygame.mixer.Sound(buffer=sound_bytes)
            sound.set_volume(self.sfx_volume * self.master_volume)
            return sound
        except:
            # If that fails, create a minimal silent sound
            silent_sound = pygame.mixer.Sound(buffer=b'\x00' * 1000)
            return silent_sound
        
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"Could not play sound {sound_name}: {e}")
        else:
            print(f"Sound {sound_name} not found")
            
    def play_music(self, loops=-1):
        """Play background music"""
        if self.music_loaded:
            try:
                pygame.mixer.music.play(loops)
            except pygame.error as e:
                print(f"Could not play music: {e}")
        else:
            print("No music loaded")
            
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        
    def pause_music(self):
        """Pause background music"""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Unpause background music"""
        pygame.mixer.music.unpause()
        
    def set_master_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self.update_volumes()
        
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
            
    def update_volumes(self):
        """Update all volumes based on master volume"""
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
            
    def toggle_mute(self):
        """Toggle mute on/off"""
        if self.master_volume > 0:
            self.previous_volume = self.master_volume
            self.set_master_volume(0)
        else:
            self.set_master_volume(getattr(self, 'previous_volume', MASTER_VOLUME))
