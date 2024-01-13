"""Projekt WDI IQ puzzle - Wojciech Mierzejek 459435"""
from math import ceil
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def read_file(directory: str) -> np.ndarray:
    """Read file and return numpy array"""
    with open(directory, 'r', encoding='UTF-8') as file:
        data = file.read().splitlines()
    board = [[int(j) for j in i.split()] for i in data[1:]]
    board = np.array(board)
    return board

def read_all_pieces_from_board(board: np.ndarray) -> list:
    """Returns a setted list of numbers of pieces included in a board"""
    temp = board.tolist()
    return set(list(chain(*temp)))

def draw_an_element(element: int, board: np.ndarray) -> np.ndarray:
    """Draws a small numpy array including only specific element"""
    row_indexes, column_indexes = np.where(board == element)
    drawed = np.zeros((max(row_indexes)-min(row_indexes)+1,
                       max(column_indexes)-min(column_indexes)+1))
    # print(drawed)
    row_shift, col_shift = min(row_indexes), min(column_indexes)
    for row, column in zip(row_indexes, column_indexes):
        drawed[row-row_shift, column-col_shift] = element
    return drawed

def show(main_board: np.ndarray, unused_pieces: [np.ndarray]) -> None:
    """Shows in one windows main board and all the pieces"""
    colors = ['white', 'blue', 'yellow', 'green', 'orange', 'purple', 'pink',
               'brown', 'red', 'cyan', 'magenta', 'gray', 'lightgreen']
    if len(unused_pieces) < 2:
        width = len(unused_pieces) + 1
    else:
        width = 3
    height = ceil(len(unused_pieces)/2)

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(height, width, width_ratios=[2]+[1]*(width-1), height_ratios=[1]*height)
    colormap = ListedColormap(colors)

    main_plot = fig.add_subplot(gs[0, 0])
    unused_plots = [fig.add_subplot(gs[i, j+1]) for i in range(height) for j in range(width-1)]

    main_plot.imshow(main_board, cmap=colormap)
    main_plot.set_title("Układana plansza")
    # get rid of axes descriptions
    main_plot.set_xticks([])
    main_plot.set_yticks([])

    for board, plot in zip(unused_pieces, unused_plots):
        # add unused piece and make it specific color
        plot.imshow(board,
                cmap=ListedColormap([colors[0]]+[colors[int(max(list(chain(*board.tolist()))))]]))
        plot.set_xticks([])
        plot.set_yticks([])
    plt.tight_layout()
    plt.show()


def dopa

# get input
SOLVED_BOARD = read_file('plansza.txt')
board_in_progress = read_file('plansza2.txt')

# get basic info from input - all pieces, read how not placed pieces look like 
ALL_PIECES = read_all_pieces_from_board(SOLVED_BOARD)
PLACED = set(list(chain(*board_in_progress.tolist())))
# pieces - list of np.ndarrays representing 
pieces = [draw_an_element(i, SOLVED_BOARD) for i in ALL_PIECES if i not in PLACED]

