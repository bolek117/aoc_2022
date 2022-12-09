import sys
from typing import List, Tuple

from helpers import header


class Move:
    def __init__(self, name: str, points: int, is_opponent: bool):
        self.move = name
        self.points = points
        self.is_opponent = is_opponent

    def __str__(self):
        player = 'op' if self.is_opponent else 'me'
        return f'{player}: {self.move} ({self.points})'

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
    in_file = 'input_day_02.txt' if len(sys.argv) == 1 else 'input_day_02_test.txt'

    with open(in_file, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    result = []
    for line in lines:
        me = map_move_sign_to_move(line[0])
        opponent = map_move_sign_to_move(line[2])
        result.append((me, opponent))

    return result


def get_score_for(op: Move, me: Move) -> int:
    r = 'rock'
    p = 'paper'
    s = 'scissors'

    win = 6
    draw = 3
    lost = 0

    symbol_points = -1
    result_points = -1
    if me.move == r:
        symbol_points = 1
        result_points = win if op.move == s else draw if op.move == r else lost

    if me.move == p:
        symbol_points = 2
        result_points = win if op.move == r else draw if op.move == p else lost

    if me.move == s:
        symbol_points = 3
        result_points = win if op.move == p else draw if op.move == s else lost

    return symbol_points + result_points


def main():
    header('strategy')
    strategy = get_strategy()
    total: int = 0
    for move in strategy:
        score = get_score_for(move[0], move[1])
        print(f'{move} = {score}')
        total += score

    print(f'Result: {total}')


if __name__ == '__main__':
    main()
