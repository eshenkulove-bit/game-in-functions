import os
import sys
import random
import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Моя игра — Охота на монстров")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BORDER = 30
FIELD = pygame.Rect(BORDER, BORDER, WIDTH - 2 * BORDER, HEIGHT - 2 * BORDER)


def load_image(name):
    return pygame.image.load(os.path.join(BASE_DIR, name)).convert_alpha()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

        self.frames = [load_image("player_walk1.png"), load_image("player_walk2.png")]
        self.attack_image = load_image("player_attack.png")
        self.image = self.frames[0]

        self.current_frame = 0
        self.animation_speed = 0.15
        self.facing_left = False

        self.attacking = False
        self.attack_timer = 0
        self.score = 0

    def start_attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = 15

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def get_attack_rect(self):
        return self.get_rect().inflate(30, 30)

    def update(self, keys):
        is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.facing_left = True
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.facing_left = False
            is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            is_moving = True

        if self.attacking:
            self.image = self.attack_image
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        elif is_moving:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]
        else:
            self.image = self.frames[0]

        if self.x < FIELD.left:
            self.x = FIELD.left
        if self.x > FIELD.right - self.image.get_width():
            self.x = FIELD.right - self.image.get_width()
        if self.y < FIELD.top:
            self.y = FIELD.top
        if self.y > FIELD.bottom - self.image.get_height():
            self.y = FIELD.bottom - self.image.get_height()

    def draw(self, surface):
        img = self.image
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, (self.x, self.y))


class Monster:
    image = None

    def __init__(self):
        if Monster.image is None:
            big = load_image("monster.png")
            Monster.image = pygame.transform.scale(big, (48, 66))

        w, h = Monster.image.get_size()
        self.x = random.randint(FIELD.left, FIELD.right - w)
        self.y = random.randint(FIELD.top, FIELD.bottom - h)
        self.dx = random.choice([-3, -2, -1, 1, 2, 3])
        self.dy = random.choice([-3, -2, -1, 1, 2, 3])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, Monster.image.get_width(), Monster.image.get_height())

    def update(self):
        if random.randint(1, 60) == 1:
            self.dx = random.choice([-3, -2, -1, 1, 2, 3])
            self.dy = random.choice([-3, -2, -1, 1, 2, 3])

        self.x += self.dx
        self.y += self.dy

        w, h = Monster.image.get_size()
        if self.x < FIELD.left or self.x > FIELD.right - w:
            self.dx = -self.dx
            self.x = max(FIELD.left, min(self.x, FIELD.right - w))
        if self.y < FIELD.top or self.y > FIELD.bottom - h:
            self.dy = -self.dy
            self.y = max(FIELD.top, min(self.y, FIELD.bottom - h))

    def draw(self, surface):
        surface.blit(Monster.image, (self.x, self.y))


player = Player(WIDTH // 2, HEIGHT // 2)

monsters = []
for i in range(8):
    monsters.append(Monster())

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.start_attack()

    player.update(pygame.key.get_pressed())

    for monster in monsters:
        monster.update()

    if player.attacking:
        zone = player.get_attack_rect()
        for monster in monsters[:]:
            if zone.colliderect(monster.get_rect()):
                monsters.remove(monster)
                player.score += 1
                monsters.append(Monster())

    screen.fill((40, 44, 52))
    pygame.draw.rect(screen, (255, 255, 255), FIELD, 3)

    for monster in monsters:
        monster.draw(screen)
    player.draw(screen)

    text = font.render(f"Побеждено монстров: {player.score}   (Пробел — удар)", True, (255, 255, 255))
    screen.blit(text, (BORDER, 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
