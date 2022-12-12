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
        return f'{self.x}:{self.y}=({self.height})'

    def __repr__(self):
        return str(self)


def load_map() -> (List[List[Pos]]):
    test_suffix = '' if len(sys.argv) == 1 else '_test'
    filename = f'input_day_12{test_suffix}.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    result = []

    x = 0
    y = 0
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


def find_value(map: List[List[Pos]], value: int) -> List[Pos]:
    result = []
    for row in map:
        for p in row:
            if p.height == value:
                result.append(p)

    return result


def get_height(character: str) -> int:
    return ord(character[0])-ord('a')+1


class Cluster:
    def __init__(self, cluster: List[Pos]):
        self.e = cluster

    def __str__(self):
        r1 = self.e[0:2]
        r2 = self.e[3:5]
        r3 = self.e[6:8]

        def row_str(row: List[Pos]):
            return ', '.join([str(i) for i in row])

        return f'{row_str(r1)}; {row_str(r2)}; {row_str(r3)}'

    def __repr__(self):
        return str(self)


def make_clusters(map: List[List[Pos]]) -> List[Cluster]:
    rows = len(map)
    columns = len(map[0])


    result = []
    for i in range(rows):
        for j in range(columns):
            base = map[i][j]

            def val(x, y) -> Pos:
                if x < 0 or x >= rows or y < 0 or y >= columns:
                    return Pos(x, y, -100)

                r = map[x][y]
                return Pos(x, y, base.height - r.height)

            cluster = [
                val(i-1, j-1), val(i-1, j), val(i-1, j+1),
                val(i, j-1), base, val(i, j+1),
                val(i+1, j-1), val(i+1, j), val(i+1, j+1),
            ]

            result.append(Cluster(cluster))

    return result


def main():
    map = load_map()
    pos_start = find_value(map, VAL_START)
    pos_end = find_value(map, VAL_END)

    pos_z = find_value(map, get_height('z'))
    pos_a = find_value(map, get_height('a'))

    clusters = make_clusters(map)
    pass


if __name__ == '__main__':
    main()
