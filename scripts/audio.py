import pygame.mixer
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        self.current_music = None

    def play_music(self, filename, loop=-1):
        """Play a background track by name (supports .wav, .mp3, .ogg automatically)."""
        # Find file regardless of extension
        found_path = None
        for ext in [".mp3", ".wav", ".ogg", ".m4a"]:
            path = os.path.join(self.sound_path, filename.replace(".mp3", "").replace(".wav", "") + ext)
            if os.path.exists(path):
                found_path = path
                break

        if not found_path:
            print(f"Music file not found for: {filename}")
            return

        try:
            if self.current_music != found_path:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(found_path)
                pygame.mixer.music.play(loop)
                self.current_music = found_path
                print(f" Playing music: {os.path.basename(found_path)}")
        except Exception as e:
            print(f"Error playing music {found_path}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sfx(self, name):
        """Play sound effects by name (supports multiple formats)."""
        for ext in [".wav", ".mp3", ".ogg", ".m4a"]:
            sfx_path = os.path.join(self.sound_path, f"{name}{ext}")
            if os.path.exists(sfx_path):
                try:
                    sfx = pygame.mixer.Sound(sfx_path)
                    sfx.play()
                    return
                except Exception as e:
                    print(f" Error playing sfx {sfx_path}: {e}")
        print(f" SFX not found for: {name}")
