import pygame

def draw_text(screen, text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

def draw_health_bars(screen, font, player_health, monster_health):
    draw_text(screen, "PLAYER HEALTH", font, (255,255,255), 50, 20)
    draw_text(screen, "MONSTER HEALTH", font, (255,255,255), 750, 20)

    # Player health
    pygame.draw.rect(screen, (255,255,255), (48,58,204,24))
    player_bar_width = max(0, min(200, player_health * 2))
    pygame.draw.rect(screen, (0,255,0), (50,60,player_bar_width,20))

    # Monster health (fixed width, capped)
    pygame.draw.rect(screen, (255,255,255), (748,58,204,24))
    monster_bar_width = max(0, min(200, monster_health * 2))
    pygame.draw.rect(screen, (255,0,0), (750,60,monster_bar_width,20))

def draw_leaderboard(screen, font, players):
    draw_text(screen, "TOP PLAYERS ", font, (255,255,0), 400, 420)
    y = 460
    for name, score in players:
        draw_text(screen, f"{name:<12} - {score:>4}", font, (255,255,255), 420, y)
        y += 30
