import pygame
from vectormath import Vector2 as Vector

WIDTH = 800
HEIGHT = 600
title = "Pong"
running = True


class Pong(object):
    def __init__(self, x=1):
        self.x = x
        self.vel = 7
        self.acc = 0.05
        self.pos = Vector(WIDTH // 2, HEIGHT // 2)
        self.dir = Vector(self.vel * self.x, 0)
        self.rad = 15
        self.color = (255, 255, 255)

    def render(self):
        pygame.draw.circle(window, self.color, (int(self.pos.x), int(self.pos.y)), self.rad)

    def update(self):
        self.pos += self.dir


class Paddle(object):
    def __init__(self, x, color):
        self.x = x
        self.y = HEIGHT // 2
        self.width = 18
        self.height = 100
        self.vel = 6
        self.color = color

    def render(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        if self.y <= 0:
            self.y = 0
        elif self.y + self.height >= HEIGHT:
            self.y = HEIGHT - self.height

    def move(self, dir):
        if dir == "up":
            self.y -= self.vel
        elif dir == "down":
            self.y += self.vel

    def collide(self, ball) -> bool:
        pass


def init():
    global window, clock
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()


def loop():
    global running
    pong = Pong(-1)
    paddle1 = Paddle(10, (230, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            paddle1.move("up")
        elif key[pygame.K_s]:
            paddle1.move("down")

        window.fill((0, 0, 0))
        pong.update()
        pong.render()
        paddle1.update()
        paddle1.render()
        pygame.display.flip()
        clock.tick(60)


def main():
    init()
    loop()
    pygame.quit()


if __name__ == "__main__":
    main()
