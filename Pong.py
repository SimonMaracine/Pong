import os
from random import randint, choice

import pygame
from vectormath import Vector2 as Vector

WIDTH = 800
HEIGHT = 600
title = "Pong"
version = "v0.1"
running = True
fullscreen = False


class Pong(object):
    def __init__(self, x):
        self.x = x
        self.speed = 11
        self.pos = Vector(WIDTH // 2, HEIGHT // 2)
        self.init_vel = Vector(self.speed * self.x, randint(-2, 2))
        self.vel = self.init_vel
        self.rad = 12
        self.color = [255, 255, 255]

    def render(self):
        pygame.draw.circle(window, self.color, (int(self.pos.x), int(self.pos.y)), self.rad)

    def update(self):
        self.pos += self.vel
        if self.pos.y - self.rad <= 3 or self.pos.y + self.rad >= HEIGHT - 3:
            hit_high.play()
            self.vel.y *= -1

    def collide(self, paddle) -> bool:
        if paddle.x < self.pos.x - self.rad < paddle.x + paddle.width or \
                paddle.x + paddle.width > self.pos.x + self.rad > paddle.x:
            if self.pos.y + self.rad > paddle.y and self.pos.y - self.rad < paddle.y + paddle.height:
                hit_low.play()
                return True
        return False

    def bounce(self, paddle):
        if paddle.name == "left":
            self.pos.x += 10
        elif paddle.name == "right":
            self.pos.x -= 10

        # Bounce on the x axis.
        self.vel.x *= -1

        # Bounce on the y axis.
        segment = paddle.height / 8
        if self.pos.y - self.rad <= paddle.y + segment:  # segment -3
            self.vel.y = -6
            self.vel.x = self.speed * 1.21 if self.vel.x >= 0 else -self.speed * 1.21
            # print(-3)
        elif self.pos.y <= paddle.y + segment * 2:  # segment -2
            self.vel.y = -5
            self.vel.x = self.speed * 1.14 if self.vel.x >= 0 else -self.speed * 1.14
            # print(-2)
        elif self.pos.y <= paddle.y + segment * 3:  # segment -1
            self.vel.y = -3
            self.vel.x = self.speed * 1.08 if self.vel.x >= 0 else -self.speed * 1.08
            # print(-2)
        elif self.pos.y <= paddle.y + segment * 4:  # segment 0
            self.vel.y = 0
            self.vel.x = self.speed if self.vel.x >= 0 else -self.speed
            # print(0)
        elif self.pos.y <= paddle.y + segment * 5:  # segment 0
            self.vel.y = 0
            self.vel.x = self.speed if self.vel.x >= 0 else -self.speed
            # print(0)
        elif self.pos.y <= paddle.y + segment * 6:  # segment 1
            self.vel.y = 3
            self.vel.x = self.speed * 1.08 if self.vel.x >= 0 else -self.speed * 1.08
            # print(1)
        elif self.pos.y <= paddle.y + segment * 7:  # segment 2
            self.vel.y = 5
            self.vel.x = self.speed * 1.14 if self.vel.x >= 0 else -self.speed * 1.14
            # print(2)
        elif self.pos.y <= paddle.y + segment * 8 + self.rad:  # segment 3
            self.vel.y = 6
            self.vel.x = self.speed * 1.21 if self.vel.x >= 0 else -self.speed * 1.21
            # print(3)

    def score(self) -> str:
        if self.pos.x - self.rad // 2 <= 0:
            score_left.play()
            return "player1"
        elif self.pos.x + self.rad // 2 >= WIDTH:
            score_right.play()
            return "player2"
        else:
            return "who?"

    def go_harder(self):
        if self.color[1] > 50:
            self.speed += 0.8
            self.color[1] -= 50
            self.color[2] -= 50


class Paddle(object):
    def __init__(self, name, x, color):
        self.name = name
        self.x = x
        self.width = 16
        self.height = 85
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 10
        self.color = color

    def render(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        if self.y <= -16:
            self.y = -16
        elif self.y + self.height >= HEIGHT + 16:
            self.y = HEIGHT - self.height + 16

    def move(self, dir):
        if dir == "up":
            self.y -= self.speed
        elif dir == "down":
            self.y += self.speed


def toggle_fullscreen(mode):
    global window, fullscreen
    if mode == "init":
        if not fullscreen:
            window = pygame.display.set_mode((WIDTH, HEIGHT))
        else:
            window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        last_frame = window.copy()
        if not fullscreen:
            window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            fullscreen = True
        else:
            window = pygame.display.set_mode((WIDTH, HEIGHT))
            fullscreen = False
        window.blit(last_frame, (0, 0))


def info_state() -> int:
    global running
    q = 0
    info_font = pygame.font.Font(masaaki, 40)
    instructions_font = pygame.font.Font(masaaki, 28)
    about_text = info_font.render("Pong clone coded by Simon.", True, (240, 240, 240))
    masaaki_text = info_font.render("Font, Masaaki-Regular, by Philippe Moesch.", True, (240, 240, 240))
    instructions_text1 = instructions_font.render("Move paddles using W-S and Up-Down.", True, (240, 240, 240))
    instructions_text2 = instructions_font.render("First player to score 10 points wins.", True, (240, 240, 240))
    instructions_text3 = instructions_font.render("Press P to pause the game, F to switch fullscreen,",
                                                  True, (240, 240, 240))
    instructions_text4 = instructions_font.render("ESC to quit and, while in start menu, H to display help.",
                                                  True, (240, 240, 240))
    go_back_text = info_font.render("Press SPACE to go back.", True, (240, 240, 240))
    info = True

    while info:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                info = False
                running = False
                q = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    info = False
                    running = False
                    q = 1
                elif event.key == pygame.K_f:
                    toggle_fullscreen("menu")
                elif event.key == pygame.K_SPACE:
                    info = False

        window.fill((2, 2, 2))
        window.blit(about_text, (WIDTH // 2 - about_text.get_width() // 2, HEIGHT // 2 - 240))
        window.blit(masaaki_text, (WIDTH // 2 - masaaki_text.get_width() // 2, HEIGHT // 2 - 180))
        window.blit(instructions_text1, (WIDTH // 2 - instructions_text1.get_width() // 2, HEIGHT // 2 - 50))
        window.blit(instructions_text2, (WIDTH // 2 - instructions_text2.get_width() // 2, HEIGHT // 2))
        window.blit(instructions_text3, (WIDTH // 2 - instructions_text3.get_width() // 2, HEIGHT // 2 + 50))
        window.blit(instructions_text4, (WIDTH // 2 - instructions_text4.get_width() // 2, HEIGHT // 2 + 100))
        window.blit(go_back_text, (WIDTH // 2 - go_back_text.get_width() // 2, HEIGHT // 2 + 210))
        show_version()
        pygame.display.flip()
        clock.tick(60)
    return q


def pause_game_state() -> int:
    global running
    q = 0
    pause_font = pygame.font.Font(masaaki, 55)
    pause_text = pause_font.render("PAUSED", True, (240, 240, 240))
    pause_width = pause_text.get_width()
    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
                running = False
                q = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    running = False
                    q = 1
                elif event.key == pygame.K_f:
                    toggle_fullscreen("menu")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    pause = False

        window.blit(pause_text, (WIDTH // 2 - pause_width // 2, HEIGHT // 2 - 50))
        pygame.display.flip()
        clock.tick(60)
    return q


def splash_screen_state() -> int:
    global running
    q = 0
    title_font = pygame.font.Font(masaaki, 110)
    start_font = pygame.font.Font(masaaki, 45)
    start_text = start_font.render("Press SPACE to start.", True, (240, 240, 240))
    start_width = start_text.get_width()
    title_text = title_font.render("PONG", True, (240, 240, 240))
    title_width = title_text.get_width()
    start = False

    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = True
                running = False
                q = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    start = True
                    running = False
                    q = 1
                elif event.key == pygame.K_SPACE:
                    start = True
                elif event.key == pygame.K_f:
                    toggle_fullscreen("menu")
                elif event.key == pygame.K_h:
                    if info_state() == 1:
                        start = True
                        q = 1

        window.fill((2, 2, 2))
        window.blit(title_text, (WIDTH // 2 - title_width // 2, 100))
        window.blit(start_text, (WIDTH // 2 - start_width // 2, HEIGHT // 2 + 140))
        show_version()
        pygame.display.flip()
        clock.tick(60)
    return q


def game_over_state(player):
    global running
    start_font = pygame.font.Font(masaaki, 45)
    game_over_font = pygame.font.Font(masaaki, 50)
    restart_text = start_font.render("Press SPACE to end match.", True, (240, 240, 240))
    restart_text_width = restart_text.get_width()
    background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    run = True

    background.fill((0, 0, 0, 96))
    if player == "player1":
        game_over_text = game_over_font.render("Player 1 wins.", True, (255, 240, 240))
        background.blit(game_over_text, (60, HEIGHT // 2 - 40))
    elif player == "player2":
        game_over_text = game_over_font.render("Player 2 wins.", True, (240, 240, 255))
        text_width = game_over_text.get_width()
        background.blit(game_over_text, (WIDTH - text_width - 60, HEIGHT // 2 - 40))
    background.blit(restart_text, (WIDTH // 2 - restart_text_width // 2, HEIGHT // 2 + 160))
    window.blit(background, (0, 0))
    pygame.display.flip()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    running = False
                elif event.key == pygame.K_SPACE:
                    run = False
                elif event.key == pygame.K_f:
                    toggle_fullscreen("menu")
                    window.blit(background, (0, 0))
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
    window.blit(fps_text, (6, HEIGHT - 30))


def show_version():
    version_text = fps_font.render(version, True, (255, 255, 255))
    window.blit(version_text, (WIDTH - 40, HEIGHT - 30))


def game_init():
    global window, clock, fps_font, score_font, player1_score, player2_score, masaaki, \
        hit_low, hit_high, score_left, score_right
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.mixer.init(22050, -16, 2, 512)
    pygame.init()
    toggle_fullscreen("init")
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load(os.path.join("gfx", "pong.png")))
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    masaaki = os.path.join("gfx", "Masaaki-Regular.otf")
    fps_font = pygame.font.Font(masaaki, 20)
    score_font = pygame.font.Font(masaaki, 50)
    hit_low = pygame.mixer.Sound(os.path.join("sounds", "hit_low.wav"))
    hit_high = pygame.mixer.Sound(os.path.join("sounds", "hit_high.wav"))
    score_left = pygame.mixer.Sound(os.path.join("sounds", "score_left.wav"))
    score_right = pygame.mixer.Sound(os.path.join("sounds", "score_right.wav"))
    player1_score = 0
    player2_score = 0


def game_loop():
    global running
    run = True
    did_once = False
    pong = None
    paddle1 = None
    paddle2 = None
    GO_FASTER = pygame.USEREVENT + 1
    pygame.time.set_timer(GO_FASTER, 7000)

    def start():
        nonlocal pong, paddle1, paddle2, did_once
        did_once = False
        pong = Pong(choice((-1, 1)))
        paddle1 = Paddle("left", 16, (230, 0, 0))
        paddle2 = Paddle("right", WIDTH - 34, (0, 0, 230))

    def update():
        global player1_score, player2_score
        nonlocal run
        pong.update()
        paddle1.update()
        paddle2.update()
        if pong.collide(paddle1):
            pong.bounce(paddle1)
        elif pong.collide(paddle2):
            pong.bounce(paddle2)
        if pong.score() == "player1":
            player2_score += 1
            start()
            pygame.time.wait(400)
        elif pong.score() == "player2":
            player1_score += 1
            start()
            pygame.time.wait(400)

    def render():
        for i in range(30):
            pygame.draw.rect(window, (230, 230, 230), (WIDTH // 2, i * 19.8 + 6, 2, 13.5))
        pygame.draw.line(window, (230, 230, 230), (0, 2), (WIDTH, 2), 3)
        pygame.draw.line(window, (230, 230, 230), (0, HEIGHT - 5), (WIDTH, HEIGHT - 5), 3)
        pong.render()
        paddle1.render()
        paddle2.render()
        show_scores()
        show_fps()

    if splash_screen_state() == 1:
        run = False
    start()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    running = False
                elif event.key == pygame.K_f:
                    toggle_fullscreen("game")
                    if pause_game_state() == 1:
                        run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if pause_game_state() == 1:
                        run = False
            elif event.type == GO_FASTER:
                pong.go_harder()

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
        if not did_once:
            pygame.time.wait(300)
            did_once = True
        if player1_score == 10:
            run = False
            game_over_state("player1")
        elif player2_score == 10:
            run = False
            game_over_state("player2")
        clock.tick(60)


if __name__ == "__main__":
    while running:
        game_init()
        game_loop()
    pygame.quit()
