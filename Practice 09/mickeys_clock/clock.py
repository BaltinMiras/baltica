import math
import pygame


class MickeyClock:
    def __init__(self, image_path, size=(700, 700)):
        self.size = size
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.smoothscale(self.background, size)
        self.center = (size[0] // 2, size[1] // 2)

    def draw_hand(self, surface, angle, length, color, width):
        radians = math.radians(angle - 90)
        end = (
            self.center[0] + math.cos(radians) * length,
            self.center[1] + math.sin(radians) * length,
        )
        pygame.draw.line(surface, color, self.center, end, width)
        pygame.draw.circle(surface, color, (int(end[0]), int(end[1])), width + 7)
        pygame.draw.circle(surface, (255, 255, 255), (int(end[0]), int(end[1])), width + 2)

    def draw(self, surface, current_time):
        surface.blit(self.background, (0, 0))
        minute_angle = current_time.minute * 6
        second_angle = current_time.second * 6
        self.draw_hand(surface, minute_angle, 190, (25, 25, 25), 9)
        self.draw_hand(surface, second_angle, 235, (210, 35, 45), 5)
        pygame.draw.circle(surface, (25, 25, 25), self.center, 15)
        pygame.draw.circle(surface, (235, 190, 70), self.center, 7)
