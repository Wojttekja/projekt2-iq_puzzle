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

    if len(unused_pieces) == 0:
        plt.imshow(main_board, cmap=ListedColormap(colors))
        plt.title("Ulozona plansza")
        plt.xticks([])
        plt.yticks([])
        plt.show()

    if len(unused_pieces) < 2:
        width = len(unused_pieces) + 1
    else:
        width = 3
    height = ceil(len(unused_pieces)/2)

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(height, width, width_ratios=[2]+[1]*(width-1), height_ratios=[1]*height)

    main_plot = fig.add_subplot(gs[0, 0])
    unused_plots = [fig.add_subplot(gs[i, j+1]) for i in range(height) for j in range(width-1)]

    main_plot.imshow(main_board, cmap=ListedColormap(colors))
    main_plot.set_title("Układana plansza")
    # get rid of axes descriptions
    main_plot.set_xticks([])
    main_plot.set_yticks([])

    for board, plot in zip(unused_pieces, unused_plots):
        # add unused piece and make it specific color
        plot.imshow(board, cmap=ListedColormap([colors[0]]+[colors[int(board.max())]]))
        plot.set_xticks([])
        plot.set_yticks([])
    plt.tight_layout()
    plt.show()

def put_piece(board: np.ndarray, piece: np.ndarray, place: (int, int)) -> bool or np.ndarray:
    """places a piece into board on specified location or return False if it doesn't fit"""
    # height, width = piece.shape
    new_board = board.copy()
    ys, xs = piece.nonzero()
    number = piece[ys[0], xs[0]]
    for y, x in zip(ys, xs):
        try:
            if new_board[y+place[0], x+place[1]] != 0:
                return False
        except IndexError:
            return False
        new_board[y+place[0], x+place[1]] = number
    return new_board

def get_all_variants(piece: np.ndarray) -> [np.ndarray]:
    """returns list of variants of given piece, 
    varaints meaning roteted or fliped piece"""
    all_varaints = []
    listed_variants = []
    for k in range(-1, 3):
        temp = np.rot90(piece, k=k)
        listed_temp = temp.tolist()
        if listed_temp not in listed_variants:
            listed_variants.append(listed_temp)
            all_varaints.append(temp)

    fliped = np.flip(piece, 0)
    for k in range(-1, 3):
        temp = np.rot90(fliped, k=k)
        listed_temp = temp.tolist()
        if listed_temp not in listed_variants:
            listed_variants.append(listed_temp)
            all_varaints.append(temp)

    return all_varaints

def place_last_piece(board: np.ndarray, piece: np.ndarray) -> np.ndarray:
    """Bruttally trying to place last piece into board"""
    variants = get_all_variants(piece)
    # import pdb; pdb.set_trace()
    height, width = board.shape
    for y in range(height):
        for x in range(width):
            for v in variants:
                attempt = put_piece(board, v, (y, x))
                if isinstance(attempt, np.ndarray):
                    return attempt
    return False

def place_piece_in_every_place(board: np.ndarray, piece: np.ndarray) -> [np.ndarray]:
    """returns list of boards with placed some piece"""
    outcome = []
    variants = get_all_variants(piece)
    height, width = board.shape
    for y in range(height):
        for x in range(width):
            for v in variants:
                attempt = put_piece(board, v, (y, x))
                if isinstance(attempt, np.ndarray):
                    outcome.append(attempt)
    return outcome


# get input
SOLVED_BOARD = read_file('plansza.txt')
BOARD_TO_SOLVE = read_file('plansza3.txt')

# get basic info from input - all pieces, read how not placed pieces look like
ALL_PIECES = read_all_pieces_from_board(SOLVED_BOARD)
PLACED = set(list(chain(*BOARD_TO_SOLVE.tolist())))
NOT_PLACED = [i for i in ALL_PIECES if i not in PLACED]
# pieces - list of np.ndarrays representing

pieces = [draw_an_element(i, SOLVED_BOARD) for i in ALL_PIECES if i not in PLACED]
posibilities = [BOARD_TO_SOLVE]

while len(pieces) > 1:
    new = []
    for b in posibilities:
        new += place_piece_in_every_place(b, pieces[0])
    posibilities = new.copy()
    pieces.pop(0)

print(len(posibilities))
for posiblity in posibilities:
    temp = place_last_piece(posiblity, pieces[0])
    if isinstance(temp, np.ndarray):
        print(temp)
        # show solving
        break