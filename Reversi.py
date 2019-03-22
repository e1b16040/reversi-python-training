from collections import defaultdict
from collections import deque
import copy

import Common
from ReversiBoard import Board

BOARD_SIZE = 64
BOARD_ROWS = 8
BLACK_PIECE = 'O'
WHITE_PIECE = 'X'
NONE_PIECE = ' '

class Reversi(object):
    """
    class of Reversi

    Attributes
    ------------
    black_player : function
        function of black player, call as follows
        row, col = self.black_player(black_board, white_board, is_black)
    white_player : function
        same as above
    """

    def __init__(self):
        self.board = Board()
        self.result = defaultdict(int)
        self.hist = deque()
    
    def set_player_color(self, color):
        self.player_is_black = color == 0
    
    def register_AI_for_pvc(self, black_player):
        self.black_player = black_player

    def register_AI_for_cvc(self, black_player, white_player):
        self.black_player = black_player
        self.white_player = white_player
    
    def reset_board(self):
        self.board.reset()
        self.hist = deque()

    def show_result(self):
        """
        Shows the result of the game
        """
        black_score, white_score = self.board.count_pieces()

        print("black vs white")
        print("{}, {}".format(black_score, white_score))
        self.result['game'] += 1
        if black_score > white_score:
            self.result['black_win'] += 1
            print("black win!")
        elif black_score < white_score:
            self.result['white_win'] += 1
            print("white win")
        else:
            self.result['draw'] += 1
            print("draw!")

    def show_statistic(self):
        for key, value in self.result.items():
            print(key + ": " + str(value))

    def go_back_step(self):
        if self.hist:
            self.board = self.hist.pop()

    def input_move(self):
        print("input 'row col' to put piece there")
        print("input 'p' to pass")
        print("input 'b' to go back one step")
        print("input 'q' to quit the game")
        while True:
            input_str = input("input: ")
            if input_str == 'p':
                return -1, -1
            if input_str == 'b':
                return -2, -2
            if input_str == 'q':
                return -3, -3
            try:
                row, col = tuple(map(int, input_str.split()))
                if row >= 0 and row < 8 and col >= 0 and col < 8:
                    return row, col
            except ValueError:
                pass
            print("input value is invalid, please input again")

    def pvp(self):
        while True:
            self.board.show_board()
            row, col = self.input_move()
            if row == -2 and col == -2:
                self.go_back_step()
                continue
            if row == -3 and col == -3:
                print('quit the game')
                break
            self.hist.append(copy.copy(self.board))
            self.board.put(row, col)
            if Common.is_game_finished(self.board.black_board, self.board.white_board):
                self.board.show_board()
                self.show_result()
                return
    
    def pvc(self):
        while True:
            if self.player_is_black:
                self.board.show_board()
                row, col = self.input_move()
                if row == -2 and col == -2:
                    self.go_back_step()
                    continue
                if row == -3 and col == -3:
                    print('quit the game')
                break
                self.hist.append(copy.copy(self.board))
                self.board.put(row, col)
                if Common.is_game_finished(self.board.black_board, self.board.white_board):
                    self.board.show_board()
                    self.show_result()
                    return
                self.board.show_board()
                row, col = self.black_player(self.board.white_board,
                    self.board.black_board)
                self.board.put(row, col)
                if Common.is_game_finished(self.board.black_board, self.board.white_board):
                    self.board.show_board()
                    self.show_result()
                    return
            else:
                self.board.show_board()
                row, col = self.black_player(self.board.black_board,
                    self.board.white_board)
                self.board.put(row, col)
                if Common.is_game_finished(self.board.black_board, self.board.white_board):
                    self.board.show_board()
                    self.show_result()
                    return
                self.board.show_board()
                row, col = self.input_move()
                if row == -2 and col == -2:
                    self.go_back_step()
                    continue
                if row == -3 and col == -3:
                    print('quit the game')
                break
                self.hist.append(copy.copy(self.board))
                self.board.put(row, col)
                if Common.is_game_finished(self.board.black_board, self.board.white_board):
                    self.board.show_board()
                    self.show_result()
                    return


    def cvc(self, show=True):
        while True:
            if show:
                self.board.show_board()
            if self.board.is_black:
                row, col = self.black_player(self.board.black_board, self.board.white_board)
            else:
                row, col = self.white_player(self.board.white_board, self.board.black_board)
            self.board.put(row, col)
            if Common.is_game_finished(self.board.black_board, self.board.white_board):
                self.board.show_board()
                self.show_result()
                return


def main():
    pass


if __name__ == '__main__':
    main()