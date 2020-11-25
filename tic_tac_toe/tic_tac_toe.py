import pygame
from pygame import *
import sys
import time

# global variables
xo = "x"
winner = None
draw = False

width = 500
height = 500

white = (250, 250, 250)
line_color = (88, 88, 88)

# tic tac toe 3x3 surface
surface = [[None] * 3, [None] * 3, [None] * 3]

# initializing pygame window
pygame.init()
fps = 30
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((width, height + 100), 0, 32)
pygame.display.set_caption("Tic Tac Toe")

# loading the images
opening = pygame.image.load("tic.png")
x_img = pygame.image.load('x.png')
o_img = pygame.image.load('o.png')

# resizing images
x_img = pygame.transform.scale(x_img, (90, 110))
o_img = pygame.transform.scale(o_img, (80, 100))
opening = pygame.transform.scale(opening, (width, height + 120))


def start_game():
    screen.blit(opening, (0, 0))
    pygame.display.update()
    time.sleep(1)
    screen.fill(white)

# drawing vertical lines
    pygame.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 12)
    pygame.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 12)
# drawing horizontal lines
    pygame.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 12)
    pygame.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 12)
    equal_status()


def equal_status():
    if winner is None:
        message = xo.upper() + "'s Turn"
    else:
        message = winner.upper() + " Won!"

    if draw:
        message = "Game is Draw!"

    end_font = pygame.font.SysFont("aerial", 70, "bold")
    text = end_font.render(message, True, (200, 0, 0))

    # copy the rendered message onto surface
    screen.fill((88, 88, 88), (0, 500, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 600 - 50))
    screen.blit(text, text_rect)
    pygame.display.update()


def check_win():
    global surface, winner, draw
    # check for winning rows
    for row in range(0, 3):
        if (surface[row][0] == surface[row][1] == surface[row][2]) and (surface[row][0] is not None):
            winner = surface[row][0]
            pygame.draw.line(screen, (200, 0, 0), (0, (row + 1) * height / 3 - height / 6),
                             (width, (row + 1) * height / 3 - height / 6), 33)
            break

    # check for winning columns
    for col in range(0, 3):
        if (surface[0][col] == surface[1][col] == surface[2][col]) and (surface[0][col] is not None):
            winner = surface[0][col]
            pygame.draw.line(screen, (200, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                             ((col + 1) * width / 3 - width / 6, height), 33)
            break

    # check for diagonal winners
    if (surface[0][0] == surface[1][1] == surface[2][2]) and (surface[0][0] is not None):
        winner = surface[0][0]
        pygame.draw.line(screen, (200, 70, 70), (50, 50), (450, 450), 33)

    if (surface[0][2] == surface[1][1] == surface[2][0]) and (surface[0][2] is not None):
        winner = surface[0][2]
        pygame.draw.line(screen, (200, 70, 70), (450, 50), (50, 450), 33)

    if all([all(row) for row in surface]) and winner is None:
        draw = True
    equal_status()


def draw_xo(row, col):
    global surface, xo, pos_y, pos_x
    if row == 1:
        pos_x = 30
    if row == 2:
        pos_x = width / 3 + 30
    if row == 3:
        pos_x = width / 3 * 2 + 30

    if col == 1:
        pos_y = 30
    if col == 2:
        pos_y = height / 3 + 30
    if col == 3:
        pos_y = height / 3 * 2 + 30
    surface[row - 1][col - 1] = xo
    if xo == "x":
        screen.blit(x_img, (pos_y, pos_x))
        xo = "o"
    else:
        screen.blit(o_img, (pos_y, pos_x))
        xo = "x"
    pygame.display.update()


def mouse_click():
    # get coordinates of mouse click
    x, y = pygame.mouse.get_pos()

    # get column of mouse click (1-3)
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # get row of mouse click (1-3)
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and surface[row - 1][col - 1] is None:
        global xo

        # draw the x or o on surface
        draw_xo(row, col)
        check_win()


def reset():
    global surface, winner, xo, draw
    time.sleep(3)
    xo = 'x'
    draw = False
    start_game()
    winner = None
    surface = [[None] * 3, [None] * 3, [None] * 3]


start_game()


# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click()
            if winner or draw:
                reset()

    pygame.display.update()
    CLOCK.tick(fps)

