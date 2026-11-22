import pygame
from ball import Ball


pygame.init()
width, height = 700, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()
ball = Ball(width // 2, height // 2)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                ball.move(0, -ball.speed, width, height)
            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.speed, width, height)
            elif event.key == pygame.K_LEFT:
                ball.move(-ball.speed, 0, width, height)
            elif event.key == pygame.K_RIGHT:
                ball.move(ball.speed, 0, width, height)
    screen.fill((255, 255, 255))
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
