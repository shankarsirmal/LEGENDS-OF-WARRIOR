import pygame

def load_animations(sheet_path, columns, rows, actions, frames_per_row):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // columns
    frame_height = sheet_height // rows

    animations = {}
    for r in range(rows):
        name = actions[r] if r < len(actions) else f"row{r}"
        frames = []
        for c in range(frames_per_row[r]):
            rect = pygame.Rect(c * frame_width, r * frame_height, frame_width, frame_height)
            frames.append(sheet.subsurface(rect).copy())
        animations[name] = frames
    return animations


class Animator:
    def __init__(self, animations, frame_time=100, scale=1.6):
        """Handle animations with optional scaling for clearer display."""
        self.animations = {
            name: [pygame.transform.scale(frame, (
                int(frame.get_width() * scale), int(frame.get_height() * scale)
            )) for frame in frames]
            for name, frames in animations.items()
        }
        self.frame_time = frame_time
        self.last_update = pygame.time.get_ticks()
        self.frame_index = 0
        self.current_anim = next(iter(self.animations))

    def set_animation(self, name):
        if name not in self.animations: return
        if name != self.current_anim:
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
