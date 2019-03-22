import Common

BOARD_SIZE = 64
BOARD_ROWS = 8

class Board(object):
    """
    class of Reversi Board

    Attributes
    ------------
    black_board : Uint64
        first turn bitboard
    white_board : Uint64
        second turn bitboard
    is_black : boolean
        current turn: true is black, false is white
    elapsed_turn : int
        number of elapsed turns, start with 1
    """

    def __init__(self):
        self.black_board = 0x0000000810000000
        self.white_board = 0x0000001008000000
        self.is_black = True
        self.elapsed_turn = 1
    
    def reset(self):
        self.black_board = 0x0000000810000000
        self.white_board = 0x0000001008000000
        self.is_black = True
        self.elapsed_turn = 1

    def forward_turn(self):
        self.is_black = not self.is_black
        self.elapsed_turn += 1

    def put(self, row, col):
        """
        put a piece of current turn

        Parameters
        ------------
        col : int
            how many rows to put a piece from the left 0 <= col < 8
        row : int
            how many column to put a piece from the top 0 <= row < 8
        """

        if row == -1 and col == -1:
            self.forward_turn()
            print("pass")
            return True

        assert row >= 0 and row < 8 and col >= 0 and col < 8,'func: put, a value outside the range was entered'

        move = 0x8000000000000000
        move = move >> (row + col * 8)

        if self.is_black:
            rev = Common.get_reverse_pattern(self.black_board,
                self.white_board, move)
            if not rev:
                return False
            self.black_board ^= move | rev
            self.white_board ^= rev
        else:
            rev = Common.get_reverse_pattern(self.white_board,
                self.black_board, move)
            if not rev:
                return False
            self.white_board ^= move | rev
            self.black_board ^= rev

        self.forward_turn()
        return True

    def show_board(self):
        """
        show the board to stdout
        """
        if self.is_black:
            print("Turn: BLACK")
        else:
            print("Turn: WHITE")
        Common.show_board(self.black_board, self.white_board)

    def count_pieces(self):
        return Common.count_pieces(self.black_board), Common.count_pieces(self.white_board)

    def get_board_list(self):
        if self.is_black:
            return Common.convert_bit_to_list(self.black_board, self.white_board)
        else:
            return Common.convert_bit_to_list(self.white_board, self.black_board)


def main():
    pass


if __name__ == '__main__':
    main()