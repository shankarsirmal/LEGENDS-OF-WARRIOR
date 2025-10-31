import pygame, os, random, math
from animation import load_animations, Animator
from projectiles import Projectile
from config import SPRITE_LAYOUTS

class Monster(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"monster_lvl{level}.png")

        columns, rows = SPRITE_LAYOUTS["monster"][level]
        sheet_img = pygame.image.load(sheet).convert_alpha()
        frame_w = sheet_img.get_width() // columns
        frame_h = sheet_img.get_height() // rows

        base_actions = ["idle", "attack", "walk", "death", "roar"]
        if len(base_actions) < rows:
            base_actions += [f"row{i}" for i in range(len(base_actions), rows)]
        action_names = base_actions[:rows]

        animations = load_animations(sheet, frame_w, frame_h, columns, rows, action_names)
        self.animator = Animator(animations, 100)

        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(800, 520))
        self.health = 200
        self.level = level
        self.projectiles = []
        self.speed = 2 + level
        self.attack_cooldown = 800
        self.last_attack_time = 0

        # Screen bounds
        self.min_x = 500
        self.max_x = 950

        # Invisibility and respawn management
        self.visible = True
        self.invisible_duration = 2000   # milliseconds monster stays invisible
        self.last_invisible_time = 0

    def chase_player(self, player):
        """Monster moves toward the player."""
        if player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed
        elif player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed

        # Clamp within screen so monster is always visible
        self.rect.x = max(self.min_x, min(self.rect.x, self.max_x))

    def melee_attack(self, player, audio):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.animator.set_animation("attack")
            audio.play_sfx(f"monster{min(self.level, 3)}")
            player.health = max(0, player.health - random.randint(6, 12))
            self.last_attack_time = now

    def ranged_attack(self, player, audio):
        self.animator.set_animation("attack")
        audio.play_sfx(f"monster{min(self.level, 3)}")
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        self.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, dx/dist*8, dy/dist*8, True))

    def disappear_and_respawn(self, player):
        """Handles monster disappearing and reappearing near player."""
        now = pygame.time.get_ticks()

        # Randomly trigger disappearance
        if self.visible and random.randint(1, 600) == 1:  # 1 in 600 chance each frame
            self.visible = False
            self.last_invisible_time = now

        # If invisible, check if it's time to respawn
        if not self.visible and now - self.last_invisible_time >= self.invisible_duration:
            # Respawn near player (random offset)
            offset_x = random.randint(-150, 150)
            offset_y = random.randint(-50, 50)
            self.rect.centerx = player.rect.centerx + offset_x
            self.rect.centery = player.rect.centery + offset_y

            # Clamp within game area
            self.rect.x = max(self.min_x, min(self.rect.x, self.max_x))
            self.rect.y = max(300, min(self.rect.y, 520))  # arbitrary Y bounds

            self.visible = True

    def update(self, player, audio):
        self.disappear_and_respawn(player)

        if not self.visible:
            return  # Skip logic while invisible

        dist = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)

        if dist > 120:
            self.animator.set_animation("walk")
            self.chase_player(player)
            if random.randint(1, 120) == 1:
                self.ranged_attack(player, audio)
        else:
            self.melee_attack(player, audio)

        self.image = self.animator.update()

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
