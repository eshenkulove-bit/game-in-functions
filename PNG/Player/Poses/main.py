import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Моя игра — Управление персонажем")

clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

        self.frames = [
            pygame.image.load("player_walk1.png").convert_alpha(),
            pygame.image.load("player_walk2.png").convert_alpha()
        ]
        
        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.frames[0]

    def update(self, keys):
        is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            is_moving = True

        if is_moving:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]
        else:
            self.image = self.frames[0]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

player = Player(WIDTH // 2, HEIGHT // 2)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill((40, 44, 52))
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()