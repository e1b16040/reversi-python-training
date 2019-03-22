import MyDeco
from Reversi import Reversi
import AI

@MyDeco.time_record
@MyDeco.func_info
def main():
    selected_mode = select_mode()

    if selected_mode == 0:
        pvp()
    elif selected_mode == 1:
        pvc()
    elif selected_mode == 2:
        cvc()

def y_or_n():
    while True:
        try:
            yorn = input('input y/n: ')
            if yorn == 'y' or yorn == 'Y':
                return True
            elif yorn == 'n' or yorn == 'N':
                return False
        except ValueError:
            print('input value is invalid, please input again')


def input_times():
    while True:
        try:
            times = int(input('input times: '))
            if times >= 0:
                return times
        except ValueError:
            print('input value is invalid, please input again')


def select(choices_num):
    while True:
        try:
            selected = int(input('enter the corresponding number: '))
            if selected in range(choices_num):
                return selected
            print('input value is invalid, please input again')
        except ValueError:
            print('input value is invalid, please input again')


def select_mode():
    print('this reversi has 3 modes, PvP, PvC, CvC')
    print('please select mode')
    print('PvP: 0, PvC: 1, CvC: 2')
    return select(3)


def select_AI():
    print('please select AI')
    print('all random: 0, random and full search: 1, nega alpha: 2')
    return select(3)


def select_color():
    print('select your color')
    print('black: 0, white: 1')
    return select(2)


def pvp():
    reversi = Reversi()
    reversi.pvp()


AI_list = [AI.put_randomly, AI.random_full_search, AI.nega_alpha]


def pvc():
    print('select cpu AI')
    black = select_AI()
    player_color = select_color()
    reversi = Reversi()
    reversi.set_player_color(player_color)
    reversi.register_AI_for_pvc(AI_list[black])
    reversi.pvc()


def cvc():
    print('black players cpu')
    black = select_AI()
    print('white players cpu')
    white = select_AI()
    print('how many times will you play?')
    times = input_times()
    print('do you want to display the board in the middle?')
    is_show = y_or_n()
    reversi = Reversi()
    reversi.register_AI_for_cvc(AI_list[black], AI_list[white])
    for _ in range(times):
        reversi.cvc(show=is_show)
        reversi.reset_board()
    print()
    reversi.show_statistic()


if __name__ == '__main__':
    main()