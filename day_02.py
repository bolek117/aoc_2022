import sys
from typing import List, Tuple

from helpers import header

points_rock = 1
points_paper = 2
points_scissors = 3


class Move:
    def __init__(self, points: int, is_opponent: bool):
        self.move = 'rock' if points == 1 else 'paper' if points == 2 else 'scissors' if points == 3 else -1
        self.points = points
        self.is_opponent = is_opponent

    def __str__(self):
        player = 'op' if self.is_opponent else 'me'
        return f'{player}: {self.move} ({self.points})'

    def __repr__(self):
        return str(self)


def map_move_sign_to_move(move_sign: str) -> Move:
    move_sign = move_sign[0].lower()

    if move_sign in ['a', 'b', 'c']:
        sign_points = 1 if move_sign == 'a' else 2 if move_sign == 'b' else 3
        return Move(sign_points, True)

    return Move(-1, True)


def map_move_to_strategy(move_sign: str, op_move: Move) -> Move:
    move_sign = move_sign[0].lower()
    expected_move = ''
    if move_sign == 'x':  # loose
        expected_move = points_paper if op_move.points == points_scissors else \
            points_scissors if op_move.points == points_rock else \
            points_rock
    elif move_sign == 'y':  # draw
        expected_move = points_rock if op_move.points == points_rock else \
            points_scissors if op_move.points == points_scissors else \
            points_paper
    elif move_sign == 'z':  # win
        expected_move = points_rock if op_move.points == points_scissors else \
            points_scissors if op_move.points == points_paper else \
            points_paper

    return Move(expected_move, False)


def get_strategy() -> List[Tuple[Move, Move]]:
    in_file = 'input_day_02.txt' if len(sys.argv) == 1 else 'input_day_02_test.txt'

    with open(in_file, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    result = []
    for line in lines:
        opponent = map_move_sign_to_move(line[0])
        me = map_move_to_strategy(line[2], opponent)
        result.append((opponent, me))

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
