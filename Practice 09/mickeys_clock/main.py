from datetime import datetime
from pathlib import Path
import pygame
from clock import MickeyClock


pygame.init()
size = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()
image_path = Path(__file__).parent / "images" / "mickeyclock.jpeg"
app = MickeyClock(str(image_path), size)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    app.draw(screen, datetime.now())
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
