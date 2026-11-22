from pathlib import Path
import pygame
from player import MusicPlayer


pygame.init()
width, height = 700, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 34)
small_font = pygame.font.Font(None, 26)
clock = pygame.time.Clock()
music_dir = Path(__file__).parent / "music"
player = MusicPlayer(music_dir)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()

    screen.fill((24, 28, 40))
    title = font.render("Music Player", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(width // 2, 65)))
    if player.current_track:
        track_text = player.current_track.name
        status_text = "Playing" if player.playing else "Stopped"
        position_text = f"Position: {player.position_seconds()} sec"
    else:
        track_text = "No tracks found. Add MP3, WAV, or OGG files to music/."
        status_text = "Waiting for music"
        position_text = "Position: 0 sec"
    lines = [track_text, status_text, position_text, "P: Play   S: Stop   N: Next   B: Previous   Q: Quit"]
    for index, line in enumerate(lines):
        rendered = small_font.render(line, True, (220, 225, 235))
        screen.blit(rendered, rendered.get_rect(center=(width // 2, 145 + index * 48)))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
