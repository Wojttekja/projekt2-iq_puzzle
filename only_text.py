"""Solves iq puzzle and prints only text version of solved board and a timer"""
from datetime import datetime
from itertools import chain
import argparse
import numpy as np
from main import read_file, read_all_puzzles_from_board
from main import draw_an_element, put_puzzle, get_all_variants

start = datetime.now()

def solve_without_showing(board_to_solve: np.ndarray,
                          puzzles: [np.ndarray], current_puzzle: int) -> np.ndarray:
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
                    temp2 = solve_without_showing(temp, puzzles, current_puzzle+1)
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

    print(solve_without_showing(board_to_solve, puzzles_to_place, 0))
    print(datetime.now()-start)


if __name__ == "__main__":
    main()
