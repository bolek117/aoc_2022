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
        return int(f'{self.x:07d}{self.y:07d}')


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
        if pos not in self.world.keys():
            return UNKNOWN

        return self.world[pos]

    def world_str(self) -> str:
        result = []
        for y in range(min(0, self.min.y), self.max.y):
            row = []

            for x in range(min(0, self.min.x), self.max.x):
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
            for row in world_str():
                f.write(row)

    def fill(self, sensors: List[Definition]) -> 'World':
        def update_bounds(new_point: Point):
            self.max = Point(max(new_point.x, self.max.x), max(new_point.y, self.max.y))
            self.min = Point(min(new_point.x, self.min.x, 0), min(new_point.y, self.min.y, 0))

        for s in sensors:
            self.world[s.sensor_pos] = SENSOR
            self.world[s.beacon_pos] = BEACON

            update_bounds(s.sensor_pos)
            update_bounds(s.beacon_pos)

        if self.max.x < 50:
            print(self.world_str())

        return self

    def fill_restrictions(self, definitions: List[Definition]) -> 'World':
        for s in definitions:
            dist_x = abs(s.sensor_pos.x - s.beacon_pos.x)
            dist_y = abs(s.sensor_pos.y - s.beacon_pos.y)

            dist = dist_x + dist_y
            min_x = s.sensor_pos.x - dist
            max_x = s.sensor_pos.x + dist

            min_y = s.sensor_pos.y - dist
            max_y = s.sensor_pos.y + dist


            pass

        return self


def prepare_empty_world(sensors: List[Definition]) -> World:
    x_set = set()
    y_set = set()

    for s in sensors:
        x_set.add(s.sensor_pos.x)
        x_set.add(s.beacon_pos.x)

        y_set.add(s.sensor_pos.y)
        y_set.add(s.beacon_pos.y)

    min_x = min(x_set)
    max_x = max(x_set)+1

    min_y = min(y_set)
    max_y = max(y_set)+1

    width = max_x - min_x
    height = max_y - min_y

    result = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(UNKNOWN)

        result.append(row)

    world = World(result, min_x, min_y, max_x, max_y)
    return world


def day_15():
    debug = False

    def log(txt) -> None:
        if debug:
            print(txt)

    filename = f'input_day_15{"_" + sys.argv[1] if len(sys.argv) > 1 else ""}.txt'
    sensors = load_sensors(filename)

    header('Filling world')
    world = World(sensors)
    log(world.world_str())

    header('Calculating restrictions')
    restricted_world = world.fill_restrictions(sensors)
    pass


if __name__ == '__main__':
    day_15()
    