import re
import sys
from typing import List, Dict

from helpers import header


class Point:
    def __init__(self, x: int, y: int):
        self.x: int = int(x)
        self.y: int = int(y)

    @staticmethod
    def from_text(txt: str) -> 'Point':
        r = re.findall(r'at x=(-?[0-9]+), y=(-?[0-9]+)', txt, re.IGNORECASE)

        if len(r) > 0:
            point = Point(int(r[0][0]), int(r[0][1]))
            return point

        raise ValueError(f'Unable to find point description in `{txt}`')

    def pos(self) -> str:
        return f'({self.x},{self.y})'

    def __str__(self):
        return self.pos()

    def __repr__(self):
        return self.pos()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False

        return other.x == self.x and other.y == self.y

    def __hash__(self) -> int:
        x_str = f'{self.x:07d}'.replace('-', '9')
        y_str = f'{self.y:07d}'.replace('-', '9')
        combined = f'{x_str}{y_str}'

        return int(combined)


class Definition:
    def __init__(self, sensor: Point, closest_beacon: Point):
        self.sensor_pos = sensor
        self.beacon_pos = closest_beacon

    def __str__(self):
        return f'{str(self.sensor_pos)},{str(self.beacon_pos)}'

    def __repr__(self):
        return str(self)


def load_sensors(filename: str) -> List[Definition]:
    with open(filename, 'r') as f:
        lines = f.readlines()

    result: List[Definition] = []
    for line in lines:
        line = line.strip()
        parts = line.split(': ')

        sensor_pos = Point.from_text(parts[0])
        beacon_pos = Point.from_text(parts[1])

        sensor = Definition(sensor_pos, beacon_pos)
        result.append(sensor)

    return result


UNKNOWN: int = 0
SENSOR: int = 2
BEACON: int = 4
NO_BEACON: int = 8


def int_to_chr(val: int) -> str:
    return '.' if val == UNKNOWN else 'S' if val == SENSOR else 'B' if val == BEACON else '#'


class World:
    def __init__(self, sensors: List[Definition]):
        self.max: Point = Point(0, 0)
        self.min: Point = Point(0, 0)
        self.world: Dict[Point, int] = dict()

        self.fill(sensors)

    def as_list(self) -> List[List[Point | int]]:
        return [[k, v] for k, v in self.world.items()]

    def __str__(self):
        elements = self.as_list()
        result = ''.join(str(elements))
        return result

    def get_at(self, pos: Point) -> int:
        if pos.x > self.max.x or pos.x < self.min.x or pos.y < self.min.y or pos.y > self.max.y:
            return UNKNOWN

        if pos not in self.world.keys():
            return UNKNOWN

        return self.world[pos]

    def world_str(self) -> str:
        start_y, end_y = min(0, self.min.y), self.max.y
        start_x, end_x = min(0, self.min.x), self.max.x

        result = [f'   {self.min.x} -> {self.max.x}']
        for y in range(start_y, end_y):
            row = [f'{y:03d} ']

            for x in range(start_x, end_x):
                point = Point(x, y)
                value = self.get_at(point)
                letter = int_to_chr(value)

                row.append(letter)

            result.append(''.join(row))

        world_str = [f'{row}\n' for row in result]

        return ''.join(world_str)

    def dump(self) -> None:
        world_str = self.world_str()
        with open('day_15_output.txt', 'w') as f:
            f.write(world_str)

    def update_bounds(self, new_point: Point) -> None:

        max_x = max(new_point.x + 1, self.max.x)
        max_y = max(new_point.y + 1, self.max.y)

        min_x = min(new_point.x, self.min.x, 0)
        min_y = min(new_point.y, self.min.y, 0)

        self.max = Point(max_x, max_y)
        self.min = Point(min_x, min_y)

    def fill(self, sensors: List[Definition]) -> 'World':
        for s in sensors:
            self.world[s.sensor_pos] = SENSOR
            self.world[s.beacon_pos] = BEACON

            self.update_bounds(s.sensor_pos)
            self.update_bounds(s.beacon_pos)

        return self

    def fill_restrictions(self, definitions: List[Definition]) -> 'World':
        def d(p1: Point, p2: Point) -> int:
            dx = abs(p1.x - p2.x)
            dy = abs(p1.y - p2.y)

            return dx + dy

        for s in definitions:
            sensor_beacon_dist = d(s.sensor_pos, s.beacon_pos)
            min_pos = Point(s.sensor_pos.x - sensor_beacon_dist - 1, s.sensor_pos.y - sensor_beacon_dist - 1)
            max_pos = Point(s.sensor_pos.x + sensor_beacon_dist + 1, s.sensor_pos.y + sensor_beacon_dist + 1)

            self.update_bounds(min_pos)
            self.update_bounds(max_pos)

            for i in range(min_pos.y-1, max_pos.y+1):
                for j in range(min_pos.x-1, max_pos.x+1):
                    p = Point(j, i)
                    dist = d(s.sensor_pos, p) - 1
                    val_at = self.get_at(p)

                    if dist < sensor_beacon_dist and val_at == UNKNOWN:
                        self.world[p] = '#'
            pass

        return self


def day_15():
    is_test = len(sys.argv) > 1

    def log(txt) -> None:
        if is_test:
            print(txt)

    filename = f'input_day_15{"_" + sys.argv[1] if is_test else ""}.txt'
    sensors = load_sensors(filename)

    header('Filling world')
    world = World(sensors)
    log(world.world_str())

    header('Calculating restrictions')
    restricted_world = world.fill_restrictions(sensors)
    log(restricted_world.world_str())
    world.dump()
    pass


if __name__ == '__main__':
    day_15()
    