import pygame, os, random
from animation import load_animations, Animator
from config import SPRITE_LAYOUTS

class Monster(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"monster_lvl{level}.png")
        layout = SPRITE_LAYOUTS["monster"][level]

        animations = load_animations(sheet, layout["columns"], layout["rows"],
                                     layout["actions"], layout["frames_per_row"])

        self.animator = Animator(animations, 120, scale=1.6)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(820, 540))
        self.health = 120 + level * 25
        self.level = level
        self.speed = 1.5 + level * 0.5
        self.attack_cooldown = 0

    def update(self, player, audio):
        # move slightly toward player, but only in right half
        if player.rect.centerx < self.rect.centerx and self.rect.centerx > 500:
            self.rect.x -= self.speed
        elif player.rect.centerx > self.rect.centerx and self.rect.centerx < 950:
            self.rect.x += self.speed

        # attack occasionally
        dist = abs(player.rect.centerx - self.rect.centerx)
        now = pygame.time.get_ticks()
        if dist < 140 and now - self.attack_cooldown > 800:
            self.animator.set_animation("attack1" if "attack1" in self.animator.animations else "attack2")
            audio.play_sfx("monster_attack")
            player.health = max(0, player.health - 3)
            self.attack_cooldown = now
        else:
            self.animator.set_animation("act" if "act" in self.animator.animations else "idle")

        self.image = self.animator.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
