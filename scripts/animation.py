import pygame

def load_animations(sheet_path, frame_width, frame_height, columns, rows, action_names=None):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    animations = {}
    if action_names and len(action_names) != rows:
        raise ValueError("action_names must match number of rows")
    for r in range(rows):
        name = action_names[r] if action_names else f"row{r}"
        frames = []
        for c in range(columns):
            rect = pygame.Rect(c * frame_width, r * frame_height, frame_width, frame_height)
            frames.append(sheet.subsurface(rect).copy())
        animations[name] = frames
    return animations

class Animator:
    def __init__(self, animations, frame_time=100):
        self.animations = animations
        self.frame_time = frame_time
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        self.current_anim = next(iter(animations))

    def set_animation(self, name):
        if name in self.animations and name != self.current_anim:
            self.current_anim = name
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        frames = self.animations[self.current_anim]
        if now - self.last_update >= self.frame_time:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(frames)
        return frames[self.frame_index]
