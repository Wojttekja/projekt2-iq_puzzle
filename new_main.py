"""Projekt WDI IQ puzzle - Wojciech Mierzejek 459435"""
from math import ceil
from itertools import chain
import argparse
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
    """returns list of variants of given piece, varaints meaning roteted or fliped piece"""
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

def solve(board_to_solve: np.ndarray, pieces: [np.ndarray]) -> np.ndarray:
    """"returns solved board using given pieces or False if board is unsolvable"""
    posibilities = [board_to_solve]
    while len(pieces) > 1:
        new = []
        for b in posibilities:
            new += place_piece_in_every_place(b, pieces[0])
        posibilities = new.copy()
        pieces.pop(0)
    for posiblity in posibilities:
        maybe_finished = place_last_piece(posiblity, pieces[0])
        if isinstance(maybe_finished, np.ndarray):
            return maybe_finished
    return False

def show_solving(solved: np.ndarray, drawed_pieces: {int: np.ndarray},
                 pieces_to_place: list, pause: float) -> None:
    """sets pieces in random order and places them one by one"""
    colors = ['white', 'blue', 'yellow', 'green', 'orange', 'purple', 'pink',
               'brown', 'red', 'cyan', 'magenta', 'gray', 'lightgreen']
    width = 3
    height = ceil(len(pieces_to_place)/2)
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(height, width, width_ratios=[2, 1, 1], height_ratios=[1]*height)

    main_plot = fig.add_subplot(gs[0, 0])
    unused_plots = [fig.add_subplot(gs[i, j]) for i in range(height) for j in range(1, width)]

    # initialize plots and show starting board and pieces
    in_progress = solved.copy()
    for number in pieces_to_place:
        in_progress[in_progress == number] = 0
    main_show = main_plot.imshow(in_progress, cmap=ListedColormap(colors))
    main_plot.set_title("Układana plansza")
    main_plot.set_xticks([])
    main_plot.set_yticks([])
    unused_show = []
    for piece, plot in zip(pieces_to_place, unused_plots):
        unused_show.append(plot.imshow(drawed_pieces[piece],
                                       cmap=ListedColormap([colors[0]]+[colors[piece]])))
        plot.set_xticks([])
        plot.set_yticks([])
    plt.tight_layout()

    # start placing puzzles one by one
    for i in range(len(pieces_to_place)):
        plt.pause(pause)
        unused_show[i].set_data(np.zeros(drawed_pieces[pieces_to_place[0]].shape))
        pieces_to_place.pop(0)
        in_progress = solved.copy()
        for number in pieces_to_place:
            in_progress[in_progress == number] = 0

        main_show.set_data(in_progress)

    plt.show()

def main():
    """Parsing arguments, solving and showing solving process"""
    parser = argparse.ArgumentParser(description='IQ puzzle solver')
    parser.add_argument('-n', '--pausetime', type=float,
                        help='Input how long should program wait between moves', default=1.0)
    parser.add_argument('-p', '--solved', type=str,
                        help='Input directory to file with solved puzzle', default='plansza.txt')
    parser.add_argument('input_file', type=str, help='Input file with puzzle to solve')
    args = parser.parse_args()
    pause = args.pausetime
    solved_file = args.solved
    file_to_solve = args.input_file

    solved_board = read_file(solved_file)
    board_to_solve = read_file(file_to_solve)

    all_pieces = read_all_pieces_from_board(solved_board)
    placed = set(list(chain(*board_to_solve.tolist())))
    not_placed = [i for i in all_pieces if i not in placed]
    drawed_pieces = {i: draw_an_element(i, solved_board) for i in not_placed}
    pieces_to_place = list(drawed_pieces.values())

    show_solving(solve(board_to_solve, pieces_to_place), drawed_pieces, not_placed, pause)


if __name__ == "__main__":
    main()
