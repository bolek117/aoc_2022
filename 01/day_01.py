from typing import List


def header(msg: str) -> None:
    print(f'\n--- {msg} ---')


class Elf:
    def __init__(self):
        self.sum: int = 0
        self.elements: List[int] = []

    def add_calories(self, calories: int) -> None:
        self.elements.append(calories)
        self.sum += calories

    def __str__(self):
        return f'{self.sum}: {", ".join(str(e) for e in self.elements)}'

    def __repr__(self):
        return self.__str__()


def elfs_list(elfs: List[Elf]) -> str:
    return '\n'.join([str(e) for e in elfs])


def get_elfs():
    with open('input_day_01.txt', 'r') as f:
        file_data = f.readlines()

    elfs = []
    elf = Elf()
    for line in file_data:
        line = line.strip()

        if len(line) == 0:
            elfs.append(elf)
            elf = Elf()
            continue

        calories = int(line)
        elf.add_calories(calories)

    elfs.append(elf)
    print(elfs_list(elfs))

    return elfs


def sort_by_calories(elfs: List[Elf]) -> List[Elf]:
    sorted_by_calories = sorted(elfs, key=lambda x: x.sum, reverse=True)
    return sorted_by_calories


def main():
    elfs = get_elfs()

    header('Part 1')
    max_calories = max([e.sum for e in elfs])
    print(max_calories)

    header('Part 2')
    sorted_by_calories = sort_by_calories(elfs)
    top_3 = sorted_by_calories[:3]
    print(elfs_list(top_3))
    print('Sum:', sum([c.sum for c in top_3]))


if __name__ == '__main__':
    main()
