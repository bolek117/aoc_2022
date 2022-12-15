import math
import sys
from typing import List, Tuple

import astar

VAL_START = 0
VAL_END = ord('z')-ord('a')+2


class Pos:
    def __init__(self, x: int, y: int, height: int):
        self.x: int = x
        self.y: int = y
        self.height = height

    def __str__(self):
        return f'{self.x}:{self.y}=({self.height})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Pos):
            return False

        return self.x == other.x and self.y == other.y

    def __hash__(self):
        s = f'{self.x:03d}{self.y:03d}'
        h = int(s)
        return h


def load_map() -> (List[List[Pos]]):
    test_suffix = '' if len(sys.argv) == 1 else '_' + sys.argv[1]
    filename = f'input_day_12{test_suffix}.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    result = []

    x = 0
    for line in lines:
        y = 0
        row = []
        for c in line:
            if c.isupper():
                point = Pos(x, y, 0 if c == 'S' else VAL_END)
            else:
                point = Pos(x, y, ord(c)-ord('a')+1)

            row.append(point)
            y += 1

        result.append(row)
        x += 1

    return result


def find_value(world_map: List[List[Pos]], value: int) -> List[Pos]:
    result = []
    for row in world_map:
        for p in row:
            if p.height == value:
                result.append(p)

    return result


class AstarImpl(astar.AStar):
    def __init__(self, map: List[List[Pos]]):
        self.map: List[List[Pos]] = map

    def heuristic_cost_estimate(self, current: Pos, goal: Pos) -> float:
        x_diff = abs(goal.x - current.x)
        y_diff = abs(goal.y - current.x)

        dist_square = math.pow(x_diff, 2) + math.pow(y_diff, 2)
        dist = math.sqrt(dist_square)

        return dist * 2

    def distance_between(self, n1: Pos, n2: Pos) -> float:
        diff = n2.height - n1.height
        if diff <= 1:
            return 1

        return 1e9999999

    def neighbors(self, node: Pos) -> List[Pos]:
        x, y = node.x, node.y
        result = []

        def is_valid_pos(row: int, column: int) -> bool:
            return 0 <= row < len(self.map) and 0 <= column < len(self.map[0])

        if is_valid_pos(x-1, y):
            result.append(self.map[x-1][y])

        if is_valid_pos(x+1, y):
            result.append(self.map[x+1][y])

        if is_valid_pos(x, y-1):
            result.append(self.map[x][y-1])

        if is_valid_pos(x, y+1):
            result.append(self.map[x][y+1])

        return result

    def is_goal_reached(self, current: Pos, goal: Pos) -> bool:
        return current.x == goal.x and current.y == goal.y


def save_route(route: List[Pos], world: List[List[Pos]]):
    rows, columns = len(world), len(world[0])
    result = [[' ' for _ in range(columns)] for _ in range(rows)]

    for p in route:
        result[p.x][p.y] = chr(world[p.x][p.y].height + ord('a')-1)

    txt = []
    for r in result:
        line = ''.join([str(s) for s in r])
        txt.append(line)

    lines = '\n'.join(txt)
    with open('day_12_output.txt', 'w') as f:
        f.write(lines)


def main():
    world_map = load_map()
    pos_start = find_value(world_map, VAL_START)[0]
    pos_end = find_value(world_map, VAL_END)[0]

    finder = AstarImpl(world_map)
    route = finder.astar(pos_start, pos_end)

    route = list(route)
    i = 0
    for p in route:
        print(i, p)
        i += 1

    steps = len(route) - 1
    print(f'Steps: {steps}')

    save_route(route, world_map)
    pass


if __name__ == '__main__':
    main()
