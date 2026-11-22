import pygame


class Ball:
    def __init__(self, x, y, radius=25, speed=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move(self, dx, dy, width, height):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.radius <= new_x <= width - self.radius and self.radius <= new_y <= height - self.radius:
            self.x = new_x
            self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), self.radius)
