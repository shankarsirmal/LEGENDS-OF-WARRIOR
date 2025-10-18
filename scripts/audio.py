import pygame.mixer, os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        self.current_music = None

    def play_music(self, filename, loop=-1):
        music_path = os.path.join(self.sound_path, filename)
        if not os.path.exists(music_path):
            print(f"⚠️ Music not found: {music_path}")
            return
        if self.current_music != filename:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(loop)
                self.current_music = filename
            except Exception as e:
                print(f"Error playing music {music_path}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sfx(self, name):
        # supports .mp3 and .wav
        for ext in [".mp3", ".wav","m4a"]:
            sfx_path = os.path.join(self.sound_path, f"{name}{ext}")
            if os.path.exists(sfx_path):
                try:
                    sfx = pygame.mixer.Sound(sfx_path)
                    sfx.play()
                    return
                except Exception as e:
                    print(f"Error playing sfx {sfx_path}: {e}")
        # not found
        print(f"⚠️ SFX not found for: {name}")
