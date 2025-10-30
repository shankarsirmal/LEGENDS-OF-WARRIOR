import pygame.mixer, os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        self.current_music = None

    def play_music(self, filename, loop=-1):
        music_path = os.path.join(self.sound_path, filename)
        if os.path.exists(music_path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loop)
            self.current_music = filename

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sfx(self, name):
        for ext in [".mp3", ".wav", ".m4a"]:
            path = os.path.join(self.sound_path, f"{name}{ext}")
            if os.path.exists(path):
                pygame.mixer.Sound(path).play()
                return
