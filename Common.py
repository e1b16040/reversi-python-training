def get_valid_moves(black, white):
    """
    get valid moves bitboard

    Parameters
    ------------
    black : Uint64
        own bitboard
    white : Uint64
        opponent player's bitboard
    Returns
    -----------
    Uint64
        valid moves bitboard
    """
    valid = 0
    blank = ~(black | white)

    horizontal_masked_white = white & 0x7e7e7e7e7e7e7e7e
    vertical_masked_white = white & 0x00ffffffffffff00
    all_masked_white = white & 0x007e7e7e7e7e7e00

    #top
    tmp = vertical_masked_white & (black >> 8)
    tmp |= vertical_masked_white & (tmp >> 8)
    tmp |= vertical_masked_white & (tmp >> 8)
    tmp |= vertical_masked_white & (tmp >> 8)
    tmp |= vertical_masked_white & (tmp >> 8)
    tmp |= vertical_masked_white & (tmp >> 8)
    valid |= blank & (tmp >> 8)

    #top-right
    tmp = all_masked_white & (black >> 7)
    tmp |= all_masked_white & (tmp >> 7)
    tmp |= all_masked_white & (tmp >> 7)
    tmp |= all_masked_white & (tmp >> 7)
    tmp |= all_masked_white & (tmp >> 7)
    tmp |= all_masked_white & (tmp >> 7)
    valid |= blank & (tmp >> 7)

    #right
    tmp = horizontal_masked_white & (black << 1)
    tmp |= horizontal_masked_white & (tmp << 1)
    tmp |= horizontal_masked_white & (tmp << 1)
    tmp |= horizontal_masked_white & (tmp << 1)
    tmp |= horizontal_masked_white & (tmp << 1)
    tmp |= horizontal_masked_white & (tmp << 1)
    valid |= blank & (tmp << 1)

    #bottom-right
    tmp = all_masked_white & (black << 9)
    tmp |= all_masked_white & (tmp << 9)
    tmp |= all_masked_white & (tmp << 9)
    tmp |= all_masked_white & (tmp << 9)
    tmp |= all_masked_white & (tmp << 9)
    tmp |= all_masked_white & (tmp << 9)
    valid |= blank & (tmp << 9)

    #bottom
    tmp = vertical_masked_white & (black << 8)
    tmp |= vertical_masked_white & (tmp << 8)
    tmp |= vertical_masked_white & (tmp << 8)
    tmp |= vertical_masked_white & (tmp << 8)
    tmp |= vertical_masked_white & (tmp << 8)
    tmp |= vertical_masked_white & (tmp << 8)
    valid |= blank & (tmp << 8)

    #bottom-left
    tmp = all_masked_white & (black << 7)
    tmp |= all_masked_white & (tmp << 7)
    tmp |= all_masked_white & (tmp << 7)
    tmp |= all_masked_white & (tmp << 7)
    tmp |= all_masked_white & (tmp << 7)
    tmp |= all_masked_white & (tmp << 7)
    valid |= blank & (tmp << 7)

    #left
    tmp = horizontal_masked_white & (black >> 1)
    tmp |= horizontal_masked_white & (tmp >> 1)
    tmp |= horizontal_masked_white & (tmp >> 1)
    tmp |= horizontal_masked_white & (tmp >> 1)
    tmp |= horizontal_masked_white & (tmp >> 1)
    tmp |= horizontal_masked_white & (tmp >> 1)
    valid |= blank & (tmp >> 1)
    
    #top-left
    tmp = all_masked_white & (black >> 9)
    tmp |= all_masked_white & (tmp >> 9)
    tmp |= all_masked_white & (tmp >> 9)
    tmp |= all_masked_white & (tmp >> 9)
    tmp |= all_masked_white & (tmp >> 9)
    tmp |= all_masked_white & (tmp >> 9)
    valid |= blank & (tmp >> 9)
    
    return valid


