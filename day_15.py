import re
import sys
from typing import List

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

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return str(self)


class Sensor:
    def __init__(self, sensor: Point, closest_beacon: Point):
        self.sensor = sensor
        self.beacon = closest_beacon

    def __str__(self):
        return f'S:{str(self.sensor)},B:{str(self.beacon)}'

    def __repr__(self):
        return str(self)


def load_sensors(filename: str) -> List[Sensor]:
    with open(filename, 'r') as f:
        lines = f.readlines()

    result: List[Sensor] = []
    for line in lines:
        line = line.strip()
        parts = line.split(': ')

        sensor_pos = Point.from_text(parts[0])
        beacon_pos = Point.from_text(parts[1])

        sensor = Sensor(sensor_pos, beacon_pos)
        result.append(sensor)

    return result


UNKNOWN: int = 0
SENSOR: int = 2
BEACON: int = 4
NO_BEACON: int = 8


class World:
    def __init__(self, world: List[List[int]], min_x: int, min_y: int, max_x: int, max_y: int):
        self.max_y: int = max_y
        self.max_x: int = max_x
        self.min_y: int = min_y
        self.min_x: int = min_x
        self.world: List[List[int]] = world

    def __str__(self):
        result = []

        def get_letter(i: int) -> str:
            if i == UNKNOWN:
                return '.'
            elif i == BEACON:
                return 'B'
            elif i == SENSOR:
                return 'S'
            else:
                return 'X'

        for row in self.world:
            row_str = ''.join([get_letter(i) for i in row])
            result.append(row_str)

        result = '\n'.join(result)
        return result

    def get_real_x(self, x: int) -> int:
        return x + self.min_x

    def get_real_y(self, y: int) -> int:
        return y + self.min_y

    def get_real_pos(self, point: Point) -> Point:
        real_x = point.x - self.min_x
        real_y = point.y - self.min_y

        return Point(real_x, real_y)

    def fill(self, sensors: List[Sensor]) -> 'World':

        for s in sensors:
            sensor = self.get_real_pos(s.sensor)
            beacon = self.get_real_pos(s.beacon)

            self.world[sensor.y][sensor.x] = SENSOR
            self.world[beacon.y][beacon.x] = BEACON

        return self


def prepare_empty_world(sensors: List[Sensor]) -> World:
    x_set = set()
    y_set = set()

    for s in sensors:
        x_set.add(s.sensor.x)
        x_set.add(s.beacon.x)

        y_set.add(s.sensor.y)
        y_set.add(s.beacon.y)

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
    if world.max_x < 50:
        header('Empty world')
        print(world)

    return world


def day_15():
    debug = False

    def log(txt) -> None:
        if debug:
            print(txt)

    filename = f'input_day_15{"_" + sys.argv[1] if len(sys.argv) > 1 else ""}.txt'
    sensors = load_sensors(filename)

    header('Creating empty world')
    empty_world = prepare_empty_world(sensors)
    debug = empty_world.max_x < 50
    log(empty_world)

    header('Filling world')
    world = empty_world.fill(sensors)
    print(world)
    pass


if __name__ == '__main__':
    day_15()
    