import sys
from typing import List

VAL_START = 0
VAL_END = ord('z')-ord('a')+2


class Pos:
    def __init__(self, x: int, y: int, height: int):
        self.x: int = x
        self.y: int = y
        self.height = height

    def __str__(self):
        return f'{self.x},{self.y}: {self.height}'

    def __repr__(self):
        return str(self)


def load_map() -> List[Pos]:
    test_suffix = '' if len(sys.argv) == 1 else '_test'
    filename = f'input_day_12{test_suffix}.txt'
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    result = []

    x = 0
    for line in lines:
        y = 0
        for c in line:
            if c.isupper():
                point = Pos(x, y, 0 if c == 'S' else VAL_END)
            else:
                point = Pos(x, y, ord(c)-ord('a')+1)

            result.append(point)
            y += 1

        x += 1

    return result


def find_value(map: List[Pos], value: int) -> List[Pos]:
    result = []
    for p in map:
        if p.height == value:
            result.append(p)

    return result


def get_height(character: str) -> int:
    return ord(character[0])-ord('a')+1


def main():
    map = load_map()
    pos_start = find_value(map, VAL_START)
    pos_end = find_value(map, VAL_END)

    pos_z = find_value(map, get_height('z'))
    pos_a = find_value(map, get_height('a'))
    pass


if __name__ == '__main__':
    main()
