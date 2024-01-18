"""Solves iq puzzle and prints only text version of solved board and a timer"""
from datetime import datetime
from itertools import chain
import argparse
import numpy as np

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


def solve(board_to_solve: np.ndarray, puzzles: [np.ndarray], current_puzzle: int) -> np.ndarray:
    """solves puzzle recursively"""
    if len(puzzles) == current_puzzle:
        return board_to_solve
    variants = get_all_variants(puzzles[current_puzzle])
    height, width = board_to_solve.shape
    for y in range(height):
        for x in range(width):
            for v in variants:
                temp = put_puzzle(board_to_solve, v, (y, x))
                if isinstance(temp, np.ndarray):
                    temp2 = solve(temp, puzzles, current_puzzle+1)
                    if isinstance(temp2, np.ndarray):
                        return temp2
    return False


def main():
    """Parsing arguments, solving and showing solving process"""
    parser = argparse.ArgumentParser(description='IQ puzzle solver')
    parser.add_argument('-p', '--solved', type=str,
                        help='Input directory to file with solved puzzle', default='plansza.txt')
    parser.add_argument('input_file', type=str, help='Input file with puzzle to solve')
    args = parser.parse_args()
    solved_file = args.solved
    file_to_solve = args.input_file

    solved_board = read_file(solved_file)
    board_to_solve = read_file(file_to_solve)

    all_puzzles = read_all_puzzles_from_board(solved_board)
    placed = set(list(chain(*board_to_solve.tolist())))
    not_placed = [i for i in all_puzzles if i not in placed]
    drawed_puzzles = {i: draw_an_element(i, solved_board) for i in not_placed}
    puzzles_to_place = list(drawed_puzzles.values())

    print(solve(board_to_solve, puzzles_to_place, 0))
    print(datetime.now()-start)


if __name__ == "__main__":
    main()
