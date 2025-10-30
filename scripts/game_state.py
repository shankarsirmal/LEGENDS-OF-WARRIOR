import pygame, time
from ui import draw_text, draw_health_bars, draw_leaderboard
from database import init_db, save_player, get_top_players

class GameState:
    def __init__(self, Player, Monster, AudioManager, screen, backgrounds, bg_home):
        init_db()
        self.Player, self.Monster = Player, Monster
        self.audio = AudioManager()
        self.screen = screen
        self.bg_levels = backgrounds
        self.bg_home = bg_home
        self.state = "name_entry"
        self.player_name = ""
        self.level = 1
        self.score = 0
        self.paused = False
        self.player = None
        self.monster = None

    def start_game(self):
        self.player = self.Player(self.level)
        self.monster = self.Monster(self.level)
        self.audio.play_music(f"bg_music{self.level}.wav")
        self.start_time = time.time()

    def handle_event(self, event):
        if self.state == "name_entry":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player_name:
                    self.state = "home"
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif getattr(event, "unicode", "").isprintable() and len(self.player_name) < 12:
                    self.player_name += event.unicode

        elif self.state == "home":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = "play"
                    self.start_game()
                elif event.key == pygame.K_q:
                    pygame.quit(); exit()

        elif self.state == "play":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    save_player(self.player_name, self.level, self.score)
                    self.state = "home"

        elif self.state in ["win", "over"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "home"

    def update(self, font_label, font_title, font_small):
        if self.state == "name_entry":
            self.screen.fill((0, 0, 0))
            draw_text(self.screen, "ENTER YOUR NAME", font_title, (255,255,255), 300, 200)
            pygame.draw.rect(self.screen, (255,255,255), (350, 300, 300, 50), 2)
            draw_text(self.screen, self.player_name, font_label, (255,255,0), 360, 310)
            return

        if self.state == "home":
            self.screen.blit(self.bg_home, (0, 0))
            draw_text(self.screen, "LEGEND OF WARRIOR", font_title, (255,255,0), 220, 100)
            draw_text(self.screen, f"Welcome {self.player_name}", font_label, (200,200,255), 380, 180)
            draw_leaderboard(self.screen, font_label, get_top_players())
            return

        if self.state == "play":
            if self.paused:
                overlay = pygame.Surface(self.screen.get_size())
                overlay.set_alpha(150)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))
                draw_text(self.screen, "⏸ PAUSED - Press P to resume", font_title, (255,255,255), 150, 250)
                return

            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.update(keys, self.audio)
            self.monster.update(self.player, self.audio)

            for p in self.player.projectiles[:]:
                p.move()
                if p.rect.colliderect(self.monster.rect):
                    self.monster.health -= 2
                    self.score += 10
                    self.player.projectiles.remove(p)
                elif p.x > 1200:
                    self.player.projectiles.remove(p)

            for m in self.monster.projectiles[:]:
                m.move()
                if m.rect.colliderect(self.player.rect):
                    self.player.health -= 3
                    self.monster.projectiles.remove(m)
                elif m.x < -100:
                    self.monster.projectiles.remove(m)

            self.screen.blit(self.bg_levels[self.level-1], (0,0))
            self.player.draw(self.screen)
            self.monster.draw(self.screen)
            for p in self.player.projectiles: p.draw(self.screen)
            for m in self.monster.projectiles: m.draw(self.screen)
            draw_health_bars(self.screen, font_label, self.player.health, self.monster.health)
            draw_text(self.screen, f"{self.player_name} | SCORE: {self.score}", font_label, (255,255,0), 40, 560)

            if self.player.health <= 0:
                save_player(self.player_name, self.level, self.score)
                self.state = "over"
            elif self.monster.health <= 0:
                self.level += 1
                if self.level > len(self.bg_levels):
                    save_player(self.player_name, self.level, self.score)
                    self.state = "win"
                else:
                    self.start_game()

        elif self.state == "win":
            self.screen.fill((0,0,0))
            draw_text(self.screen, f"🏆 YOU WON! {self.player_name}", font_title, (255,255,0), 200, 250)
            draw_text(self.screen, f"Score: {self.score}", font_label, (255,255,255), 440, 320)
            draw_text(self.screen, "Press ESC to return Home", font_label, (255,255,255), 340, 380)

        elif self.state == "over":
            self.screen.fill((0,0,0))
            draw_text(self.screen, f"💀 GAME OVER {self.player_name}", font_title, (255,0,0), 220, 250)
            draw_text(self.screen, f"Score: {self.score}", font_label, (255,255,255), 440, 320)
            draw_text(self.screen, "Press ESC to return Home", font_label, (255,255,255), 340, 380)
