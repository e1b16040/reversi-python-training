from enum import Enum, auto
import random
import sys

import Common

BOARD_SIZE = 64
BOARD_ROWS = 8

def put_randomly(black, white):
    """
    put a piece at random

    Parameters
    ------------
    black : Uint64
        Bitboard of current turn player
    white : Uint64
        Bitboard of next turn player

    Returns
    ------------
    Tuple (row:int, col:int)
        If pass, returns (-1, -1)
    """

    valid_moves = Common.get_valid_moves(black, white)
    if valid_moves == 0:
        return (-1, -1)

    valid_moves_indexes = []
    mask = 0x8000000000000000
    for i in range(BOARD_SIZE):
        if (mask & valid_moves) != 0:
            valid_moves_indexes.append(i)
        mask = mask >> 1
    
    random_move = random.choice(valid_moves_indexes)
    return (random_move % BOARD_ROWS, random_move // BOARD_ROWS)



class Result(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()

def _full_search(black, white):
    """
    Recursive function
    Full search and get better moves
    When first called, black is turn player and white is opposing player, 
    but black and white are assigned alternately each time called

    Parameters
    ------------
    black : Uint64
        Bitboard of black
    white : Uint64
        Bitboard of white
    
    Returns
    ------------
    int
        1: Black player can win
        0: draw
        -1: cannot win
    int, int
        Row, Column
        If passing, returns -1, -1
        If game is end, returns -2, -2
    """

    black_valid_moves = Common.get_valid_moves(black, white)

    # if game is finished, returns result
    if Common.is_game_finished(black, white):
        black_score = Common.count_pieces(black)
        white_score = Common.count_pieces(white)
        if black_score > white_score:
            return Result.WIN, -2, -2
        elif black_score < white_score:
            return Result.LOSE, -2, -2
        else:
            return Result.DRAW, -2, -2

    # full search
    moves = {}
    mask = 0x8000000000000000
    for i in range(BOARD_SIZE):
        move = mask & black_valid_moves
        if move != 0:
            rev = Common.get_reverse_pattern(black, white, move)
            result, _, _ = _full_search(white ^ rev, black ^ move | rev)
            moves[i] = result
        mask = mask >> 1

    # When passing
    if not moves:
        opposing_win, _, _ = _full_search(white, black)
        if opposing_win == Result.WIN:
            return Result.LOSE, -1, -1
        elif opposing_win == Result.LOSE:
            return Result.WIN, -1, -1
        else:
            return Result.DRAW, -1, -1

    for move, opposing_win in moves.items():
        if opposing_win == Result.LOSE:
            return Result.WIN, move % BOARD_ROWS, move // BOARD_ROWS

    move = random.choice(list(moves.keys()))
    return Result.LOSE, move % BOARD_ROWS, move // BOARD_ROWS


def random_full_search(black, white):
    pieces = black | white
    piece_num = Common.count_pieces(pieces)

    if piece_num < 55:
        return put_randomly(black, white)
    else:
        result, row, col = _full_search(black, white)
        if result == Result.WIN:
            print('can win')
        elif result == Result.LOSE:
            print('cannot win')
        else:
            print('draw')
        return row, col


def input_from_console(black, white):
    while True:
        input_str = input("input [row col]: ")
        try:
            row, col = tuple(map(int, input_str.split()))
            if row == -1 and col == -1:
                return row, col
            if row >= 0 and row < 8 and col >= 0 and col < 8:
                return row, col
            print("input value is invalid, please input again")
        except ValueError:
            print("input value is invalid, please input again")


EVAL_LIST = [ 45, -11,  4, -1, -1,  4, -11,  45,
             -11, -16, -1, -3, -3, -1, -16, -11,
               4,  -1,  2, -1, -1,  2,  -1,   4,
              -1,  -3, -1,  0,  0, -1,  -3,  -1,
              -1,  -3, -1,  0,  0, -1,  -3,  -1,
               4,  -1,  2, -1, -1,  2,  -1,   4,
             -11, -16, -1, -3, -3, -1, -16, -11,
              45, -11,  4, -1, -1,  4, -11,  45]

def _evaluate(board):
    score = 0
    mask = 0x8000000000000000
    for i in range(BOARD_SIZE):
        if (mask & board) != 0:
            score += EVAL_LIST[i]
        mask = mask >> 1
    return score


def evaluate(black, white):
    black_score = _evaluate(black)
    white_score = _evaluate(white)
    return black_score - white_score

FLOAT_MAX = sys.float_info.max

def _nega_alpha(black, white, depth=3, alpha=-FLOAT_MAX, beta=FLOAT_MAX):
    # Common.show_board(black, white)
    if Common.is_game_finished(black, white):
        black_score = Common.count_pieces(black)
        white_score = Common.count_pieces(white)
        if black_score > white_score:
            return 1, -2, -2
        elif black_score < white_score:
            return -1, -2, -2
        else:
            return 0, -2, -2

    if depth == 0:
        return evaluate(black, white), -2, -2
    
    moves = Common.get_valid_moves(black, white)
    # Common.show_board(moves, 0)
    better_move = -1
    mask = 0x8000000000000000
    for i in range(BOARD_SIZE):
        move = mask & moves
        if move != 0:
            rev = Common.get_reverse_pattern(black, white, move)
            # Common.show_board(rev, 0)
            tmp_alpha, _, _ = _nega_alpha(white ^ rev, black ^ move | rev, depth-1, -beta, -alpha)
            tmp_alpha = -tmp_alpha

            if tmp_alpha > alpha:
                alpha = tmp_alpha
                better_move = i

            if alpha >= beta:
                return alpha, i % BOARD_ROWS, i // BOARD_ROWS
        mask = mask >> 1
    
    if better_move != -1:
        return alpha, better_move % BOARD_ROWS, better_move // BOARD_ROWS
    return alpha, -1, -1


def nega_alpha(black, white):
    _, row, col = _nega_alpha(black, white, depth=5)
    return row, col


if __name__ == '__main__':
    black = 0x9ff3ff8f8fa7d3ff
    white = 0x000c007070582c00
    result = nega_alpha(white, black)
    print(result)


