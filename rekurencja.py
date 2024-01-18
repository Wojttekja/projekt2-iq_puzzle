"""Projekt WDI IQ puzzle - Wojciech Mierzejek <nrindeksu>"""
from math import ceil
from itertools import chain
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from datetime import datetime
start = datetime.now()

def read_file(directory: str) -> np.ndarray:
    """Read file and return numpy array"""
    with open(directory, 'r', encoding='UTF-8') as file:
        data = file.read().splitlines()
    board = [[int(j) for j in i.split()] for i in data[1:]]
    board = np.array(board)
    return board

def read_all_puzzles_from_board(board: np.ndarray) -> list:
    """Returns a setted list of numbers of puzzles included in a board"""
    temp = board.tolist()
    return set(list(chain(*temp)))

def draw_an_element(element: int, board: np.ndarray) -> np.ndarray:
    """Draws a small numpy array including only specific element"""
    row_indexes, column_indexes = np.where(board == element)
    drawed = np.zeros((max(row_indexes)-min(row_indexes)+1,
                       max(column_indexes)-min(column_indexes)+1))
    row_shift, col_shift = min(row_indexes), min(column_indexes)
    for row, column in zip(row_indexes, column_indexes):
        drawed[row-row_shift, column-col_shift] = element
    return drawed

def put_puzzle(board: np.ndarray, puzzle: np.ndarray, place: (int, int)) -> bool or np.ndarray:
    """places a puzzle into board on specified location or return False if it doesn't fit"""
    new_board = board.copy()
    ys, xs = puzzle.nonzero()
    number = puzzle[ys[0], xs[0]]
    for y, x in zip(ys, xs):
        try:
            if new_board[y+place[0], x+place[1]] != 0:
                return False
        except IndexError:
            return False
        new_board[y+place[0], x+place[1]] = number
    return new_board

def get_all_variants(puzzle: np.ndarray) -> [np.ndarray]:
    """returns list of variants of given puzzle, varaints meaning roteted or fliped puzzle"""
    all_varaints = []
    listed_variants = []
    for k in range(-1, 3):
        temp = np.rot90(puzzle, k=k)
        listed_temp = temp.tolist()
        if listed_temp not in listed_variants:
            listed_variants.append(listed_temp)
            all_varaints.append(temp)

    fliped = np.flip(puzzle, 0)
    for k in range(-1, 3):
        temp = np.rot90(fliped, k=k)
        listed_temp = temp.tolist()
        if listed_temp not in listed_variants:
            listed_variants.append(listed_temp)
            all_varaints.append(temp)

    return all_varaints

def place_last_puzzle(board: np.ndarray, puzzle: np.ndarray) -> np.ndarray:
    """Bruttally trying to place last puzzle into board"""
    variants = get_all_variants(puzzle)
    height, width = board.shape
    for y in range(height):
        for x in range(width):
            for v in variants:
                attempt = put_puzzle(board, v, (y, x))
                if isinstance(attempt, np.ndarray):
                    return attempt
    return False

def place_puzzle_in_every_place(board: np.ndarray, puzzle: np.ndarray) -> [np.ndarray]:
    """returns list of boards with placed some puzzle"""
    outcome = []
    variants = get_all_variants(puzzle)
    height, width = board.shape
    for y in range(height):
        for x in range(width):
            for v in variants:
                attempt = put_puzzle(board, v, (y, x))
                if isinstance(attempt, np.ndarray):
                    outcome.append(attempt)
    return outcome

def solve(board_to_solve: np.ndarray, puzzles: [np.ndarray]) -> np.ndarray:
    """"returns solved board using given puzzles or False if board is unsolvable"""
    posibilities = [board_to_solve]
    while len(puzzles) > 1:
        new = []
        for b in posibilities:
            new += place_puzzle_in_every_place(b, puzzles[0])
        posibilities = new.copy()
        puzzles.pop(0)
    for posiblity in posibilities:
        maybe_finished = place_last_puzzle(posiblity, puzzles[0])
        if isinstance(maybe_finished, np.ndarray):
            return maybe_finished
    return False


def new_solve(board_to_solve: np.ndarray, puzzles: [np.ndarray]) -> np.ndarray:
    """solves puzzle recursively"""
    if len(puzzles) == 0:
        return board_to_solve
    variants = get_all_variants(puzzles[0])
    height, width = board_to_solve.shape
    for y in range(height):
        for x in range(width):
            for v in variants:
                temp = put_puzzle(board_to_solve, v, (y, x))
                if isinstance(temp, np.ndarray):
                    
                    temp2 = new_solve(temp, puzzles[1:])
                    if isinstance(temp2, np.ndarray):
                        return temp2
    return False

def show_solving(solved: np.ndarray, drawed_puzzles: {int: np.ndarray},
                 puzzles_to_place: list, pause: float) -> None:
    """sets puzzles in random order and places them one by one"""
    colors = ['white', 'blue', 'yellow', 'green', 'orange', 'purple', 'pink',
               'brown', 'red', 'cyan', 'magenta', 'gray', 'lightgreen']
    width = 3
    height = ceil(len(puzzles_to_place)/2)
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(height, width, width_ratios=[2, 1, 1], height_ratios=[1]*height)

    main_plot = fig.add_subplot(gs[0, 0])
    unused_plots = [fig.add_subplot(gs[i, j]) for i in range(height) for j in range(1, width)]

    # initialize plots and show starting board and puzzles
    in_progress = solved.copy()
    for number in puzzles_to_place:
        in_progress[in_progress == number] = 0
    main_show = main_plot.imshow(in_progress, cmap=ListedColormap(colors))
    main_plot.set_title("Układana plansza")
    main_plot.set_xticks([])
    main_plot.set_yticks([])
    unused_show = []
    for puzzle, plot in zip(puzzles_to_place, unused_plots):
        unused_show.append(plot.imshow(drawed_puzzles[puzzle],
                                       cmap=ListedColormap([colors[0]]+[colors[puzzle]])))
    for plot in unused_plots:
        plot.set_xticks([])
        plot.set_yticks([])
    plt.tight_layout()

    # start placing puzzles one by one
    for i in range(len(puzzles_to_place)):
        plt.pause(pause)
        unused_show[i].set_data(np.zeros(drawed_puzzles[puzzles_to_place[0]].shape))
        puzzles_to_place.pop(0)
        in_progress = solved.copy()
        for number in puzzles_to_place:
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

    all_puzzles = read_all_puzzles_from_board(solved_board)
    placed = set(list(chain(*board_to_solve.tolist())))
    not_placed = [i for i in all_puzzles if i not in placed]
    drawed_puzzles = {i: draw_an_element(i, solved_board) for i in not_placed}
    puzzles_to_place = list(drawed_puzzles.values())

    # show first board
    colors = ['white', 'blue', 'yellow', 'green', 'orange', 'purple', 'pink',
               'brown', 'red', 'cyan', 'magenta', 'gray', 'lightgreen']
    width = 3
    height = ceil(len(puzzles_to_place)/2)
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(height, width, width_ratios=[2, 1, 1], height_ratios=[1]*height)
    main_plot = fig.add_subplot(gs[0, 0])
    unused_plots = [fig.add_subplot(gs[i, j]) for i in range(height) for j in range(1, width)]


    # show_solving(solve(board_to_solve, puzzles_to_place), drawed_puzzles, not_placed, pause)
    print(new_solve(board_to_solve, puzzles_to_place))
    print(datetime.now() - start)


if __name__ == "__main__":
    main()