def get_reverse_pattern(black, white, move):
    """

    Parameters
    ------------
    black : Uint64
        own bitboard
    white : Uint64
        opponent player's bitboard
    move : Uint64
        bitboard of the move
    
    Returns
    ------------
    Uint64
        bitboard of inside out piece
    """

    if ((black | white) & move) != 0:
        return

    rev = 0
    
    #top
    tmp_rev = 0
    mask = move << 8
    while (mask != 0 and (mask & white) != 0):
        tmp_rev |= mask
        mask = mask << 8
    if (mask & black) != 0:
        rev |= tmp_rev
    
    #top-right
    tmp_rev = 0
    mask = move << 7 & 0x7f7f7f7f7f7f7f7f
    while mask != 0 and (mask & white) != 0:
        tmp_rev |= mask
        mask = mask << 7 & 0x7f7f7f7f7f7f7f7f
    if (mask & black) != 0:
        rev |= tmp_rev

    #right
    tmp_rev = 0
    mask = move >> 1 & 0x7f7f7f7f7f7f7f7f
    while mask != 0 and (mask & white) != 0:
        tmp_rev |= mask
        mask = mask >> 1 & 0x7f7f7f7f7f7f7f7f
    if (mask & black) != 0:
        rev |= tmp_rev

    #bottom-right
    tmp_rev = 0
    mask = move >> 9 & 0x7f7f7f7f7f7f7f7f
    while mask != 0 and (mask & white) != 0:
        tmp_rev |= mask
        mask = mask >> 9 & 0x7f7f7f7f7f7f7f7f
    if (mask & black) != 0:
        rev |= tmp_rev

    #bottom
    tmp_rev = 0
    mask = move >> 8
    while mask != 0 and (mask & white) != 0:
        tmp_rev |= mask
        mask = mask >> 8
    if (mask & black) != 0:
        rev |= tmp_rev

    #bottom-left
    tmp_rev = 0
    mask = move >> 7 & 0xfefefefefefefefe
    while mask != 0 and (mask & white) != 0:
        tmp_rev |= mask
        mask = mask >> 7 & 0xfefefefefefefefe
    if (mask & black) != 0:
        rev |= tmp_rev

    #left
    tmp_rev = 0
    mask = move << 1 & 0xfefefefefefefefe
    while (mask != 0 and (mask & white) != 0):
        tmp_rev |= mask
        mask = mask << 1 & 0xfefefefefefefefe
    if (mask & black) != 0:
        rev |= tmp_rev

    #top-left
    tmp_rev = 0
    mask = move << 9 & 0xfefefefefefefefe
    while (mask != 0 and (mask & white) != 0):
        tmp_rev |= mask
        mask = mask << 9 & 0xfefefefefefefefe
    if (mask & black) != 0:
        rev |= tmp_rev

    return rev


def count_pieces(board):
    """
    get the number of pieces

    Returns
    ------------
    int
        the number of pieces
    """

    board = board - ((board >> 1) & 0x5555555555555555)
    board = (board & 0x3333333333333333) + ((board >> 2) & 0x3333333333333333)
    board = (board + (board >> 4)) & 0x0f0f0f0f0f0f0f0f
    board = board + (board >> 8)
    board = board + (board >> 16)
    board = board + (board >> 32)
    return board & 0x000000000000007f



def is_game_finished(black, white):
    """
    it is judged whether the game is over

    Returns
    ------------
    boolean
        finished: True, continue: False
    """

    black_valid_moves = get_valid_moves(black, white)
    white_valid_moves = get_valid_moves(white, black)

    if (black_valid_moves == 0 and
        white_valid_moves == 0):
        return True
    else:
        return False


def convert_list_to_bit(board=None):
    if not board:
        return 0
    
    assert len(board) == 64, 'func: convert_list_to_bit, boardのサイズが不正です'

    black = 0x0000000000000000
    white = 0x0000000000000000
    mask = 0x8000000000000000

    for piece in board:
        if piece == 1:
            black = black ^ mask
        if piece == 2:
            white = white ^ mask
        mask = mask >> 1
    
    return black, white



def convert_bit_to_list(black, white):
    list_board = []
    mask = 0x8000000000000000
    for shift in range(64):
        tmp_mask = mask >> shift
        if (black & tmp_mask) != 0:
            list_board.append(1)
        elif (white & tmp_mask) != 0:
            list_board.append(2)
        else:
            list_board.append(0)
    return list_board


BLACK_PIECE = 'O'
WHITE_PIECE = 'X'
NONE_PIECE = ' '


def convert_bit_to_show_list(black, white):
    list_board = []
    mask = 0x8000000000000000
    for shift in range(64):
        tmp_mask = mask >> shift
        if shift % 8 == 0:
            list_line = []
            list_board.append(list_line)
        if (black & tmp_mask) != 0:
            list_line.append(BLACK_PIECE)
        elif (white & tmp_mask) != 0:
            list_line.append(WHITE_PIECE)
        else:
            list_line.append(NONE_PIECE)
    
    return list_board


def show_board(black, white):
    black_count = count_pieces(black)
    white_count = count_pieces(white)
    print("black: {} white: {}".format(
        black_count, white_count
    ))
    print("=" * 18)
    print("  0 1 2 3 4 5 6 7")
    list_board = convert_bit_to_show_list(black, white)
    for i, line in enumerate(list_board):
        print(i, end=' ')
        str_line = " ".join(line)
        print(str_line)
    print("=" * 18)
    print()

if __name__ == '__main__':
    reversi_list = convert_bit_to_list(0x0000000810000000, 0x0000001008000000)
    for i, x in enumerate(reversi_list):
        if i % 8 == 0:
            print()
        print(x, end='')
    print()
    black, white = convert_list_to_bit(reversi_list)
    reversi_list = convert_bit_to_list(black, white)
    for i, x in enumerate(reversi_list):
        if i % 8 == 0:
            print()
        print(x, end='')
