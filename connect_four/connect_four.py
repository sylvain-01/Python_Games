import numpy as np
import pygame
import sys
import math

red = (255, 11, 22)
green = (11, 255, 22)
blue = (11, 22, 255)
black = (0, 0, 0)

row_count = 6
column_count = 7


# functions
def create_board():
    board = np.zeros((row_count, column_count))
    return board


def drop_item(board, row, col, item):
    board[row][col] = item


def valid_location(board, col):
    return board[row_count - 1][col] == 0


def get_next_row(board, col):
    for r in range(row_count):
        if board[r][col] == 0:
            return r


def win(board, item):
    # check horizontal locations
    for c in range(column_count - 3):
        for r in range(row_count):
            if board[r][c] == item and board[r][c+1] == item and board[r][c+2] == item and board[r][c+3] == item:
                return True
    # check horizontal locations
    for c in range(column_count):
        for r in range(row_count - 3):
            if board[r][c] == item and board[r + 1][c] == item and board[r + 2][c] == item and board[r + 3][c] == item:
                return True
    # check positively sloped diagonals
    for c in range(column_count - 3):
        for r in range(row_count - 3):
            if board[r][c] == item and board[r + 1][c + 1] == item and board[r + 2][c + 2] == item \
                    and board[r + 3][c + 3] == item:
                return True
    # check negatively sloped diagonals
    for c in range(column_count - 3):
        for r in range(3, row_count):
            if board[r][c] == item and board[r - 1][c + 1] == item and board[r - 2][c + 2] == item \
                    and board[r - 3][c + 3] == item:
                return True


def draw_board(board):
    for c in range(column_count):
        for r in range(row_count):
            pygame.draw.rect(screen, blue, [c * square_size, r * square_size + square_size, square_size, square_size])
            pygame.draw.circle(screen, black, (
                int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), radius)

    for c in range(column_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(screen, red, (
                    int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, green, (
                    int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), radius)
    pygame.display.update()


# variables
board = create_board()
game_over = False
turn = 0

pygame.init()

square_size = 100
width = column_count * square_size
height = (row_count + 1) * square_size
size = (width, height)
radius = int(square_size / 2 - 4)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")
draw_board(board)
pygame.display.update()
my_font = pygame.font.SysFont("roman", 75)


# reset
def reset():
    global board, game_over
    game_over = False
    draw_board(board)
    board = create_board()
    pygame.time.wait(3000)
    pygame.display.update()


# game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, [0, 0, width, square_size])
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, [pos_x, square_size / 2], radius)
            else:
                pygame.draw.circle(screen, green, [pos_x, square_size / 2], radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, [0, 0, width, square_size])

            if turn == 0:
                pos_x = event.pos[0]
                col = math.floor(pos_x / square_size)

                if valid_location(board, col):
                    row = get_next_row(board, col)
                    drop_item(board, row, col, 1)

                    if win(board, 1):
                        label = my_font.render("Player 1 Wins", True, red)
                        screen.blit(label, (125, 10))
                        reset()

            else:
                pos_x = event.pos[0]
                col = math.floor(pos_x / square_size)

                if valid_location(board, col):
                    row = get_next_row(board, col)
                    drop_item(board, row, col, 2)

                    if win(board, 2):
                        label = my_font.render("Player 2 Wins", True, green)
                        screen.blit(label, (125, 10))
                        reset()

            draw_board(board)

            turn += 1
            turn = turn % 2
        pygame.display.update()






