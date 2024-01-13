"""Projekt WDI IQ puzzle - Wojciech Mierzejek 459435"""
import sys
import os
import pygame
pygame.init()
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from itertools import chain

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
# assumption there won't be more than 12 unplaced pieces
UNUSED_PIC_SIZE = 230
POSITIONS_FOR_UNUSED_PIECES = [(x, y) for x in range(SCREEN_WIDTH//2+10, SCREEN_WIDTH, UNUSED_PIC_SIZE+10) for y in range(SCREEN_HEIGHT//4, SCREEN_HEIGHT-200, UNUSED_PIC_SIZE+10)]
print(POSITIONS_FOR_UNUSED_PIECES)
# quit()
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IQ puzzle")
font = pygame.font.Font(None, 36)


# read arguments
TIME = 1



def display_text(word: str, side: bool, font: pygame.font.Font, color: tuple, SCREEN_WIDTH: int, screen: pygame.surface.Surface) -> None:
    """display text on the left side if side True, or on right if false"""
    text = font.render(word, True, color)

    # position the text
    if side:
        positioned_text = text.get_rect(center=(SCREEN_WIDTH // 4, 50))
    else:
        positioned_text = text.get_rect(center=(3 * SCREEN_WIDTH // 4, 50))

    # Display the text on the screen
    screen.blit(text, positioned_text)

def display_image(directory: str, side: bool, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, screen: pygame.surface.Surface) -> None:
    image = pygame.image.load(directory)
    image = pygame.transform.scale(image, (450, 400))
    if side:
        positioned = image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    else:
        positioned = image.get_rect(center=(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    screen.blit(image, positioned)

def read_file(directory: str) -> np.ndarray:
    """Read file and return numpy array"""
    with open(directory, 'r') as file:
        data = file.read().splitlines()
    board = [[int(j) for j in i.split()] for i in data[1:]]
    board = np.array(board)
    return board

def make_image(array: np.ndarray, directory: str) -> None:
    """Show numpy array as matplotlib board and save to file"""
    plt.imshow(array)
    plt.savefig(directory)


# running = True
board_in_progress = read_file("plansza2.txt")
SOLVED = read_file("plansza.txt")

# read all unused pieces
def read_all_pieces_from_board(board: np.ndarray) -> list:
    """Returns a setted list of numbers of pieces included in a board"""
    temp = board.tolist()
    return set(list(chain(*temp)))


def draw_an_element(element: int, board: np.ndarray) -> np.ndarray:
    """Draws a small numpy array including only specific element"""
    row_indexes, column_indexes = np.where(board == element)
    drawed = np.zeros((max(row_indexes)-min(row_indexes)+1, max(column_indexes)-min(column_indexes)+1))
    # print(drawed)
    row_shift, col_shift = min(row_indexes), min(column_indexes)
    for row, column in zip(row_indexes, column_indexes):
        drawed[row-row_shift, column-col_shift] = element
    return drawed

ALL_PIECES = read_all_pieces_from_board(SOLVED)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)

    # line
    pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 3)

    display_text("Układana plansza", True, font, BLACK, SCREEN_WIDTH, screen)
    display_text("Pozostałe elementy", False, font, BLACK, SCREEN_WIDTH, screen)
    make_image(board_in_progress, "solved.png")
    display_image("solved.png", True, SCREEN_WIDTH, SCREEN_HEIGHT, screen)


    # show current not placed pieces
    used = read_all_pieces_from_board(board_in_progress)
    unused = [i for i in ALL_PIECES if i not in used]

    for piece in unused:
        array = draw_an_element(piece, SOLVED)
        make_image(array, f"unused{piece}.png")
    image_files = [f"unused{i}.png" for i in unused]
    images = []
    for img_file in image_files:
        img = pygame.image.load(os.path.join('', img_file)).convert_alpha()
        img_height, img_width = img.get_height(), img.get_width()
        # resize
        if img_width > img_height:
            resized_img = pygame.transform.scale(img, (UNUSED_PIC_SIZE, img_height * UNUSED_PIC_SIZE // img_width)) 
        else:
            resized_img = pygame.transform.scale(img, (img_width * UNUSED_PIC_SIZE // img_height, UNUSED_PIC_SIZE)) 
        images.append(resized_img)
    for img, pos in zip(images, POSITIONS_FOR_UNUSED_PIECES):
        screen.blit(img, pos)

    pygame.display.update()
    sleep(1)

pygame.quit()
sys.exit()
