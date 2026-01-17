# PONG pygame
# Original version by Vinoth Pandian
# Modified for lzscc.200 by Marco Caminati

import pygame, random, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0
speed_increment = 1.1

myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
MENU = "menu"
GAME = "game"
PLAY = "play"
COMMAND_LIST = "command list"
menu_items = {}
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Hello World")


def ball_init(right):
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)
    if right == False:
        horz = -horz
    ball_vel = [horz, -vert]


def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)


def draw_text(text, font, text_color, x_pos, y_pos, canvas):
    img = font.render(text, True, text_color)
    rect = img.get_rect()
    rect.center = (x_pos, y_pos)
    canvas.blit(img, rect)
    return rect


def draw_menu(canvas):
    canvas.fill(BLACK)
    menu_items["START"] = draw_text("START GAME", myfont1, WHITE, 300, 200, canvas)
    menu_items["COMMAND"] = draw_text("COMMANDS", myfont1, WHITE, 300, 250, canvas)
    draw_text("SELECT DIFFICULTY:", myfont1, RED, 300, 220, canvas)
    menu_items["EASY"] = draw_text("EASY (5%)", myfont1, GREEN, 200, 270, canvas)
    menu_items["MEDIUM"] = draw_text("MEDIUM (10%)", myfont1, GREEN, 300, 270, canvas)
    menu_items["HARD"] = draw_text("HARD (20%)", myfont1, GREEN, 420, 270, canvas)
    return menu_items


def draw_command(canvas):
    canvas.fill(BLACK)
    draw_text("PLAYER ONE", myfont1, WHITE, 300, 50, canvas)
    draw_text("up: up", myfont1, WHITE, 300, 100, canvas)
    draw_text("down: down", myfont1, WHITE, 300, 150, canvas)
    draw_text("PLAYER TWO", myfont1, WHITE, 300, 200, canvas)
    draw_text("up: W", myfont1, WHITE, 300, 250, canvas)
    draw_text("down: S", myfont1, WHITE, 300, 300, canvas)
    menu_items["COME BACK"] = draw_text(
        "COME BACK TO THE MAIN MENU", myfont1, WHITE, 300, 350, canvas
    )
    return menu_items


def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score, speed_increment
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(
        canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1
    )
    pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(
        canvas,
        GREEN,
        [
            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
        ],
        0,
    )
    pygame.draw.polygon(
        canvas,
        GREEN,
        [
            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
        ],
        0,
    )

    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(
        paddle1_pos[1] - HALF_PAD_HEIGHT, paddle1_pos[1] + HALF_PAD_HEIGHT, 1
    ):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= speed_increment
        ball_vel[1] *= speed_increment
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(
        ball_pos[1]
    ) in range(paddle2_pos[1] - HALF_PAD_HEIGHT, paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= speed_increment
        ball_vel
