"""Projekt WDI IQ puzzle - Wojciech Mierzejek <nrindeksu>"""
from math import ceil
from itertools import chain
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
from matplotlib.colors import ListedColormap

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

def draw_element(element: int, board: np.ndarray) -> np.ndarray:
    """Draws a small numpy array including only specified puzzle"""
    row_indexes, column_indexes = np.where(board == element)
    drawed = np.zeros((max(row_indexes)-min(row_indexes)+1,
                       max(column_indexes)-min(column_indexes)+1))
    row_shift, col_shift = min(row_indexes), min(column_indexes)
    for row, column in zip(row_indexes, column_indexes):
        drawed[row-row_shift, column-col_shift] = element
    return drawed

def put_puzzle(board: np.ndarray, puzzle: np.ndarray, place: (int, int)) -> bool or np.ndarray:
    """Places a puzzle into board on specified location or return False if it doesn't fit"""
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
    """Returns list of variants of given puzzle, variants meaning rotated or fliped puzzle"""
    all_varaints = [puzzle]
    listed_variants = [puzzle.tolist()]
    for k in (-1, 1, 2):
        temp = np.rot90(puzzle, k=k)
        listed_temp = temp.tolist()
        if listed_temp not in listed_variants:
            listed_variants.append(listed_temp)
            all_varaints.append(temp)

    fliped = np.flip(puzzle, 0)
    for k in (-1, 0, 1, 2):
        temp = np.rot90(fliped, k=k)
        listed_temp = temp.tolist()
        if listed_temp not in listed_variants:
            listed_variants.append(listed_temp)
            all_varaints.append(temp)

    return all_varaints

def solve(board_to_solve: np.ndarray, puzzles: [[np.ndarray]], current_puzzle: int,
          pause: float, main_show: AxesImage, unused_show: [AxesImage]) -> np.ndarray:
    """Solves puzzle recursively"""
    main_show.set_data(board_to_solve)
    for puzzle, plot, i in zip(puzzles, unused_show, range(len(puzzles))):
        if i < current_puzzle:
            plot.set_data(np.zeros(puzzle[0].shape))
        else:
            plot.set_data(puzzle[0])
    plt.pause(pause)

    if len(puzzles) == current_puzzle:
        return board_to_solve
    height, width = board_to_solve.shape
    for y in range(height):
        for x in range(width):
            for v in puzzles[current_puzzle]:
                temp = put_puzzle(board_to_solve, v, (y, x))
                if isinstance(temp, np.ndarray):
                    temp2 = solve(temp, puzzles, current_puzzle+1, pause, main_show, unused_show)
                    if isinstance(temp2, np.ndarray):
                        return temp2
    return False

def start_showing(main_board: np.ndarray, puzzles: {int: np.ndarray}) -> (AxesImage, [AxesImage]):
    """Initializes a window and shows first board and puzzles to place"""
    colors = ['white', 'blue', 'yellow', 'green', 'orange', 'purple', 'pink',
               'brown', 'red', 'cyan', 'magenta', 'gray', 'lightgreen']
    puzzles_to_place = list(puzzles.values())
    width = 3
    height = ceil(len(puzzles_to_place)/2)
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(height, width, width_ratios=[2, 1, 1], height_ratios=[1]*height)
    main_plot = fig.add_subplot(gs[0, 0])
    unused_plots = [fig.add_subplot(gs[i, j]) for i in range(height) for j in range(1, width)]
    main_show = main_plot.imshow(main_board, cmap=ListedColormap(colors))
    main_plot.set_title("Układana plansza")
    main_plot.set_xticks([])
    main_plot.set_yticks([])
    unused_show = []
    for puzzle, plot in zip(puzzles.keys(), unused_plots):
        unused_show.append(plot.imshow(puzzles[puzzle],
                                       cmap=ListedColormap([colors[0]]+[colors[puzzle]])))
    for plot in unused_plots:
        plot.set_xticks([])
        plot.set_yticks([])
    plt.tight_layout()

    return main_show, unused_show

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
    drawed_puzzles = {i: draw_element(i, solved_board) for i in not_placed}

    # show first board
    main_show, unused_show = start_showing(board_to_solve, drawed_puzzles)
    solve(board_to_solve, [get_all_variants(i) for i in drawed_puzzles.values()],
          0, pause, main_show, unused_show)

    plt.show()


if __name__ == "__main__":
    main()
