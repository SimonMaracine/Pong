from random import randint, choice

import pygame
from vectormath import Vector2 as Vector

WIDTH = 800
HEIGHT = 600
title = "Pong"
running = True
player1_score = 0
player2_score = 0
fullscreen = False


class Pong(object):
    def __init__(self, x=1):
        self.x = x
        self.vel = 6
        self.acc = 0.05
        self.pos = Vector(WIDTH // 2, HEIGHT // 2)
        self.dir = Vector(self.vel * self.x, randint(-2, 2))
        self.rad = 14
        self.color = (255, 255, 255)

    def render(self):
        pygame.draw.circle(window, self.color, (int(self.pos.x), int(self.pos.y)), self.rad)

    def update(self):
        self.pos += self.dir
        if self.pos.y - self.rad <= 0 or self.pos.y + self.rad >= HEIGHT:
            self.dir.y *= -1

    def collide(self, paddle) -> bool:
        if paddle.x + paddle.width - self.vel < self.pos.x - self.rad < paddle.x + paddle.width or \
                paddle.x + self.vel > self.pos.x + self.rad > paddle.x:
            if self.pos.y + self.rad > paddle.y and self.pos.y - self.rad < paddle.y + paddle.height:
                return True
        return False

    def bounce(self):
        self.dir.x *= -1

    def score(self) -> str:
        if self.pos.x <= 0:
            return "player1"
        elif self.pos.x >= WIDTH:
            return "player2"
        else:
            return "who?"


class Paddle(object):
    def __init__(self, x, color):
        self.x = x
        self.width = 17
        self.height = 95
        self.y = HEIGHT // 2 - self.height // 2
        self.vel = 5
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


def toggle_fullscreen():
    global window, fullscreen
    last_frame = window.copy()
    if not fullscreen:
        window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen = True
    else:
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        fullscreen = False
    window.blit(last_frame, (0, 0))
    pause_game()


def pause_game():
    global running
    pause_text = pause_font.render("PAUSED", True, (240, 240, 240))
    pause_width = pause_text.get_width()
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    running = False
                elif event.key == pygame.K_p:
                    pause = False
                elif event.key == pygame.K_f:
                    toggle_fullscreen()

        window.blit(pause_text, (WIDTH // 2 - pause_width // 2, HEIGHT // 2 - 50))
        pygame.display.flip()
        clock.tick(60)


def show_scores():
    score1_text = score_font.render("Score: " + str(player1_score), True, (255, 140, 140))
    score2_text = score_font.render("Score: " + str(player2_score), True, (140, 140, 255))
    score2_width = score2_text.get_width()
    window.blit(score1_text, (30, 16))
    window.blit(score2_text, (WIDTH - score2_width - 30, 16))


def show_fps():
    fps_text = fps_font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
    window.blit(fps_text, (6, HEIGHT - 18))


def init():
    global window, clock, fps_font, score_font, pause_font
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load("pong.png"))
    clock = pygame.time.Clock()
    fps_font = pygame.font.SysFont("calibri", 16, True)
    score_font = pygame.font.SysFont("calibri", 40, True)
    pause_font = pygame.font.SysFont("calibri", 50, True)


def loop():
    global running
    pong = None
    paddle1 = None
    paddle2 = None

    def start():
        nonlocal pong, paddle1, paddle2
        pong = Pong(choice((-1, 1)))
        paddle1 = Paddle(10, (230, 0, 0))
        paddle2 = Paddle(WIDTH - 28, (0, 0, 230))
        pygame.time.wait(400)

    def update():
        global player1_score, player2_score
        pong.update()
        paddle1.update()
        paddle2.update()
        if pong.collide(paddle1) or pong.collide(paddle2):
            pong.bounce()
        if pong.score() == "player1":
            player2_score += 1
            start()
        elif pong.score() == "player2":
            player1_score += 1
            start()

    def render():
        pong.render()
        paddle1.render()
        paddle2.render()
        pygame.draw.line(window, (200, 200, 200), (0, 0), (WIDTH, 0), 2)
        pygame.draw.line(window, (200, 200, 200), (0, HEIGHT - 2), (WIDTH, HEIGHT - 2), 2)
        show_scores()
        show_fps()

    start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_f:
                    toggle_fullscreen()

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            paddle1.move("up")
        elif key[pygame.K_s]:
            paddle1.move("down")
        if key[pygame.K_UP]:
            paddle2.move("up")
        elif key[pygame.K_DOWN]:
            paddle2.move("down")

        window.fill((2, 2, 2))
        update()
        render()
        pygame.display.flip()
        clock.tick(60)


def main():
    init()
    loop()
    pygame.quit()


if __name__ == "__main__":
    main()
