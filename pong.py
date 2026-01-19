# PONG pygame
# Original version by Vinoth Pandian
# Modified for lzscc.200 by Marco Caminati
# You might need to install pygame:
# python3 -m pip install --user pygame
# If the command above doesn't work, try venv:
# python3 -m venv ~/pongenv
# source ~/pongenv/bin/activate
# python3 -m pip install pygame

import pygame, random, sys

from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255,255,165)

# globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
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

x_speed_increment_level = 1
y_speed_increment_level = 1
hit_increment = 1.20

myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
MENU = 'menu'
GAME = 'game'
PLAY = 'play'
COMMAND_LIST  = 'command list'
SET_LEVEL = 'set level'
GAME_OVER = 'game_over'
EXIT_GAME = False
WAIT_END = 10000
menu_items = {}
# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Super Pong 2026")


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = - horz

    ball_vel = [horz* x_speed_increment_level, -vert*y_speed_increment_level]


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)


def draw_text(text, font, text_color, x_pos, y_pos ,canvas):
    img = font.render(text, True, text_color)
    rect = img.get_rect()  # get rect FIRST
    rect.center = (x_pos, y_pos)  # then center it
    canvas.blit(img, rect)
    return  rect

def draw_menu(canvas):
    canvas.fill(BLACK)
    menu_items ['START'] = draw_text("START GAME",myfont1, WHITE,300,150,  canvas  )
    menu_items ['COMMAND'] =  draw_text("COMMANDS",myfont1, WHITE,300,200,  canvas  )
    menu_items ['SET LEVEL'] =  draw_text("SELECT LEVEL", myfont1, WHITE, 300, 250, canvas)
    return menu_items

def draw_game_over(canvas):
    menu_items = {}
    canvas.fill(BLACK)
    if l_score > r_score:
        draw_text('THE RESULT IS: ', myfont1, WHITE, 300, 100, canvas)
        score = f'{l_score} TO {r_score}'
        draw_text('WIN PLAYER ONE!', myfont1, WHITE, 300, 150, canvas)
        draw_text(score, myfont1, WHITE, 300, 200, canvas)

    if l_score < r_score:
        draw_text('THE RESULT IS: ', myfont1, WHITE, 300, 100, canvas)
        score = f'{l_score} TO {r_score}'
        draw_text('WIN PLAYER TWO!', myfont1, WHITE, 300, 150, canvas)
        draw_text(score, myfont1, WHITE, 300, 200, canvas)

    if l_score == r_score:
        draw_text('THE RESULT IS: ', myfont1, WHITE, 300, 100, canvas)
        score = f'{l_score} TO {r_score}'
        draw_text('NO ONE WIN', myfont1, WHITE, 300, 150, canvas)
        draw_text(score, myfont1, WHITE, 300, 200, canvas)



    game_over = 'GAME OVER!'
    menu_items ['GAME_OVER'] = draw_text(game_over, myfont1, WHITE, 300, 300, canvas)
    return menu_items


def draw_command(canvas):
    menu_items = {}
    canvas.fill(BLACK)
    player_one = 'PLAYER ONE'
    draw_text(player_one, myfont1, WHITE, 300, 50, canvas)
    move_up = 'up: W'
    draw_text(move_up, myfont1, WHITE, 300, 100, canvas)
    move_down = 'down: S'
    draw_text(move_down, myfont1, WHITE, 300, 150, canvas)

    player_two = 'PLAYER TWO'
    draw_text(player_two, myfont1, WHITE, 300, 200, canvas)
    move_up = 'up: UP'
    draw_text(move_up, myfont1, WHITE, 300, 250, canvas)
    move_down = 'down: DOWN'
    rectangle = draw_text(move_down, myfont1, WHITE, 300, 300, canvas)
    back_main = 'COME BACK TO THE MAIN MENU'
    menu_items ['COME BACK'] = draw_text(back_main, myfont1, WHITE, 300, 350, canvas)
    return menu_items


def draw_level(canvas):
    canvas.fill(BLACK)
    menu_items = {}
    menu_items["EASY"] = draw_text("EASY (1.00)", myfont1, GREEN, 300, 100, canvas)
    menu_items["MEDIUM"] = draw_text("MEDIUM (1.50)", myfont1, ORANGE, 300, 150, canvas)
    menu_items["HARD"] = draw_text("HARD (2.00)", myfont1, RED, 300, 200, canvas)
    back_main = 'COME BACK TO THE MAIN MENU'
    menu_items ['LEVEL COME BACK'] = draw_text(back_main, myfont1, WHITE, 300, 250, canvas)
    return menu_items

# draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
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

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, BALL_RADIUS, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                        [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    # ball collision check on top and bottom walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # ball collison check on gutters or paddles
    if (
            ball_pos[0] <= BALL_RADIUS + PAD_WIDTH
            and paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT
            and paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT
    ):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= hit_increment
        ball_vel[1] *= hit_increment
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)

    if (
            ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH
            and paddle2_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT
    ):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= hit_increment
        ball_vel[1] *= hit_increment
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    # update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 0))
    canvas.blit(label2, (470, 20))

    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("press Q for Exit ", 1, (255, 255, 0))
    canvas.blit(label1, (220, 20))


# keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel

    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8


# keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0


init()

game_state = MENU
start_rect = None
# game loop
while True:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q and  game_state == PLAY:
               game_state = GAME_OVER
            else: keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        if event.type == QUIT or EXIT_GAME:
            pygame.time.wait(WAIT_END)
            pygame.quit()
            sys.exit()

        if game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect["START"].collidepoint(event.pos):
                    game_state = PLAY
                if start_rect["COMMAND"].collidepoint(event.pos):
                    game_state = COMMAND_LIST
                if start_rect['SET LEVEL'].collidepoint(event.pos):
                    game_state = SET_LEVEL
         

        elif game_state == COMMAND_LIST:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect["COME BACK"].collidepoint(event.pos):
                    game_state = MENU

        elif game_state == SET_LEVEL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if  start_rect["EASY"].collidepoint(event.pos):
                    x_speed_increment_level = 1.00
                    y_speed_increment_level = 1.00
                    ball_init(True)
                    
                elif start_rect["MEDIUM"].collidepoint(event.pos):
                    x_speed_increment_level = 1.50
                    y_speed_increment_level = 1.50
                    ball_init(True)
                 
                elif start_rect["HARD"].collidepoint(event.pos):
                    x_speed_increment_level = 2.00
                    y_speed_increment_level = 2.00
                    ball_init(True)
        
                elif start_rect["LEVEL COME BACK"].collidepoint(event.pos):
                     game_state = MENU

        
        elif game_state == PLAY:
            if event.type == KEYDOWN:
                keydown(event)
            elif event.type == KEYUP:
                keyup(event)
        

    # --------------------
    # 1. DRAW
    # --------------------
    if game_state == MENU:
        start_rect = draw_menu(window)

    elif game_state == COMMAND_LIST:
        start_rect = draw_command(window)

    elif game_state == SET_LEVEL:
        start_rect = draw_level(window)

    elif game_state == PLAY:
        draw(window)

    elif game_state == GAME_OVER:
        draw_game_over(window)
        EXIT_GAME = True

    pygame.display.update()
    fps.tick(90)
