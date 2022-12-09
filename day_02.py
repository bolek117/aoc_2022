from typing import List, Tuple

from helpers import header


class Move:
    def __init__(self, name: str, points: int, is_opponent: bool):
        self.op_name = name
        self.points = points
        self.is_opponent = is_opponent

    def __str__(self):
        return f'{self.op_name} ({self.points} for {"me" if not self.is_opponent else "opponent"})'

    def __repr__(self):
        return str(self)


def map_move_sign_to_move(move_sign: str) -> Move:
    rock = ['A', 'X']
    paper = ['B', 'Y']
    scissors = ['C', 'Z']

    move_sign = move_sign[0].upper()
    if move_sign in rock:
        return Move('rock', 1, move_sign == 'A')
    elif move_sign in paper:
        return Move('paper', 2, move_sign == 'B')
    elif move_sign in scissors:
        return Move('scissors', 3, move_sign == 'C')

    return Move('UNKNOWN', -1, True)


def get_strategy() -> List[Tuple[Move, Move]]:
    with open('input_day_02.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    result = []
    for l in lines:
        me = map_move_sign_to_move(l[0])
        opponent = map_move_sign_to_move(l[2])
        result.append((me, opponent))

    return result


def get_score_for(me: Move, opponent: Move) -> int:
    r = 'rock'
    p = 'paper'
    s = 'scissors'

    win = 6
    draw = 3
    lost = 0

    symbol_points = -1
    result_points = -1
    if me.op_name == r:
        symbol_points = 1
        result_points = win if opponent.op_name == s else draw if opponent.op_name == r else lost

    if me.op_name == p:
        symbol_points = 2
        result_points = win if opponent.op_name == r else draw if opponent.op_name == p else lost

    if me.op_name == s:
        symbol_points = 3
        result_points = win if opponent.op_name == p else draw if opponent.op_name == s else lost

    return symbol_points + result_points


def main():
    header('strategy')
    strategy = get_strategy()
    for move in strategy:
        score = get_score_for(move[0], move[1])
        print(f'{move} = {score}')


if __name__ == '__main__':
    main()
